"""
scripts/create_unified_database_backup.py
=========================================
Creates an all-inclusive, disaster-recovery database backup archive (.zip) containing:
1. Supabase Cloud Database:
   - JSON exports of all 10 tables (profiles, relationships, journeys, journey_events, 
     help_requests, notifications, assignment_history, schemes, scheme_releases, activity_log)
   - CSV exports of all populated tables
   - Supabase GoTrue Auth accounts metadata (auth_users.json)
2. Local SQLite Database (cluster_a.db):
   - The binary cluster_a.db file
   - Full SQL dump script (cluster_a_dump.sql)
   - JSON exports of all local tables
3. Comprehensive Manifest & Metadata (manifest.json & README.md)
"""

import os
import sys
import json
import csv
import base64
import sqlite3
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from services.auth import get_supabase_admin_client, _get_secrets
from scripts.supabase_backup_manager import BACKUP_TABLES, backup_storage_files, _with_retry


def _json_default(obj):
    if isinstance(obj, bytes):
        return base64.b64encode(obj).decode("ascii")
    return str(obj)

ALL_TABLES = BACKUP_TABLES

BACKUP_DIR = PROJECT_ROOT / "backups"
SQLITE_DB_PATH = PROJECT_ROOT / "cluster_a.db"


def generate_unified_backup():
    print("=" * 75)
    print(" [FULCRUM-INDIA] Building All-Inclusive Unified Database Backup Archive")
    print("=" * 75)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_base_name = f"fulcrum_database_backup_{timestamp}"
    work_dir = BACKUP_DIR / backup_base_name
    shutil.rmtree(work_dir, ignore_errors=True)
    os.makedirs(work_dir, exist_ok=True)

    supabase_dir = work_dir / "supabase_cloud"
    sqlite_dir = work_dir / "sqlite_local"
    os.makedirs(supabase_dir, exist_ok=True)
    os.makedirs(sqlite_dir, exist_ok=True)

    manifest = {
        "backup_name": backup_base_name,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "created_at_local": datetime.now().isoformat(),
        "project": "FULCRUM-INDIA (Cluster A / Cluster B Architecture)",
        "supabase_backup": {
            "status": "pending",
            "url": "",
            "auth_users_count": 0,
            "table_counts": {},
            "total_records": 0,
            "storage_files": {},
            "total_storage_files": 0,
        },
        "sqlite_backup": {
            "status": "pending",
            "db_file": "cluster_a.db",
            "file_size_bytes": 0,
            "table_counts": {},
            "total_records": 0
        }
    }

    # ─────────────────────────────────────────────────────────────
    # PART 1: SUPABASE CLOUD BACKUP
    # ─────────────────────────────────────────────────────────────
    print("\n[PART 1/3] Extracting Supabase Cloud PostgreSQL Data...")
    url, pub_key, sec_key = _get_secrets()
    manifest["supabase_backup"]["url"] = url
    admin = get_supabase_admin_client()

    if admin:
        try:
            # 1. Auth Users
            print("  -> Fetching Supabase Auth Users...")
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
            with open(supabase_dir / "auth_users.json", "w", encoding="utf-8") as f:
                json.dump(auth_data, f, indent=2, ensure_ascii=False)
            manifest["supabase_backup"]["auth_users_count"] = len(auth_data)
            print(f"     [OK] {len(auth_data)} Auth accounts exported")

            # 2. Database Tables
            total_supa_records = 0
            profile_ids = []
            for table in ALL_TABLES:
                try:
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

                    # Save JSON
                    with open(supabase_dir / f"{table}.json", "w", encoding="utf-8") as f:
                        json.dump(records, f, indent=2, default=_json_default, ensure_ascii=False)

                    # Save CSV
                    if records:
                        fieldnames = list(records[0].keys())
                        with open(supabase_dir / f"{table}.csv", "w", newline="", encoding="utf-8") as f:
                            writer = csv.DictWriter(f, fieldnames=fieldnames)
                            writer.writeheader()
                            for row in records:
                                cleaned_row = {
                                    k: (
                                        base64.b64encode(v).decode("ascii")
                                        if isinstance(v, bytes)
                                        else (json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v)
                                    )
                                    for k, v in row.items()
                                }
                                writer.writerow(cleaned_row)

                    manifest["supabase_backup"]["table_counts"][table] = len(records)
                    total_supa_records += len(records)
                    print(f"     [OK] Table '{table}': {len(records)} records")
                except Exception as tbl_err:
                    manifest["supabase_backup"]["table_counts"][table] = f"error: {tbl_err}"
                    print(f"     [!] Table '{table}' error: {tbl_err}")

            # 3. Storage Buckets (Profile Photos & Headshots)
            bucket_counts, total_files = backup_storage_files(admin, str(supabase_dir), profile_ids=profile_ids)
            manifest["supabase_backup"]["storage_files"] = bucket_counts
            manifest["supabase_backup"]["total_storage_files"] = total_files

            manifest["supabase_backup"]["total_records"] = total_supa_records
            manifest["supabase_backup"]["status"] = "success"
        except Exception as e:
            print(f"  [!] Supabase export warning: {e}")
            manifest["supabase_backup"]["status"] = f"error: {e}"
    else:
        print("  [!] Supabase admin client unavailable; skipped cloud export.")
        manifest["supabase_backup"]["status"] = "unavailable"

    # ─────────────────────────────────────────────────────────────
    # PART 2: LOCAL SQLITE DATABASE BACKUP (cluster_a.db)
    # ─────────────────────────────────────────────────────────────
    print("\n[PART 2/3] Extracting Local SQLite Database (cluster_a.db)...")
    if SQLITE_DB_PATH.exists():
        manifest["sqlite_backup"]["file_size_bytes"] = SQLITE_DB_PATH.stat().st_size
        
        # 1. Copy raw cluster_a.db binary file
        shutil.copy2(SQLITE_DB_PATH, sqlite_dir / "cluster_a.db")
        print(f"  -> Raw cluster_a.db copied ({manifest['sqlite_backup']['file_size_bytes'] / 1024:.1f} KB)")

        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # 2. Generate full SQL dump
        dump_path = sqlite_dir / "cluster_a_dump.sql"
        with open(dump_path, "w", encoding="utf-8") as f:
            for line in conn.iterdump():
                f.write(f"{line}\n")
        print(f"  -> Generated SQL dump: {dump_path.name}")

        # 3. Export each table to JSON and CSV
        total_sqlite_records = 0
        for table in ALL_TABLES:
            try:
                cur.execute(f"SELECT * FROM {table}")
                rows = [dict(r) for r in cur.fetchall()]

                with open(sqlite_dir / f"{table}.json", "w", encoding="utf-8") as f:
                    json.dump(rows, f, indent=2, default=_json_default, ensure_ascii=False)

                if rows:
                    fieldnames = list(rows[0].keys())
                    with open(sqlite_dir / f"{table}.csv", "w", newline="", encoding="utf-8") as f:
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        for row in rows:
                            cleaned_row = {
                                k: (
                                    base64.b64encode(v).decode("ascii")
                                    if isinstance(v, bytes)
                                    else (json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v)
                                )
                                for k, v in row.items()
                            }
                            writer.writerow(cleaned_row)
                manifest["sqlite_backup"]["table_counts"][table] = len(rows)
                total_sqlite_records += len(rows)
                print(f"     [OK] Table '{table}': {len(rows)} records")
            except Exception as e:
                manifest["sqlite_backup"]["table_counts"][table] = f"error: {e}"
                print(f"     [!] Table '{table}' error: {e}")

        conn.close()
        manifest["sqlite_backup"]["total_records"] = total_sqlite_records
        manifest["sqlite_backup"]["status"] = "success"
    else:
        print("  [!] cluster_a.db not found.")
        manifest["sqlite_backup"]["status"] = "not_found"

    # ─────────────────────────────────────────────────────────────
    # PART 3: MANIFEST & README
    # ─────────────────────────────────────────────────────────────
    print("\n[PART 3/3] Generating Manifest, Documentation, and Packaging ZIP...")

    with open(work_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    readme_content = f"""# FULCRUM-INDIA Database Backup Archive
======================================
- Generated at: {manifest['created_at_local']} (UTC: {manifest['created_at_utc']})
- Project: {manifest['project']}

## Archive Contents

### 1. `supabase_cloud/` (Production Live Cloud Database)
- Source URL: {manifest['supabase_backup'].get('url')}
- Auth Accounts: {manifest['supabase_backup'].get('auth_users_count')}
- Total Database Records: {manifest['supabase_backup'].get('total_records')}
- Storage Files (Photos): {manifest['supabase_backup'].get('total_storage_files', 0)}
- Tables Included:
{chr(10).join([f"  - {t}: {c} rows" for t, c in manifest['supabase_backup'].get('table_counts', {}).items()])}
- Files: JSON and CSV representations of each table, `auth_users.json`, and `storage_files/`

### 2. `sqlite_local/` (Local / Offline Testing Database)
- Source File: `cluster_a.db` ({manifest['sqlite_backup'].get('file_size_bytes', 0) / 1024:.1f} KB)
- Total Database Records: {manifest['sqlite_backup'].get('total_records')}
- Tables Included:
{chr(10).join([f"  - {t}: {c} rows" for t, c in manifest['sqlite_backup'].get('table_counts', {}).items()])}
- Files:
  - `cluster_a.db` (Binary SQLite database)
  - `cluster_a_dump.sql` (Full SQL DDL & DML script)
  - JSON and CSV files for all tables

## How to Restore

### To Restore into Supabase:
```bash
python scripts/supabase_backup_manager.py restore <path_to_zip>
```

### To Restore into Local SQLite:
```bash
python scripts/supabase_backup_manager.py restore-sqlite <path_to_zip>
```
Or directly copy `sqlite_local/cluster_a.db` into the project root.
"""
    with open(work_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    # Compress into ZIP
    zip_path = BACKUP_DIR / f"{backup_base_name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(work_dir):
            for file in files:
                file_full = Path(root) / file
                rel_path = file_full.relative_to(work_dir)
                zipf.write(file_full, rel_path)

    # Clean up working temp directory
    shutil.rmtree(work_dir, ignore_errors=True)

    zip_size_kb = zip_path.stat().st_size / 1024
    print("=" * 75)
    print(" [SUCCESS] Unified Database Backup Archive Created Successfully!")
    print(f" Archive File : {zip_path}")
    print(f" Size         : {zip_size_kb:.1f} KB")
    print(f" Supabase DB  : {manifest['supabase_backup']['total_records']} rows, {manifest['supabase_backup']['auth_users_count']} auth accounts, {manifest['supabase_backup'].get('total_storage_files', 0)} photos")
    print(f" Local SQLite : {manifest['sqlite_backup']['total_records']} rows, {manifest['sqlite_backup']['file_size_bytes'] / 1024:.1f} KB")
    print("=" * 75)
    return str(zip_path)


if __name__ == "__main__":
    generate_unified_backup()
