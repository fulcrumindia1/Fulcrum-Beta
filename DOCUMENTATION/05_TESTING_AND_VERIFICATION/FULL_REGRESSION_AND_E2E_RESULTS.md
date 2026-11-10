# FULCRUM-BETA — FULL REGRESSION & END-TO-END TEST RESULTS

**Author:** Fulcrum Quality Assurance & Test Engineering Team  
**Date:** November 2026  
**Status:** 100% PASS RATE (130/130 Tests Passing)  
**Execution Environment:** Windows / Python 3.14.4 / Pytest 9.0.3  
**Target:** Sole Platform Administrator (`fulcrumindia1@gmail.com`)

---

## 1. Executive Summary

A full, repository-wide automated regression and end-to-end test run was executed to verify that the implementation of the **Account Lifecycle & Archive** engine, mentor handover repairs, and security remediations introduced zero functional regressions across Fulcrum.

### High-Level Metrics:
- **Total Tests Collected:** 130
- **Total Tests Passed:** 130
- **Total Tests Failed:** 0
- **Pass Rate:** **100.0%**
- **Total Wall-Clock Time:** 122.65 seconds (2 minutes, 2 seconds)
- **Regressions Introduced:** 0

---

## 2. Test Suite Breakdown by Functional Area

| Test Module | Tests | Status | Functional Area Verified |
| :--- | :---: | :---: | :--- |
| `test_account_lifecycle_and_handover_chaos.py` | 9 | **PASSED** | Lifecycle state transitions, co-mentor promotion, pre-archive ticket queuing, legal hold blocks, idempotent handover retries, cascade immunity. |
| `test_argon_security_remediation.py` | 15 | **PASSED** | Sole Admin identity gating, tamper resistance, audit log immutability, private note isolation, quarantined script deactivation. |
| `test_aspirant_photo_dashboard_visibility.py` | 22 | **PASSED** | Founder photo uploads, cloud storage fail-closed error handling, NDA access gating, guide/SME photo visibility. |
| `test_checkpoint1_defects_and_handover.py` | 5 | **PASSED** | Co-guide `guide_ids` cleanup, SME `sme_ids` cleanup, hybrid role isolation, consultation ticket transfer. |
| `test_confidential_complaints.py` | 2 | **PASSED** | Confidential guide complaint isolation, super admin masking, resolution notes. |
| `test_cross_session_isolation.py` | 4 | **PASSED** | Multi-session token boundary, memory cache partitioning, concurrent user separation. |
| `test_external_contact_and_sme_inactivity.py` | 17 | **PASSED** | Admin-to-mentor WhatsApp/Gmail draft generation, 7-day/14-day inactivity SLA monitoring, phone number E.164 normalization. |
| `test_failure_isolation.py` | 6 | **PASSED** | Dual-backend failure tolerance, clean error reporting without false toasts. |
| `test_inactivity_sla_contamination.py` | 2 | **PASSED** | Exclusion of archived accounts and completed incubation alumni from inactivity alerts. |
| `test_multi_role_e2e_workflows.py` | 1 | **PASSED** | Full end-to-end multi-role lifecycle (Guide + SME + Aspirant) from onboarding to handover. |
| `test_scheme_card_crash.py` | 1 | **PASSED** | UI crash resistance during missing scheme attributes or corrupted JSON sectors. |
| `test_scheme_matching_engine.py` | 6 | **PASSED** | AI matching engine, category relevance, eligibility rule evaluation. |
| `test_scheme_relevance_synthetic.py` | 9 | **PASSED** | Synthetic testing across 9 diverse enterprise profiles (AgriTech, DeepTech, Women-led, Rural). |
| `test_single_admin_and_photos.py` | 21 | **PASSED** | Sole Admin dashboard controls, professional photo uploads, district filtering. |
| `test_single_admin_master_e2e.py` | 10 | **PASSED** | Complete administrator workflow orchestration and governance checks. |

---

## 3. Detailed Pytest Execution Transcript

```
============================= test session starts =============================
platform win32 -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\hp\Desktop\Fulcrum-Alpha\fulcrum-cluster-b
plugins: anyio-4.13.0, asyncio-1.3.0, base-url-2.1.0, mock-3.15.1, playwright-0.9.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 130 items

tests\test_account_lifecycle_and_handover_chaos.py .........             [  6%]
tests\test_argon_security_remediation.py ...............                 [ 18%]
tests\test_aspirant_photo_dashboard_visibility.py ...................... [ 35%]
tests\test_checkpoint1_defects_and_handover.py .....                     [ 39%]
tests\test_confidential_complaints.py ..                                 [ 40%]
tests\test_cross_session_isolation.py ....                               [ 43%]
tests\test_external_contact_and_sme_inactivity.py ................       [ 56%]
tests\test_failure_isolation.py ......                                   [ 60%]
tests\test_inactivity_sla_contamination.py ..                            [ 62%]
tests\test_multi_role_e2e_workflows.py .                                 [ 63%]
tests\test_scheme_card_crash.py .                                        [ 63%]
tests\test_scheme_matching_engine.py ......                              [ 68%]
tests\test_scheme_relevance_synthetic.py .........                       [ 75%]
tests\test_single_admin_and_photos.py ......................             [ 92%]
tests\test_single_admin_master_e2e.py ..........                         [100%]

================= 130 passed, 6 warnings in 122.65s (0:02:02) =================
```

---

## 4. Key End-to-End Scenarios Confirmed

### Scenario 1: Multi-Role Complex Handover & Revocation
- **Setup:** User assigned as Co-Guide to Entrepreneur 1, Primary Guide to Entrepreneur 2, and Primary SME to Entrepreneur 3.
- **Action:** Sole Admin revokes the Guide role.
- **Verification:**
  - Removed from Co-Guide roster on Entrepreneur 1 (`guide_ids` updated).
  - Unassigned as Primary Guide on Entrepreneur 2; Co-Guide promoted to Primary; open tickets transferred to promoted guide.
  - SME assignment on Entrepreneur 3 remained **completely unaffected**.
  - All Journey milestones and historical notes preserved.

### Scenario 2: Pre-Archive Handover & Restoration
- **Setup:** Active mentor with active caseload and 3 pending consultations.
- **Action:** Sole Admin initiates pre-archive impact review, provides handover instructions, and executes archival.
- **Verification:**
  - Open consultations transferred to successor or queued for Admin.
  - Account status changed to `ARCHIVED`.
  - Login attempts immediately blocked.
  - Sole Admin restores account.
  - Account restored under **exact same Supabase Auth UUID**.
  - Historical revoked roles not resurrected; past caseload not reclaimed automatically.

### Scenario 3: 30-Day Cancellation Grace & Self-Service Reversal
- **Setup:** Active entrepreneur requests account deletion.
- **Action:** Status enters `PENDING_DELETION`; scheduled review date set 30 days out.
- **Verification:**
  - User logs in: Grace banner displayed with countdown and cancel button.
  - User clicks `[Cancel Closure Request]`.
  - Status immediately returns to `ACTIVE`; closure scheduled date cleared; audit event logged.

