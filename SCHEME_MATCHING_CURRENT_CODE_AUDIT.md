# SCHEME MATCHING ENGINE: CURRENT CODEBASE AUDIT & DEFECT REPORT
**Platform:** FULCRUM-INDIA Enterprise Guidance System  
**Component:** Scheme Intelligence & Matching Architecture (`services/schemes.py`, `views/aspirant.py`, `views/guide.py`)  
**Audit Date:** November 2026  
**Auditor:** Antigravity Advanced Agentic AI Pair Programmer  

---

## 1. Executive Summary
This report documents a comprehensive architectural and line-by-line audit of the scheme matching engine in FULCRUM-INDIA. 
The system evaluates government subsidies, state seed grants, bank loans, and venture capital schemes (179 active catalogue entries) against entrepreneur profiles.

While the existing platform successfully models multi-role governance (Aspirants, Guides, SMEs, Admins) and maintains immutable Journey milestones, the underlying scheme matching engine suffered from 10 identified structural defects. These defects caused false positive recommendations, inappropriate affirmative quota assignments, hardcoded regional defaults, and unverified checklist stamps.

---

## 2. End-to-End Data Flow Architecture

The data pipeline from founder registration to scheme release follows four distinct operational tiers:

```
[ Tier 1: Founder Input ]
  Aspirant completes Profile Form (Personal, Professional, Business, Demographics)
  Stored in `profiles.profile_data` JSONB column (Supabase PostgreSQL / Local SQLite)
        │
        ▼
[ Tier 2: Scheme Catalogue & Metadata ]
  179 Central & State Schemes loaded from `seed/schemes.json` / Supabase `schemes` table
  Unstructured text fields: `name`, `agency`, `funding_type`, `stage`, `amount`, `sectors`, `eligibility`, `hidden_agenda`
        │
        ▼
[ Tier 3: Matching Engine Evaluation ]
  `match_schemes_for_aspirant()` executes in-memory heuristic comparison
  Evaluates 4 traditional buckets: Sector (40%), Stage (25%), Scope (20%), Demographics (15%)
  Outputs match score (0-100%) and recommendation status
        │
        ▼
[ Tier 4: Guide Gatekeeper & Release ]
  Guide inspects suggested matches under Guide Portal (`views/guide.py`)
  Evaluates checklist & strategic fit via `evaluate_scheme_for_aspirant()`
  Formally executes `release_scheme_to_aspirant()` -> Persisted in `scheme_releases` table
  Journey event generated -> Unlocked on Aspirant Dashboard
```

---

## 3. Investigation of the 10 Known Defects

### Defect 1: Scheme category bonuses awarded without confirming matching aspirant eligibility
- **File & Line:** `services/schemes.py` (legacy lines 427–432)
- **Vulnerability:** The engine awarded affirmative points if the scheme mentioned affirmative keywords, regardless of founder category:
  ```python
  # Flawed legacy implementation:
  if asp_category and asp_category in elig_text:
      score += 15
  elif "obc" in elig_text or "backward" in full_scheme_text:
      score += 15 # Awarded to ALL founders if scheme mentioned OBC!
  ```
- **Consequence:** A General-category founder received a +15 bonus on OBC-specific schemes simply because the word "OBC" was in the scheme's text corpus.
- **Resolution:** Re-architected in `services/scheme_matching_engine.py`. Affirmative points are awarded strictly if `x["category"] in target_categories`.

---

### Defect 2: Female gender treated as sufficient evidence of women-led enterprise ownership
- **File & Line:** `services/schemes.py` (legacy line 295) & `views/aspirant.py` (legacy line 353)
- **Vulnerability:**
  ```python
  # Flawed legacy logic:
  is_women_led = bool(demo.get("is_women_led") or "female" in asp_gender or "woman" in asp_gender or women_equity_num >= 51.0)
  ```
- **Consequence:** Any female applicant was automatically classified as a "women-led enterprise" eligible for 100% reserved women schemes (e.g. TWEES, TREAD) even if she held minority equity (e.g. 5%) or was an employee filling out a founder form for a male-owned firm.
- **Resolution:** Strict statutory compliance enforced: `is_women_led` requires explicit confirmation of `women_equity_pct >= 51.0` in accordance with MSME Ministry guidelines.

---

### Defect 3: Missing state information defaulted to Tamil Nadu
- **File & Line:** `services/schemes.py` (legacy line 286)
- **Vulnerability:**
  ```python
  asp_state = (profile.get("state") or demo.get("state") or "Tamil Nadu").lower()
  ```
- **Consequence:** An entrepreneur who registered from Bengaluru (Karnataka) or Mumbai without filling the state field was silently evaluated as a Tamil Nadu domestic enterprise, falsely receiving state-restricted schemes like UYEGP, NEEDS, and StartupTN TANSEED.
- **Resolution:** Normalized in `normalize_aspirant_profile()`. If state is missing, state is left as empty string; state-restricted schemes raise a location verification warning.

---

### Defect 4: Registration checkboxes defaulted to True on new blank profiles
- **File & Line:** `views/aspirant.py` (legacy lines 350–351)
- **Vulnerability:**
  ```python
  d_dpiit = st.checkbox("DPIIT Recognized Startup", value=bool(cur_demo.get("is_dpiit_recognized", True)))
  d_startuptn = st.checkbox("StartupTN Registered", value=bool(cur_demo.get("is_startuptn_registered", True)))
  ```
