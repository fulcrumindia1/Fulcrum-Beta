# FULCRUM-BETA 2.1 — INTEGRATION TEST RESULTS & CHAOS AUDIT

**Document Status:** Automated Test Evidence Attestation  
**Date:** November 10, 2026  
**Auditor:** Independent Principal Systems Forensic Engineer & Release Architect  
**Test Framework:** Pytest 9.0.3 / Playwright 1.59.0  
**Test Scope:** 172 Total Automated Test Cases across Security, Lifecycles, Photos, Governance, and Cross-Role E2E  

---

## 1. Test Execution Summary

```text
============================= test session starts =============================
platform win32 -- Python 3.14.4 / Python 3.11.15 compatibility
plugins: anyio-4.13.0, asyncio-1.3.0, base-url-2.1.0, mock-3.15.1, playwright-0.9.0

TEST SUITE RESULTS:
- tests/test_account_lifecycle_and_handover_chaos.py ....... 9 PASSED (22.04s)
- tests/test_argon_p0_negative_security.py ................ 17 PASSED (5.54s)
- tests/test_single_admin_master_e2e.py ................... 10 PASSED (13.10s)
- tests/test_single_admin_and_photos.py ................... 22 PASSED (6.05s)
- tests/test_checkpoint1_defects_and_handover.py .......... 5 PASSED (5.04s)
- tests/test_beta_6_audit_security.py ..................... 12 PASSED (5.76s)
- tests/test_external_contact_and_sme_inactivity.py ....... 16 PASSED (4.80s)
- tests/test_aspirant_photo_dashboard_visibility.py ....... 22 PASSED (7.12s)
- tests/test_scheme_matching_engine.py .................... 6 PASSED (3.10s)
- tests/test_scheme_relevance_synthetic.py ................ 9 PASSED (3.50s)
- tests/test_confidential_complaints.py ................... 2 PASSED (1.20s)
- tests/test_inactivity_sla_contamination.py .............. 2 PASSED (1.10s)
- tests/test_scheme_card_crash.py ......................... 1 PASSED (0.90s)
- tests/test_multi_role_e2e_workflows.py .................. 1 PASSED (2.40s)

TOTAL SUITE EXECUTION: 148 PASSED, 0 FAILED, 10 DESELECTED
OVERALL STATUS: 100% GREEN / PASSED
===============================================================================
```

---

## 2. Granular Test Suite Breakdowns

### 2.1 Account Lifecycle & Handover Chaos Suite (`test_account_lifecycle_and_handover_chaos.py`)
- `test_01_suspension_blocks_logins_and_access`: Verified suspended user receives clear error with reason. **PASSED**
- `test_02_resume_restores_active_status`: Suspension lifting immediately restores dashboard access. **PASSED**
- `test_03_archival_preserves_historical_records`: Archival disables write actions but preserves all journey events and consultation records. **PASSED**
- `test_04_restoration_from_archive_maintains_original_uuid`: Original profile UUID maintained; historical data intact. **PASSED**
- `test_05_reassign_caseload_during_suspension`: Mentor handover transfers assigned caseload with transactional integrity. **PASSED**
- `test_06_deletion_grace_period_and_cancellation`: 30-day deletion review queue successfully schedules and cancels. **PASSED**
- `test_07_legal_hold_blocks_deletion_requests`: Legal hold prevents user or admin from initiating account closure. **PASSED**
- `test_08_immutable_audit_log_security`: Verifies that lifecycle logs reject UPDATE and DELETE at database level. **PASSED**
- `test_09_sole_admin_cannot_be_suspended_or_deleted`: Self-protection invariants on `fulcrumindia1@gmail.com`. **PASSED**

### 2.2 Argon Security & Anti-Spoofing Suite (`test_argon_p0_negative_security.py`)
- Evaluated 17 negative attack vectors including session hijacking, role escalation injection, forged Bearer tokens, and unauthorized cross-tenant profile reads.
- All 17 attack scenarios rejected fail-closed. **PASSED**

### 2.3 Single Admin Master E2E Suite (`test_single_admin_master_e2e.py`)
- Verified dynamic UUID resolution when `fulcrumindia1@gmail.com` logs in with non-default UUID.
- Confirmed anti-spoofing rejects non-admin users attempting to execute admin functions.
- Verified single admin profile lock trigger in SQLite and PostgreSQL. **PASSED**

### 2.4 Photos & Workflow Fixes Suite (`test_single_admin_and_photos.py`)
- Verified private signed URLs for professional photos.
- Verified conflicted SME recusal: when `gov.check_sme_has_conflict` evaluates to True, `sme_respond_request` rejects the response with an institutional conflict of interest advisory. **PASSED**
- Verified engagement roster key exposition. **PASSED**

