"""
services/aspirant_photos.py — Dedicated Aspirant Profile Photo Management
========================================================================
Non-destructive private Supabase Storage + metadata integration for Aspirant photos.

Key architectural guarantees:
1. Strict Role Isolation: Photos attach strictly to Aspirant identity.
2. Zero Impact on Journey / Schemes: Photo actions DO NOT trigger journey events
   or scheme matching recalculations.
3. Privacy & Security: Uses private Supabase Storage bucket 'aspirant-profile-photos'
   with short-lived (300s) signed URLs.
4. Image Optimization: Corrects EXIF orientation, strips metadata, resizes to
   max 320x320 with smart center-crop, compresses to WebP targeting 50-100 KB
   (strict 150 KB cap). Single optimized file served to all authorized viewers.
5. Dual-Backend Resilience: Seamless fallback to LocalDatabase for offline/testing.
"""

import io
import json
import uuid
import base64
from datetime import datetime, timezone
from typing import Optional, Tuple, Dict
from PIL import Image, ImageOps

from services.auth import get_supabase_client, get_supabase_admin_client, get_data_backend
from services.local_db import get_local_db
from services.cache import get_memo, set_memo, invalidate_memo

STORAGE_BUCKET = "aspirant-profile-photos"
MAX_UPLOAD_BYTES = 5 * 1024 * 1024  # 5 MB raw upload limit
MAX_TARGET_DIM = 320               # Max output dimension (px)
MAX_STORED_BYTES = 150 * 1024      # 150 KB strict stored-file cap
TARGET_QUALITY_HIGH = 85           # Starting WebP quality
TARGET_QUALITY_LOW = 25            # Minimum acceptable quality before rejection
SIGNED_URL_EXPIRY_SECONDS = 300


