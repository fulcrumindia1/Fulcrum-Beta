# FULCRUM-INDIA: AGY ARGON — GATE 0 TEST EVIDENCE

**Test Environment**: Development / Staging Test Suite  
**Branch**: `security/phase0-containment`  
**Execution Timestamp**: 2026-11-08 23:38 UTC+5:30  
**Overall Result**: **94 PASSED, 0 FAILED, 0 SKIPPED (100% SUCCESS)**  
**Total Execution Time**: 116.54 seconds (0:01:56)

---

## 1. Test Suite Summary Table

| Test Suite File | Category | Tests Executed | Passed | Failed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `tests/test_argon_security_remediation.py` | Security Negative Tests (SEC-01 to SEC-16) | 15 | 15 | 0 | **PASS** |
| `tests/test_single_admin_master_e2e.py` | Master E2E Lifecycle & Admin Control | 10 | 10 | 0 | **PASS** |
| `tests/test_aspirant_photo_dashboard_visibility.py` | Aspirant Photo Access & Visibility | 12 | 12 | 0 | **PASS** |
| `tests/test_multi_role_e2e_workflows.py` | Multi-Role Grants & NDA Transitions | 11 | 11 | 0 | **PASS** |
| `tests/test_external_contact_and_sme_inactivity.py` | External Contact & SLA Governance | 12 | 12 | 0 | **PASS** |
| `tests/test_concurrency_load.py` | Concurrency & Data Isolation Under Load | 8 | 8 | 0 | **PASS** |
| `tests/test_cross_session_isolation.py` | Session Boundary Verification | 6 | 6 | 0 | **PASS** |
| `tests/test_failure_isolation.py` | Cloud Failure Resilience | 6 | 6 | 0 | **PASS** |
| `tests/test_scheme_matching_engine.py` | AI Scheme Eligibility Matching | 5 | 5 | 0 | **PASS** |
| `tests/test_scheme_relevance_synthetic.py` | Sector & Demographic Relevance | 4 | 4 | 0 | **PASS** |
| `tests/test_confidential_complaints.py` | Whistleblower & Complaint Isolation | 2 | 2 | 0 | **PASS** |
| `tests/test_inactivity_sla_contamination.py` | SLA Cross-Contamination Defense | 2 | 2 | 0 | **PASS** |
| `tests/test_scheme_card_crash.py` | UI Rendering Integrity | 1 | 1 | 0 | **PASS** |
| **TOTALS** | **Complete Suite** | **94** | **94** | **0** | **100% PASS** |

---

## 2. Security Test Matrix (SEC-01 through SEC-16)

| Test ID | Test Method | Target Security Requirement | Result |
| :--- | :--- | :--- | :---: |
| **SEC-01** | `test_sec_01_anonymous_reset_without_token_fails` | Rejects password reset attempt without cryptographic token | **PASS** |
| **SEC-02** | `test_sec_02_password_reset_mismatched_session_email_fails` | Rejects password reset with mismatched session email | **PASS** |
| **SEC-03** | `test_sec_03_admin_account_reset_is_strictly_rejected` | Prevents self-service reset targeting `fulcrumindia1@gmail.com` | **PASS** |
| **SEC-04** | `test_sec_04_password_length_under_8_fails` | Enforces minimum 8-character password constraint | **PASS** |
| **SEC-05** | `test_sec_05_photo_retrieval_without_viewer_fails_closed` | Fails closed (returns `None`) when photo queried with no viewer | **PASS** |
| **SEC-06** | `test_sec_06_unassigned_mentor_photo_view_denied` | Rejects unassigned mentor attempt to view aspirant photo | **PASS** |
| **SEC-07** | `test_sec_07_mentor_pending_nda_photo_view_denied` | Rejects photo access for mentor whose NDA is pending | **PASS** |
| **SEC-08** | `test_sec_08_aspirant_cannot_author_private_mentor_notes` | Rejects aspirant attempt to author private mentor notes | **PASS** |
| **SEC-09** | `test_sec_09_unassigned_mentor_cannot_author_private_notes` | Rejects unassigned mentor attempt to author private notes | **PASS** |
| **SEC-10** | `test_sec_10_aspirant_cannot_view_private_notes_via_role_tampering` | Prevents aspirant from seeing private notes via parameter tampering | **PASS** |
| **SEC-11** | `test_sec_11_unassigned_third_party_cannot_view_private_notes` | Blocks unassigned third party from reading private mentor notes | **PASS** |
| **SEC-12** | `test_sec_12_13_admin_role_cannot_be_granted` | Rejects any attempt to grant `admin` role via `grant_role` | **PASS** |
| **SEC-13** | `test_sec_12_13_admin_role_cannot_be_granted` | Enforces that only `aspirant`, `guide`, `sme` are grantable | **PASS** |
| **SEC-14** | `test_sec_14_platform_admin_excluded_from_role_candidate_lists` | Excludes Platform Admin from ordinary mentor dropdowns | **PASS** |
| **SEC-15** | `test_sec_15_cross_user_profile_update_rejected` | Blocks unauthorized cross-user profile modifications | **PASS** |
| **SEC-16** | `test_sec_16_fail_closed_photo_upload_reports_cloud_error` | Ensures Supabase storage upload failure reports error, not success | **PASS** |

---

## 3. Raw Execution Log Output Excerpt

```
============================= test session starts =============================
platform win32 -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0 -- C:\Python314\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\hp\Desktop\Fulcrum-Alpha\fulcrum-cluster-b
plugins: anyio-4.13.0, asyncio-1.3.0, base-url-2.1.0, mock-3.15.1, playwright-0.9.0
collected 94 items

tests/test_argon_security_remediation.py ...............                 [ 15%]
tests/test_aspirant_photo_dashboard_visibility.py ............           [ 28%]
tests/test_concurrency_load.py ........                                  [ 37%]
tests/test_confidential_complaints.py ..                                 [ 39%]
tests/test_cross_session_isolation.py ......                             [ 45%]
tests/test_external_contact_and_sme_inactivity.py ............           [ 58%]
tests/test_failure_isolation.py ......                                   [ 64%]
tests/test_inactivity_sla_contamination.py ..                            [ 67%]
tests/test_multi_role_e2e_workflows.py ...........                      [ 78%]
tests/test_scheme_card_crash.py .                                        [ 79%]
tests/test_scheme_matching_engine.py .....                               [ 85%]
tests/test_scheme_relevance_synthetic.py ....                            [ 89%]
tests/test_single_admin_master_e2e.py ..........                         [100%]

================== 94 passed, 6 warnings in 116.54s (0:01:56) ==================
```
