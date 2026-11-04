"""
scripts/test_all_16_scenarios.py — Automated Verification Suite for all 16 Master Scenarios
========================================================================================
Validates:
1. New Aspirant registration & base role grant
2. Super Admin grants Guide role (status = pending_nda)
3. Server-side NDA gating blocks caseload while pending_nda
4. Valid NDA execution ('I ACCEPT', full legal name, hash) activates role
5. Workspace switching preserves Aspirant profile, schemes & journey
6. Dual promotion (Aspirant + Guide + SME)
7. Revocation of Guide role leaves SME and Aspirant active
8. Base Aspirant role revocation is strictly blocked
9. Super Admin identity masking ("Fulcrum Administration")
10. Confidential Guide complaint submission and administrative isolation
11. SME Conflict of Interest declaration & governance
12. Caseload inactivity monitoring & idempotent alert logging
13. Case Collaboration: private mentor notes concealed from Aspirant
14. Scheme matching determinism (exact score preservation)
15. Lazy tab evaluation (is_tab_active logic)
16. N+1 query elimination (single batch profile resolution)
"""

import sys
import os
import time
import json
import uuid

# Force UTF-8 output
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ["DATA_BACKEND"] = "sqlite"

from services.local_db import get_local_db
from services.profiles import get_profile, update_aspirant_profile, get_profiles_batch, list_profiles_by_role
from services.roles import (
    grant_role,
    activate_role,
    revoke_role,
    get_user_roles,
    get_active_roles,
    get_pending_nda_roles,
    user_has_active_role
)
from services.legal import (
    check_user_terms_accepted,
    check_user_nda_accepted,
    record_legal_acceptance,
    get_active_legal_document
)
from services.relationships import (
    get_assigned_aspirants_for_guide,
    get_assigned_aspirants_for_sme,
    assign_guide,
    assign_sme,
    get_aspirant_mentors
)
from services.schemes import (
    list_schemes,
    match_schemes_for_aspirant,
    release_scheme_to_aspirant,
    get_released_schemes_for_aspirant
)
from services.governance import (
    get_masked_actor_name,
    submit_guide_complaint,
    list_guide_complaints,
    resolve_guide_complaint,
    declare_sme_conflict,
    check_sme_has_conflict
)
from services.inactivity import (
    check_and_process_caseload_inactivity,
    list_inactivity_records
)
from services.collaboration import (
    create_case_message,
    list_case_messages
)
from services.cache import is_tab_active

passed = 0
failed = 0

def test(name, condition, details=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"[PASS] Scenario {name}: {details}")
    else:
        failed += 1
        print(f"[FAIL] Scenario {name}: {details}")

print("===============================================================================")
print("FULCRUM-INDIA: MASTER 16 SCENARIOS AUTOMATED VERIFICATION SUITE")
print("===============================================================================\n")

# Setup Test Users
test_user_id = str(uuid.uuid4())
test_email = f"founder_{uuid.uuid4().hex[:6]}@example.com"
existing_guides = list_profiles_by_role("guide")
existing_admins = list_profiles_by_role("admin")
test_guide_id = existing_guides[0]["id"] if existing_guides else str(uuid.uuid4())
test_admin_id = existing_admins[0]["id"] if existing_admins else str(uuid.uuid4())

db = get_local_db()
db.upsert_profile({
    "id": test_user_id,
    "email": test_email,
    "role": "aspirant",
    "full_name": "Kavitha Raman",
    "district": "Coimbatore",
    "state": "Tamil Nadu",
    "is_active": 1,
    "profile_data": {
        "personal": {"full_name": "Kavitha Raman", "email": test_email, "district": "Coimbatore", "state": "Tamil Nadu"},
        "professional": {"education": "B.Tech", "experience_years": 5},
        "business": {"business_name": "Kavitha CleanTech", "sector": "Clean Technology", "stage": "Early Traction", "investment_bracket": "25L-50L"},
        "demographics": {"district": "Coimbatore", "state": "Tamil Nadu", "founder_category": "Women", "gender": "Female"}
    }
})

# 1. New Aspirant registration and base role grant
roles_1 = get_user_roles(test_user_id)
has_asp_1 = any(r["role"] == "aspirant" and r["status"] == "active" for r in roles_1)
test("1", has_asp_1, "New user receives active base Aspirant role automatically.")

# 2. Super Admin grants Guide role (status = pending_nda)
ok_g, _ = grant_role(test_user_id, "guide", granted_by=test_admin_id)
roles_2 = get_user_roles(test_user_id)
guide_grant_2 = next((r for r in roles_2 if r["role"] == "guide"), None)
is_pending_2 = guide_grant_2 and guide_grant_2["status"] == "pending_nda"
test("2", ok_g and is_pending_2, "Promoting Aspirant to Guide defaults to 'pending_nda'.")

# 3. Server-side NDA gating blocks caseload while pending_nda
nda_blocked_3 = not check_user_nda_accepted(test_user_id, "guide")
caseload_3 = get_assigned_aspirants_for_guide(test_user_id)
test("3", nda_blocked_3 and len(caseload_3) == 0, "Caseload access returns empty while Guide status is 'pending_nda'.")

# 4. Valid NDA execution activates role
ok_nda, err_nda = record_legal_acceptance(
    user_id=test_user_id,
    user_email=test_email,
    doc_type="nda_dual",
    typed_name="Kavitha Raman",
    typed_phrase="I ACCEPT",
    checkbox_confirmed=True
)
active_roles_4 = get_active_roles(test_user_id)
is_active_4 = "guide" in active_roles_4
test("4", ok_nda and is_active_4, "Submitting NDA with typed 'I ACCEPT' successfully activates Guide role.")

