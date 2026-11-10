"""
scripts/supabase_backup_manager.py — Enterprise Backup & Disaster Recovery for Supabase
======================================================================================
Usage:
    # 1. Take a full backup of all Supabase data into a timestamped .zip:
    python scripts/supabase_backup_manager.py backup

    # 2. Restore data from a backup .zip back into Supabase:
    python scripts/supabase_backup_manager.py restore backups/supabase_backup_YYYY-MM-DD_HH-MM-SS.zip

    # 3. Restore data from a backup .zip into Local SQLite (if Supabase is down):
    python scripts/supabase_backup_manager.py restore-sqlite backups/supabase_backup_YYYY-MM-DD_HH-MM-SS.zip
"""

import os
import sys
import json
import csv
import time
import shutil
import zipfile
from datetime import datetime

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from services.auth import get_supabase_admin_client, get_supabase_client

BACKUP_TABLES = [
    # 1. Identity, Roles & Permissions
    "profiles",
    "user_roles",

    # 2. Legal Compliance & NDAs
    "legal_documents",
    "legal_acceptances",

    # 3. Core Entrepreneur Journeys & Milestones
    "journeys",
    "journey_events",
    "journey_event_revisions",

    # 4. Mentorship Allocations & Operational Review
    "relationships",
    "assignment_history",
    "scheme_support_reviews",
    "case_discussions",
    "guide_complaints",
    "sme_conflict_declarations",
    "inactivity_logs",
    "external_contact_logs",

    # 5. Schemes Catalogue & Gatekeeper Releases
    "schemes",
    "scheme_releases",

    # 6. Communications & In-App Alerts
    "help_requests",
    "notifications",

    # 7. Photo Records Metadata
    "aspirant_photos",
    "professional_photos",

    # 8. Immutable Governance & Audit Logs
    "activity_log",
    "account_lifecycle_log",
]

STORAGE_BUCKETS = [
    "aspirant-profile-photos",
    "professional-headshots",
]

BACKUP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backups"))


def backup_storage_files(admin, target_dir: str, profile_ids: list | None = None) -> tuple[dict, int]:
    """
    Downloads uploaded images/headshots from Supabase Storage buckets into target_dir/storage_files/.
    Combines explicit DB paths (aspirant_photos / professional_photos) with bucket scanning.
    Returns (bucket_counts_dict, total_files_downloaded).
    """
    print("\n[3/4] Exporting Supabase Storage Buckets (Profile Photos & Headshots)...")
    storage_base = os.path.join(target_dir, "storage_files")
    os.makedirs(storage_base, exist_ok=True)
    bucket_counts = {}
    total_downloaded = 0

    # 1. Collect all explicit file paths from photo tables
    files_to_download: dict[str, set[str]] = {b: set() for b in STORAGE_BUCKETS}
    for table, default_bucket in [
        ("aspirant_photos", "aspirant-profile-photos"),
        ("professional_photos", "professional-headshots"),
    ]:
        try:
            res = admin.table(table).select("storage_bucket, storage_path").execute()
            for row in (res.data or []):
                b = row.get("storage_bucket") or default_bucket
                p = row.get("storage_path")
                if b and p:
                    files_to_download.setdefault(b, set()).add(p)
        except Exception as e:
            print(f"  Notice querying {table} paths: {e}")

    # 2. Check bucket roots and active user folders
    active_ids_set = set(str(pid) for pid in (profile_ids or []) if pid)
    for bucket in STORAGE_BUCKETS:
        try:
            root_items = admin.storage.from_(bucket).list("", {"limit": 1000}) or []
            folders = [it.get("name") for it in root_items if it.get("name") and it.get("id") is None]
            root_files = [it.get("name") for it in root_items if it.get("name") and it.get("id") is not None]
            for rf in root_files:
                files_to_download[bucket].add(rf)

            # Scan all folders if small count (<= 25), otherwise scan folders for active profiles
            folders_to_scan = folders if len(folders) <= 25 else [f for f in folders if f in active_ids_set]
            for folder_name in folders_to_scan:
                for attempt in range(2):
                    try:
                        sub_items = admin.storage.from_(bucket).list(folder_name, {"limit": 50}) or []
                        for sub in sub_items:
                            sub_name = sub.get("name")
                            if sub_name and sub.get("id") is not None:
                                files_to_download[bucket].add(f"{folder_name}/{sub_name}")
                        break
                    except Exception:
                        time.sleep(0.5)
        except Exception as e:
            print(f"  Notice listing bucket '{bucket}': {e}")

    # 3. Download all discovered files with retry logic
    for bucket, paths in files_to_download.items():
        bucket_dir = os.path.join(storage_base, bucket)
        os.makedirs(bucket_dir, exist_ok=True)
        count = 0
        for rel_path in sorted(paths):
            dest_file = os.path.join(bucket_dir, rel_path.replace("/", os.sep))
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            for attempt in range(4):
                try:
                    data = admin.storage.from_(bucket).download(rel_path)
                    if data:
                        with open(dest_file, "wb") as f:
                            f.write(data)
                        count += 1
                        break
                except Exception as dl_err:
                    if attempt == 3:
                        print(f"  ⚠ Failed downloading {bucket}/{rel_path}: {dl_err}")
                    time.sleep(1)

        bucket_counts[bucket] = count
        total_downloaded += count
        print(f"  ✓ Storage bucket '{bucket}': {count} files saved")

    return bucket_counts, total_downloaded


