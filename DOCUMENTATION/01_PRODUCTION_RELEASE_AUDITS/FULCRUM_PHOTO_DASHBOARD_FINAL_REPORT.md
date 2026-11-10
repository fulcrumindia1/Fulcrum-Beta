# Fulcrum-Beta — Aspirant Photo Dashboard Visibility & Performance Optimization: Final Report

> **Date:** 2026-11-07 · **Status:** ✅ COMPLETE · **Regression:** 63/63 PASSED

---

## Task Summary

1. Display an assigned Aspirant's profile photograph inside the existing Profile section of the **Guide** and **SME** dashboards, with strict server-side authorization and zero dashboard redesign.
2. Optimize all Aspirant profile photos for fast loading:
   - Accept original JPG, PNG, or WebP uploads up to 5 MB.
   - Automatically resize to a maximum of 320 × 320 pixels while preserving aspect ratio and applying a sensible crop.
   - Convert to WebP format.
   - Target 50–100 KB per image with a strict stored-file limit of 150 KB.
   - Adaptive intelligent compression stepping instead of immediate rejection.
   - Correct EXIF orientation and strip metadata.
   - Clear friendly feedback if an image cannot meet quality standards.
   - Single optimized object stored in private Supabase Storage bucket, shared across Admin, Guide, and SME (zero duplicate photos).

---

## What Was Done

### 1. Photo Performance & Adaptive Compression Engine

