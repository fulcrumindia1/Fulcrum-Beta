"""
services/professional_photos.py — Private Professional Headshots for Guides & SMEs
==================================================================================
Implements:
  - Strict Confidentiality:
      * Sole Platform Admin (fulcrumindia1@gmail.com) can view/manage all Guide & SME photos.
      * A Guide or SME can view/upload/replace/remove ONLY their own professional photo.
      * Aspirants and peer Guides/SMEs can NEVER view or generate URLs for professional photos.
  - Dual-Role Continuity & Isolation:
      * Guide+SME hybrid users share 1 single professional photo across both roles.
      * Aspirant+Guide/SME hybrid users keep their aspirant_photo and professional_photo
        in completely separate tables and private buckets.
  - Image Normalization:
      * Validates magic bytes (JPEG, PNG, WEBP), min 120x120 px, max 5 MB raw upload.
      * Strips EXIF/GPS metadata, center-crops to 320x320 px (1:1), encodes to WebP <= 150 KB.
  - Atomic Lifecycle:
      * Upload new object -> Upsert DB metadata -> Delete old Storage object only after success.
      * Resilient Storage-folder fallback if public.professional_photos DDL has not yet been run.
  - Batch Prefetching:
      * get_professional_photos_batch() resolves all Guide/SME avatars in 1 batch call.
"""

import io
import uuid
import base64
import hashlib
import html
from datetime import datetime, timezone
from typing import Optional, Tuple, Dict, List
from PIL import Image, ImageOps

from services.auth import get_supabase_admin_client, get_data_backend
from services.local_db import get_local_db
from services.roles import is_strict_admin, get_active_roles, get_pending_nda_roles
from services.cache import get_memo, set_memo, invalidate_memo

PROFESSIONAL_PHOTO_BUCKET = "professional-headshots"
MAX_RAW_UPLOAD_BYTES = 5 * 1024 * 1024  # 5 MB
MAX_NORMALIZED_BYTES = 150 * 1024       # 150 KB hard cap
TARGET_SIZE = (320, 320)
MIN_DIMENSION = 120
MAX_DIMENSION = 8000
SIGNED_URL_TTL_SECONDS = 900            # 15 minutes
CACHE_TTL_SECONDS = 600                 # 10 minutes
ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}


def ensure_professional_photo_bucket() -> bool:
    """Idempotently ensures the private 'professional-headshots' bucket exists in Supabase."""
    if get_data_backend() != "supabase":
        return True
    admin = get_supabase_admin_client()
    if not admin:
        return False
    try:
        buckets = admin.storage.list_buckets()
        exists = any(getattr(b, "id", None) == PROFESSIONAL_PHOTO_BUCKET or getattr(b, "name", None) == PROFESSIONAL_PHOTO_BUCKET for b in (buckets or []))
        if not exists:
            admin.storage.create_bucket(
                PROFESSIONAL_PHOTO_BUCKET,
                options={
                    "public": False,
                    "file_size_limit": MAX_RAW_UPLOAD_BYTES,
                    "allowed_mime_types": ["image/jpeg", "image/png", "image/webp"],
                },
            )
        return True
    except Exception:
        return False


def _user_holds_mentor_role(user_id: str) -> bool:
    """True if user holds active or pending_nda Guide or SME role (or profile.role in guide/sme)."""
    if not user_id:
        return False
    active = get_active_roles(user_id)
    pending = get_pending_nda_roles(user_id)
    if any(r in ("guide", "sme") for r in (active + pending)):
        return True
    try:
        from services.profiles import get_profile
        p = get_profile(user_id)
        if p and str(p.get("role") or "").strip().lower() in ("guide", "sme"):
            return True
    except Exception:
        pass
    return False


