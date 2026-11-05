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
4. Image Optimization: Strips EXIF metadata, resizes to max 512x512, compresses to WebP.
5. Dual-Backend Resilience: Seamless fallback to LocalDatabase for offline/testing.
"""

import io
import uuid
import base64
from datetime import datetime, timezone
from typing import Optional, Tuple, Dict
from PIL import Image

from services.auth import get_supabase_client, get_supabase_admin_client, get_data_backend
from services.local_db import get_local_db

STORAGE_BUCKET = "aspirant-profile-photos"
MAX_UPLOAD_BYTES = 5 * 1024 * 1024  # 5 MB
MAX_TARGET_DIM = 512
SIGNED_URL_EXPIRY_SECONDS = 300


def validate_and_process_photo(raw_bytes: bytes) -> Tuple[bool, Optional[bytes], Optional[str], Optional[int], Optional[int], Optional[str]]:
    """
    Validates, strips EXIF, resizes (max 512x512), and compresses to WebP.
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

        # Convert colorspace safely (strip EXIF metadata by loading raw pixel data)
        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            # Create a clean RGB canvas with white background if transparency exists
            clean_img = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            clean_img.paste(img, mask=img.split()[3] if len(img.split()) >= 4 else None)
            img = clean_img
        elif img.mode != "RGB":
            img = img.convert("RGB")

        # Resize with high-quality LANCZOS while preserving aspect ratio
        img.thumbnail((MAX_TARGET_DIM, MAX_TARGET_DIM), Image.Resampling.LANCZOS)
        width, height = img.size

        # Save to WebP format without EXIF metadata
        out_buf = io.BytesIO()
        img.save(out_buf, format="WEBP", quality=85, method=6)
        processed_bytes = out_buf.getvalue()

        return True, processed_bytes, "image/webp", width, height, None
    except Exception as e:
        return False, None, None, None, None, f"Failed to process image: {str(e)}"


def get_aspirant_photo(user_id: str) -> Optional[Dict]:
    """
    Retrieves photo metadata and short-lived signed URL or base64 data URI.
    Returns None if no photo is registered for this aspirant.
    """
    if not user_id:
        return None

    backend = get_data_backend()

    # 1. Supabase Mode
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
                        # Generate fresh signed URL
                        signed_res = client.storage.from_(bucket).create_signed_url(path, SIGNED_URL_EXPIRY_SECONDS)
                        signed_url = (
                            signed_res.get("signedURL")
                            or signed_res.get("signedUrl")
                            or (signed_res.get("data", {}).get("signedUrl") if isinstance(signed_res, dict) else None)
                        )
                        record["url"] = signed_url
                        return record
            except Exception as e:
                # Fallback to local DB check if table is not yet migrated in Supabase
                pass

    # 2. Local Database / Fallback Mode
    local_record = get_local_db().get_aspirant_photo(user_id)
    if local_record:
        data_blob = local_record.get("data_blob")
        if data_blob:
            b64_data = base64.b64encode(data_blob).decode("ascii")
            local_record["url"] = f"data:{local_record.get('content_type', 'image/webp')};base64,{b64_data}"
            return local_record

    return None


def upload_aspirant_photo(user_id: str, file_bytes: bytes, filename: str = "avatar.webp") -> Tuple[bool, Optional[str]]:
    """
    Validates, compresses, and saves aspirant photo.
    IMPORTANT: Non-destructive — never invokes update_aspirant_profile() or journey logging.
    """
    if not user_id:
        return False, "User ID is required."

    ok, processed_bytes, content_type, width, height, err = validate_and_process_photo(file_bytes)
    if not ok:
        return False, err

    backend = get_data_backend()
    now_iso = datetime.now(timezone.utc).isoformat()
    obj_id = str(uuid.uuid4())
    storage_path = f"{user_id}/avatar_{uuid.uuid4().hex[:8]}.webp"

    # Always persist locally for offline/test reliability
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

    # Supabase upload
    if backend == "supabase":
        admin = get_supabase_admin_client() or get_supabase_client()
        if admin:
            try:
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

                # 2. Upload new compressed file
                upload_res = admin.storage.from_(STORAGE_BUCKET).upload(
                    storage_path,
                    processed_bytes,
                    {"content-type": content_type, "upsert": "true"}
                )

                # 3. Upsert metadata in aspirant_photos
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

                return True, None
            except Exception as e:
                # Stored in local fallback
                return True, None

    return True, None


def delete_aspirant_photo(user_id: str) -> Tuple[bool, Optional[str]]:
    """
    Deletes the photo from storage and removes metadata records.
    """
    if not user_id:
        return False, "User ID is required."

    backend = get_data_backend()

    # Supabase cleanup
    if backend == "supabase":
        admin = get_supabase_admin_client() or get_supabase_client()
        if admin:
            try:
                res = admin.table("aspirant_photos").select("storage_path").eq("user_id", user_id).limit(1).execute()
                if res.data and len(res.data) > 0:
                    old_path = res.data[0].get("storage_path")
                    if old_path:
                        try:
                            admin.storage.from_(STORAGE_BUCKET).remove([old_path])
                        except Exception:
                            pass
                admin.table("aspirant_photos").delete().eq("user_id", user_id).execute()
            except Exception:
                pass

    # Local DB cleanup
    get_local_db().delete_aspirant_photo(user_id)
    return True, None

