"""
services/scheme_rules.py — Structured Scheme Eligibility & Assistance Rules Layer
==================================================================================
Provides structured machine-readable metadata and rules for government schemes,
enabling rigorous 3-stage X + Y -> Z matching:
- Stage 1: Mandatory / Gatekeeper Eligibility (Hard constraints)
- Stage 2: Relevance & Purpose Alignment (X + Y matching)
- Stage 3: Human Review & Evidence Checklist

Terminology:
- Allowed states and districts
- Permitted enterprise development stages
- Eligible industry sectors
- Target demographic criteria (women-led, SC/ST/OBC, minorities)
- Minimum equity thresholds (e.g. 51% for women schemes)
- Required statutory registrations (UDYAM, GST, DPIIT, StartupTN)
- Assistance/Support types and funding quantum brackets
"""

from typing import Dict, List, Optional, Any
import re

# ── MASTER TAXONOMY FOR ASSISTANCE NEED (Y) ──
ASSISTANCE_GOALS = [
    "ALL",
    "Capital Grant / Seed Subsidy",
    "Subsidized Debt / Term Loan / Working Capital",
    "Equity Investment / Angel / Seed Fund",
    "R&D / Prototype / Product Development",
    "Market Access / Export / Trade Promotion",
    "Infrastructure / Technology Upgradation / Machinery"
]

SUPPORT_TYPES_BY_GOAL = {
    "Capital Grant / Seed Subsidy": [
        "All Capital Grants",
        "Direct Project Subsidy (Capex)",
        "Proof of Concept / Prototype Grant",
        "Marketing / Packaging / Branding Grant",
        "Special Affirmative Quota Grant (SC/ST/Women)"
    ],
    "Subsidized Debt / Term Loan / Working Capital": [
        "All Subsidized Debt",
        "Collateral-Free Bank Loan (CGTMSE)",
        "Micro-Enterprise Loan (MUDRA)",
        "State Enterprise Term Loan (TIIC / Needs)",
        "Interest Subvention / Soft Loan"
    ],
    "Equity Investment / Angel / Seed Fund": [
        "All Equity Funds",
        "Government Seed Fund (SISFS)",
        "State Angel Fund (Tanfund / AngelsTN)",
        "Venture Capital / Growth Co-Investment"
    ],
    "R&D / Prototype / Product Development": [
        "All R&D & Tech Support",
        "Innovation Grant (TANSEED / IVP)",
        "Patent / IP Reimbursement",
        "Biotech / DeepTech Challenge Fund"
    ],
    "Market Access / Export / Trade Promotion": [
        "All Market Access",
        "GeM Public Procurement Preference",
        "Export Incentive / Overseas Fair Subsidy",
        "E-Commerce Onboarding Support"
    ],
    "Infrastructure / Technology Upgradation / Machinery": [
        "All Infrastructure & Machinery",
        "Capital Machinery Subsidy (CLCSS / Credit Linked)",
        "Common Facility Centre / Cluster Grant",
        "Testing / Quality Certification Subsidy (ZED / ISO)"
    ]
}

FUNDING_QUANTUM_RANGES = [
    "ANY_AMOUNT",
    "MICRO (< ₹5 Lakhs)",
    "SMALL (₹5 Lakhs – ₹25 Lakhs)",
    "MEDIUM (₹25 Lakhs – ₹1 Crore)",
    "LARGE (₹1 Crore – ₹5 Crores)",
    "EXPANSION (> ₹5 Crores)"
]

TIMEFRAME_OPTIONS = [
    "ANY_TIMEFRAME",
    "IMMEDIATE (< 30 Days)",
    "NEAR_TERM (1 to 3 Months)",
    "MEDIUM_TERM (3 to 6 Months)",
    "STRATEGIC (> 6 Months)"
]