def can_view_professional_photo(
    viewer_id: Optional[str],
    subject_user_id: Optional[str],
    viewer_email: Optional[str] = None,
) -> Tuple[bool, Optional[str]]:
    """
    Strict Confidentiality Gate for Guide/SME Professional Photographs:
      1. Sole Platform Admin (fulcrumindia1@gmail.com) -> ALLOWED
      2. Self access by the Guide/SME themselves (viewer_id == subject_user_id) -> ALLOWED
      3. Aspirants (assigned or unassigned) -> STRICTLY DENIED
      4. Other Guides or SMEs -> STRICTLY DENIED
    """
    if not viewer_id or not subject_user_id:
        return False, "Unauthorized: Viewer and subject user IDs are required."

    v_str = str(viewer_id).strip()
    s_str = str(subject_user_id).strip()

    # 1. Sole Platform Admin
    if is_strict_admin(user_id=v_str, email=viewer_email):
        return True, None

    # 2. Self access by a Guide or SME
    if v_str == s_str and _user_holds_mentor_role(s_str):
        return True, None

    return False, "Unauthorized: Professional photographs are private to the Guide/SME and Platform Administration."


def can_manage_professional_photo(
    actor_id: Optional[str],
    subject_user_id: Optional[str],
    actor_email: Optional[str] = None,
) -> Tuple[bool, Optional[str]]:
    """Checks whether actor_id is permitted to upload/replace/remove subject_user_id's professional photo."""
    return can_view_professional_photo(viewer_id=actor_id, subject_user_id=subject_user_id, viewer_email=actor_email)


def validate_and_normalize_professional_photo(
    file_bytes: bytes,
    filename: str = "",
) -> Tuple[bool, Optional[bytes], str, int, int, str, Optional[str]]:
    """
    Validates magic bytes and dimensions, strips EXIF, center-crops to 320x320 RGB,
    and encodes to WebP <= 150 KB.
    Returns: (ok, webp_bytes, mime_type, width, height, sha256_hash, error_msg)
    """
    if not file_bytes or len(file_bytes) == 0:
        return False, None, "", 0, 0, "", "Uploaded file is empty."

    if len(file_bytes) > MAX_RAW_UPLOAD_BYTES:
        mb = len(file_bytes) / (1024 * 1024)
        return False, None, "", 0, 0, "", f"File size ({mb:.1f} MB) exceeds the 5.0 MB maximum limit."

    try:
        verify_img = Image.open(io.BytesIO(file_bytes))
        fmt = (verify_img.format or "").upper()
        verify_img.verify()
    except Exception:
        return False, None, "", 0, 0, "", "Invalid or corrupted image file. Please upload a valid JPG, PNG, or WEBP photograph."

    if fmt not in ALLOWED_FORMATS:
        return False, None, "", 0, 0, "", f"Unsupported image format '{fmt}'. Only JPG, PNG, and WEBP are allowed."

    try:
        img = Image.open(io.BytesIO(file_bytes))
        img = ImageOps.exif_transpose(img)
        w, h = img.size
        if w < MIN_DIMENSION or h < MIN_DIMENSION:
            return False, None, "", 0, 0, "", f"Image resolution ({w}x{h}px) is too small. Minimum required is {MIN_DIMENSION}x{MIN_DIMENSION} pixels."
        if w > MAX_DIMENSION or h > MAX_DIMENSION:
            return False, None, "", 0, 0, "", f"Image dimensions ({w}x{h}px) exceed safety limits."

        # Flatten alpha onto clean light slate background (#F8FAFC) and strip all EXIF metadata
        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            alpha_img = img.convert("RGBA")
            bg = Image.new("RGB", alpha_img.size, (248, 250, 252))
            bg.paste(alpha_img, mask=alpha_img.split()[3])
            clean_rgb = bg
        else:
            clean_rgb = img.convert("RGB")

        # 1:1 square center-crop to 320x320 px
        cropped = ImageOps.fit(clean_rgb, TARGET_SIZE, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))

        # Encode to WebP <= 150 KB
        webp_bytes = b""
        for quality in (82, 75, 68, 60, 50):
            buf = io.BytesIO()
            cropped.save(buf, format="WEBP", quality=quality, method=4)
            candidate = buf.getvalue()
            webp_bytes = candidate
            if len(candidate) <= MAX_NORMALIZED_BYTES:
                break

        if len(webp_bytes) > MAX_NORMALIZED_BYTES:
            return False, None, "", 0, 0, "", "Normalized image exceeds 150 KB limit. Please try a simpler headshot."

        sha256_hex = hashlib.sha256(webp_bytes).hexdigest()
        return True, webp_bytes, "image/webp", TARGET_SIZE[0], TARGET_SIZE[1], sha256_hex, None
    except Exception as e:
        return False, None, "", 0, 0, "", f"Image processing failed: {e}"


