# THE FULCRUM-INDIA X + Y → Z SCHEME MATCHING MODEL
**Formula:** `X (Aspirant Identity & Venture) + Y (Assistance Need) → Z (Qualified Schemes)`  
**Platform Version:** Fulcrum-Beta 1.0  
**Classification:** Core Algorithm Specification  

---

## 1. Architectural Philosophy

In traditional entrepreneurship portals, scheme matching operates either as a keyword search engine or as a generic questionnaire. Both models fail:
1. Keyword search returns hundreds of irrelevant programmes.
2. Generic questionnaires ask founders for legal parameters they do not understand, resulting in erroneous disqualifications or false hopes.

FULCRUM-INDIA implements the **X + Y → Z Principle**:
- **X** encapsulates everything known about the entrepreneur and their business from their verified profile.
- **Y** captures the immediate and strategic assistance the entrepreneur is actively seeking.
- **Z** represents the curated subset of schemes that:
  - Meet all mandatory gatekeeper statutory eligibility conditions.
  - Maximize the relevance of funding and support to the venture's actual needs.
  - Provide an evidence-backed checklist for the human Guide's formal release.

```
┌─────────────────────────────────┐       ┌─────────────────────────────────┐
│     X: WHO THE FOUNDER IS       │       │    Y: WHAT ASSISTANCE IS NEEDED │
│ ─────────────────────────────── │       │ ─────────────────────────────── │
│ • Location: State & District    │       │ • Assistance Goal (e.g. Grant)  │
│ • Industry Sector & Biz Type    │   +   │ • Specific Support Sub-Type     │
│ • Venture Development Stage     │       │ • Quantum Range (e.g. ₹5L-₹25L) │
│ • Gender & Equity Shareholding  │       │ • Urgency / Timeframe           │
│ • Social Category (SC/ST/OBC)   │       └────────────────┬────────────────┘
│ • Statutory Regs (DPIIT/Udyam)  │                        │
└────────────────┬────────────────┘                        │
                 │                                         │
                 └────────────────────┬────────────────────┘
                                      │
                                      ▼
             ┌─────────────────────────────────────────────────┐
             │       3-STAGE INTELLIGENT MATCHING PIPELINE     │
             │ ─────────────────────────────────────────────── │
             │  Stage 1: Mandatory Gatekeeper (Hard Pass/Fail) │
             │  Stage 2: Relevance & Purpose Scoring (0-100%)  │
             │  Stage 3: Evidence Checklist & Human Release    │
             └────────────────────────┬────────────────────────┘
                                      │
                                      ▼
             ┌─────────────────────────────────────────────────┐
             │           Z: QUALIFIED SCHEME RECOMMENDATION    │
             │ ─────────────────────────────────────────────── │
             │ • Highly Recommended (≥80%)                     │
             │ • Recommended (65%–79%)                         │
             │ • Potentially Eligible (50%–64%)                │
             │ • Explicitly Disqualified with Explanations     │
             └─────────────────────────────────────────────────┘
```

---

## 2. Vector X: Founder Identity & Venture Parameters

Vector X is extracted from `profiles.profile_data` via `normalize_aspirant_profile()`.

