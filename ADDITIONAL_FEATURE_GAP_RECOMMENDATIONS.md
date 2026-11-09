# FULCRUM-BETA — ADDITIONAL FEATURE GAP RECOMMENDATIONS

**Author:** Fulcrum Systems Architecture & Product Strategy Team  
**Date:** November 2026  
**Status:** PROPOSED & PRIORITIZED (For Future Implementation Sprints)  
**Target:** Sole Platform Administrator (`fulcrumindia1@gmail.com`)

---

## 1. Executive Summary

During the development, audit, and testing of the Account Lifecycle & Archive system, several strategic feature gaps and operational enhancements were identified. While the core lifecycle engine and mentor handover repairs are complete, implementing the following 6 recommendations will further enhance governance, compliance, scalability, and user experience.

---

## 2. Recommended Enhancements

### Recommendation 1: Co-Mentor Consultation Visibility & Multi-Turn Collaboration
- **Current Limitation:** In `services/help_requests.py`, tickets store a single `assigned_guide_id` and `assigned_sme_id`. Co-guides assigned to an entrepreneur cannot see the ticket in their active queue unless explicitly forwarded or reassigned.
- **Proposed Enhancement:**
  - Update `list_guide_requests()` so that all guides assigned to an entrepreneur (primary guide and co-guides) have read access to the ticket queue.
  - Allow co-guides to post follow-up comments under their own verified identity, visible to the primary guide and entrepreneur.
- **Value:** Prevents bottlenecks when the primary guide is temporarily unavailable; enables true tag-team mentorship.
- **Priority:** High | **Effort:** Medium

### Recommendation 2: SME Recusal Re-Entry & Conflict Resolution Workflow
- **Current Limitation:** When an SME declares a conflict of interest under `services/governance.py`, the recusal status is set to `RECUSED`. There is currently no UI workflow for the Admin to formally mark the conflict resolved (e.g., if the SME divested from a competing venture or the entrepreneur altered their business model).
- **Proposed Enhancement:**
  - Add a "Review & Lift Recusal" action in Tab 12 (SME Conflict Governance).
  - Admin provides an audit justification, transitions status to `RESOLVED_PERMITTED`, and notifies both parties.
- **Value:** Eliminates permanent deadlocks for specialized domain experts.
- **Priority:** Medium | **Effort:** Low

### Recommendation 3: DPDP-Compliant Lawful Erasure Runbook
- **Current Limitation:** Permanent account purge is intentionally disabled in this phase. However, regulatory frameworks (such as the Digital Personal Data Protection Act) require an eventual lawful erasure mechanism for departed users.
- **Proposed Enhancement:**
  - Implement a dedicated `execute_lawful_erasure(user_id)` procedure restricted to Sole Admin with two-factor approval.
  - **Pseudonymization Strategy:** Scrub personal identifiers (`full_name = 'Former Entrepreneur [Anonymized]'`, `email = 'erased_<hash>@erased.local'`, phone cleared, photos removed from cloud storage), while **preserving the original UUID and relational foreign keys**.
  - Retain financial logs, scheme releases, and audit records to satisfy legal compliance while purging personal data.
- **Value:** Guarantees 100% regulatory compliance with zero risk of database cascade corruption.
- **Priority:** High | **Effort:** Medium

### Recommendation 4: Dedicated Alumni Portal & Milestone Dossier Export
- **Current Limitation:** When an entrepreneur completes incubation, their journey is marked `status = 'completed'` / `stage = 'scale'`. However, they currently navigate the standard incubator dashboard with empty active milestones.
- **Proposed Enhancement:**
  - Render an "Incubation Graduate / Alumni" workspace variant.
  - Showcase an interactive timeline of completed milestones, verified scheme grants received, and a downloadable high-resolution "Fulcrum Incubation Certificate" PDF.
- **Value:** High-prestige user experience for successful founders; clean separation from active caseloads.
- **Priority:** Medium | **Effort:** Medium

### Recommendation 5: AI-Assisted Mentor Caseload Balancing Assistant
- **Current Limitation:** When archiving a mentor or reassigning an entrepreneur, the Admin must manually browse the mentor directory to find available guides with relevant sector expertise.
- **Proposed Enhancement:**
  - Within the Pre-Archive Impact Preview, provide an "Automated Recommendation" widget that scores candidate mentors by:
    1. District proximity.
    2. Relevant sector experience (e.g., AgriTech, DeepTech).
    3. Current active mentee count (load balancing).
- **Value:** Drastically reduces administrative overhead during large-scale cohort transitions.
- **Priority:** Low | **Effort:** Medium

### Recommendation 6: Cold-Storage Partitioning for Audit Logs
- **Current Limitation:** All account lifecycle and security activity logs are written to single tables (`account_lifecycle_log`, `activity_log`). Over multi-year operations, these tables will accumulate high row counts.
- **Proposed Enhancement:**
  - Implement PostgreSQL table partitioning by year (`account_lifecycle_log_2026`, etc.).
  - Automatically archive partitions older than 3 years to compressed read-only cold storage.
- **Value:** Ensures sub-second query performance on admin dashboards indefinitely.
- **Priority:** Low | **Effort:** High

---

## 3. Prioritized Implementation Roadmap

```
+-----------------------------------------------------------------------------+
| SPRINT 1 (Next Release):                                                    |
| - Co-Mentor Consultation Visibility (Recommendation 1)                      |
| - SME Recusal Re-Entry Workflow (Recommendation 2)                          |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
| SPRINT 2 (Compliance & Prestige):                                           |
| - DPDP-Compliant Lawful Erasure Runbook (Recommendation 3)                  |
| - Alumni Portal & Milestone Dossier Export (Recommendation 4)               |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
| SPRINT 3 (Scale & Automation):                                              |
| - AI-Assisted Mentor Caseload Balancing Assistant (Recommendation 5)        |
| - Cold-Storage Partitioning for Audit Logs (Recommendation 6)               |
+-----------------------------------------------------------------------------+
```