def _invalidate_prof_photo_cache(user_id: str) -> None:
    invalidate_memo(f"prof_photo_url:{user_id}")
    invalidate_memo("prof_photos_batch:")


def upload_professional_photo(
    subject_user_id: str,
    file_bytes: bytes,
    uploaded_by: Optional[str] = None,
    filename: str = "",
    actor_email: Optional[str] = None,
) -> Tuple[bool, Optional[str]]:
    """
    Atomically validates, normalizes, and uploads a Guide/SME professional headshot:
      1. Authorize caller (Self Guide/SME or Sole Admin).
      2. Validate & normalize to 320x320 WebP <= 150 KB.
      3. Capture previous storage_path if replacing.
      4. Upload new object to 'professional-headshots/{user_id}/headshot_{uuid8}.webp'.
      5. Upsert metadata row in public.professional_photos (with SQLite & Storage fallback).
      6. Delete previous storage_path only after step 4 & 5 succeed.
    """
    actor_id = str(uploaded_by or subject_user_id or "").strip()
    target_id = str(subject_user_id or "").strip()

    ok_auth, auth_err = can_manage_professional_photo(actor_id, target_id, actor_email=actor_email)
    if not ok_auth:
        return False, auth_err

    ok_img, webp_bytes, mime_type, width, height, sha256_hex, img_err = validate_and_normalize_professional_photo(
        file_bytes, filename=filename
    )
    if not ok_img or not webp_bytes:
        return False, img_err

    new_storage_path = f"{target_id}/headshot_{uuid.uuid4().hex[:8]}.webp"
    now_iso = datetime.now(timezone.utc).isoformat()
    backend = get_data_backend()
    db = get_local_db()

    if backend == "supabase":
        admin = get_supabase_admin_client()
        if not admin:
            return False, "Supabase admin client unavailable."

        ensure_professional_photo_bucket()

        # 1. Discover existing storage path(s) before uploading new one
        old_paths: List[str] = []
        try:
            res_old = admin.table("professional_photos").select("storage_path").eq("user_id", target_id).execute()
            for r in (res_old.data or []):
                if r.get("storage_path"):
                    old_paths.append(r["storage_path"])
        except Exception:
            pass
        try:
            listed = admin.storage.from_(PROFESSIONAL_PHOTO_BUCKET).list(target_id)
            for item in (listed or []):
                name = item.get("name") if isinstance(item, dict) else getattr(item, "name", None)
                if name and not name.startswith("."):
                    p_cand = f"{target_id}/{name}"
                    if p_cand not in old_paths:
                        old_paths.append(p_cand)
        except Exception:
            pass

        # 2. Upload new object to private bucket FIRST (fail-closed: old photo untouched if this fails)
        try:
            admin.storage.from_(PROFESSIONAL_PHOTO_BUCKET).upload(
                path=new_storage_path,
                file=webp_bytes,
                file_options={"content-type": mime_type, "upsert": "true"},
            )
        except Exception as e:
            return False, f"Failed to persist professional headshot to cloud storage: {e}"

        # 3. Upsert metadata row in public.professional_photos (if table exists in PostgreSQL)
        db_row = {
            "user_id": target_id,
            "storage_bucket": PROFESSIONAL_PHOTO_BUCKET,
            "storage_path": new_storage_path,
            "mime_type": mime_type,
            "byte_size": len(webp_bytes),
            "width": width,
            "height": height,
            "sha256_hash": sha256_hex,
            "uploaded_by": actor_id,
            "uploaded_at": now_iso,
            "updated_at": now_iso,
        }
        try:
            admin.table("professional_photos").upsert(db_row, on_conflict="user_id").execute()
        except Exception as db_exc:
            err_s = str(db_exc)
            # If the table exists and threw a real constraint/DB error (not missing-table PGRST205), rollback upload
            if "PGRST205" not in err_s and "professional_photos" not in err_s:
                try:
                    admin.storage.from_(PROFESSIONAL_PHOTO_BUCKET).remove([new_storage_path])
                except Exception:
                    pass
                return False, f"Database error saving headshot metadata: {db_exc}"

        # 4. Cleanup old storage objects ONLY after new object + metadata are safely committed
        stale_to_remove = [p for p in old_paths if p != new_storage_path]
        if stale_to_remove:
            try:
                admin.storage.from_(PROFESSIONAL_PHOTO_BUCKET).remove(stale_to_remove)
            except Exception:
                pass

    # Always sync local SQLite metadata + blob for fast local testability
    try:
        db.upsert_professional_photo({
            "user_id": target_id,
            "storage_bucket": PROFESSIONAL_PHOTO_BUCKET,
            "storage_path": new_storage_path,
            "mime_type": mime_type,
            "byte_size": len(webp_bytes),
            "width": width,
            "height": height,
            "sha256_hash": sha256_hex,
            "uploaded_by": actor_id,
            "data_blob": webp_bytes,
            "uploaded_at": now_iso,
        })
    except Exception as e:
        if backend != "supabase":
            return False, f"Failed to save professional photo in SQLite: {e}"

    _invalidate_prof_photo_cache(target_id)
    return True, None


