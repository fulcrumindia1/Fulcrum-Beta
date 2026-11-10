# Fulcrum-India — Deterministic Schemes & Journey Preservation Report
**Project:** Fulcrum-India (Cluster B)  
**Date:** November 5, 2026  
**Auditor:** Antigravity Engineering  
**Scope:** Scheme Matching Determinism, Gatekeeper Governance, Living Journey Spine, Dossier PDF Verification

---

## 1. Directive & Invariant Compliance

Section 0 and Part D of the Master Prompt enforce an absolute directive:
> **"Preserve Fulcrum's entrepreneurship guidance, mentorship, Journey and government-scheme support platform... THIS IS A NON-DESTRUCTIVE ENHANCEMENT. IT IS NOT A REBUILD."**

Under no circumstances may matching weights be altered, scheme criteria relaxed, or the chronological Journey spine ("Movie & Post-Credits") modified.

This report establishes empirical proof that all core algorithms and journey data structures remain 100% preserved.

---

## 2. Scheme Catalogue & Matching Determinism

### 2.1 Master Catalogue Preservation
- All 170+ master schemes in [`seed/schemes.json`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/seed/schemes.json) remain identical.
- Categories preserved: Central Government, Tamil Nadu State, Departmental Grants, Venture Capital, and Subsidized Credit.
- Hidden intelligence preserved: Secret evaluation agendas (`hidden_agenda`), warning flags (`red_flags`), and application prompts.

### 2.2 Matching Score Determinism
- Algorithm: [`services/schemes.py:match_schemes_for_aspirant()`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/schemes.py#L225-L360).
- Evaluates: Stage compatibility, sector alignment, investment bracket, social category, women-led status, and district eligibility.
- Verified in Scenario 14:
  - Exact match scores generated before optimization were compared against scores generated post-optimization for test venture `Kavitha CleanTech`.
  - **Result:** Exact identical score array and ordering produced **[PASS]**.

---

## 3. The Gatekeeper Workflow Preserved

The core governance gatekeeper pattern remains untouched:
1. **Unreleased State:** Public aspirants cannot see raw matched schemes directly.
2. **Guide Curation:** Certified Guides inspect the matches, review hidden agendas and red flags, and click **"🚀 Release to Aspirant"** with custom advisory notes.
3. **Released State:** Schemes only appear on the founder's portal once an active record exists in `scheme_releases` with status `RELEASED`.
4. **Withdrawal:** Guides retain the ability to withdraw releases with an audit trail.

---

## 4. The Entrepreneur's Journey ("The Movie & Post-Credits")

The chronological living timeline in [`services/journey.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/journey.py) remains completely preserved:
- **Milestone Events:** Inception, Mentor Sessions, DPR Filings, Sanctions, Capital Disbursements.
- **Actor Attribution:** Every event attributes the actor (`aspirant`, `guide`, `sme`, or masked `admin`).
- **Soft Deletion & Audit:** Events are never hard-deleted; soft deletion preserves audit history with `deleted_at` and `deleted_by`.
- **Roadmap Toggle:** Founders and mentors can toggle event inclusion in the exportable roadmap.
- **Dossier PDF Generator:** [`services/pdf_generator.py:generate_aspirant_dossier_pdf()`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/pdf_generator.py) continues to compile full entrepreneur dossiers, venture profiles, mentor notes, and released funding intelligence seamlessly.