| Parameter | Data Type | Source Field | Example Values | Matching Purpose |
|:---|:---|:---|:---|:---|
| `state` | String | `profiles.state` | `"Tamil Nadu"`, `"Karnataka"` | Hard Gatekeeper for state-level funds |
| `district` | String | `profiles.district` | `"Madurai"`, `"Chennai"` | District DIC jurisdiction & local quotas |
| `sector` | String | `business.sector` | `"Food Processing & Agribusiness"` | Domain alignment & vertical specialization |
| `biz_type` | String | `business.business_type` | `"Manufacturing"`, `"Services"` | Capex vs opex subsidy applicability |
| `stage` | String | `business.stage` | `"Pre-Seed / Seed"`, `"Ideation"` | Stage-gating (R&D vs Commercialization) |
| `gender` | String | `personal.gender` | `"Male"`, `"Female"` | Demographic profiling |
| `women_equity_pct`| Float | `demographics.women_equity_pct`| `100.0`, `51.0`, `0.0` | **Statutory gatekeeper** for women quotas |
| `is_women_led` | Boolean | Computed ($\ge 51\%$) | `True` / `False` | Fast boolean indicator |
| `category` | String | `demographics.founder_category`| `"OBC"`, `"SC"`, `"ST"`, `"General"`| Affirmative statutory subsidies |
| `is_dpiit` | Boolean | `demographics.is_dpiit_recognized`| `True` / `False` | Startup India Seed Fund, tax exemptions |
| `is_startuptn` | Boolean | `demographics.is_startuptn_registered`| `True` / `False` | TANSEED grants, StartupTN benefits |
| `is_udyam` | Boolean | `demographics.is_udyam_registered`| `True` / `False` | MSME collateral-free loans (CGTMSE) |

---

## 3. Vector Y: Assistance Requirements

Vector Y is configured interactively by the founder or their Guide through the **Find Funding & Support** 4-level dependent dropdown interface:

### Level 1: Primary Assistance Goal
1. `Capital Grant / Seed Subsidy` (Non-dilutive government capital, capex reimbursement)
2. `Subsidized Debt / Term Loan / Working Capital` (Bank debt, low-interest state credit)
3. `Equity Investment / Angel / Seed Fund` (Dilutive venture capital, seed rounds)
4. `R&D / Prototype / Product Development` (Proof of concept funding, clinical trials)
5. `Market Access / Export / Trade Promotion` (GeM onboarding, overseas exhibitions)
6. `Infrastructure / Technology Upgradation / Machinery` (Credit linked capital subsidies)

### Level 2: Support Sub-Type (Filtered dynamically by Level 1)
- Under *Capital Grant*: Direct Project Subsidy, PoC Grant, Marketing Grant, SC/ST Special Grant.
- Under *Subsidized Debt*: Collateral-Free CGTMSE, Micro-Enterprise MUDRA, TIIC Term Loan.
- Under *Equity Investment*: Government Seed Fund (SISFS), State Angel Fund (Tanfund), VC Co-Investment.
- Under *R&D / Prototype*: TANSEED, Innovation Voucher Programme (IVP), Patent Reimbursement.

### Level 3: Funding Quantum Range
- `MICRO (< ₹5 Lakhs)` — e.g. MUDRA Shishu/Kishore, micro-subsidies.
- `SMALL (₹5 Lakhs – ₹25 Lakhs)` — e.g. UYEGP, TANSEED, PMEGP micro-manufacturing.
- `MEDIUM (₹25 Lakhs – ₹1 Crore)` — e.g. NEEDS scheme, Startup India Seed Fund.
- `LARGE (₹1 Crore – ₹5 Crores)` — e.g. PMFME Cluster, TIIC term loan.
- `EXPANSION (> ₹5 Crores)` — e.g. Mega Food Park, Large Infrastructure Subsidy.

### Level 4: Deployment Timeframe
- `IMMEDIATE (< 30 Days)` — Prioritizes schemes with continuous monthly sanction committees.
- `NEAR_TERM (1 to 3 Months)` — Standard bank term loans and state seed disbursements.
- `MEDIUM_TERM (3 to 6 Months)` — Competitive grant challenges with jury rounds.
- `STRATEGIC (> 6 Months)` — Multi-tranche capital expenditure programmes.

---

## 4. The 3-Stage Pipeline: From X + Y to Z

### Stage 1: Mandatory Gatekeeper (Hard Constraints)
Every scheme in the catalogue possesses non-negotiable statutory boundaries. If Vector X fails any hard constraint, the scheme is immediately assigned **`DISQUALIFIED`** with 0 match points and an explicit explanation.