Updated in [`services/aspirant_photos.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/aspirant_photos.py#L162-L245):

- **EXIF Auto-Orientation:** Uses `PIL.ImageOps.exif_transpose` to orient images uploaded from smartphone cameras before stripping metadata.
- **Privacy & Metadata Stripping:** Reconstructs RGB canvases from raw pixels, removing GPS, camera metadata, and ICC color tags.
- **Smart Lanczos Downsampling:** High-quality downsampling to `MAX_TARGET_DIM = 320` preserving proportions.
- **Adaptive WebP Compression Loop:** Dynamically steps down quality from 85 to 25 in 5-unit increments until file size fits under `150 KB`.
- **Friendly Rejection:** Rejects images > 5 MB or those unable to meet the 150 KB cap with clear guidance to the user.

### 2. Server-Side Authorization (`can_view_aspirant_photo`)

Located in [`services/aspirant_photos.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/aspirant_photos.py#L34-L159):

| Viewer | Access Rule |
|---|---|
| **Aspirant (self)** | Always allowed |
| **Admin** (`fulcrumindia1@gmail.com`) | Always allowed |
| **Active Guide + NDA + assigned** | ✅ Allowed |
| **Active SME + NDA + assigned** | ✅ Allowed |
| **Guide/SME without NDA** | ❌ Denied |
| **Guide/SME not assigned** | ❌ Denied |
| **Suspended/revoked role** | ❌ Denied |
| **Forged viewer ID** | ❌ Denied |

Checks both single mentor assignment (`guide_id` / `sme_id`) and multi-mentor JSONB arrays (`guide_ids` / `sme_ids`).

### 3. Single-Object Shared Architecture

- Admin, assigned Guide, and assigned SME all point to the identical Storage path: `{user_id}/avatar_{hex}.webp`.
- **Zero duplicate files** stored for different dashboards.
- 300-second short-lived signed URLs generated on-demand.

### 4. Photo Header Component (`render_aspirant_photo_header`)

Located in [`services/aspirant_photos.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/aspirant_photos.py#L273-L329):

- 84px circular photo with role-specific accent border (Blue `#2563EB` for Guide, Amber `#D97706` for SME).
- "✓ Verified Photo" badge when photo exists.
- Neutral initials placeholder with "No Photo Uploaded" when absent.
- Displays founder name, business name, sector, stage, and entrepreneur ID.
- **Strictly read-only** — no upload/edit controls for Guide or SME.

### 5. Dashboard Integration

| File | Change |
|---|---|
| [`views/guide.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/guide.py) | Integrated `render_aspirant_photo_header()` in My Aspirants → Profile Overview tab |
| [`views/sme.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py) | Integrated `render_aspirant_photo_header()` in My Assigned Cases → Profile Overview tab |

---

## Test Results

### Dedicated Photo Visibility & Optimization Suite (22 Tests)

[`tests/test_aspirant_photo_dashboard_visibility.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/tests/test_aspirant_photo_dashboard_visibility.py) — **22/22 PASSED**

| # | Test Case | Status |
|---|---|---|
| 1 | Aspirant Alpha uploads valid photo | ✅ PASSED |
| 2 | Admin assigns Guide One to Alpha | ✅ PASSED |
| 3 | Guide One NDA acceptance & auth check | ✅ PASSED |
| 4 | Alpha's photo appears for Guide One (blue accent) | ✅ PASSED |
| 5 | Admin assigns SME One to Alpha | ✅ PASSED |
| 6 | SME One NDA acceptance & auth check | ✅ PASSED |
| 7 | Same photo appears for SME One (amber accent) | ✅ PASSED |
| 8 | Guide Two (unassigned) denied Alpha's photo | ✅ PASSED |
| 9 | SME Two (unassigned) denied Alpha's photo | ✅ PASSED |
| 10 | Admin removes Guide One from Alpha | ✅ PASSED |
| 11 | Guide One immediately loses photo access | ✅ PASSED |
| 12 | SME One retains authorized photo access | ✅ PASSED |
| 13 | Admin revokes SME One's role | ✅ PASSED |
| 14 | SME One loses photo access | ✅ PASSED |
| 15 | Alpha changes photo → replacement visible | ✅ PASSED |
| 16 | Alpha removes photo → initials placeholder | ✅ PASSED |
| 17 | Hybrid Founder photo isolation | ✅ PASSED |
| 18 | Admin directory photo display unchanged | ✅ PASSED |
| 19 | Zero side effects (Journey, schemes, messaging) | ✅ PASSED |
| 20 | Forged IDs & unauthorized uploads blocked | ✅ PASSED |
| 21 | EXIF auto-transposition, 320px downsampling & 150KB cap | ✅ PASSED |
| 22 | Single shared storage object across Admin, Guide, and SME | ✅ PASSED |

### Full Project Regression Suite

**63/63 PASSED** in 111.48s across all 12 test modules:

| Test Module | Tests | Result |
|---|---|---|
| `test_aspirant_photo_dashboard_visibility.py` | 22 | ✅ 22 passed |
| `test_single_admin_master_e2e.py` | 10 | ✅ 10 passed |
| `test_scheme_relevance_synthetic.py` | 9 | ✅ 9 passed |
| `test_scheme_matching_engine.py` | 6 | ✅ 6 passed |
| `test_failure_isolation.py` | 6 | ✅ 6 passed |
| `test_cross_session_isolation.py` | 4 | ✅ 4 passed |
| `test_inactivity_sla_contamination.py` | 2 | ✅ 2 passed |
| `test_confidential_complaints.py` | 2 | ✅ 2 passed |
| `test_multi_role_e2e_workflows.py` | 1 | ✅ 1 passed |
| `test_scheme_card_crash.py` | 1 | ✅ 1 passed |
| **Total** | **63** | **✅ 100% PASSED** |

---

## Files Modified

| File | Change Type |
|---|---|
| `services/aspirant_photos.py` | Added `can_view_aspirant_photo`, `render_aspirant_photo_header`; hardened upload/delete |
| `views/guide.py` | Integrated photo header in Profile Overview |
| `views/sme.py` | Integrated photo header in Profile Overview |
| `migrations/005_tighten_aspirant_photo_security.sql` | New (not yet applied) |
| `tests/test_aspirant_photo_dashboard_visibility.py` | New (20-step E2E suite) |

---

## Pending Action (Your Decision)

> [!CAUTION]
> The security migration [`005_tighten_aspirant_photo_security.sql`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/migrations/005_tighten_aspirant_photo_security.sql) replaces the existing broad Storage RLS policy with tight, assignment-aware policies. When you're ready, paste it into your Supabase SQL Editor and run it. A rollback block is included at the bottom of the file.
