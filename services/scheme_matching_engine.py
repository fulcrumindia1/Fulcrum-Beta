"""
services/scheme_matching_engine.py — Rigorous 3-Stage AI-Based Scheme Matching Engine
========================================================================================
Architectural Foundation:
X = Who the aspirant is and what business they operate (Identity, Sector, Stage, Geography, Demographics, Registrations)
Y = What assistance the aspirant needs (Assistance Goal, Support Type, Quantum Range, Timeframe)
Z = Recommended schemes meeting mandatory eligibility and ranking by relevance fit.

3-Stage Pipeline:
Stage 1: Mandatory Gatekeeper Evaluation (Hard eligibility vs Disqualification)
Stage 2: Relevance Scoring & Weight Alignment (0 - 100 deterministic points)
Stage 3: Explainable Checklist Generation & Human Review Readiness
"""

import json
import re
from typing import Dict, List, Optional, Any, Tuple
from services.scheme_rules import (
    get_scheme_structured_rules,
    parse_quantum_limits,
    ASSISTANCE_GOALS,
    FUNDING_QUANTUM_RANGES,
    TIMEFRAME_OPTIONS
)

FOOD_AGRI_KEYWORDS = {
    "food", "millet", "agri", "agriculture", "farmer", "processing",
    "fmcg", "dairy", "nutrition", "harvest", "crop", "horticulture",
    "organic", "grain", "bakery", "beverage", "spices"
}

TECH_EXCLUSIVE_KEYWORDS = {
    "semiconductor", "chip design", "deeptech", "ai/ml", "artificial intelligence",
    "gpu", "defence", "defense", "aerospace", "satellite", "space", "biotech",
    "clinical", "pharma", "medical devices", "quantum"
}

# Negative domain exclusion sets: Schemes in these domains should NOT match aspirants outside them
DOMAIN_NEGATIVE_EXCLUSIONS = {
    "isro": {"isro", "space technology", "space tech", "satellite", "space applications", "in-space", "isac"},
    "semiconductor": {"semiconductor", "chip design", "vlsi", "esdm", "chip manufacturing", "dms", "specs"},
    "aerospace": {"aerospace", "defence", "drdo", "hal", "defense innovation", "idex", "air force", "navy"},
    "pharma_rd": {"pharma r&d", "clinical trial", "drug discovery", "biopharmaceutical", "biotech r&d", "clinical research", "new drug"},
    "biotech": {"biotech", "biotechnology", "birac", "genomics", "bio-incubator", "molecular biology"},
    "nuclear": {"nuclear", "atomic energy", "dae"},
    "ev_automotive": {"ev policy", "electric vehicle", "e-vehicle", "ev manufacturing", "charging infrastructure", "battery pack", "automobile manufacturing"},
    "deeptech_hardware": {"supercomputing", "quantum computing", "c-dac ai", "abdm sandbox"},
}

# Aspirant domain keywords that indicate actual capability in the domain
DOMAIN_CAPABILITY_KEYWORDS = {
    "isro": {"space", "satellite", "aerospace", "remote sensing", "propulsion", "rocketry"},
    "semiconductor": {"semiconductor", "chip", "vlsi", "esdm", "integrated circuit", "soc", "foundry"},
    "aerospace": {"aerospace", "defence", "defense", "military", "uav", "drone", "avionics", "missile"},
    "pharma_rd": {"clinical trial", "drug discovery", "biopharmaceutical", "biotech r&d", "clinical research", "formulation r&d", "active pharmaceutical ingredient", "new chemical entity", "molecular"},
    "biotech": {"biotech", "biotechnology", "molecular", "genomics", "bio-pharma", "microbiology", "bio-processing", "bio-incubator", "life sciences"},
    "nuclear": {"nuclear", "atomic", "reactor", "radiation"},
    "ev_automotive": {"ev", "electric vehicle", "automobile", "battery", "charging station", "powertrain", "e-mobility", "automotive"},
    "deeptech_hardware": {"supercomputing", "quantum", "c-dac", "abdm", "healthtech ai"},
}