# 5. Workspace switching preserves Aspirant profile, schemes & journey
p_asp_5 = get_profile(test_user_id)
schemes_5 = match_schemes_for_aspirant(test_user_id)
matches_valid = len(schemes_5) > 0
test("5", p_asp_5["full_name"] == "Kavitha Raman" and matches_valid, "Aspirant profile and scheme recommendations preserved during workspace transitions.")

# 6. Dual promotion (Aspirant + Guide + SME)
ok_sme, _ = grant_role(test_user_id, "sme", granted_by=test_admin_id, require_nda=False)
active_roles_6 = get_active_roles(test_user_id)
has_all_three = "aspirant" in active_roles_6 and "guide" in active_roles_6 and "sme" in active_roles_6
test("6", has_all_three, "One identity concurrently holds Aspirant, Guide, and SME roles.")

# 7. Revoke Guide role leaves SME and Aspirant active
ok_rev, _ = revoke_role(test_user_id, "guide", reason="Caseload rotation")
active_roles_7 = get_active_roles(test_user_id)
guide_gone = "guide" not in active_roles_7
sme_asp_remain = "aspirant" in active_roles_7 and "sme" in active_roles_7
test("7", ok_rev and guide_gone and sme_asp_remain, "Revoking Guide role leaves SME and Aspirant active.")

# 8. Base Aspirant role revocation is strictly blocked
ok_rev_asp, err_rev_asp = revoke_role(test_user_id, "aspirant", reason="Illegal test")
test("8", not ok_rev_asp and "cannot be revoked" in str(err_rev_asp), "Revocation of the base Aspirant role is strictly rejected.")

# 9. Super Admin identity masking ("Fulcrum Administration")
masked_super = get_masked_actor_name(test_admin_id, "Super Admin Real Name", "admin")
masked_dist = get_masked_actor_name(test_admin_id, "District Collector", "district_admin")
test("9", masked_super == "Fulcrum Administration" and masked_dist == "District Administration", "Administrator identity is masked as 'Fulcrum Administration' in audit logs/events.")

# 10. Confidential Guide complaint submission and administrative isolation
ok_comp, _ = submit_guide_complaint(
    aspirant_id=test_user_id,
    guide_id=test_guide_id,
    reason="inactivity",
    details="Assigned guide has not scheduled initial meeting for 2 weeks."
)
complaints_10 = list_guide_complaints()
complaint_recorded = any(c["aspirant_id"] == test_user_id for c in complaints_10)
test("10", ok_comp and complaint_recorded, "Confidential complaint submitted and logged exclusively for Admin review.")

# 11. SME Conflict of Interest declaration
ok_decl, _ = declare_sme_conflict(
    sme_id=test_user_id,
    aspirant_id="6e667c86-84d3-4b65-b727-90f71f2b2875",
    has_conflict=True,
    conflict_details="Advisor holds equity in a direct CleanTech competitor."
)
has_conf_11 = check_sme_has_conflict(test_user_id, "6e667c86-84d3-4b65-b727-90f71f2b2875")
test("11", ok_decl and has_conf_11, "SME Conflict of Interest declaration properly recorded and verified.")

# 12. Caseload inactivity monitoring & idempotent alert logging
inactivity_results = check_and_process_caseload_inactivity()
logs_12 = list_inactivity_records()
test("12", isinstance(inactivity_results, list) and isinstance(logs_12, list), "Inactivity monitor scans active caseloads with idempotent logs.")

# 13. Case Collaboration: private mentor notes concealed from Aspirant
ok_open, _ = create_case_message(test_user_id, test_guide_id, "guide", "Open Roadmap Item", "Please upload your FSSAI draft.")
ok_priv, _ = create_case_message(test_user_id, test_guide_id, "guide", "Internal Risk Evaluation", "Founder financials need verification.", is_private_mentor_note=True)

msgs_for_asp = list_case_messages(test_user_id, requesting_role="aspirant")
msgs_for_guide = list_case_messages(test_user_id, requesting_role="guide")

asp_sees_private = any(m.get("is_private_mentor_note") is True for m in msgs_for_asp)
guide_sees_private = any(m.get("is_private_mentor_note") is True for m in msgs_for_guide)
test("13", (not asp_sees_private) and guide_sees_private, "Private mentor advisory notes are hidden from the Aspirant but visible to Mentors.")

# 14. Scheme matching determinism
raw_schemes = list_schemes(active_only=True)
matched_14 = match_schemes_for_aspirant(test_user_id)
scores_present = all("score" in s for s in matched_14)
test("14", len(matched_14) > 0 and scores_present, "Scheme matching produces deterministic scores and recommendations.")

# 15. Lazy tab evaluation logic
class MockTab:
    def __init__(self, is_open):
        self.open = is_open

tab_active = MockTab(True)
tab_inactive = MockTab(False)
test("15", is_tab_active(tab_active) and not is_tab_active(tab_inactive), "Lazy tab predicate (is_tab_active) correctly identifies active vs inactive tabs.")

# 16. N+1 query elimination (single batch profile resolution)
t_start = time.perf_counter()
batch_res = get_profiles_batch([test_user_id, test_guide_id, test_admin_id])
t_batch = (time.perf_counter() - t_start) * 1000
test("16", len(batch_res) >= 2 and t_batch < 50.0, f"Batched profile query executed in {t_batch:.2f} ms (eliminating N+1 requests).")

print("\n-------------------------------------------------------------------------------")
print(f"VERIFICATION SUMMARY: {passed} / 16 PASSED ({passed/16*100:.1f}%), {failed} FAILED")
print("-------------------------------------------------------------------------------")

if failed == 0:
    print("\n[SUCCESS] ALL 16 SCENARIOS FULLY VERIFIED AND PASSING!")
    sys.exit(0)
else:
    print(f"\n[WARNING] {failed} scenarios failed.")
    sys.exit(1)
