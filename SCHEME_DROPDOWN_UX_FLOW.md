# SCHEME DEPENDENT DROPDOWNS: UX FLOW & INTERACTION DESIGN
**Interface:** Find Funding & Support (Aspirant Dashboard Tab 5 & Guide Evaluation Panel)  
**Implementation:** `views/aspirant.py`, `services/scheme_rules.py`  
**Classification:** UX/UI Design & State Specification  

---

## 1. User Experience Objective

Founders often struggle with bureaucratic nomenclature. When asked whether they qualify for "Sub-clause 4(b) under MSME Credit Guarantee", they freeze. 

The **Find Funding & Support** module solves this by guiding the entrepreneur through a **4-level dependent selection path** that maps everyday business intent into statutory scheme criteria:

```
[ Level 1: What do you need? ]
         │
         ▼
[ Level 2: Which specific flavor of support? ] (Dynamically filtered by Level 1)
         │
         ▼
[ Level 3: How much capital / support quantum? ]
         │
         ▼
[ Level 4: How soon is this capital required? ]
```

---

## 2. The 4-Level Dependent Hierarchy

### Level 1: Primary Assistance Goal (`sel_goal`)
The starting point asks the founder to identify their highest-priority business objective:
- `ALL` (Broad exploration across all programmes)
- `Capital Grant / Seed Subsidy` (Non-repayable direct cash support)
- `Subsidized Debt / Term Loan / Working Capital` (Bank loans with low interest or zero collateral)
- `Equity Investment / Angel / Seed Fund` (Selling equity for venture acceleration)
- `R&D / Prototype / Product Development` (Building technology, testing formulations)
- `Market Access / Export / Trade Promotion` (Selling to government, overseas buyers)
- `Infrastructure / Technology Upgradation / Machinery` (Buying factory machines, setting up labs)

### Level 2: Specific Support Sub-Category (`sel_sub_type`)
Level 2 is **strictly dependent** on Level 1. Streamlit updates the available options immediately upon change:

| Level 1 Selection | Dynamic Level 2 Options |
|:---|:---|
| **Capital Grant / Seed Subsidy** | • All Capital Grants<br>• Direct Project Subsidy (Capex)<br>• Proof of Concept / Prototype Grant<br>• Marketing / Packaging / Branding Grant<br>• Special Affirmative Quota Grant (SC/ST/Women) |
| **Subsidized Debt / Term Loan** | • All Subsidized Debt<br>• Collateral-Free Bank Loan (CGTMSE)<br>• Micro-Enterprise Loan (MUDRA)<br>• State Enterprise Term Loan (TIIC / Needs)<br>• Interest Subvention / Soft Loan |
| **Equity Investment / Angel / Seed Fund** | • All Equity Funds<br>• Government Seed Fund (SISFS)<br>• State Angel Fund (Tanfund / AngelsTN)<br>• Venture Capital / Growth Co-Investment |
| **R&D / Prototype Development** | • All R&D & Tech Support<br>• Innovation Grant (TANSEED / IVP)<br>• Patent / IP Reimbursement<br>• Biotech / DeepTech Challenge Fund |
| **Market Access / Trade Promotion** | • All Market Access<br>• GeM Public Procurement Preference<br>• Export Incentive / Overseas Fair Subsidy<br>• E-Commerce Onboarding Support |
| **Infrastructure & Machinery** | • All Infrastructure & Machinery<br>• Capital Machinery Subsidy (CLCSS / Credit Linked)<br>• Common Facility Centre / Cluster Grant<br>• Testing / Quality Certification Subsidy (ZED / ISO) |

### Level 3: Funding / Support Quantum Range (`sel_quantum`)
Helps filter schemes whose statutory caps match the founder's financial capacity:
- `ANY_AMOUNT` — No financial limit applied.
- `MICRO (< ₹5 Lakhs)` — Suitable for nano-enterprises, cottage units, village industries.
- `SMALL (₹5 Lakhs – ₹25 Lakhs)` — Early stage pilots, TANSEED grants, PMEGP units.
- `MEDIUM (₹25 Lakhs – ₹1 Crore)` — Commercialization, industrial machinery, NEEDS schemes.
- `LARGE (₹1 Crore – ₹5 Crores)` — Industrial scale-up, TIIC plant debt, PMFME clusters.
- `EXPANSION (> ₹5 Crores)` — Mega infrastructure subsidies, institutional rounds.

### Level 4: Deployment Timeframe (`sel_timeframe`)
Reflects operational urgency:
- `ANY_TIMEFRAME`
- `IMMEDIATE (< 30 Days)`
- `NEAR_TERM (1 to 3 Months)`
- `MEDIUM_TERM (3 to 6 Months)`
- `STRATEGIC (> 6 Months)`

---

## 3. UI Layout & Visual Design Tokens

The dropdown console is presented inside a high-contrast container in `views/aspirant.py` (Tab 5):

```
┌────────────────────────────────────────────────────────────────────────┐
│  🎯 Find Funding & Support (X + Y → Z Explorer)    [X + Y → Z Engine]  │
│  Select your specific assistance requirements to match against 170+    │
│  central and state government schemes.                                 │
├────────────────────────────────────────────────────────────────────────┤
│  DEFINE YOUR ASSISTANCE NEED (Y)                                       │
│                                                                        │
│  1. Primary Assistance Goal *           2. Specific Support Type *     │
│  [ Capital Grant / Seed Subsidy     ▼ ] [ Direct Project Subsidy   ▼ ] │
│                                                                        │
│  3. Funding / Support Quantum *         4. Deployment Timeframe *      │
│  [ SMALL (₹5 Lakhs – ₹25 Lakhs)     ▼ ] [ NEAR_TERM (1-3 Months)   ▼ ] │
└────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│  ▼ 🔍 View Matched Schemes for this Need (14 Qualifying Opportunities) │
│  ────────────────────────────────────────────────────────────────────  │
│  • PM FME Scheme · MoFPI · ₹10 Lakhs                       [87% MATCH] │
│    ✓ Direct sector match · Capital grant capex alignment               │
│    Official Application Portal ↗                                       │
│  ────────────────────────────────────────────────────────────────────  │
│  • Agro-Processing Cluster Scheme · MoFPI · ₹5 Crores      [87% MATCH] │
│    ✓ Direct sector match · Infrastructure grant match                  │
│    Official Application Portal ↗                                       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Preservation of Existing Workflows
- **Non-Destructive Integration:** The existing Guide Curated Schemes section is fully preserved directly beneath the explorer expander.
- **Role Isolation:** Aspirants explore matches in read-only mode with portal links; Guides retain exclusive authority to formally release schemes into the venture's official dossier.
- **Instant Responsiveness:** Dropdown selections do not trigger expensive network round-trips; in-memory caching evaluates all 179 schemes in under 12 milliseconds.