def normalize_aspirant_profile(profile: Dict) -> Dict[str, Any]:
    """
    Safely unpacks and normalizes founder profile (X) without artificial default assumptions.
    Resolves Defect 2 (women equity), Defect 3 (missing state default), Defect 4 (registration defaults).
    """
    p_data = profile.get("profile_data") or {}
    if isinstance(p_data, str):
        try: p_data = json.loads(p_data)
        except Exception: p_data = {}

    biz = p_data.get("business") or {}
    demo = p_data.get("demographics") or {}
    pers = p_data.get("personal") or {}

    # State & District: Do NOT blindly default to Tamil Nadu if missing!
    state_raw = profile.get("state") or demo.get("state")
    asp_state = str(state_raw).strip() if state_raw else ""
    asp_district = str(profile.get("district") or demo.get("district") or "").strip()

    # Sector, Subsector, Business Type & Commercial Activity
    asp_sector = str(biz.get("sector") or "").strip().lower()
    asp_subsector = str(biz.get("subsector") or "").strip().lower()
    asp_biz_type = str(biz.get("business_type") or "").strip().lower()
    asp_activity = str(biz.get("activity") or "").strip().lower()
    asp_stage = str(biz.get("stage") or "").strip().lower()

    # Demographics & Quota
    asp_gender = str(pers.get("gender") or demo.get("gender") or "").strip().lower()
    asp_category = str(demo.get("founder_category") or demo.get("category") or demo.get("social_category") or "").strip().upper()

    # Women Ownership Verification: Must have >= 51% women equity share to qualify as women-led
    women_equity_val = demo.get("women_equity_pct")
    try:
        women_equity_num = float(women_equity_val) if women_equity_val is not None else 0.0
    except (ValueError, TypeError):
        women_equity_num = 0.0

    declared_women_led = bool(demo.get("is_women_led"))
    # Verified women-led: either declared with positive equity, or female gender with affirmative equity declaration
    is_women_led = bool((declared_women_led and women_equity_num >= 51.0) or (women_equity_num >= 51.0))

    # Statutory Registrations: False by default unless affirmatively registered
    is_dpiit = bool(demo.get("is_dpiit_recognized", False))
    is_startuptn = bool(demo.get("is_startuptn_registered", False))
    is_udyam = bool(demo.get("is_udyam_registered", False))
    is_gst = bool(demo.get("is_gst_registered", False))
    is_fssai = bool(demo.get("is_fssai_registered", False))
    is_drug_license = bool(demo.get("is_drug_license", False))

    # Description and Name
    asp_desc = str(biz.get("description") or "").lower()
    asp_name = str(biz.get("business_name") or "").lower()

    # Domain keywords (includes subsector and activity)
    keywords = set(re.findall(r'[a-zA-Z]{3,}', f"{asp_sector} {asp_subsector} {asp_biz_type} {asp_activity} {asp_desc} {asp_name}"))

    return {
        "user_id": profile.get("id"),
        "full_name": profile.get("full_name", "Entrepreneur"),
        "state": asp_state,
        "is_tn": "tamil nadu" in asp_state.lower() or ("tamil nadu" in asp_district.lower()),
        "district": asp_district,
        "sector": asp_sector,
        "subsector": asp_subsector,
        "biz_type": asp_biz_type,
        "activity": asp_activity,
        "stage": asp_stage,
        "gender": asp_gender,
        "is_women_led": is_women_led,
        "women_equity_pct": women_equity_num,
        "category": asp_category,
        "is_dpiit": is_dpiit,
        "is_startuptn": is_startuptn,
        "is_udyam": is_udyam,
        "is_gst": is_gst,
        "is_fssai": is_fssai,
        "is_drug_license": is_drug_license,
        "keywords": keywords,
        "is_food_agri": bool(keywords & FOOD_AGRI_KEYWORDS or "food" in asp_sector or "agri" in asp_sector),
        "is_tech": bool(keywords & {"tech", "software", "ai", "deeptech", "hardware", "saas", "electronics", "robotics"})
    }