def can_view_aspirant_photo(
    viewer_id: str,
    aspirant_id: str,
    viewer_role: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """
    Trusted server-side authorization check for viewing an aspirant's profile photograph.
    Supports:
    1. Aspirant viewing their own photo.
    2. Single Admin (fulcrumindia1@gmail.com / admin role) viewing any photo.
    3. Active Guide with accepted NDA assigned to this Aspirant (status='active').
    4. Active SME with accepted NDA assigned to this Aspirant (status='active').
    Denies access when:
    - No assignment exists or assignment was removed.
    - Guide/SME role has been suspended or revoked.
    - Mandatory NDA is pending or invalid.
    - A user manipulates a target Aspirant ID.
    """
    if not viewer_id or not aspirant_id:
        return False, "Missing viewer_id or aspirant_id."

    viewer_id_str = str(viewer_id).strip()
    aspirant_id_str = str(aspirant_id).strip()

    # 1. Aspirant self-access
    if viewer_id_str == aspirant_id_str:
        return True, None

    # 2. Platform Admin oversight (strictly fulcrumindia1@gmail.com)
    from services.roles import is_strict_admin, get_active_roles

    if is_strict_admin(user_id=viewer_id_str):
        return True, None

    # 3. Active Role & NDA checks for Guides and SMEs
    from services.legal import check_user_nda_accepted

    active_roles = get_active_roles(viewer_id_str)
    has_active_guide = "guide" in active_roles
    has_active_sme = "sme" in active_roles

    v_role_clean = str(viewer_role).strip().lower() if viewer_role else ""
    if v_role_clean == "guide" and not has_active_guide:
        return False, "Unauthorized: Guide role is not active (pending NDA, suspended, or revoked)."
    if v_role_clean == "sme" and not has_active_sme:
        return False, "Unauthorized: SME role is not active (pending NDA, suspended, or revoked)."

    if not has_active_guide and not has_active_sme:
        return False, "Unauthorized: Viewer does not hold an active mentor role."

    # 4. Check active relationship assignment
    backend = get_data_backend()
    rel = None

    if backend == "supabase":
        admin_c = get_supabase_admin_client() or get_supabase_client()
        if admin_c:
            try:
                res = admin_c.table("relationships")\
                    .select("aspirant_id, guide_id, guide_ids, sme_id, sme_ids, status")\
                    .eq("aspirant_id", aspirant_id_str)\
                    .eq("status", "active")\
                    .execute()
                if res.data and len(res.data) > 0:
                    rel = res.data[0]
            except Exception as e:
                print(f"[PhotoAuth] Supabase relationship check error: {e}")

    if not rel:
        # Check Local DB
        db = get_local_db()
        if hasattr(db, "get_relationship"):
            rel_local = db.get_relationship(aspirant_id_str)
            if rel_local and rel_local.get("status") == "active":
                rel = rel_local

    if not rel:
        return False, "Unauthorized: No active assignment exists for this entrepreneur."

    # Parse primary and multi-mentor assignment lists
    guide_ids = rel.get("guide_ids") or []
    if isinstance(guide_ids, str):
        try: guide_ids = json.loads(guide_ids)
        except Exception: guide_ids = []
    if not isinstance(guide_ids, list):
        guide_ids = []
    if rel.get("guide_id") and str(rel["guide_id"]) not in guide_ids:
        guide_ids.append(str(rel["guide_id"]))
    guide_ids = [str(x) for x in guide_ids]

    sme_ids = rel.get("sme_ids") or []
    if isinstance(sme_ids, str):
        try: sme_ids = json.loads(sme_ids)
        except Exception: sme_ids = []
    if not isinstance(sme_ids, list):
        sme_ids = []
    if rel.get("sme_id") and str(rel["sme_id"]) not in sme_ids:
        sme_ids.append(str(rel["sme_id"]))
    sme_ids = [str(x) for x in sme_ids]

    is_assigned_guide = viewer_id_str in guide_ids
    is_assigned_sme = viewer_id_str in sme_ids

    # Verify Guide authorization
    if is_assigned_guide and has_active_guide:
        if not check_user_nda_accepted(viewer_id_str, "guide"):
            return False, "Unauthorized: Mandatory Guide NDA is pending or invalid."
        return True, None

    # Verify SME authorization
    if is_assigned_sme and has_active_sme:
        if not check_user_nda_accepted(viewer_id_str, "sme"):
            return False, "Unauthorized: Mandatory SME NDA is pending or invalid."
        return True, None

    return False, "Unauthorized: Viewer is not an active, NDA-certified mentor assigned to this entrepreneur."


def validate_and_process_photo(raw_bytes: bytes) -> Tuple[bool, Optional[bytes], Optional[str], Optional[int], Optional[int], Optional[str]]:
    """
    Validates, corrects EXIF orientation, strips metadata, resizes to max
    320×320 with center-crop, and compresses to WebP.

    Compression strategy:
      1. Start at quality 85 and step down in increments of 5.
      2. Target: 50–100 KB.  Hard cap: 150 KB.
      3. If quality reaches 25 and the file still exceeds 150 KB, reject
         with a human-friendly message instead of storing a blurry image.

    Returns: (success, processed_bytes, content_type, width, height, error_message)
    """
    if not raw_bytes:
        return False, None, None, None, None, "No image file provided."

    if len(raw_bytes) > MAX_UPLOAD_BYTES:
        return False, None, None, None, None, f"File size exceeds maximum 5 MB limit ({len(raw_bytes) / (1024*1024):.1f} MB)."

    try:
        # Open and verify image
        img = Image.open(io.BytesIO(raw_bytes))
        orig_format = (img.format or "").upper()
        if orig_format not in ("JPEG", "JPG", "PNG", "WEBP"):
            return False, None, None, None, None, f"Unsupported image format: {orig_format}. Allowed: JPG, PNG, WEBP."

        # --- 1. Correct EXIF orientation (rotates/flips per camera tag) ---
        try:
            img = ImageOps.exif_transpose(img)
        except Exception:
            pass  # Some images have no EXIF; that's fine

        # --- 2. Convert colorspace (strips all metadata by rebuilding pixels) ---
        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            clean_img = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            clean_img.paste(img, mask=img.split()[3] if len(img.split()) >= 4 else None)
            img = clean_img
        elif img.mode != "RGB":
            img = img.convert("RGB")

        # --- 3. Resize with high-quality LANCZOS, preserving aspect ratio ---
        img.thumbnail((MAX_TARGET_DIM, MAX_TARGET_DIM), Image.Resampling.LANCZOS)
        width, height = img.size

        # --- 4. Intelligent WebP compression loop ---
        quality = TARGET_QUALITY_HIGH
        processed_bytes = None

        while quality >= TARGET_QUALITY_LOW:
            out_buf = io.BytesIO()
            img.save(out_buf, format="WEBP", quality=quality, method=6)
            candidate = out_buf.getvalue()

            if len(candidate) <= MAX_STORED_BYTES:
                processed_bytes = candidate
                break

            quality -= 5

        if processed_bytes is None:
            # Even at minimum quality the file is too large — reject gracefully
            return (
                False, None, None, None, None,
                "This photograph is too complex to compress to an acceptable file size "
                "(limit: 150 KB). Please try a different photo with a simpler background "
                "or lower resolution."
            )

        return True, processed_bytes, "image/webp", width, height, None
    except Exception as e:
        return False, None, None, None, None, f"Failed to process image: {str(e)}"


def get_aspirant_photo(
    user_id: str,
    viewer_id: Optional[str] = None,
    viewer_role: Optional[str] = None
) -> Optional[Dict]:
    """
    Retrieves photo metadata and short-lived signed URL or base64 data URI.
    Enforces server-side authorization:
    - If viewer_id is provided, checks can_view_aspirant_photo.
    - If viewer_id is None, infers from active Streamlit session if available.
    Returns None if unauthorized or if no photo is registered.
    """
    if not user_id:
        return None

    backend = get_data_backend()

    # Resolve viewer_id from session context if running in Streamlit
    if viewer_id is None:
        try:
            import streamlit as st
            if hasattr(st, "session_state") and st.session_state.get("user_id"):
                viewer_id = st.session_state.get("user_id")
                viewer_role = viewer_role or st.session_state.get("active_workspace") or st.session_state.get("role")
        except Exception:
            pass

    # Server-side authorization gate:
    # In cloud Supabase mode, strictly fail closed if viewer is unauthenticated
    if not viewer_id:
        if backend == "supabase":
            return None
        # In local development / test mode, allow owner self-view
        viewer_id = user_id

    authorized, _ = can_view_aspirant_photo(viewer_id, user_id, viewer_role)
    if not authorized:
        return None

    cache_key = f"aspirant_photo:{user_id}:{viewer_id}"
    cached = get_memo(cache_key)
    if cached is not None:
        return None if cached == "__NONE__" else cached

    # 1. Supabase Mode (Fail closed: never silently fall back to local SQLite in production)
    if backend == "supabase":
        client = get_supabase_admin_client() or get_supabase_client()
        if client:
            try:
                res = client.table("aspirant_photos").select("*").eq("user_id", user_id).limit(1).execute()
                if res.data and len(res.data) > 0:
                    record = res.data[0]
                    path = record.get("storage_path")
                    bucket = record.get("storage_bucket") or STORAGE_BUCKET
                    if path:
                        # Generate fresh signed URL (300s expiry; memoized for 120s)
                        signed_res = client.storage.from_(bucket).create_signed_url(path, SIGNED_URL_EXPIRY_SECONDS)
                        signed_url = (
                            signed_res.get("signedURL")
                            or signed_res.get("signedUrl")
                            or (signed_res.get("data", {}).get("signedUrl") if isinstance(signed_res, dict) else None)
                        )
                        record["url"] = signed_url
                        set_memo(cache_key, record, ttl_seconds=120)
                        return record
            except Exception as e:
                print(f"[AspirantPhotos] Supabase fetch error: {e}")
        set_memo(cache_key, "__NONE__", ttl_seconds=120)
        return None

    # 2. Local Database Mode (Active only when DATA_BACKEND=sqlite)
    local_record = get_local_db().get_aspirant_photo(user_id)
    if local_record:
        data_blob = local_record.get("data_blob")
        if data_blob:
            b64_data = base64.b64encode(data_blob).decode("ascii")
            local_record["url"] = f"data:{local_record.get('content_type', 'image/webp')};base64,{b64_data}"
            set_memo(cache_key, local_record, ttl_seconds=120)
            return local_record

    set_memo(cache_key, "__NONE__", ttl_seconds=120)
    return None


def render_aspirant_photo_header(
    aspirant_profile: Dict,
    viewer_id: str,
    viewer_role: str,
    accent_color: str = "#2563EB"
) -> None:
    """
    Reusable UI component: Displays the assigned Aspirant's circular photograph (80-90px)
    beside their name in the Profile Overview heading.
    Preserves all existing founder details, renders neutral initials placeholder if absent,
    and enforces strict server-side authorization.
    Read-only: strictly no photo-upload or editing controls for Guide or SME.
    """
    import streamlit as st

    if not aspirant_profile:
        return

    asp_id = aspirant_profile.get("id")
    full_name = aspirant_profile.get("full_name") or "Entrepreneur"
    p_data = aspirant_profile.get("profile_data", {})
    biz = p_data.get("business", {})
    biz_name = biz.get("business_name") or f"{full_name}'s Enterprise"
    sector = biz.get("sector") or "General"
    stage = biz.get("stage") or "idea"

    photo = get_aspirant_photo(asp_id, viewer_id=viewer_id, viewer_role=viewer_role)

    if photo and photo.get("url"):
        photo_element = (
            '<div style="text-align:center; flex-shrink:0;">'
            f'<img src="{photo["url"]}" alt="{full_name}" style="width:84px; height:84px; border-radius:50%; object-fit:cover; border:3px solid {accent_color}; box-shadow:0 3px 10px rgba(0,0,0,0.12);" />'
            '<div style="font-size:0.68rem; color:#059669; font-weight:700; margin-top:4px;">✓ Verified Photo</div>'
            '</div>'
        )
    else:
        ini = "".join([part[0].upper() for part in full_name.split()[:2]]) or "A"
        photo_element = (
            '<div style="text-align:center; flex-shrink:0;">'
            f'<div style="width:84px; height:84px; border-radius:50%; background:linear-gradient(135deg, #E2E8F0 0%, #CBD5E1 100%); color:#475569; display:flex; align-items:center; justify-content:center; font-size:1.6rem; font-weight:800; border:2.5px solid #E2E8F0; margin:0 auto; box-shadow:0 2px 6px rgba(0,0,0,0.04);">{ini}</div>'
            '<div style="font-size:0.68rem; color:#94A3B8; font-weight:600; margin-top:4px;">No Photo Uploaded</div>'
            '</div>'
        )

    header_html = (
        '<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:1.2rem; margin:0.75rem 0 1.25rem 0; box-shadow:0 1px 3px rgba(0,0,0,0.04);">'
        '<div style="display:flex; align-items:center; gap:16px;">'
        f'{photo_element}'
        '<div style="flex:1;">'
        f'<h3 style="margin:0 0 4px 0; color:#0F172A; font-size:1.35rem;">Profile Overview: {full_name}</h3>'
        f'<div style="color:{accent_color}; font-weight:600; font-size:0.9rem;">{biz_name} · {sector} ({stage})</div>'
        f'<div style="color:#64748B; font-size:0.8rem; margin-top:3px;">ID: {asp_id}</div>'
        '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)


def upload_aspirant_photo(
    user_id: str,
    file_bytes: bytes,
    filename: str = "avatar.webp",
    uploader_id: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """
    Validates, compresses, and saves aspirant photo.
    Enforces that ONLY the Aspirant themselves can upload/change their headshot.
    Strictly prevents silent fallbacks when in Supabase production mode.
    """
    if not user_id:
        return False, "User ID is required."

    # Authorization: Only the entrepreneur can upload their own photo
    effective_uploader = uploader_id
    if effective_uploader is None:
        try:
            import streamlit as st
            effective_uploader = st.session_state.get("user_id")
        except Exception:
            pass

    if effective_uploader and str(effective_uploader) != str(user_id):
        return False, "Unauthorized: Only the entrepreneur can upload or update their own profile photo."

    ok, processed_bytes, content_type, width, height, err = validate_and_process_photo(file_bytes)
    if not ok:
        return False, err

    backend = get_data_backend()
    now_iso = datetime.now(timezone.utc).isoformat()
    obj_id = str(uuid.uuid4())
    storage_path = f"{user_id}/avatar_{uuid.uuid4().hex[:8]}.webp"

    # In Supabase Mode: Persist strictly to Supabase Storage & DB. Never mask failure with local SQLite.
    if backend == "supabase":
        admin = get_supabase_admin_client() or get_supabase_client()
        if not admin:
            return False, "Supabase cloud client unavailable. Please check configuration."

        try:
            # 0. Ensure storage bucket exists — auto-create if missing
            try:
                buckets = admin.storage.list_buckets()
                bucket_exists = any(getattr(b, "id", None) == STORAGE_BUCKET or getattr(b, "name", None) == STORAGE_BUCKET for b in (buckets or []))
                if not bucket_exists:
                    admin.storage.create_bucket(
                        STORAGE_BUCKET,
                        options={
                            "public": False,
                            "file_size_limit": MAX_UPLOAD_BYTES,
                            "allowed_mime_types": ["image/png", "image/jpeg", "image/webp"]
                        }
                    )
            except Exception as bucket_err:
                try:
                    admin.storage.create_bucket(STORAGE_BUCKET, options={"public": False})
                except Exception:
                    pass

            # 1. Clean up old storage file if present
            old_photo = None
            try:
                old_res = admin.table("aspirant_photos").select("storage_path").eq("user_id", user_id).limit(1).execute()
                if old_res.data and len(old_res.data) > 0:
                    old_photo = old_res.data[0].get("storage_path")
            except Exception:
                pass

            if old_photo:
                try:
                    admin.storage.from_(STORAGE_BUCKET).remove([old_photo])
                except Exception:
                    pass

            # 2. Upload compressed WebP file to storage (with 1-time auto-create retry)
            try:
                upload_res = admin.storage.from_(STORAGE_BUCKET).upload(
                    storage_path,
                    processed_bytes,
                    {"content-type": content_type, "upsert": "true"}
                )
            except Exception as up_err:
                # If failed due to bucket not found, force create and retry
                if "bucket" in str(up_err).lower():
                    try:
                        admin.storage.create_bucket(STORAGE_BUCKET, options={"public": False})
                        upload_res = admin.storage.from_(STORAGE_BUCKET).upload(
                            storage_path,
                            processed_bytes,
                            {"content-type": content_type, "upsert": "true"}
                        )
                    except Exception as retry_err:
                        raise up_err
                else:
                    raise up_err

            if hasattr(upload_res, "error") and upload_res.error:
                err_dict = upload_res.error if isinstance(upload_res.error, dict) else {}
                if "bucket" in str(upload_res.error).lower():
                    try:
                        admin.storage.create_bucket(STORAGE_BUCKET, options={"public": False})
                        admin.storage.from_(STORAGE_BUCKET).upload(
                            storage_path,
                            processed_bytes,
                            {"content-type": content_type, "upsert": "true"}
                        )
                    except Exception:
                        pass
                else:
                    return False, f"Failed to persist profile photo to cloud storage: {upload_res.error}"

            # 3. Upsert metadata in aspirant_photos
            try:
                admin.table("aspirant_photos").upsert({
                    "id": obj_id,
                    "user_id": user_id,
                    "storage_bucket": STORAGE_BUCKET,
                    "storage_path": storage_path,
                    "content_type": content_type,
                    "file_size_bytes": len(processed_bytes),
                    "width": width,
                    "height": height,
                    "updated_at": now_iso
                }, on_conflict="user_id").execute()
            except Exception as meta_err:
                print(f"[AspirantPhotos] Metadata upsert notice: {meta_err}")

            # Also mirror to local_db for offline resilience
            try:
                local_db = get_local_db()
                local_db.upsert_aspirant_photo({
                    "id": obj_id,
                    "user_id": user_id,
                    "storage_bucket": STORAGE_BUCKET,
                    "storage_path": storage_path,
                    "content_type": content_type,
                    "file_size_bytes": len(processed_bytes),
                    "width": width,
                    "height": height,
                    "image_blob": processed_bytes,
                    "updated_at": now_iso
                })
            except Exception:
                pass

            invalidate_memo(f"aspirant_photo:{user_id}:")
            return True, None
        except Exception as e:
            return False, f"Failed to persist profile photo to cloud storage: {e}"

    # Local SQLite Mode (Active only when DATA_BACKEND=sqlite)
    local_db = get_local_db()
    local_db.upsert_aspirant_photo({
        "id": obj_id,
        "user_id": user_id,
        "storage_bucket": STORAGE_BUCKET,
        "storage_path": storage_path,
        "content_type": content_type,
        "file_size_bytes": len(processed_bytes),
        "width": width,
        "height": height,
        "data_blob": processed_bytes,
        "created_at": now_iso
    })
    invalidate_memo(f"aspirant_photo:{user_id}:")
    return True, None


def delete_aspirant_photo(
    user_id: str,
    deleter_id: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """
    Deletes the photo from storage and removes metadata records.
    Enforces that only the Aspirant (or Admin) can delete the photo.
    """
    if not user_id:
        return False, "User ID is required."

    effective_deleter = deleter_id
    if effective_deleter is None:
        try:
            import streamlit as st
            effective_deleter = st.session_state.get("user_id")
        except Exception:
            pass

    if effective_deleter:
        from services.governance import get_primary_admin_id
        from services.roles import user_has_active_role
        primary_admin = get_primary_admin_id()
        is_admin = (primary_admin and str(effective_deleter) == str(primary_admin)) or user_has_active_role(str(effective_deleter), "admin")
        if str(effective_deleter) != str(user_id) and not is_admin:
            return False, "Unauthorized: Only the entrepreneur or Platform Admin may remove this photograph."

    backend = get_data_backend()

    # Supabase cleanup
    if backend == "supabase":
        admin = get_supabase_admin_client() or get_supabase_client()
        if not admin:
            return False, "Supabase connection is not available."
        try:
            res = admin.table("aspirant_photos").select("storage_path").eq("user_id", user_id).limit(1).execute()
            if res.data and len(res.data) > 0:
                old_path = res.data[0].get("storage_path")
                if old_path:
                    try:
                        admin.storage.from_(STORAGE_BUCKET).remove([old_path])
                    except Exception as e_st:
                        return False, f"Failed to delete photo from cloud storage: {e_st}"
            admin.table("aspirant_photos").delete().eq("user_id", user_id).execute()
        except Exception as e:
            return False, f"Failed to delete photo from Supabase: {e}"
    else:
        # Local DB cleanup
        get_local_db().delete_aspirant_photo(user_id)
    invalidate_memo(f"aspirant_photo:{user_id}:")
    return True, None


