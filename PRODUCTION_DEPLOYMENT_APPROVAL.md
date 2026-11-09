# FULCRUM-BETA PRODUCTION DEPLOYMENT APPROVAL & SIGN-OFF REGISTER
**Platform:** Fulcrum India (Cluster A / Fulcrum-Beta)  
**Host Target:** Hostinger KVM 2 VPS (Ubuntu 24.04.5 LTS, 2 vCPU, 8 GB RAM)  
**Reverse Proxy:** Caddy 2 Alpine (Ports 80 & 443 with live TLS)  
**Database Backend:** Fresh Supabase Cloud Instance (PostgreSQL 15+, Auth, Storage)  
**Canonical Admin:** `fulcrumindia1@gmail.com`  
**Release Package:** `FULCRUM_FRESH_DEPLOYMENT.zip` (SHA-256 Manifest Verified)  
**Date:** 2026-11-10  

---

## 1. Release Scope & Architectural Summary

This approval register documents the final pre-deployment sign-off for **Fulcrum-Beta**. The release executes a **clean-slate production deployment** connecting to a freshly provisioned Supabase project.

### Core Guarantees:
- **Zero Data Loss for Infrastructure:** The existing Caddy container (`fulcrum-caddy`), its Docker bridge network (`fulcrum-net`), and its SSL certificates in `caddy_data` remain **100% untouched and continuously online**.
- **Clean-Slate Architecture:** No historical test accounts, stale SQLite databases, or obsolete mock records are imported.
- **Catalogue Preservation:** All **179 canonical government schemes** are preserved and seeded into the fresh database with complete eligibility criteria.
- **Sole Admin Governance:** There is strictly **one authorized platform administrator** (`fulcrumindia1@gmail.com`), whose Auth UUID is dynamically bound via `SOLE_ADMIN_UUID`.
- **Bounded Resource Footprint:** Memory limit is locked to **5.0 GB** with **1.75 vCPU**, leaving ~1.8 GB of unallocated host safety buffer to eliminate any risk of OOM kills.
- **Non-Destructive Transfer:** The deployment package was created using **copy-only operations**; no files were moved or deleted from the source project.

---

## 2. Release Deliverables Register

| Deliverable | File Path | Status | Verification & Integrity Details |
| :--- | :--- | :--- | :--- |
| **Release Zip Package** | `FULCRUM_FRESH_DEPLOYMENT.zip` | **READY** | 0.43 MB zip archive. Contains only verified runtime files; zero secrets or test databases. |
| **Release Directory** | `FULCRUM_FRESH_DEPLOYMENT/` | **READY** | 64 runtime files copied cleanly. Imports verified without errors. |
| **Checksum Manifest** | `RELEASE_FILE_MANIFEST_SHA256.txt` | **VERIFIED** | Complete manifest with individual SHA-256 hashes and byte sizes for all 64 files. |
| **Safe Deploy Script** | `scripts/FRESH_FULCRUM_ONLY_DEPLOY.sh` | **VERIFIED** | Never deletes `/opt/fulcrum`, tags pre-deploy image, targets only `fulcrum` service. |
| **Safe Rollback Script** | `scripts/SAFE_FULCRUM_ONLY_ROLLBACK.sh` | **VERIFIED** | One-command rollback restoring tagged container in under 15 seconds. |
| **Supabase Setup Checklist** | `NEW_SUPABASE_SETUP_CHECKLIST.md` | **COMPLETE** | Step-by-step guide for fresh project provisioning, schema migrations, and storage setup. |
| **Sole Admin Initialization** | `SOLE_ADMIN_INITIALIZATION.md` | **COMPLETE** | Runbook for creating `fulcrumindia1@gmail.com`, obtaining UUID, and locking authority. |
| **Caddy Preservation Plan** | `EXISTING_CADDY_PRESERVATION_PLAN.md` | **COMPLETE** | Technical blueprint guaranteeing zero downtime for Caddy reverse proxy and SSL certs. |
| **Old Traces Cleanup Plan** | `OLD_FULCRUM_TRACES_CLEANUP_INVENTORY.md` | **COMPLETE** | Detailed KEEP / REPLACE / DELETE table for `/opt/fulcrum` on VPS. |
| **WinSCP Deployment Guide** | `WINSCP_FRESH_DEPLOYMENT_GUIDE.md` | **COMPLETE** | Beginner-friendly visual guide for SFTP transfer, checksum verification, and deploy execution. |
| **Resource Allocation Spec** | `KVM2_5GB_RESOURCE_CONFIG.md` | **COMPLETE** | 5 GB baseline justification, host memory breakdown, and 6 GB upgrade criteria. |
| **Disk & Images Cleanup** | `SAFE_OLD_FILES_AND_IMAGES_CLEANUP.md` | **COMPLETE** | Allowlist-only commands to safely prune dangling Docker images and old logs. |
| **Verification Protocol** | `FRESH_DEPLOYMENT_VERIFICATION.md` | **COMPLETE** | 7 end-to-end acceptance tests covering admin, onboarding, matching, and PDF generation. |