def delete_professional_photo(
    subject_user_id: str,
    actor_id: Optional[str] = None,
    actor_email: Optional[str] = None,
) -> Tuple[bool, Optional[str]]:
    """Removes a Guide/SME professional photo from Storage and Database."""
    caller_id = str(actor_id or subject_user_id or "").strip()
    target_id = str(subject_user_id or "").strip()

    ok_auth, auth_err = can_manage_professional_photo(caller_id, target_id, actor_email=actor_email)
    if not ok_auth:
        return False, auth_err

    backend = get_data_backend()
    db = get_local_db()

    if backend == "supabase":
        admin = get_supabase_admin_client()
        if admin:
            paths_to_remove: List[str] = []
            try:
                res = admin.table("professional_photos").select("storage_path").eq("user_id", target_id).execute()
                for r in (res.data or []):
                    if r.get("storage_path"):
                        paths_to_remove.append(r["storage_path"])
                admin.table("professional_photos").delete().eq("user_id", target_id).execute()
            except Exception:
                pass
            try:
                listed = admin.storage.from_(PROFESSIONAL_PHOTO_BUCKET).list(target_id)
                for item in (listed or []):
                    name = item.get("name") if isinstance(item, dict) else getattr(item, "name", None)
                    if name and not name.startswith("."):
                        p_cand = f"{target_id}/{name}"
                        if p_cand not in paths_to_remove:
                            paths_to_remove.append(p_cand)
            except Exception:
                pass
            if paths_to_remove:
                try:
                    admin.storage.from_(PROFESSIONAL_PHOTO_BUCKET).remove(paths_to_remove)
                except Exception:
                    pass

    try:
        db.delete_professional_photo(target_id)
    except Exception:
        pass

    _invalidate_prof_photo_cache(target_id)
    return True, None


