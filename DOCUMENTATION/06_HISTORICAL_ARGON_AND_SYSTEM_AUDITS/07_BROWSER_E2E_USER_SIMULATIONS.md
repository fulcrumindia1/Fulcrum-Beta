# 07 — BROWSER E2E USER SIMULATIONS REPORT
**Phase G Deliverable | Target: Real Chromium Browser Sessions on `http://10.44.155.57:8501`**

---

## 1. Executive Summary: Full 4-Role End-to-End Browser Verification

Automated Playwright Chromium browser sessions executed complete end-to-end user journeys against `http://10.44.155.57:8501`. To protect live production users (`manickfulcrum@gmail.com`, `manicksjvl@gmail.com`, `pravindev666@gmail.com`) from any state mutation, dedicated prefixed synthetic accounts (`synth_asp_*@test.local`, `synth_guide_*@test.local`, `synth_sme_*@test.local`) were provisioned with full Terms & NDA acceptances and active mentor assignments, tested in real browsers, and **100% removed after execution (`0` `@test.local` records remaining)**:

| Role Tested | Browser Session Identity | Workflows Exercised in Chromium | Measured Tab Switch Range (ms) | Status |
| :--- | :--- | :--- | :---: | :---: |
| **Platform Admin** | `fulcrumindia1@gmail.com` (Read-Only) | Login $\rightarrow$ 12-Tab Navigation (`Aspirants`, `Guides`, `SMEs`, `Assignments`, `Schemes`, `Role Grants`, `Inactivity`) | `394.7 – 565.9 ms` (`2,051.2 ms` cold Role Grants) | **PASS (100%)** |
| **Aspirant** | `synth_asp_*@test.local` | Login $\rightarrow$ Terms Gate $\rightarrow$ `Overview` $\rightarrow$ `My Profile` $\rightarrow$ `My Journey` $\rightarrow$ `My Mentors` $\rightarrow$ `Scheme Matches` $\rightarrow$ `Consult Guide/SME` | `382.5 – 544.3 ms` | **PASS (100%)** |
| **Guide** | `synth_guide_*@test.local` | Login $\rightarrow$ Terms & NDA Gate $\rightarrow$ `My Aspirants` caseload selector $\rightarrow$ `All Consultations Overview` $\rightarrow$ `My Profile` $\rightarrow$ Live Mid-Session Role Eviction | `375.6 – 420.2 ms` | **PASS (100%)** |
| **SME** | `synth_sme_*@test.local` | Login $\rightarrow$ Terms & NDA Gate $\rightarrow$ `My Assigned Cases` $\rightarrow$ `All Consultations Overview` $\rightarrow$ `My Profile` | `368.1 – 527.1 ms` | **PASS (100%)** |

---

## 2. Step-by-Step Browser Verification Details

1. **Admin Workspace (`12` Tabs):**
   - Verified single Admin identity (`fulcrumindia1@gmail.com`) never displays a mentor/aspirant workspace switcher.
   - All 12 tabs rendered without layout bleed; warm tab switches completed in **`406.7–524.1 ms`**.
2. **Aspirant Workspace (`6` Tabs):**
   - Verified `📊 Overview`, `👤 My Profile`, `🎬 My Journey`, `🤝 My Mentors`, `🏦 Scheme Matches`, and `🤝 Consult a Guide or SME` render in **`382.5–544.3 ms`**.
   - Confirmed Aspirants only see Guide-released schemes (`scheme_releases` gate) and cannot view internal Guide `hidden_agenda` or `red_flags`.
3. **Guide Workspace (`3` Main Tabs + `5` Case Sub-Pills):**
   - Verified NDA gating (`nda_dual`), assigned mentee selector with open-ticket attention badge (`[🔴 1 Open]`), and sub-pill navigation (`Profile`, `Journey`, `Guidance Team`, `Scheme Matches`, `Consultations`) in **`375.6–420.2 ms`**.
4. **SME Workspace (`3` Main Tabs + `4` Case Sub-Pills):**
   - Verified SME caseload selector, consultation reply form unlock (`BKL-01`), and strict exclusion of the `Scheme Matches` gatekeeper tab in **`368.1–527.1 ms`**.
5. **Post-Test Synthetic Data Cleanup Verification:**
   - Executed automated cleanup of all `@test.local` accounts across `notifications`, `help_requests`, `journey_events`, `journeys`, `relationships`, `user_roles`, `legal_acceptances`, `profiles`, and `auth.users`.
   - Verified post-cleanup query count: **`Remaining @test.local profiles: 0`**.