def parse_quantum_limits(amount_str: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Extracts min and max funding limits in INR (in Lakhs) from text.
    e.g. 'Up to ₹25 Lakhs' -> (None, 25.0)
    '₹50 Lakhs to ₹5 Crores' -> (50.0, 500.0)
    """
    if not amount_str:
        return None, None

    text = amount_str.lower()
    all_values = []

    for val in re.findall(r'(\d+(?:\.\d+)?)\s*(?:cr|crore)', text):
        all_values.append(float(val) * 100.0)

    for val in re.findall(r'(\d+(?:\.\d+)?)\s*(?:lakh|lac)', text):
        all_values.append(float(val))

    if not all_values:
        return None, None

    max_amt = max(all_values)
    min_amt = min(all_values) if len(all_values) > 1 else None
    return min_amt, max_amt


def get_scheme_structured_rules(scheme: Dict) -> Dict[str, Any]:
    """
    Extracts structured rule metadata from a scheme record.
    Uses explicit scheme fields, naming patterns, agencies, and known statutory guidelines.
    """
    s_name = (scheme.get("name") or "").lower()
    s_agency = (scheme.get("agency") or "").lower()
    s_brief = (scheme.get("brief") or "").lower()
    s_desc = (scheme.get("description") or "").lower()
    scope = (scheme.get("state_scope") or scheme.get("geography") or "All India").lower()
    fund_type = (scheme.get("funding_type") or scheme.get("scheme_type") or "Grant").lower()
    amt_str = scheme.get("amount") or ""

    # 1. Geographic Jurisdiction
    is_tn_only = any(x in scope for x in ["tamil nadu", "tn"]) or any(x in s_agency for x in ["startuptn", "tamil nadu", "tiic", "msme tn", "editn"])
    allowed_states = ["Tamil Nadu"] if is_tn_only else ["ALL"]

    # 2. Gender / Women Quota
    is_women_only = (
        any(w in s_name for w in ["women", "mahila", "nari", "twees", "tread"]) or
        "women entrepreneur" in s_name or
        "for women" in s_name or
        ("women" in s_brief and "only" in s_brief)
    )
    mandatory_women_equity_pct = 51.0 if is_women_only else 0.0

    # 3. Social Category Quota (SC / ST / OBC)
    is_sc_st_only = any(x in s_name for x in ["sc/st", "sc-st", "tribal", "stand up india", "annasaheb"]) or "sc/st" in s_brief
    target_categories = ["SC", "ST"] if is_sc_st_only else []

    # 4. Sector Applicability
    sectors = scheme.get("sectors") or []
    if isinstance(sectors, str):
        import json
        try: sectors = json.loads(sectors)
        except Exception: sectors = [sectors]
    sectors_lower = [str(x).lower() for x in sectors]

    is_all_sectors = any(x in sectors_lower for x in ["all sectors", "cross-sector", "cross-sector / all sectors", "any"]) or not sectors_lower
    
    # 5. Development Stage Applicability
    s_stage = (scheme.get("stage") or "all").lower()
    if any(x in s_stage for x in ["all", "agnostic", "multi"]):
        allowed_stages = ["ALL"]
    else:
        allowed_stages = [x.strip() for x in s_stage.split("/") if x.strip()]

    # 6. Registrations Mandatory
    mandatory_registrations = []
    if "dpiit" in s_desc or "dpiit" in s_name or "startup india" in s_agency:
        mandatory_registrations.append("dpiit")
    if "startuptn" in s_agency or "tanseed" in s_name:
        mandatory_registrations.append("startuptn")
    if "udyam" in s_desc or "msme" in s_agency:
        mandatory_registrations.append("udyam")

    # 7. Quantum Limits
    min_lakhs, max_lakhs = parse_quantum_limits(amt_str)

    # 8. Primary Support Goal Tagging
    if "grant" in fund_type or "subsidy" in fund_type or "tanseed" in s_name or "pmfme" in s_name or "uyegp" in s_name:
        primary_goal = "Capital Grant / Seed Subsidy"
    elif "loan" in fund_type or "debt" in fund_type or "mudra" in s_name or "cgtmse" in s_name or "tiic" in s_name:
        primary_goal = "Subsidized Debt / Term Loan / Working Capital"
    elif "equity" in fund_type or "angel" in fund_type or "venture" in fund_type or "seed fund" in fund_type:
        primary_goal = "Equity Investment / Angel / Seed Fund"
    elif "r&d" in fund_type or "ivp" in s_name or "innovation" in s_name:
        primary_goal = "R&D / Prototype / Product Development"
    elif "export" in fund_type or "market" in fund_type or "gem" in s_name:
        primary_goal = "Market Access / Export / Trade Promotion"
    else:
        primary_goal = "Capital Grant / Seed Subsidy"

    return {
        "scheme_id": scheme.get("id") or scheme.get("source_id"),
        "allowed_states": allowed_states,
        "is_tn_only": is_tn_only,
        "is_women_only": is_women_only,
        "mandatory_women_equity_pct": mandatory_women_equity_pct,
        "is_sc_st_only": is_sc_st_only,
        "target_categories": target_categories,
        "is_all_sectors": is_all_sectors,
        "sectors": sectors_lower,
        "allowed_stages": allowed_stages,
        "mandatory_registrations": mandatory_registrations,
        "min_lakhs": min_lakhs,
        "max_lakhs": max_lakhs,
        "primary_goal": primary_goal,
        "funding_type": fund_type
    }
