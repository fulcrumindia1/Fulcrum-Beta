# SCHEME ELIGIBILITY RULE SCHEMA & METADATA SPECIFICATION
**Standard:** FULCRUM-SRS-2026-V1  
**Module:** `services/scheme_rules.py`  
**Classification:** Schema & Data Engineering Specification  

---

## 1. Overview
Government scheme descriptions typically consist of bureaucratic PDF circulars, complex guidelines, and free-text sentences. To execute deterministic and explainable matching, FULCRUM-INDIA maps every scheme into a structured, machine-readable rule schema.

This specification details the standard schema fields, validation constraints, and JSON representation.

---

## 2. JSON Schema Definition

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "FulcrumSchemeRule",
  "type": "object",
  "required": [
    "scheme_id",
    "allowed_states",
    "is_tn_only",
    "is_women_only",
    "mandatory_women_equity_pct",
    "is_sc_st_only",
    "target_categories",
    "is_all_sectors",
    "sectors",
    "allowed_stages",
    "mandatory_registrations",
    "primary_goal",
    "funding_type"
  ],
  "properties": {
    "scheme_id": {
      "type": "string",
      "description": "Unique UUID or legacy source ID (e.g., SCH-001 or UUID)"
    },
    "allowed_states": {
      "type": "array",
      "items": { "type": "string" },
      "description": "List of permissible Indian states. ['ALL'] represents Central schemes."
    },
    "is_tn_only": {
      "type": "boolean",
      "description": "True if strictly restricted to Tamil Nadu registered enterprises."
    },
    "is_women_only": {
      "type": "boolean",
      "description": "True if scheme is statutory quota reserved exclusively for women founders."
    },
    "mandatory_women_equity_pct": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 100.0,
      "default": 0.0,
      "description": "Minimum required female equity ownership share (typically 51.0%)."
    },
    "is_sc_st_only": {
      "type": "boolean",
      "description": "True if strictly reserved for Scheduled Caste / Scheduled Tribe entrepreneurs."
    },
    "target_categories": {
      "type": "array",
      "items": { "type": "string", "enum": ["SC", "ST", "OBC", "EWS", "GENERAL", "MINORITY"] },
      "description": "Specific social affirmative quota categories eligible for subsidies."
    },
    "is_all_sectors": {
      "type": "boolean",
      "description": "True if cross-sector agnostic."
    },
    "sectors": {
      "type": "array",
      "items": { "type": "string" },
      "description": "List of normalized industry sectors eligible for support."
    },
    "allowed_stages": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Development stages allowed: ['ideation', 'pre-seed', 'seed', 'early', 'growth', 'scale', 'all']"
    },
    "mandatory_registrations": {
      "type": "array",
      "items": { "type": "string", "enum": ["dpiit", "startuptn", "udyam", "gst", "fssai"] },
      "description": "Statutory certificates mandatory before application sanction."
    },
    "min_lakhs": {
      "type": ["number", "null"],
      "description": "Minimum funding quantum in Lakhs INR."
    },
    "max_lakhs": {
      "type": ["number", "null"],
      "description": "Maximum funding quantum in Lakhs INR."
    },
    "primary_goal": {
      "type": "string",
      "enum": [
        "Capital Grant / Seed Subsidy",
        "Subsidized Debt / Term Loan / Working Capital",
        "Equity Investment / Angel / Seed Fund",
        "R&D / Prototype / Product Development",
        "Market Access / Export / Trade Promotion",
        "Infrastructure / Technology Upgradation / Machinery"
      ]
    },
    "funding_type": {
      "type": "string",
      "description": "Relational categorization (Grant, Loan, Subsidy, Equity)."
    }
  }
}
```

---

## 3. Sample Structured Records

### Case 1: PMFME (Pradhan Mantri Formalisation of Micro food processing Enterprises)
```json
{
  "scheme_id": "SCH-PMFME-01",
  "allowed_states": ["ALL"],
  "is_tn_only": false,
  "is_women_only": false,
  "mandatory_women_equity_pct": 0.0,
  "is_sc_st_only": false,
  "target_categories": ["SC", "ST", "OBC", "GENERAL"],
  "is_all_sectors": false,
  "sectors": ["food processing & agribusiness", "agriculture", "dairy", "organic processing"],
  "allowed_stages": ["pre-seed", "seed", "early", "growth"],
  "mandatory_registrations": ["udyam", "fssai"],
  "min_lakhs": 1.0,
  "max_lakhs": 10.0,
  "primary_goal": "Capital Grant / Seed Subsidy",
  "funding_type": "Credit Linked Subsidy (35% Capex Subsidy up to ₹10 Lakhs)"
}
```

### Case 2: TWEES (Tamil Nadu Women Entrepreneurs Empowerment Scheme)
```json
{
  "scheme_id": "SCH-TWEES-TN",
  "allowed_states": ["Tamil Nadu"],
  "is_tn_only": true,
  "is_women_only": true,
  "mandatory_women_equity_pct": 51.0,
  "is_sc_st_only": false,
  "target_categories": ["GENERAL", "OBC", "SC", "ST"],
  "is_all_sectors": true,
  "sectors": ["all sectors"],
  "allowed_stages": ["ideation", "pre-seed", "seed", "early"],
  "mandatory_registrations": ["udyam"],
  "min_lakhs": 5.0,
  "max_lakhs": 50.0,
  "primary_goal": "Capital Grant / Seed Subsidy",
  "funding_type": "Subsidized Term Loan with 25% Capital Subsidy"
}
```

### Case 3: StartupTN TANSEED (Tamil Nadu Seed Fund)
```json
{
  "scheme_id": "SCH-TANSEED-V5",
  "allowed_states": ["Tamil Nadu"],
  "is_tn_only": true,
  "is_women_only": false,
  "mandatory_women_equity_pct": 0.0,
  "is_sc_st_only": false,
  "target_categories": ["SC", "ST", "OBC", "GENERAL"],
  "is_all_sectors": true,
  "sectors": ["all sectors", "deeptech", "agritech", "fintech", "cleantech"],
  "allowed_stages": ["pre-seed", "seed", "prototype", "early"],
  "mandatory_registrations": ["dpiit", "startuptn"],
  "min_lakhs": 10.0,
  "max_lakhs": 15.0,
  "primary_goal": "Capital Grant / Seed Subsidy",
  "funding_type": "Seed Grant (₹15 Lakhs Non-Dilutive Grant)"
}
```

---

## 4. Rule Parsing and Normalization Architecture

The rule extractor in `services/scheme_rules.py` implements regular expressions and statutory keyword lookups:

```python
def parse_quantum_limits(amount_str: str) -> Tuple[Optional[float], Optional[float]]:
    # Extracts Crores (* 100 Lakhs) and Lakhs
    cr_matches = re.findall(r'(\d+(?:\.\d+)?)\s*(?:cr|crore)', text)
    lakh_matches = re.findall(r'(\d+(?:\.\d+)?)\s*(?:lakh|lac)', text)
    ...
```

This ensures that whenever new schemes are added through the Admin Scheme Catalogue CRUD (`views/admin.py`), the structured rule layer dynamically ingests the scheme and assigns appropriate gatekeepers.