def get_professional_photo_url(
    viewer_id: Optional[str],
    subject_user_id: Optional[str],
    viewer_email: Optional[str] = None,
) -> Optional[str]:
    """
    Returns a short-lived signed URL (or data URI in SQLite mode) ONLY if viewer_id
    is authorized (Sole Admin or Self Guide/SME). Returns None for Aspirants and peer mentors.
    """
    ok_auth, _ = can_view_professional_photo(viewer_id=viewer_id, subject_user_id=subject_user_id, viewer_email=viewer_email)
    if not ok_auth:
        return None

    target_id = str(subject_user_id).strip()
    cache_key = f"prof_photo_url:{target_id}"
    cached = get_memo(cache_key)
    if cached is not None:
        return cached if cached != "__NONE__" else None

    backend = get_data_backend()
    if backend == "supabase":
        admin = get_supabase_admin_client()
        if admin:
            storage_path = None
            try:
                res = admin.table("professional_photos").select("storage_path").eq("user_id", target_id).limit(1).execute()
                if res.data and res.data[0].get("storage_path"):
                    storage_path = res.data[0]["storage_path"]
            except Exception:
                pass

            if not storage_path:
                try:
                    listed = admin.storage.from_(PROFESSIONAL_PHOTO_BUCKET).list(target_id)
                    valid_files = [
                        (item.get("name") if isinstance(item, dict) else getattr(item, "name", None))
                        for item in (listed or [])
                    ]
                    valid_files = [f for f in valid_files if f and f.endswith(".webp")]
                    if valid_files:
                        storage_path = f"{target_id}/{ sorted(valid_files)[-1] }"
                except Exception:
                    pass

            if storage_path:
                try:
                    signed = admin.storage.from_(PROFESSIONAL_PHOTO_BUCKET).create_signed_url(
                        storage_path, SIGNED_URL_TTL_SECONDS
                    )
                    url = signed.get("signedURL") or signed.get("signedUrl")
                    if url:
                        set_memo(cache_key, url, ttl_seconds=CACHE_TTL_SECONDS)
                        return url
                except Exception:
                    pass

    # SQLite fallback / local blob
    db = get_local_db()
    row = db.get_professional_photo(target_id)
    if row and row.get("data_blob"):
        b64 = base64.b64encode(row["data_blob"]).decode("ascii")
        mime = row.get("mime_type") or "image/webp"
        data_uri = f"data:{mime};base64,{b64}"
        set_memo(cache_key, data_uri, ttl_seconds=CACHE_TTL_SECONDS)
        return data_uri

    set_memo(cache_key, "__NONE__", ttl_seconds=120)
    return None


def get_professional_photos_batch(
    viewer_id: Optional[str],
    user_ids: List[str],
    viewer_email: Optional[str] = None,
) -> Dict[str, Optional[str]]:
    """
    Batch-prefetches signed URLs for a list of Guide/SME user_ids.
    Only Sole Admin receives all requested mentor URLs; a Guide/SME receives only their own.
    Aspirants receive an empty dict (zero DB/Storage calls).
    """
    if not viewer_id or not user_ids:
        return {}

    clean_ids = sorted({str(u).strip() for u in user_ids if u})
    if not clean_ids:
        return {}

    is_admin = is_strict_admin(user_id=str(viewer_id), email=viewer_email)
    if not is_admin:
        # Non-admin can at most view their own professional photo if they are a Guide/SME
        v_str = str(viewer_id).strip()
        if v_str in clean_ids and _user_holds_mentor_role(v_str):
            return {v_str: get_professional_photo_url(v_str, v_str, viewer_email=viewer_email)}
        return {}

    batch_key = f"prof_photos_batch:{','.join(clean_ids)}"
    cached = get_memo(batch_key)
    if cached is not None:
        return cached

    result: Dict[str, Optional[str]] = {uid: None for uid in clean_ids}
    backend = get_data_backend()

    if backend == "supabase":
        admin = get_supabase_admin_client()
        if admin:
            path_by_uid: Dict[str, str] = {}
            try:
                res = admin.table("professional_photos").select("user_id, storage_path").in_("user_id", clean_ids).execute()
                for r in (res.data or []):
                    if r.get("user_id") and r.get("storage_path"):
                        path_by_uid[str(r["user_id"])] = r["storage_path"]
            except Exception:
                # Fallback if table not migrated yet: check storage or local_db
                pass

            if path_by_uid:
                paths_list = list(path_by_uid.values())
                try:
                    signed_list = admin.storage.from_(PROFESSIONAL_PHOTO_BUCKET).create_signed_urls(
                        paths_list, SIGNED_URL_TTL_SECONDS
                    )
                    url_by_path = {}
                    for item in (signed_list or []):
                        p = item.get("path")
                        u = item.get("signedURL") or item.get("signedUrl")
                        if p and u:
                            url_by_path[p] = u
                    for uid, spath in path_by_uid.items():
                        if spath in url_by_path:
                            result[uid] = url_by_path[spath]
                except Exception:
                    for uid, spath in path_by_uid.items():
                        result[uid] = get_professional_photo_url(viewer_id, uid, viewer_email=viewer_email)
            else:
                for uid in clean_ids:
                    result[uid] = get_professional_photo_url(viewer_id, uid, viewer_email=viewer_email)
    else:
        for uid in clean_ids:
            result[uid] = get_professional_photo_url(viewer_id, uid, viewer_email=viewer_email)

    set_memo(batch_key, result, ttl_seconds=CACHE_TTL_SECONDS)
    return result


