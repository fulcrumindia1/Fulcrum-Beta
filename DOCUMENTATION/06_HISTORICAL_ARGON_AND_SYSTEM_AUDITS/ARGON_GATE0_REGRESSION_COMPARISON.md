# FULCRUM-INDIA: AGY ARGON — GATE 0 REGRESSION COMPARISON

## 1. Scope & Preservation Invariant Verification

In accordance with **Invariant 3 (Data Preservation)** and **Invariant 4 (UI Layout & Navigation Preservation)**, static code inspections and regression tests confirm that:
- Zero existing pages were deleted or restructured.
- Zero microservice rewrites were introduced.
- All Streamlit entry points, tab layouts, CSS styles, and badges remain identical.
- All existing users, profiles, journeys, schemes, consultations, and legal logs are preserved.

---

## 2. Before vs. After Feature & Security Comparison

| Workflow / Component | Prior State (Fulcrum-Beta Baseline) | Remediated State (AGY Argon Gate 0) | Regression Impact |
| :--- | :--- | :--- | :---: |
| **Password Reset** | Anyone with an email address could override any password via unauthenticated Admin API bypass. | Strictly requires verified Supabase Auth recovery token session. Admin account cannot be reset via self-service. | **ZERO REGRESSION** (Exploit closed) |
| **Login Surface** | "Set New Password Here →" button rendered reset form without email link. | Recovery form renders only when an authentic recovery link with token is clicked. | **ZERO REGRESSION** (Flow secured) |
| **Aspirant Photo Upload** | Upload failures to Supabase were swallowed; photos saved to ephemeral local SQLite, disappearing on reboot. | Fail-closed cloud upload. Supabase errors reported clearly; local SQLite used strictly in `DATA_BACKEND=sqlite`. | **ZERO REGRESSION** (Data loss prevented) |
| **Aspirant Photo Access** | `get_aspirant_photo` returned photos even when `viewer_id` was `None`. | Fails closed immediately if `viewer_id` is missing in Supabase mode. Verifies assignment & NDA for mentors. | **ZERO REGRESSION** (Privacy guaranteed) |
| **Private Case Notes** | Any caller passing `requesting_role="guide"` could view confidential mentor notes. | Derives identity from session; validates assignment and NDA status. Parameter tampering strictly eliminated. | **ZERO REGRESSION** (Confidentiality enforced) |
| **Admin Role Promotion** | Potential to grant `admin` or legacy roles (`district_admin`). | `grant_role` strictly rejects `admin`. Only `aspirant`, `guide`, and `sme` are grantable. Single Admin isolated. | **ZERO REGRESSION** (Invariant 1 preserved) |
| **Mentor Provisioning** | Created with static predictable passwords (`Guide@123`, `Sme@123`); plaintext passwords toasted. | Cryptographically strong temporary passwords generated with `secrets.token_urlsafe(12)`. No credential toasts. | **ZERO REGRESSION** (Security hardened) |
| **Aspirant Scheme Matching** | Deterministic rule matching evaluated across 179 government schemes. | Completely untouched; all 179 schemes and evaluation rules remain 100% identical. | **ZERO REGRESSION** |
| **Mentor Assignments** | Multi-mentor assignments (Co-Guides & Concurrent Multi-SMEs) managed by Admin. | Fully functional; queries now guarantee the Platform Admin is excluded from mentor candidate lists. | **ZERO REGRESSION** |
| **Legal & NDA Records** | Cryptographic SHA-256 audit trail for Terms & Conditions and Mentor NDAs. | Fully functional; Supabase mode writes fail-closed with zero silent SQLite fallbacks. | **ZERO REGRESSION** |
| **Inactivity Monitoring** | 14-day SLA escalation and WhatsApp/Gmail compose links. | Fully functional; templates and compose links completely preserved. | **ZERO REGRESSION** |
