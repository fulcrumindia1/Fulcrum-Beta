# SCHEME RELEASE WORKFLOW & GUIDE GATEKEEPER INTEGRATION
**Workflow:** Guide Curated Release & Institutional Governance  
**Modules:** `views/guide.py`, `services/schemes.py`, `services/journey.py`  
**Classification:** Operational Governance Specification  

---

## 1. Architectural Role of the Guide as Gatekeeper

Government grant portals often overwhelm entrepreneurs with confusing application portals, causing high rejection rates and wasted time. In FULCRUM-INDIA:
1. **The Algorithm is an Advisor, Not the Decider:** The X + Y → Z matching engine calculates recommendations, scores, and concern flags.
2. **The Guide is the Gatekeeper:** Schemes do not become active on an Aspirant's roadmap until a human Guide reviews the candidate, verifies the evidence checklist, crafts a personalized recommendation note, and executes a formal **Release Action**.

```
[ Algorithmic Engine ] ──> [ Guide Evaluation Console ] ──> [ Institutional Gatekeeper ] ──> [ Aspirant Roadmap ]
(Calculates X + Y -> Z)    (Reviews Evidence Checklist)     (Enforces Compliance Gate)        (Unlocked with Guide Note)
```

---

## 2. Guide Evaluation Interface (`views/guide.py`)

When an assigned Guide inspects an Aspirant in the **Guide Portal (Tabs: Entrepreneurs Directory → Scheme Intelligence)**:
1. **Suggested Matches:** Displays all active schemes meeting the baseline match threshold ($\ge 60\%$), ranked by match score.
2. **Match Reasoning Banner:** Displays exact reasons for the match (e.g. `✓ Direct sector match: Food Processing`, `✓ Tamil Nadu jurisdiction match`).
3. **Potential Concerns:** Displays statutory caveats (e.g. `⚠ DPIIT registration required for official portal application`, `⚠ Requires commercial DPR`).
4. **Itemized Evidence Checklist:**
   - Items with `Verified Eligible` are tagged with green checkmarks.
   - Items with `Self-Declared / Pending Evidence` indicate documents the Guide must review.
   - Items with `Action Required` highlight next steps for the founder.

---

## 3. Disqualification Barrier & Override Governance

To address **Defect 7** (where disqualified schemes could previously be released without hindrance), the release function enforces a two-stage barrier:

```python
eval_res = evaluate_scheme_for_aspirant(aspirant_id, scheme)
if eval_res.get("is_disqualified") and not allow_disqualified_override:
    disq_reasons = "; ".join(eval_res.get("potential_concerns", []))
    return False, f"Gatekeeper Restriction: Scheme does not meet mandatory criteria ({disq_reasons})."
```

### When Can an Override Occur?
An override is permitted only when the Guide possesses offline evidence that supersedes database attributes (e.g. the founder has executed an un-registered partnership deed granting 51% equity to a woman co-founder, or has received an in-principle approval from the DIC). The Guide must record a written justification note which is permanently audited in the Journey timeline.

---

## 4. End-to-End Release Execution Flow

When the Guide clicks **"Release Scheme to Aspirant"**:
1. **State Persistence:** An upsert occurs in `scheme_releases` table:
   ```json
   {
     "aspirant_id": "uuid",
     "guide_id": "uuid",
     "scheme_id": "uuid",
     "status": "RELEASED",
     "guide_recommendation": "Reviewed founder's DPR and cap table. Cleared for PMFME DIC submission.",
     "eligibility_summary": "Score: 87% Match (HIGHLY RECOMMENDED) | 3 criteria met",
     "released_at": "2026-11-05T14:15:00Z"
   }
   ```
2. **Journey Event Generation:** `log_meaningful_event()` logs an immutable milestone to the founder's official Journey timeline:
   - **Category:** `SCHEME_RELEASE`
   - **Title:** `Scheme Released: PM FME Scheme`
   - **Actor:** `Guide: [Guide Full Name]`
   - **Notes:** Personalized strategic guidance note.
3. **In-App Notification:** A notification is generated in `notifications` table, alerting the founder that their Guide has unlocked a new funding dossier.
4. **Instant Dashboard Appearance:** The scheme appears under **Aspirant Dashboard → Recommended Funding Schemes** with a distinctive purple border, Guide recommendation badge, and copyable AI application prompt.