def _with_retry(fn, retries: int = 4, delay: float = 1.0):
    """Executes fn() with exponential-ish retry backoff for transient TLS/network drops."""
    last_err = None
    for attempt in range(retries):
        try:
            return fn()
        except Exception as e:
            last_err = e
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))
    raise last_err


def backup_supabase():
    """Extracts all tables, auth users, and storage photos from Supabase and packs them into a .zip archive."""
    print("=" * 70)
    print(" [FULCRUM-INDIA] Initiating Supabase Full Data Backup")
    print("=" * 70)

    admin = get_supabase_admin_client()
    if not admin:
        print("[ERROR] Supabase Admin Client unavailable. Check your .streamlit/secrets.toml configuration.")
        return None

    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    temp_folder = os.path.join(BACKUP_DIR, f"supabase_backup_{timestamp}")
    os.makedirs(temp_folder, exist_ok=True)

    metadata = {
        "timestamp": timestamp,
        "backup_date_iso": datetime.now().isoformat(),
        "tables": {},
        "storage_files": {},
        "auth_users_count": 0,
        "total_records": 0,
        "total_storage_files": 0,
    }

    # 1. Backup Auth Users Metadata
    print("\n[1/4] Exporting Supabase Auth Users...")
    try:
        users = _with_retry(lambda: admin.auth.admin.list_users())
        auth_data = []
        for u in users:
            auth_data.append({
                "id": str(getattr(u, "id", "")),
                "email": getattr(u, "email", ""),
                "role": getattr(u, "role", ""),
                "created_at": str(getattr(u, "created_at", "")),
                "last_sign_in_at": str(getattr(u, "last_sign_in_at", "")),
                "user_metadata": getattr(u, "user_metadata", {}) or {},
            })
        auth_json_path = os.path.join(temp_folder, "auth_users.json")
        with open(auth_json_path, "w", encoding="utf-8") as f:
            json.dump(auth_data, f, indent=2, ensure_ascii=False)
        metadata["auth_users_count"] = len(auth_data)
        print(f"  ✓ Exported {len(auth_data)} Auth users to auth_users.json")
    except Exception as e:
        print(f"  ⚠ Failed to export Auth users list: {e}")

    # 2. Backup Each Public Table
    print("\n[2/4] Exporting Database Tables (JSON + CSV)...")
    total_records = 0
    profile_ids = []
    for table in BACKUP_TABLES:
        try:
            # Fetch all records without pagination limits
            records = []
            page_size = 1000
            offset = 0
            while True:
                res = _with_retry(lambda t=table, o=offset: admin.table(t).select("*").range(o, o + page_size - 1).execute())
                batch = res.data or []
                records.extend(batch)
                if len(batch) < page_size:
                    break
                offset += page_size

            if table == "profiles":
                profile_ids = [r.get("id") for r in records if r.get("id")]

            # Save as JSON
            table_json_path = os.path.join(temp_folder, f"{table}.json")
            with open(table_json_path, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=2, default=str, ensure_ascii=False)

            # Save as CSV if records exist
            if records:
                table_csv_path = os.path.join(temp_folder, f"{table}.csv")
                fieldnames = list(records[0].keys())
                with open(table_csv_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in records:
                        # Serialize dicts/lists to JSON strings for CSV compatibility
                        cleaned_row = {
                            k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v)
                            for k, v in row.items()
                        }
                        writer.writerow(cleaned_row)

            metadata["tables"][table] = len(records)
            total_records += len(records)
            print(f"  ✓ Table '{table}': {len(records)} rows")
        except Exception as e:
            print(f"  ✗ Table '{table}' error: {e}")
            metadata["tables"][table] = f"Error: {e}"

    metadata["total_records"] = total_records

    # 3. Backup Storage Buckets (Profile Photos & Headshots)
    bucket_counts, total_files = backup_storage_files(admin, temp_folder, profile_ids=profile_ids)
    metadata["storage_files"] = bucket_counts
    metadata["total_storage_files"] = total_files

    # Save metadata.json
    with open(os.path.join(temp_folder, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    # 4. Create ZIP Archive
    print("\n[4/4] Packaging into Compressed ZIP Archive...")
    zip_filename = f"supabase_backup_{timestamp}.zip"
    zip_path = os.path.join(BACKUP_DIR, zip_filename)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(temp_folder):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, temp_folder)
                zipf.write(full_path, rel_path)

    # Remove temporary unzipped directory
    shutil.rmtree(temp_folder, ignore_errors=True)

    zip_size_kb = os.path.getsize(zip_path) / 1024
    print("=" * 70)
    print(" [SUCCESS] Supabase Backup Completed Successfully!")
    print(f"  ZIP File  : {zip_path}")
    print(f"  Size      : {zip_size_kb:.1f} KB")
    print(f"  Records   : {total_records} database rows + {metadata['auth_users_count']} auth accounts")
    print(f"  Photos    : {total_files} storage bucket files")
    print("=" * 70)
    return zip_path


def restore_supabase(zip_file_path: str):
    """Restores tables and storage bucket files from a backup .zip archive back into Supabase."""
    print("=" * 70)
    print(" [FULCRUM-INDIA] Initiating Supabase Data Restoration")
    print(f" Source ZIP: {zip_file_path}")
    print("=" * 70)

    if not os.path.exists(zip_file_path):
        print(f"[ERROR] Backup file not found: {zip_file_path}")
        return False

    admin = get_supabase_admin_client()
    if not admin:
        print("[ERROR] Supabase Admin Client unavailable. Cannot connect to Supabase.")
        return False

    # Extract ZIP to temporary folder
    temp_extract_dir = os.path.join(BACKUP_DIR, "temp_restore")
    shutil.rmtree(temp_extract_dir, ignore_errors=True)
    os.makedirs(temp_extract_dir, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_file_path, "r") as zipf:
            zipf.extractall(temp_extract_dir)

        # Detect data folder (handles both direct backup and unified backup archive formats)
        data_dir = temp_extract_dir
        if os.path.exists(os.path.join(temp_extract_dir, "supabase_cloud")):
            data_dir = os.path.join(temp_extract_dir, "supabase_cloud")

        # Read metadata if present
        meta_path = os.path.join(temp_extract_dir, "metadata.json")
        if not os.path.exists(meta_path) and os.path.exists(os.path.join(data_dir, "metadata.json")):
            meta_path = os.path.join(data_dir, "metadata.json")
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            print(f" Backup created at: {meta.get('timestamp')}")
            print(f" Total records in backup: {meta.get('total_records')}")

        # Pre-provision Auth Users if restoring into a fresh/new Supabase project
        auth_file = os.path.join(data_dir, "auth_users.json")
        if os.path.exists(auth_file):
            try:
                with open(auth_file, "r", encoding="utf-8") as f:
                    auth_users = json.load(f)
                existing_ids = set()
                try:
                    current_users = admin.auth.admin.list_users()
                    existing_ids = {getattr(u, "id", "") for u in current_users}
                except Exception:
                    pass

                for au in auth_users:
                    u_id = au.get("id")
                    u_email = au.get("email")
                    if u_id and u_id not in existing_ids:
                        try:
                            admin.auth.admin.create_user({
                                "id": u_id,
                                "email": u_email,
                                "email_confirm": True,
                                "user_metadata": au.get("user_metadata") or {}
                            })
                            print(f"  ✓ Provisioned Auth account for new project: {u_email}")
                        except Exception:
                            pass
            except Exception as e:
                print(f"  Notice during auth pre-provision: {e}")

        # Restore tables in dependency order
        for table in BACKUP_TABLES:
            table_file = os.path.join(data_dir, f"{table}.json")
            if not os.path.exists(table_file):
                continue

            with open(table_file, "r", encoding="utf-8") as f:
                records = json.load(f)

            if not records:
                continue

            print(f" - Restoring table '{table}' ({len(records)} records)...")
            batch_size = 100
            success_count = 0
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                try:
                    # Upsert handles existing rows gracefully without duplicate key errors
                    admin.table(table).upsert(batch, on_conflict="id").execute()
                    success_count += len(batch)
                except Exception as e:
                    print(f"   ⚠ Batch {i}-{i+len(batch)} error on '{table}': {e}")

            print(f"   ✓ Successfully upserted {success_count}/{len(records)} records into '{table}'.")

        # Restore storage files if present in the archive
        storage_dir = os.path.join(data_dir, "storage_files")
        if not os.path.exists(storage_dir) and os.path.exists(os.path.join(temp_extract_dir, "storage_files")):
            storage_dir = os.path.join(temp_extract_dir, "storage_files")

        if os.path.exists(storage_dir):
            print("\n - Restoring Storage Buckets (Profile Photos & Headshots)...")
            for bucket_name in os.listdir(storage_dir):
                b_path = os.path.join(storage_dir, bucket_name)
                if not os.path.isdir(b_path):
                    continue
                try:
                    # Idempotently ensure bucket exists
                    try:
                        admin.storage.create_bucket(bucket_name, options={"public": False})
                    except Exception:
                        pass

                    uploaded = 0
                    for root, _, files in os.walk(b_path):
                        for f in files:
                            full_p = os.path.join(root, f)
                            rel_p = os.path.relpath(full_p, b_path).replace("\\", "/")
                            with open(full_p, "rb") as fh:
                                file_bytes = fh.read()
                            try:
                                admin.storage.from_(bucket_name).upload(rel_p, file_bytes, {"upsert": "true"})
                                uploaded += 1
                            except Exception as up_err:
                                print(f"   ⚠ Could not upload {bucket_name}/{rel_p}: {up_err}")
                    print(f"   ✓ Restored {uploaded} files into bucket '{bucket_name}'.")
                except Exception as e:
                    print(f"  Notice restoring bucket '{bucket_name}': {e}")

        print("=" * 70)
        print(" [SUCCESS] Supabase Restoration Finished Successfully!")
        print("=" * 70)
        return True
    finally:
        shutil.rmtree(temp_extract_dir, ignore_errors=True)


def restore_to_sqlite(zip_file_path: str):
    """Emergency offline restore: populates local SQLite from a backup archive."""
    print("=" * 70)
    print(" [FULCRUM-INDIA] Emergency Restoration into Local SQLite Database")
    print(f" Source ZIP: {zip_file_path}")
    print("=" * 70)

    if not os.path.exists(zip_file_path):
        print(f"[ERROR] Backup file not found: {zip_file_path}")
        return False

    from services.local_db import get_local_db
    db = get_local_db()
    conn = db._get_conn()

    temp_extract_dir = os.path.join(BACKUP_DIR, "temp_restore_sqlite")
    shutil.rmtree(temp_extract_dir, ignore_errors=True)
    os.makedirs(temp_extract_dir, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_file_path, "r") as zipf:
            zipf.extractall(temp_extract_dir)

        # Detect data folder (handles both direct backup and unified backup archive formats)
        data_dir = temp_extract_dir
        if os.path.exists(os.path.join(temp_extract_dir, "supabase_cloud")):
            data_dir = os.path.join(temp_extract_dir, "supabase_cloud")
        elif os.path.exists(os.path.join(temp_extract_dir, "sqlite_local")):
            data_dir = os.path.join(temp_extract_dir, "sqlite_local")

        cur = conn.cursor()
        for table in BACKUP_TABLES:
            table_file = os.path.join(data_dir, f"{table}.json")
            if not os.path.exists(table_file):
                continue
            with open(table_file, "r", encoding="utf-8") as f:
                records = json.load(f)
            if not records:
                continue

            try:
                cols_info = cur.execute(f"PRAGMA table_info({table})").fetchall()
                if not cols_info:
                    continue
                col_names = [c[1] for c in cols_info]
                placeholders = ", ".join(["?"] * len(col_names))
                sql = f"INSERT OR REPLACE INTO {table} ({', '.join(col_names)}) VALUES ({placeholders})"
                for r in records:
                    row_vals = []
                    for c in col_names:
                        v = r.get(c)
                        if isinstance(v, (dict, list)):
                            v = json.dumps(v, ensure_ascii=False)
                        row_vals.append(v)
                    cur.execute(sql, row_vals)
                conn.commit()
                print(f"  ✓ Restored {len(records)} rows into local SQLite table '{table}'.")
            except Exception as e:
                print(f"  ⚠ SQLite restore error on '{table}': {e}")

        print("=" * 70)
        print(" [SUCCESS] Local SQLite Emergency Restoration Complete!")
        print("=" * 70)
        return True
    finally:
        conn.close()
        shutil.rmtree(temp_extract_dir, ignore_errors=True)


def export_database_to_dict():
    """Fetches all Supabase tables and auth metadata into a single Python dict for UI/JSON export."""
    admin = get_supabase_admin_client()
    if not admin:
        return {"error": "Supabase Admin Client unavailable."}

    data = {
        "metadata": {
            "app": "FULCRUM-INDIA",
            "version": "1.0",
            "exported_at": datetime.now().isoformat(),
            "tables": {},
            "total_records": 0,
        },
        "auth_users": [],
        "tables": {},
    }

    # Auth users
    try:
        users = admin.auth.admin.list_users()
        for u in users:
            data["auth_users"].append({
                "id": str(getattr(u, "id", "")),
                "email": getattr(u, "email", ""),
                "role": getattr(u, "role", ""),
                "created_at": str(getattr(u, "created_at", "")),
                "user_metadata": getattr(u, "user_metadata", {}) or {},
            })
    except Exception as e:
        print(f"[Backup] Auth users export notice: {e}")

    total_records = 0
    for table in BACKUP_TABLES:
        try:
            records = []
            page_size = 1000
            offset = 0
            while True:
                res = admin.table(table).select("*").range(offset, offset + page_size - 1).execute()
                batch = res.data or []
                records.extend(batch)
                if len(batch) < page_size:
                    break
                offset += page_size
            data["tables"][table] = records
            data["metadata"]["tables"][table] = len(records)
            total_records += len(records)
        except Exception as e:
            data["tables"][table] = []
            data["metadata"]["tables"][table] = f"Error: {e}"

    data["metadata"]["total_records"] = total_records
    return data


def import_database_from_dict(data: dict):
    """Restores database from a parsed export dictionary into Supabase with upsert protection."""
    admin = get_supabase_admin_client()
    if not admin:
        return {"error": "Supabase Admin Client unavailable."}

    tables_data = data.get("tables", {})
    if not tables_data and any(t in data for t in BACKUP_TABLES):
        tables_data = {t: data[t] for t in BACKUP_TABLES if t in data}

    results = {"success": True, "restored": {}, "errors": {}}
    total_restored = 0

    for table in BACKUP_TABLES:
        records = tables_data.get(table, [])
        if not records:
            continue

        batch_size = 100
        success_count = 0
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            try:
                admin.table(table).upsert(batch, on_conflict="id").execute()
                success_count += len(batch)
            except Exception as e:
                results["errors"][table] = str(e)
                print(f"[Restore] Upsert error on '{table}': {e}")

        results["restored"][table] = success_count
        total_restored += success_count

    results["total_restored"] = total_restored
    return results


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "backup":
        backup_supabase()
    elif args[0] == "restore":
        if len(args) < 2:
            print("Usage: python scripts/supabase_backup_manager.py restore <path_to_backup.zip>")
        else:
            restore_supabase(args[1])
    elif args[0] in ["restore-sqlite", "restore_sqlite"]:
        if len(args) < 2:
            print("Usage: python scripts/supabase_backup_manager.py restore-sqlite <path_to_backup.zip>")
        else:
            restore_to_sqlite(args[1])
    else:
        print(f"Unknown command: {args[0]}")
        print("Available commands: backup, restore <file.zip>, restore-sqlite <file.zip>")