def get_initials(full_name: str) -> str:
    parts = [p for p in str(full_name or "M").strip().split() if p]
    if not parts:
        return "M"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return f"{parts[0][0]}{parts[-1][0]}".upper()


def render_professional_avatar_html(
    full_name: str,
    photo_url: Optional[str],
    size_px: int = 48,
    role: str = "guide",
    show_missing_badge_for_admin: bool = False,
) -> str:
    """
    Renders a circular 1:1 avatar (img if photo_url is present, or styled initials circle)
    plus an optional 'Photo Not Uploaded' badge for Admin roster views.
    """
    safe_name = html.escape(str(full_name or "Mentor"))
    initials = html.escape(get_initials(full_name))
    is_sme = str(role or "").lower() == "sme"
    bg_grad = "linear-gradient(135deg, #F59E0B, #D97706)" if is_sme else "linear-gradient(135deg, #10B981, #059669)"
    border_col = "#FDE68A" if is_sme else "#A7F3D0"
    font_px = max(12, int(size_px * 0.36))

    if photo_url:
        safe_url = html.escape(photo_url, quote=True)
        avatar_el = (
            f'<img src="{safe_url}" alt="{safe_name}" '
            f'style="width:{size_px}px; height:{size_px}px; border-radius:50%; object-fit:cover; '
            f'border:2px solid {border_col}; box-shadow:0 2px 6px rgba(15,23,42,0.08); flex-shrink:0;" />'
        )
        badge_el = ""
    else:
        avatar_el = (
            f'<div style="width:{size_px}px; height:{size_px}px; border-radius:50%; background:{bg_grad}; '
            f'color:#FFFFFF; display:inline-flex; align-items:center; justify-content:center; '
            f'font-size:{font_px}px; font-weight:800; letter-spacing:0.5px; border:2px solid {border_col}; '
            f'box-shadow:0 2px 6px rgba(15,23,42,0.06); flex-shrink:0;">{initials}</div>'
        )
        if show_missing_badge_for_admin:
            badge_el = (
                '<span style="display:inline-block; margin-left:6px; padding:2px 7px; border-radius:8px; '
                'font-size:0.68rem; font-weight:700; background:#FEF3C7; color:#92400E; border:1px solid #FDE68A;">'
                '📷 Photo Not Uploaded</span>'
            )
        else:
            badge_el = ""

    return f'<div style="display:inline-flex; align-items:center; vertical-align:middle;">{avatar_el}{badge_el}</div>'

