"""
scripts/package_fresh_release.py
================================
Packages the clean-slate, copy-only release package FULCRUM_FRESH_DEPLOYMENT/
and creates FULCRUM_FRESH_DEPLOYMENT.zip with SHA-256 file manifest.

Guarantees:
- Copy-only: does not move or delete any source files.
- Excludes .env, secrets.toml, *.db, tests/, scratch/, artifacts/, backups/, pycache.
- Computes SHA-256 hash and size for every single file.
"""

import os
import sys
import shutil
import hashlib
import zipfile

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_DIR = os.path.join(WORKSPACE_ROOT, "FULCRUM_FRESH_DEPLOYMENT")
ZIP_PATH = os.path.join(WORKSPACE_ROOT, "FULCRUM_FRESH_DEPLOYMENT.zip")
MANIFEST_PATH = os.path.join(TARGET_DIR, "RELEASE_FILE_MANIFEST_SHA256.txt")

FORBIDDEN_EXTENSIONS = {".db", ".db-journal", ".bak", ".log", ".pyc"}
FORBIDDEN_FILENAMES = {".env", "secrets.toml", "cluster_a.db", "fulcrum.db"}

def sha256_file(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def package():
    print(f"[*] Workspace Root: {WORKSPACE_ROOT}")
    print(f"[*] Target Release Directory: {TARGET_DIR}")

    if os.path.exists(TARGET_DIR):
        print(f"[*] Cleaning pre-existing target directory: {TARGET_DIR}")
        shutil.rmtree(TARGET_DIR)
    os.makedirs(TARGET_DIR, exist_ok=True)

    # 1. Define files and directories to copy
    root_files = [
        "app.py",
        "Dockerfile",
        ".dockerignore",
        "docker-compose.yml",
        "requirements.txt",
        "Caddyfile",
    ]

    explicit_copies = [
        (".streamlit/config.toml", ".streamlit/config.toml"),
        ("seed/canonical_179_schemes.json", "seed/canonical_179_schemes.json"),
        ("seed/seed_179_schemes_idempotent.sql", "seed/seed_179_schemes_idempotent.sql"),
    ]

    # Directories to copy fully (filtering .pyc and __pycache__)
    dirs_to_copy = [
        "services",
        "views",
        "migrations",
    ]

    # Specific scripts
    script_files = [
        "scripts/health_check.py",
        "scripts/FRESH_FULCRUM_ONLY_DEPLOY.sh",
        "scripts/SAFE_FULCRUM_ONLY_ROLLBACK.sh",
        "scripts/status.sh",
        "scripts/logs.sh",
        "scripts/restart.sh",
    ]

    copied_files = []

    # Copy root files
    for rf in root_files:
        src = os.path.join(WORKSPACE_ROOT, rf)
        dst = os.path.join(TARGET_DIR, rf)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            copied_files.append(rf)
        else:
            print(f"[!] Warning: Root file missing: {rf}")

    # Copy explicit files
    for rel_src, rel_dst in explicit_copies:
        src = os.path.join(WORKSPACE_ROOT, rel_src)
        dst = os.path.join(TARGET_DIR, rel_dst)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            copied_files.append(rel_dst)
        else:
            print(f"[!] Warning: Explicit file missing: {rel_src}")

    # Copy directories
    for d in dirs_to_copy:
        src_dir = os.path.join(WORKSPACE_ROOT, d)
        dst_dir = os.path.join(TARGET_DIR, d)
        for root, dirs, files in os.walk(src_dir):
            if "__pycache__" in root:
                continue
            rel_dir = os.path.relpath(root, WORKSPACE_ROOT)
            target_sub = os.path.join(TARGET_DIR, rel_dir)
            os.makedirs(target_sub, exist_ok=True)
            for f in files:
                if f.endswith(".pyc") or f.endswith(".pyo"):
                    continue
                s_file = os.path.join(root, f)
                d_file = os.path.join(target_sub, f)
                shutil.copy2(s_file, d_file)
                copied_files.append(os.path.relpath(d_file, TARGET_DIR).replace("\\", "/"))

    # Copy script files
    for sf in script_files:
        src = os.path.join(WORKSPACE_ROOT, sf)
        dst = os.path.join(TARGET_DIR, sf)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            copied_files.append(sf.replace("\\", "/"))
        else:
            print(f"[!] Warning: Script file missing: {sf}")

    # Security check on copied files
    for cf in copied_files:
        basename = os.path.basename(cf)
        ext = os.path.splitext(basename)[1].lower()
        if basename in FORBIDDEN_FILENAMES or ext in FORBIDDEN_EXTENSIONS:
            raise RuntimeError(f"SECURITY VIOLATION: Forbidden file copied into release: {cf}")

    # 2. Generate File Manifest
    manifest_lines = [
        "# ==============================================================================",
        "# FULCRUM PRODUCTION RELEASE MANIFEST — SHA-256 CHECKSUMS",
        "# Package: FULCRUM_FRESH_DEPLOYMENT",
        f"# Total Files: {len(copied_files)}",
        "# ==============================================================================",
        f"{'SHA-256 HASH':<66} {'SIZE (BYTES)':<14} {'FILE PATH'}",
        "-" * 110,
    ]

    manifest_entries = []
    for rel_path in sorted(copied_files):
        full_p = os.path.join(TARGET_DIR, rel_path.replace("/", os.sep))
        h = sha256_file(full_p)
        sz = os.path.getsize(full_p)
        manifest_lines.append(f"{h:<66} {sz:<14} {rel_path}")
        manifest_entries.append((rel_path, h, sz))

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(manifest_lines) + "\n")

    print(f"[+] Generated manifest with {len(copied_files)} files: {MANIFEST_PATH}")

    # Copy manifest also to root directory for easy inspection
    shutil.copy2(MANIFEST_PATH, os.path.join(WORKSPACE_ROOT, "RELEASE_FILE_MANIFEST_SHA256.txt"))

    # 3. Create ZIP Archive
    print(f"[*] Packaging ZIP archive: {ZIP_PATH}...")
    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(TARGET_DIR):
            for file in files:
                full_p = os.path.join(root, file)
                rel_p = os.path.relpath(full_p, TARGET_DIR)
                # Archive under root prefix FULCRUM_FRESH_DEPLOYMENT/
                arcname = os.path.join("FULCRUM_FRESH_DEPLOYMENT", rel_p).replace("\\", "/")
                zf.write(full_p, arcname)

    zip_size_mb = os.path.getsize(ZIP_PATH) / (1024 * 1024)
    print(f"[+] ZIP Package created successfully: {ZIP_PATH} ({zip_size_mb:.2f} MB)")
    print(f"[+] Verified: No secret files (.env, secrets.toml, *.db) packaged.")

if __name__ == "__main__":
    package()

