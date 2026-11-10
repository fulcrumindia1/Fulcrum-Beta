# FULCRUM-INDIA — MASTER DOCUMENTATION INDEX

Welcome to the **Fulcrum-India** engineering, architecture, operations, and governance documentation repository.

---

## 🚀 Quick Links for Operators (Start Here)

* **[WinSCP, Commands & .env Guide (ELI5)](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/DOCUMENTATION/OPERATIONAL_RUNBOOK_WINSCP_COMMANDS_AND_ENV_GUIDE.md)**  
  Step-by-step instructions on updating the VPS with WinSCP, running Docker commands, viewing logs, and editing `.env`.
* **[Password Recovery & Email Rate Limits Guide (ELI5)](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/DOCUMENTATION/PASSWORD_RECOVERY_AND_EMAIL_RATE_LIMITS_ELI5.md)**  
  Explains Supabase free email rate limits, why they occur, how to bypass during testing, and how to connect custom SMTP.

---

## 📁 Categorized Documentation Structure

### [01. Production Release Audits](./01_PRODUCTION_RELEASE_AUDITS/)
Contains official independent forensic audits, release gates, attestations, and manifests:
* **`FULCRUM_BETA_2_1_PRODUCTION_CRASH_FORENSIC_AUDIT.md`** — Independent audit of the 4 production crashes (SyntaxError, UnboundLocalError, NameError, TypeError).
* **`PASSWORD_RECOVERY_FORENSIC_REMEDIATION_REPORT.md`** — End-to-end audit and fix for the password recovery flow.
* **`RELEASE_READINESS_REPORT.md`** — Gate-by-gate release criteria and compliance matrix.
* **`FINAL_RELEASE_ATTESTATION.md`** — Official engineering release sign-off.
* **`PACKAGE_INTEGRITY_MANIFEST.md`** — SHA-256 release checksum register.
* **`STATIC_ANALYSIS_EVIDENCE.md`** — Python 3.11 AST and pyflakes compilation results.
* **`PRODUCTION_DEPLOYMENT_APPROVAL.md`** — Formal owner deployment approval register.
* **`DATA_PRESERVATION_CERTIFICATE.md`** — Attestation of 179 canonical schemes and data safety.

---

### [02. Deployment & Operations](./02_DEPLOYMENT_AND_OPERATIONS/)
Operational runbooks, resource allocation, and VPS guides:
* **`OPERATIONAL_RUNBOOK_WINSCP_COMMANDS_AND_ENV_GUIDE.md`** — Core deployment cheat sheet.
* **`PASSWORD_RECOVERY_AND_EMAIL_RATE_LIMITS_ELI5.md`** — Email and password reset operations.
* **`DEPLOYMENT_RUNBOOK_KVM2.md`** — Hostinger KVM 2 Ubuntu 24.04 server configuration.
* **`WINSCP_FRESH_DEPLOYMENT_GUIDE.md`** — Detailed visual WinSCP deployment walkthrough.
* **`ROLLBACK_CONTINGENCY_PLAN.md`** — 45-second zero-downtime rollback runbook.
* **`KVM2_5GB_RESOURCE_CONFIG.md`** — 5 GB container memory guard and swap tuning.
* **`EXISTING_CADDY_PRESERVATION_PLAN.md`** — Zero-touch Caddy reverse proxy preservation.

---

### [03. Security & Governance](./03_SECURITY_AND_GOVERNANCE/)
Authorization models, RLS policies, and administrator controls:
* **`SINGLE_ADMIN_AUTHORIZATION_MATRIX.md`** — Dynamic UUID discovery for `fulcrumindia1@gmail.com`.
* **`SOLE_ADMIN_INITIALIZATION.md`** — Bootstrap and immutable privilege model.
* **`SECURITY_AND_RLS_TEST_RESULTS.md`** — Supabase Row Level Security policy validation.
* **`FULCRUM_ARCHITECTURE_AND_GOVERNANCE_ELI5.md`** — Multi-stakeholder institutional governance architecture.
* **`SAFE_MENTOR_HANDOVER_FIXES.md`** — Mentor reassignments with audit logs.

---

### [04. Schemes & Account Lifecycle](./04_SCHEMES_AND_LIFECYCLE/)
Scheme matching engines, lifecycle state machines, and schemas:
* **`SCHEMA_CONTRACT_AUDIT_REPORT.md`** — Reconciliation of Migration 009 vs application code.
* **`ACCOUNT_LIFECYCLE_STATE_MACHINE.md`** — Active, Inactive, Suspended, Archived transitions.
* **`SCHEME_ELIGIBILITY_RULE_SCHEMA.md`** — Mathematical evaluation rules for schemes.
* **`SCHEME_FOUNDER_ELI5_REPORT.md`** — Founder-facing eligibility matching rules.
* **`SCHEME_MATCHING_CURRENT_CODE_AUDIT.md`** — Audit of the 179 canonical scheme engine.
* **`SCHEME_X_Y_Z_MODEL.md`** — Multi-dimensional matching formula.

---

### [05. Testing & Verification](./05_TESTING_AND_VERIFICATION/)
Automated integration test suites, browser simulations, and chaos engineering:
* **`INTEGRATION_TEST_RESULTS.md`** — Automated execution logs (148 tests passed).
* **`BROWSER_VERIFICATION_REPORT.md`** — 25-tab user interface verification.
* **`FULL_REGRESSION_AND_E2E_RESULTS.md`** — Circular multi-role end-to-end suite.
* **`UI_UX_FUNCTIONAL_AUDIT.md`** — Comprehensive visual and usability audit.
* **`CLUSTER_A_TEST_MATRIX.md`** — Test coverage mapping.

---

### [06. Historical Audits & Archives](./06_HISTORICAL_ARGON_AND_SYSTEM_AUDITS/)
Archived records from previous development phases (Argon checkpoints, load tests, and preliminary audits).