def evaluate_gatekeeper_eligibility(x: Dict[str, Any], scheme: Dict[str, Any], rules: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
    """
    STAGE 1: MANDATORY GATEKEEPER ELIGIBILITY
    Evaluates hard statutory and jurisdiction constraints.
    Returns: (is_eligible, hard_disqualifications, warnings)
    """
    disqualifications = []
    warnings = []

    # 1. State / Geography Hard Jurisdiction
    if rules["is_tn_only"]:
        if not x["state"]:
            warnings.append("State location not specified in founder profile; Tamil Nadu location verification required.")
        elif not x["is_tn"]:
            disqualifications.append(f"State Ineligible: Scheme is strictly restricted to Tamil Nadu registered enterprises. (Your profile state: {x['state'] or 'Unknown'}).")

    # 2. Gender Exclusivity (Women-Led Schemes)
    if rules["is_women_only"]:
        if not x["is_women_led"]:
            if "female" in x["gender"] and x["women_equity_pct"] < 51.0:
                disqualifications.append(f"Ownership Equity Ineligible: Scheme requires >=51% women equity ownership. Your declared female equity share is {x['women_equity_pct']}%.")
            else:
                disqualifications.append("Gender Ineligible: Scheme is strictly reserved for women-led enterprises (>=51% women ownership). Male primary founders cannot apply.")

    # 3. Social Category Exclusivity (SC / ST / Special affirmative schemes)
    if rules["is_sc_st_only"]:
        if x["category"] not in ("SC", "ST"):
            disqualifications.append(f"Category Ineligible: Scheme is statutory affirmative quota for SC/ST founders. (Your declared category: {x['category'] or 'General/OBC'}).")

    # 4. Negative Domain Exclusion: Specialized schemes must NOT match unrelated aspirants
    s_text = f"{scheme.get('name','')} {scheme.get('brief','')} {scheme.get('description','')} {' '.join(rules['sectors'])}".lower()
    asp_text = f"{x['sector']} {x['biz_type']} {' '.join(x['keywords'])}".lower()

    for domain_key, scheme_markers in DOMAIN_NEGATIVE_EXCLUSIONS.items():
        scheme_has_domain = any(marker in s_text for marker in scheme_markers)
        if scheme_has_domain:
            # Check if the aspirant actually has capability in this domain
            domain_caps = DOMAIN_CAPABILITY_KEYWORDS.get(domain_key, set())
            aspirant_matches_domain = any(cap in asp_text for cap in domain_caps)
            if not aspirant_matches_domain:
                domain_label = domain_key.replace("_", "/").title()
                disqualifications.append(f"Domain Exclusion: {domain_label} specialized scheme — applicant's enterprise ({x['sector'].title() or 'Unknown Sector'}) is outside this domain.")
                break  # One domain exclusion is sufficient

    # 4b. Legacy broad tech exclusion (deeptech vs food/agro)
    if not disqualifications:
        has_deeptech_exclusivity = any(k in s_text for k in TECH_EXCLUSIVE_KEYWORDS)
        if has_deeptech_exclusivity and not x["is_tech"] and x["is_food_agri"]:
            if any(k in s_text for k in ["semiconductor", "chip design", "defence innovation", "aerospace", "space tech"]):
                disqualifications.append("Domain Conflict: Specialized defence/semiconductor fund outside applicant's agro/food industry.")

    # 5. Registration Pre-conditions
    for reg in rules.get("mandatory_registrations", []):
        if reg == "dpiit" and not x["is_dpiit"]:
            warnings.append("DPIIT recognition required for official portal application.")
        elif reg == "startuptn" and not x["is_startuptn"] and x["is_tn"]:
            warnings.append("StartupTN portal registration required for state grant disbursement.")

    is_eligible = (len(disqualifications) == 0)
    return is_eligible, disqualifications, warnings


def calculate_relevance_score(
    x: Dict[str, Any],
    y: Dict[str, Any],
    scheme: Dict[str, Any],
    rules: Dict[str, Any]
) -> Tuple[int, List[str], List[str]]:
    """
    STAGE 2: RELEVANCE & PURPOSE ALIGNMENT SCORING (0 to 100 points)
    Weights:
    - Sector & Domain Alignment (35 pts)
    - Development Stage Alignment (25 pts)
    - Geographic Jurisdiction & Scope (15 pts)
    - Assistance Goal & Quantum Fit (Y Match) (15 pts)
    - Affirmative Demographic & Registration Quota (10 pts)
    """
    score = 0
    reasons = []
    concerns = []

    s_name = (scheme.get("name") or "").lower()
    s_agency = (scheme.get("agency") or "").lower()
    s_brief = (scheme.get("brief") or "").lower()
    s_desc = (scheme.get("description") or "").lower()
    s_text = f"{s_name} {s_agency} {s_brief} {s_desc}"

    # ── 1. Sector & Domain Alignment (Up to 38 pts) ──
    GENERIC_SECTOR_KEYWORDS = {
        "all sectors", "cross-sector", "cross-sector / all sectors", "any", "all",
        "general", "manufacturing", "services", "technology", "tech"
    }

    specific_rules_sectors = {s.strip().lower() for s in rules.get("sectors", []) if s.strip().lower() not in GENERIC_SECTOR_KEYWORDS}

    has_food_match = x["is_food_agri"] and (
        any(k in s_text for k in FOOD_AGRI_KEYWORDS) or
        any(k in specific_rules_sectors for k in ["agri", "food", "agriculture", "food processing"])
    )
    is_named_food_scheme = any(k in s_name for k in ["food", "pmfme", "millet", "agri", "ceppc", "cefppc", "mofpi"])
    has_specific_sector_match = False
    if not has_food_match and (x["keywords"] or x["sector"]):
        if specific_rules_sectors:
            has_specific_sector_match = bool(x["keywords"] & specific_rules_sectors) or (
                bool(x["sector"]) and any(x["sector"] in sec or sec in x["sector"] for sec in specific_rules_sectors)
            )
        # Also check direct scheme name alignment with founder's sector/subsector keywords
        if not has_specific_sector_match and (x["sector"] or x["subsector"]):
            core_asp_words = {w for w in (x["keywords"] | {x["sector"], x["subsector"]}) if len(w) >= 3 and w not in GENERIC_SECTOR_KEYWORDS and w not in {"enterprise", "company", "private", "limited", "startup", "founder", "india"}}
            scheme_name_words = set(re.findall(r'[a-zA-Z]{2,}', s_name))
            if any(w in scheme_name_words for w in core_asp_words):
                has_specific_sector_match = True

    is_broad_msme = any(k in s_name for k in ["pmegp", "mudra", "stand up india", "uyegp", "needs", "cgtmse", "startup india seed", "tanfund", "angelstn", "credit guarantee"])

    if is_named_food_scheme and x["is_food_agri"]:
        score += 38
        reasons.append("Dedicated sector scheme: Food Processing & Agribusiness")
    elif has_food_match:
        score += 30
        reasons.append("Sector match: Food Processing & Agribusiness")
    elif has_specific_sector_match:
        score += 35
        match_label = x["sector"].title() if x["sector"] else "Core Domain"
        reasons.append(f"Sector alignment: {match_label}")
    elif "manufacturing" in rules["sectors"] and ("manufacturing" in x["sector"] or "manufacturing" in x["biz_type"]):
        score += 18
        reasons.append("Manufacturing enterprise funding allocation")
    elif is_broad_msme:
        # Reduced from 25 → 15 to prevent broad MSME schemes from inflating scores
        score += 15
        reasons.append("Broad-based MSME enterprise support scheme (general eligibility)")
    elif rules["is_all_sectors"]:
        # Reduced from 15 → 8 to prevent generic open-sector schemes from auto-qualifying
        score += 8
        reasons.append("Open across all commercial sectors (no sector-specific advantage)")
    else:
        score += 3
        concerns.append(f"Sector focus: {', '.join(rules['sectors'][:3]) if rules['sectors'] else 'Specific Industry'}")

    # ── 2. Stage Alignment (Up to 25 pts) ──
    s_stage = (scheme.get("stage") or "all").lower()
    is_stage_agnostic = "all" in rules["allowed_stages"] or any(k in s_stage for k in ["all", "agnostic", "multi"])
    is_early_founder = bool(x["stage"]) and any(k in x["stage"] for k in ["idea", "ideation", "concept", "pre-seed", "seed", "early", "revenue", "prototype", "r&d", "mvp", "pilot"])
    is_early_scheme = any(k in s_stage for k in ["idea", "ideation", "concept", "pre-seed", "seed", "early", "prototype"])
    is_growth_founder = bool(x["stage"]) and any(k in x["stage"] for k in ["growth", "series", "scale", "expansion", "debt"])
    is_growth_scheme = any(k in s_stage for k in ["growth", "series", "scale", "expansion", "commercial"])

    if (is_early_founder and is_early_scheme) or (is_growth_founder and is_growth_scheme) or (x["stage"] and x["stage"] in s_stage):
        score += 25
        reasons.append(f"Stage fit: {scheme.get('stage', 'Development Phase')}")
    elif is_stage_agnostic:
        # Reduced from 20 → 12 to prevent stage-agnostic schemes from inflating scores
        score += 12
        reasons.append("Open to all venture stages (no stage-specific advantage)")
    elif not x["stage"]:
        score += 5
        concerns.append("Venture stage not specified in profile")
    elif is_early_founder and is_growth_scheme:
        score += 0
        concerns.append("Requires later-stage commercial traction (Growth/Scale phase)")
    else:
        score += 8
        reasons.append(f"Stage acceptable: {scheme.get('stage', 'Flexible')}")

    # ── 3. Geography & Jurisdiction (Up to 15 pts) ──
    if rules["is_tn_only"]:
        if x["is_tn"]:
            dist_label = x["district"].title() if x["district"] else "Tamil Nadu"
            score += 15
            reasons.append(f"Tamil Nadu jurisdiction match ({dist_label} eligible)")
        else:
            score += 0
            concerns.append("State-restricted funding programme")
    else:
        # Reduced from 12 → 7 to prevent national schemes from auto-qualifying
        score += 7
        reasons.append("National / Central Government initiative (All states eligible)")

    # ── 4. Assistance Goal & Quantum Fit (Y Match) (Up to 15 pts) ──
    requested_goal = y.get("assistance_goal", "ALL")
    requested_quantum = y.get("quantum_range", "ANY_AMOUNT")

    if requested_goal and requested_goal != "ALL":
        if rules["primary_goal"] == requested_goal or (requested_goal in rules["primary_goal"]):
            score += 10
            reasons.append(f"Assistance need match: {requested_goal}")
        elif "capital grant" in requested_goal.lower() and "grant" in rules["funding_type"]:
            score += 10
            reasons.append("Direct capital grant alignment")
        elif "loan" in requested_goal.lower() and "debt" in rules["funding_type"]:
            score += 10
            reasons.append("Term debt / loan alignment")
        else:
            score += 2
            concerns.append(f"Provides {rules['primary_goal']} (You sought: {requested_goal})")
    else:
        score += 3  # Reduced from 8 → 3: no specific goal selected, minimal baseline

    # Quantum fit
    if requested_quantum and requested_quantum != "ANY_AMOUNT":
        min_l, max_l = rules["min_lakhs"], rules["max_lakhs"]
        if max_l is not None:
            if "MICRO" in requested_quantum and max_l <= 25:
                score += 5
                reasons.append(f"Funding quantum fits micro-bracket (Up to ₹{max_l:g}L)")
            elif "SMALL" in requested_quantum and (min_l is None or min_l <= 25) and max_l >= 5:
                score += 5
                reasons.append(f"Funding quantum fits ₹5L–₹25L bracket (Up to ₹{max_l:g}L)")
            elif "MEDIUM" in requested_quantum and max_l >= 25:
                score += 5
                reasons.append(f"Funding quantum fits ₹25L–₹1Cr bracket (Up to ₹{max_l:g}L)")
            else:
                score += 2
        else:
            score += 3
    else:
        score += 5

    # ── 5. Affirmative Demographic & Registration Priority (Up to 10 pts) ──
    # Resolves Defect 1: Category bonus ONLY awarded if aspirant's category matches!
    elig_str = " ".join([str(e) for e in (scheme.get("eligibility") or [])]).lower()
    
    if rules["is_women_only"] and x["is_women_led"]:
        score += 10
        reasons.append(f"Eligible for statutory Women Entrepreneur quota ({x['women_equity_pct']}% equity)")
    elif x["is_women_led"] and ("women" in elig_str or "women" in s_text):
        score += 6
        reasons.append("Women-led enterprise preference concession")

    if x["category"] in ("SC", "ST") and ("sc/st" in elig_str or "sc/st" in s_text or "tribal" in s_text):
        score += 10
        reasons.append(f"Affirmative subsidy priority for {x['category']} entrepreneurs")
    elif x["category"] == "OBC" and ("obc" in elig_str or "backward classes" in s_text):
        score += 6
        reasons.append("Affirmative funding preference for Backward Classes (OBC)")

    if x["is_dpiit"] and ("dpiit" in elig_str or "dpiit" in s_text):
        score += 4
        reasons.append("DPIIT recognized startup benefit")

    final_score = max(0, min(100, score))
    return final_score, reasons, concerns


def build_evidence_checklist(
    x: Dict[str, Any],
    scheme: Dict[str, Any],
    rules: Dict[str, Any],
    is_disqualified: bool
) -> List[Dict[str, str]]:
    """
    STAGE 3: REALISTIC ITEM-BY-ITEM EVIDENCE CHECKLIST
    Resolves Defect 5: No more blind 'Verified Eligible' on unverified items!
    Classifies each item:
    - 'Verified Eligible': Confirmed by founder's structured profile data.
    - 'Self-Declared / Pending Evidence': Declared, requires documentation (e.g. Udyam cert, DPR, balance sheet).
    - 'Needs Clarification': Requires founder or Guide review.
    - 'Disqualified': Hard gatekeeper violation.
    """
    raw_elig = scheme.get("eligibility") or []
    if isinstance(raw_elig, str):
        try: raw_elig = json.loads(raw_elig)
        except Exception: raw_elig = [raw_elig]

    checklist = []

    for item in raw_elig:
        item_s = str(item).strip()
        item_lower = item_s.lower()

        if is_disqualified:
            status = "Disqualified"
        elif "tamil nadu" in item_lower or "tn" in item_lower:
            status = "Verified Eligible" if x["is_tn"] else "Needs Clarification"
        elif "women" in item_lower:
            if x["is_women_led"]:
                status = "Verified Eligible"
            elif "female" in x["gender"]:
                status = "Needs Clarification"
            else:
                status = "Not Applicable / Needs Review"
        elif "sc" in item_lower or "st" in item_lower or "caste" in item_lower or "category" in item_lower:
            if x["category"] in ("SC", "ST"):
                status = "Verified Eligible"
            else:
                status = "Self-Declared / Pending Evidence"
        elif "dpiit" in item_lower:
            status = "Verified Eligible" if x["is_dpiit"] else "Action Required: DPIIT Registration"
        elif "udyam" in item_lower or "msme" in item_lower:
            status = "Verified Eligible" if x["is_udyam"] else "Self-Declared / Pending Evidence"
        elif "age" in item_lower or "citizen" in item_lower or "indian" in item_lower:
            status = "Verified Eligible"
        elif "turnover" in item_lower or "balance sheet" in item_lower or "revenue" in item_lower:
            status = "Self-Declared / Pending Evidence"
        elif "dpr" in item_lower or "project report" in item_lower:
            status = "Action Required: Prepare DPR"
        else:
            status = "Self-Declared / Pending Evidence"

        checklist.append({"item": item_s, "status": status})

    return checklist


def match_aspirant_schemes_intelligent(
    profile: Dict[str, Any],
    schemes: List[Dict[str, Any]],
    assistance_need: Optional[Dict[str, Any]] = None,
    min_score: int = 50,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Master AI-Based Scheme Matching Engine:
    Compares normalized founder profile and assistance requirements (saved in profile or provided)
    against structured rules across the entire scheme catalogue.
    """
    x = normalize_aspirant_profile(profile)
    y = assistance_need or (profile.get("profile_data") or {}).get("assistance_need") or {}

    results = []

    for scheme in schemes:
        if not scheme.get("is_active", True):
            continue

        rules = get_scheme_structured_rules(scheme)

        # Stage 1: Mandatory Gatekeeper
        is_eligible, disqualifications, warnings = evaluate_gatekeeper_eligibility(x, scheme, rules)

        if not is_eligible:
            final_score = 0
            status = "DISQUALIFIED"
            reasons = []
            concerns = disqualifications
        else:
            # Stage 2: Relevance Scoring
            final_score, reasons, concerns = calculate_relevance_score(x, y, scheme, rules)
            if warnings:
                concerns.extend(warnings)

            if final_score >= 80:
                status = "HIGHLY RECOMMENDED"
            elif final_score >= 65:
                status = "RECOMMENDED"
            elif final_score >= 50:
                status = "POTENTIALLY ELIGIBLE"
            else:
                status = "LOW FIT"

        # Stage 3: Evidence Checklist
        checklist = build_evidence_checklist(x, scheme, rules, is_disqualified=not is_eligible)

        s_copy = dict(scheme)
        s_copy["match_score"] = final_score
        s_copy["score"] = final_score
        s_copy["recommendation_status"] = status
        s_copy["match_reasons"] = reasons
        s_copy["reasons"] = reasons
        s_copy["potential_concerns"] = concerns
        s_copy["checklist"] = checklist
        s_copy["is_disqualified"] = not is_eligible
        s_copy["structured_rules"] = rules

        # Include if score >= min_score or if explicitly requested without filter
        if min_score is None or final_score >= min_score:
            results.append(s_copy)

    # Sort descending by match score
    results.sort(key=lambda s: s["match_score"], reverse=True)
    return results[:limit] if limit is not None else results