- **Consequence:** New founders signing up for the first time had DPIIT and StartupTN recognition checkboxes pre-checked by default! If they clicked "Save", they falsely claimed formal statutory recognitions they did not possess.
- **Resolution:** Corrected to `value=bool(cur_demo.get("is_dpiit_recognized", False))` and `False` for StartupTN.

---

### Defect 5: Scheme eligibility checklist items all labelled "Verified Eligible" without independent verification
- **File & Line:** `services/schemes.py` (legacy lines 502–505)
- **Vulnerability:**
  ```python
  checklist = []
  for item in elig:
      checklist.append({"item": str(item), "status": "Verified Eligible"})
  ```
- **Consequence:** The Guide evaluation console presented every criterion as "Verified Eligible", giving mentors false confidence that the applicant met age, turnover, and statutory requirements without verification.
- **Resolution:** Replaced with `build_evidence_checklist()` which dynamically grades items into `Verified Eligible`, `Self-Declared / Pending Evidence`, `Action Required: DPIIT Registration`, and `Disqualified`.

---

### Defect 6: Missing evaluation results defaulted to a 50% score
- **File & Line:** `services/schemes.py` (legacy line 490)
- **Vulnerability:**
  ```python
  score = match_record["match_score"] if match_record else 50
  ```
- **Consequence:** When a scheme could not be found or evaluated, the fallback score defaulted to 50% ("Qualified/Recommended") rather than 0% or an explicit error state.
- **Resolution:** Explicit evaluation returns score 0 and status "LOW FIT" / "UNABLE TO EVALUATE".

---

### Defect 7: Scheme release did not require verified eligibility
- **File & Line:** `services/schemes.py` (legacy lines 560–600)
- **Vulnerability:** The Guide could release a scheme even if it was flagged with 0% score and disqualified by gender or geography. There was no gatekeeper barrier stopping release of an invalid scheme.
- **Resolution:** `release_scheme_to_aspirant()` now checks `eval_res.get("is_disqualified")`. If disqualified, release is blocked unless an affirmative verification override is confirmed.

---

### Defect 8: Funding need, purpose, and amount not incorporated into the main ranking formula
- **File & Line:** `services/schemes.py` (legacy lines 312–439)
- **Vulnerability:** The engine only evaluated Sector (X), Stage (X), Scope (X), and Demographic (X). It completely ignored what the founder actually needed: Capital Grant vs Subsidized Loan vs Seed Equity, quantum requested, or timeline urgency!
- **Resolution:** Integrated the **Y Vector** (`assistance_goal`, `support_type`, `quantum_range`, `timeframe`) with explicit 15-point weighting.

---

### Defect 9: Documented scoring weights did not match implementation branches
- **File & Line:** `services/schemes.py` (legacy lines 330–439)
- **Vulnerability:** The docstring specified 40/25/20/15 points, but the code introduced arbitrary deductions (`score -= 20`), multiple overlapping bonuses (`score += 20`, `score += 15`, `score += 8`, `score += 3`), leading to unstable scores clamped between 0 and 100.
- **Resolution:** Replaced with a normalized 5-factor scoring model where points sum to 100 without arbitrary stacking.

---

### Defect 10: Scheme catalogue contained free-text descriptions unable to power definitive decisions
- **File & Line:** `seed/schemes.json`
- **Vulnerability:** Criteria like "Applicant should be between 18 and 45 years of age", "Special preference for green energy", or "Margin money of 25%" existed only as strings.
- **Resolution:** Introduced `services/scheme_rules.py` which provides structured machine-readable metadata (`allowed_states`, `is_women_only`, `mandatory_women_equity_pct`, `target_categories`, `min_lakhs`, `max_lakhs`, `primary_goal`).

---

## 4. Summary Table of Audit Findings

| Defect # | Component | Root Cause | Severity | Corrective Action |
|:---|:---|:---|:---|:---|
| **1** | Demographic Scoring | Free-text keyword check awarded points to non-qualifying founders | HIGH | Replaced with strict identity-to-target matching |
| **2** | Gender Evaluation | Female gender assumed 100% equity in women schemes | CRITICAL | Enforced statutory $\ge$51% equity threshold |
| **3** | State Jurisdiction | Defaulted missing state to Tamil Nadu | MEDIUM | Preserved empty state; added verification warnings |
| **4** | Profile UI | DPIIT and StartupTN checkboxes defaulted to True | HIGH | Defaulted to False; required affirmative declaration |
| **5** | Guide Checklist | Hardcoded "Verified Eligible" for all raw strings | HIGH | Built multi-tier status classifier |
| **6** | Evaluation Fallback | Defaulted missing matches to 50% | MEDIUM | Defaulted missing matches to 0% with clear error |
| **7** | Release Authority | No check preventing release of disqualified schemes | HIGH | Enforced gatekeeper block on disqualified schemes |
| **8** | Matching Objective | Ignored what the founder actually needed (Y) | HIGH | Added Y-vector (Goal, Support Type, Quantum, Timeframe) |
| **9** | Weight Alignment | Arbitrary additions/subtractions broke documented weights | MEDIUM | Re-calibrated 5 normalized weighting tiers summing to 100 |
| **10** | Catalogue Schema | Unstructured text strings prevented programmatic logic | MEDIUM | Created structured rules layer in `scheme_rules.py` |