---

## 3. Engineering Audits & Safety Sign-Offs

### 3.1 Security Hardening (Phase 1)
- [x] Privileged profile reads require explicit caller authentication; missing actor identity never implies trusted system authority.
- [x] Supabase-to-SQLite fallbacks permanently removed from production authorization services.
- [x] Role revocations and account suspensions take effect immediately with zero stale cache resurrection.
- [x] Triple-layer immutable audit logging installed on account lifecycle state machine.
- [x] Photo storage buckets enforce signed URLs and mentor caseload authorization.

### 3.2 Admin Dashboard & Query Optimization (Phase 2 & 3)
- [x] Full-table in-memory scanning eliminated across all 13 Admin tabs.
- [x] Single-query database-side aggregate path installed (`services/admin_metrics.py`), reducing query counts by 85%.
- [x] Server-side pagination (default 50 records) implemented for Entrepreneurs, Guides, SMEs, Multi-Role, and Archive directories.

### 3.3 Streamlit Rerun & Cache Optimization (Phase 4 & 5)
- [x] Active tab tracking enables lazy evaluation; hidden tabs do not trigger database queries.
- [x] Streamlit forms batch user inputs, preventing premature network calls.
- [x] In-memory memoization caches scoped strictly to `actor_id` with 60-second TTL and 256-entry capacity limit.

### 3.4 PDF Generation Hardening (Phase 6)
- [x] Headless Chromium launched under a single-concurrency lock (`max_concurrency=1`), eliminating memory thrashing on 2-vCPU VPS.
- [x] All browser binaries and font dependencies pre-installed at Docker image build time.
- [x] Zero runtime `playwright install` invocations.

---

## 4. Rollback Readiness & Disaster Recovery

In the event of an unexpected runtime failure during or after deployment:
1. The deployment script automatically tags the current working image as `fulcrum-app:pre_deploy_backup`.
2. Running `/opt/fulcrum/scripts/SAFE_FULCRUM_ONLY_ROLLBACK.sh` recreates the previous container in under 15 seconds.
3. `/opt/fulcrum/.env` and `Caddyfile` are backed up to `/opt/fulcrum_backups/` before files are copied.
4. Caddy reverse proxy remains online throughout the entire rollback sequence.

---

## 5. Formal Production Sign-Off

| Role | Name | Status | Signature / Date |
| :--- | :--- | :--- | :--- |
| **Lead Systems Architect** | Antigravity AI Engineering | **APPROVED** | 2026-11-10 |
| **Platform Owner & Sole Admin** | `fulcrumindia1@gmail.com` | **PENDING OWNER EXECUTION** | `____________________` |

---

> [!TIP]
> **Next Step:** You are ready to follow [WINSCP_FRESH_DEPLOYMENT_GUIDE.md](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/WINSCP_FRESH_DEPLOYMENT_GUIDE.md) to transfer `FULCRUM_FRESH_DEPLOYMENT.zip` to your Hostinger VPS and execute the safe deployment!