1. **State Scope Check:** If scheme is restricted to Tamil Nadu (`is_tn_only == True`) and applicant's state is outside Tamil Nadu, scheme is disqualified.
2. **Gender Equity Check:** If scheme is designated for women entrepreneurs, applicant must have `women_equity_pct >= 51.0%`. A male primary founder with 0% women equity is disqualified.
3. **Affirmative Quota Check:** If scheme is exclusively for SC/ST founders (e.g. Special Stand-Up India or Tribal Fund) and applicant is General/OBC, scheme is disqualified.
4. **Sector Vertical Conflict:** If scheme is strictly a semiconductor or biotechnology clinical fund and founder is an organic food manufacturer, scheme is disqualified.

### Stage 2: Relevance Scoring & Weight Alignment (0 to 100 Points)
For all schemes passing Stage 1, the engine computes a multi-attribute utility score based on five transparent pillars:

$$\text{Final Score} = \text{Domain Score} (35) + \text{Stage Score} (25) + \text{Geography Score} (15) + \text{Assistance Goal Fit} (15) + \text{Affirmative Quota} (10)$$

1. **Sector & Domain (Max 35 pts):**
   - Direct specific industry match = 35 pts.
   - Manufacturing enterprise allocation = 25 pts.
   - Broad MSME eligibility = 25 pts.
   - Cross-sector agnostic fund = 15 pts.
2. **Development Stage (Max 25 pts):**
   - Exact stage match (Seed to Seed) = 25 pts.
   - Stage-agnostic fund = 20 pts.
   - Adjacent stage = 10 pts.
   - Stage mismatch (Idea applying for Series A Debt) = 0 pts.
3. **Geographic Jurisdiction (Max 15 pts):**
   - Domestic state match (TN founder on TN fund) = 15 pts.
   - National central government fund = 12 pts.
4. **Assistance Goal & Quantum Fit (Y Match) (Max 15 pts):**
   - Direct assistance goal match (Grant sought, Grant provided) = 10 pts.
   - Funding quantum fits within scheme minimum and maximum limits = 5 pts.
5. **Affirmative Quota Priority (Max 10 pts):**
   - Target SC/ST/OBC quota match = 10 pts (only if applicant affirmatively belongs to that group).
   - Target women-led concession = 10 pts (only if $\ge 51\%$ female equity).
   - DPIIT startup recognition benefit = 4 pts.

### Stage 3: Human Review & Evidence Checklist
The engine outputs an itemized evidence checklist for each scheme. Rather than blindly stamping "Verified Eligible", the system classifies every requirement into actionable states:
- **`Verified Eligible`**: Verified by structured database attributes (e.g. Tamil Nadu state verified, Seed stage confirmed).
- **`Self-Declared / Pending Evidence`**: Declared by founder; requires documentation (e.g. Udyam certificate, DPR, audited financial statement).
- **`Action Required`**: Unfulfilled pre-requisite (e.g. "Action Required: Register on DPIIT portal").
- **`Disqualified`**: Criterion failed.

---

## 5. Result Z: Structured Recommendation Categories

| Match Score | Status Badge | Definition | Workflow Action |
|:---|:---|:---|:---|
| **80% – 100%** | `HIGHLY RECOMMENDED` | Exceptional alignment across domain, stage, geography, and requested support. | Priority recommendation for Guide release dossier. |
| **65% – 79%** | `RECOMMENDED` | Strong baseline fit; minor documentation or registration steps needed. | Guide reviews checklist and suggests DPR preparation. |
| **50% – 64%** | `POTENTIALLY ELIGIBLE` | Eligible under broad criteria; requires strategic refinement or secondary quota fit. | Secondary consideration for founder growth roadmap. |
| **0% (Disqualified)**| `DISQUALIFIED` | Fails mandatory statutory boundaries (state, gender equity, sector). | Release blocked by gatekeeper; reasons displayed transparently. |

