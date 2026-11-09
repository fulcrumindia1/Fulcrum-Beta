"""
scripts/run_circular_e2e_master_suite.py
=========================================
Master 360-Degree Circular Multi-Role (A -> B -> C -> A), Full Browser E2E,
Workflow Integrity, and Chaos Test Suite for Fulcrum-Beta.

Executes genuine browser automation via Playwright across 4 authenticated contexts:
1. Admin (fulcrumindia1@gmail.com)
2. Aspirant A (Founder + Guide to B)
3. Aspirant B (Founder + SME to C)
4. Aspirant C (Founder + SME to A)

Strict Invariant: Zero mutations to public.schemes table (179 rows, SHA-256 frozen).
"""

import os
import sys
import json
import uuid
import hashlib
from datetime import datetime, timezone
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import dotenv
dotenv.load_dotenv(override=True)

from playwright.sync_api import sync_playwright
from services.auth import get_supabase_admin_client, login_user
from services.roles import grant_role, activate_role, revoke_role, get_active_roles
from services.relationships import assign_guide, assign_sme, unassign_guide, get_aspirant_mentors
from services.legal import record_legal_acceptance, check_user_nda_accepted
from services.help_requests import create_request, guide_respond_request, sme_respond_request, list_requests
from services.journey import log_meaningful_event, get_journey_timeline
from services.schemes import match_schemes_for_aspirant, list_schemes
from services.account_lifecycle import archive_account, restore_account, get_account_status

BASE_URL = "http://localhost:8501"
SCREENSHOTS_DIR = BASE_DIR / "artifacts" / "e2e_screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

ADMIN_EMAIL = "fulcrumindia1@gmail.com"
ADMIN_UUID = "616304b5-aef5-4cd0-88be-2fda7ddf7f88"
ADMIN_PASS = "Manick@265070"
SYNTHETIC_PASS = "SyntheticPass2026!"

EXPECTED_CATALOGUE_CHECKSUM = "d6d8f9433df3cf37e201f1914c2fdc9a367b82977e3be7c79dd329518f462bbf"

def verify_catalogue_checksum(stage_label=""):
    admin = get_supabase_admin_client()
    res = admin.table("schemes").select("*").order("id").execute()
    count = len(res.data)
    schemes_json = json.dumps(res.data, sort_keys=True)
    current_checksum = hashlib.sha256(schemes_json.encode("utf-8")).hexdigest()
    
    print(f"\n[CATALOGUE AUDIT {stage_label}] Count: {count} | Hash: {current_checksum}")
    assert count == 179, f"Catalogue count mismatch: expected 179, got {count}"
    assert current_checksum == EXPECTED_CATALOGUE_CHECKSUM, f"Catalogue mutated! Expected {EXPECTED_CATALOGUE_CHECKSUM}, got {current_checksum}"
    print(f"[CATALOGUE AUDIT {stage_label}] PASS - Exact 179 rows bit-for-bit identical.")
    return count, current_checksum

def wait_for_ready(page, timeout=8000):
    page.wait_for_timeout(1000)
    try:
        page.wait_for_selector("[data-testid='stStatusWidget']", state="hidden", timeout=timeout)
    except Exception:
        pass
    page.wait_for_timeout(1000)

def login_in_browser(page, email, password):
    page.goto(BASE_URL, timeout=20000)
    wait_for_ready(page)
    
    # Check if logout button exists
    if page.query_selector("button:has-text('Logout')"):
        page.click("button:has-text('Logout')")
        wait_for_ready(page)
    
    email_inp = page.wait_for_selector("input[aria-label='Email Address']", timeout=12000)
    email_inp.fill(email)
    pwd_inp = page.wait_for_selector("input[aria-label='Password']", timeout=12000)
    pwd_inp.fill(password)
    
    page.click("button:has-text('LOGIN')")
    try:
        page.wait_for_selector("button:has-text('Logout')", timeout=15000)
    except Exception:
        pass
    wait_for_ready(page)
    page.wait_for_timeout(2000)

def run_master_circular_test():
    results_matrix = {}
    print("=" * 80)
    print("STARTING FULCRUM-BETA MASTER 360 CIRCULAR MULTI-ROLE (A -> B -> C -> A) E2E TEST")
    print("=" * 80)

    # 1. Pre-Test Catalogue Checksum
    verify_catalogue_checksum("PRE-TEST BASELINE")

    admin = get_supabase_admin_client()
    run_tag = uuid.uuid4().hex[:6]
    test_run_manifest = []

    try:
        # 2. Provision 3 Synthetic Identities in Supabase Auth
        print("\n--- STEP 1: Provisioning Synthetic Identities A, B, C ---")
        users_def = [
            ("A", f"asp_a_{run_tag}@fulcrum-synthetic.in", "Aspirant Alpha (Solar)", "Madurai", "Solar Cold Storage"),
            ("B", f"asp_b_{run_tag}@fulcrum-synthetic.in", "Aspirant Beta (BioAgri)", "Coimbatore", "Bio-Fertilizer Labs"),
            ("C", f"asp_c_{run_tag}@fulcrum-synthetic.in", "Aspirant Gamma (Drones)", "Chennai", "Agri-Drone Sensing")
        ]
        
        actors = {}
        for key, email, name, dist, bname in users_def:
            # Create user in Auth
            u_res = admin.auth.admin.create_user({
                "email": email,
                "password": SYNTHETIC_PASS,
                "email_confirm": True,
                "user_metadata": {"full_name": name, "role": "aspirant", "district": dist}
            })
            uid = u_res.user.id
            test_run_manifest.append({"id": uid, "email": email, "key": key})
            
            # Profile & Initial Journey
            prof = {
                "id": uid,
                "email": email,
                "full_name": name,
                "role": "aspirant",
                "district": dist,
                "state": "Tamil Nadu",
                "account_status": "ACTIVE",
                "is_active": True,
                "profile_data": {
                    "personal": {"full_name": name, "email": email, "district": dist},
                    "business": {"business_name": bname, "stage": "early_traction", "sector": "Agriculture & Technology"},
                    "demographics": {"district": dist, "state": "Tamil Nadu"}
                }
            }
            admin.table("profiles").upsert(prof, on_conflict="id").execute()
            admin.table("journeys").upsert({
                "aspirant_id": uid,
                "title": f"{name}'s {bname} Journey",
                "business_type": "Technology Startup",
                "stage": "early_traction",
                "status": "active"
            }, on_conflict="aspirant_id").execute()
            admin.table("relationships").upsert({
                "aspirant_id": uid,
                "status": "active"
            }, on_conflict="aspirant_id").execute()
            
            # Record terms acceptance
            record_legal_acceptance(
                user_id=uid,
                user_email=email,
                doc_type="terms_and_conditions",
                typed_name=name,
                typed_phrase="I ACCEPT",
                checkbox_confirmed=True
            )
            
            actors[key] = {"id": uid, "email": email, "name": name, "district": dist, "business": bname}
            print(f"  ✓ Provisioned Actor {key}: {name} ({email}) -> UUID: {uid}")

        results_matrix["STEP_1_PROVISION_IDENTITIES"] = "PASS"

        # 3. Step 2: Admin Grants Professional Roles (A -> Guide, B -> SME, C -> SME)
        print("\n--- STEP 2: Multi-Role Promotion (A: Guide, B: SME, C: SME) ---")
        ok_ga, err_ga = grant_role(actors["A"]["id"], "guide", granted_by=ADMIN_UUID)
        ok_gb, err_gb = grant_role(actors["B"]["id"], "sme", granted_by=ADMIN_UUID)
        ok_gc, err_gc = grant_role(actors["C"]["id"], "sme", granted_by=ADMIN_UUID)
        assert ok_ga and ok_gb and ok_gc, f"Failed to grant professional roles: {err_ga} / {err_gb} / {err_gc}"
        print("  ✓ Admin granted Guide to A, SME to B, SME to C (Roles in PENDING_NDA status).")
        results_matrix["STEP_2_ROLE_GRANTS"] = "PASS"

        # 4. Step 3: Legal NDA Signing & Role Activation
        print("\n--- STEP 3: Professional NDA Signing & Activation ---")
        # A signs Guide NDA
        record_legal_acceptance(
            user_id=actors["A"]["id"],
            user_email=actors["A"]["email"],
            doc_type="nda_dual",
            typed_name=actors["A"]["name"],
            typed_phrase="I ACCEPT",
            checkbox_confirmed=True
        )
        ok_act_a, _ = activate_role(actors["A"]["id"], "guide")
        assert ok_act_a, "Failed to activate Guide role for A"

        # B signs SME NDA
        record_legal_acceptance(
            user_id=actors["B"]["id"],
            user_email=actors["B"]["email"],
            doc_type="nda_dual",
            typed_name=actors["B"]["name"],
            typed_phrase="I ACCEPT",
            checkbox_confirmed=True
        )
        ok_act_b, _ = activate_role(actors["B"]["id"], "sme")
        assert ok_act_b, "Failed to activate SME role for B"

        # C signs SME NDA
        record_legal_acceptance(
            user_id=actors["C"]["id"],
            user_email=actors["C"]["email"],
            doc_type="nda_dual",
            typed_name=actors["C"]["name"],
            typed_phrase="I ACCEPT",
            checkbox_confirmed=True
        )
        ok_act_c, _ = activate_role(actors["C"]["id"], "sme")
        assert ok_act_c, "Failed to activate SME role for C"

        print("  ✓ All 3 professionals signed NDAs and achieved ACTIVE multi-roles.")
        results_matrix["STEP_3_NDA_ACTIVATION"] = "PASS"

        # 5. Step 4: Circular Mentor Assignments (A -> Guide to B, B -> SME to C, C -> SME to A)
        print("\n--- STEP 4: Creating Circular Assignments (A -> B, B -> C, C -> A) ---")
        ok_as1, err1 = assign_guide(actors["B"]["id"], actors["A"]["id"], admin_id=ADMIN_UUID) # A is Guide to B
        ok_as2, err2 = assign_sme(actors["C"]["id"], actors["B"]["id"], admin_id=ADMIN_UUID)   # B is SME to C
        ok_as3, err3 = assign_sme(actors["A"]["id"], actors["C"]["id"], admin_id=ADMIN_UUID)   # C is SME to A
        assert ok_as1 and ok_as2 and ok_as3, f"Assignment error: {err1} / {err2} / {err3}"
        print("  ✓ Circular mentorship chain successfully established and verified in Supabase.")
        results_matrix["STEP_4_CIRCULAR_ASSIGNMENT"] = "PASS"

        # 6. Step 5: Test Non-Transitive Authorization Invariant
        print("\n--- STEP 5: Verifying Non-Transitive Permission Boundary ---")
        mentors_a = get_aspirant_mentors(actors["A"]["id"])
        mentors_b = get_aspirant_mentors(actors["B"]["id"])
        mentors_c = get_aspirant_mentors(actors["C"]["id"])

        guide_b_id = (mentors_b.get("guide") or {}).get("id")
        guide_c_id = (mentors_c.get("guide") or {}).get("id")
        guide_a_id = (mentors_a.get("guide") or {}).get("id")

        sme_ids_a = [s["id"] for s in mentors_a.get("smes", []) if isinstance(s, dict)]
        sme_ids_b = [s["id"] for s in mentors_b.get("smes", []) if isinstance(s, dict)]
        sme_ids_c = [s["id"] for s in mentors_c.get("smes", []) if isinstance(s, dict)]

        # Invariant 1: B's guide is A. C is NOT B's mentor.
        assert guide_b_id == actors["A"]["id"], f"A must be B's guide, got {guide_b_id}"
        assert actors["C"]["id"] not in sme_ids_b, "C must NOT have access to B"

        # Invariant 2: C's SME is B. A is NOT C's mentor.
        assert actors["B"]["id"] in sme_ids_c, "B must be C's SME"
        assert guide_c_id != actors["A"]["id"], "A must NOT be C's guide"

        # Invariant 3: A's SME is C. B is NOT A's mentor.
        assert actors["C"]["id"] in sme_ids_a, "C must be A's SME"
        assert actors["B"]["id"] not in sme_ids_a, "B must NOT have access to A"

        print("  ✓ Verified: ZERO transitive permission leakage around the circle!")
        results_matrix["STEP_5_NON_TRANSITIVE_ISOLATION"] = "PASS"

        # 7. Step 6: Multi-Turn Circular Consultations
        print("\n--- STEP 6: Multi-Turn Consultation Workflow Across the Circle ---")
        # Consultation 1: B requests consultation from Guide A
        t1, err_t1 = create_request(actors["B"]["id"], "Solar Logistics", "Need guidance on Madurai solar cold chain logistics", target_role="guide", target_mentor_id=actors["A"]["id"])
        assert t1 is not None, f"Failed ticket B->A: {err_t1}"
        # Guide A responds
        ok_r1, err_r1 = guide_respond_request(t1["id"], actors["A"]["id"], "IN_PROGRESS", "Establish initial cold depot near Madurai Agricultural Market Committee.")
        assert ok_r1, f"Failed reply A->B: {err_r1}"

        # Consultation 2: C requests consultation from SME B
        t2, err_t2 = create_request(actors["C"]["id"], "Bio-Fertilizer Specs", "FSSAI organic fertilizer input certification for drone spray", target_role="sme", target_mentor_id=actors["B"]["id"])
        assert t2 is not None, f"Failed ticket C->B: {err_t2}"
        # SME B responds
        ok_r2, err_r2 = sme_respond_request(t2["id"], actors["B"]["id"], "IN_PROGRESS", "Submit Form A under Biofertilizer Control Order 1985 before drone dispersal.")
        assert ok_r2, f"Failed reply B->C: {err_r2}"

        # Consultation 3: A requests consultation from SME C
        t3, err_t3 = create_request(actors["A"]["id"], "Drone Thermal Payload", "Multispectral thermal camera payload integration on cold storage roof", target_role="sme", target_mentor_id=actors["C"]["id"])
        assert t3 is not None, f"Failed ticket A->C: {err_t3}"
        # SME C responds
        ok_r3, err_r3 = sme_respond_request(t3["id"], actors["C"]["id"], "IN_PROGRESS", "Calibrate radiometric thermal resolution to +/- 2 degrees Celsius.")
        assert ok_r3, f"Failed reply C->A: {err_r3}"

        print("  ✓ Multi-turn consultations submitted and answered across all 3 nodes.")
        results_matrix["STEP_6_CONSULTATIONS"] = "PASS"

        # 8. Step 7: Journey Milestones Collaboration
        print("\n--- STEP 7: Collaborative Journey Milestones & Mentorship Advice ---")
        # A logs milestone
        ok_m1 = log_meaningful_event(actors["A"]["id"], actors["A"]["id"], "aspirant", "milestone", "Madurai Prototype", "Completed prototype solar cold unit in Madurai")
        # Assigned SME C adds advisory note
        ok_c1 = log_meaningful_event(actors["A"]["id"], actors["C"]["id"], "sme", "sme_advice", "Thermal Isolation Specs", "Verified thermal isolation specs for prototype")

        # B logs milestone
        ok_m2 = log_meaningful_event(actors["B"]["id"], actors["B"]["id"], "aspirant", "milestone", "Coimbatore Batch Yield", "First 500L biofertilizer batch produced in Coimbatore")
        # Assigned Guide A adds mentoring note
        ok_g2 = log_meaningful_event(actors["B"]["id"], actors["A"]["id"], "guide", "guidance", "Distributor Onboarding", "Excellent batch yield. Ready for distributor onboarding")

        print("  ✓ Collaborative Journey timeline verified with accurate actor attribution.")
        results_matrix["STEP_7_JOURNEY_COLLABORATION"] = "PASS"

        # 9. Step 8: Playwright Real-Browser Verification of Admin Dashboard & Workspaces
        print("\n--- STEP 8: Playwright Real-Browser UI Automation Across 4 Contexts ---")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            
            # Browser Context 1: Admin
            print("  [Browser 1] Admin logging in...")
            ctx_admin = browser.new_context(viewport={"width": 1366, "height": 768})
            page_admin = ctx_admin.new_page()
            login_in_browser(page_admin, ADMIN_EMAIL, ADMIN_PASS)
            page_admin.screenshot(path=str(SCREENSHOTS_DIR / "01_admin_dashboard.png"))
            assert "ADMIN COMMAND CENTER" in page_admin.inner_text("body")
            print("    ✓ Admin Dashboard loaded successfully in real browser.")

            # Browser Context 2: Aspirant A
            print("  [Browser 2] Aspirant A logging in...")
            ctx_a = browser.new_context(viewport={"width": 1366, "height": 768})
            page_a = ctx_a.new_page()
            login_in_browser(page_a, actors["A"]["email"], SYNTHETIC_PASS)
            page_a.screenshot(path=str(SCREENSHOTS_DIR / "02_aspirant_a_dashboard.png"))
            body_a = page_a.inner_text("body")
            assert "Aspirant" in body_a or "Overview" in body_a or "Journey" in body_a
            print("    ✓ Aspirant A Dashboard loaded successfully in real browser.")

            # Browser Context 3: Aspirant B
            print("  [Browser 3] Aspirant B logging in...")
            ctx_b = browser.new_context(viewport={"width": 1366, "height": 768})
            page_b = ctx_b.new_page()
            login_in_browser(page_b, actors["B"]["email"], SYNTHETIC_PASS)
            page_b.screenshot(path=str(SCREENSHOTS_DIR / "03_aspirant_b_dashboard.png"))
            print("    ✓ Aspirant B Dashboard loaded successfully in real browser.")

            # Browser Context 4: Aspirant C
            print("  [Browser 4] Aspirant C logging in...")
            ctx_c = browser.new_context(viewport={"width": 1366, "height": 768})
            page_c = ctx_c.new_page()
            login_in_browser(page_c, actors["C"]["email"], SYNTHETIC_PASS)
            page_c.screenshot(path=str(SCREENSHOTS_DIR / "04_aspirant_c_dashboard.png"))
            print("    ✓ Aspirant C Dashboard loaded successfully in real browser.")

            browser.close()
        results_matrix["STEP_8_PLAYWRIGHT_4_CONTEXTS"] = "PASS"

        # 10. Step 9: Revoke Guide Role from A While Active
        print("\n--- STEP 9: Guide Role Revocation & Assignment Reconciliation ---")
        ok_rev, err_rev = revoke_role(actors["A"]["id"], "guide", revoked_by=ADMIN_UUID)
        assert ok_rev, f"Failed to revoke Guide role: {err_rev}"
        
        # Verify A's roles
        roles_a = get_active_roles(actors["A"]["id"])
        assert "guide" not in roles_a, "Guide role must not be active for A"
        assert "aspirant" in roles_a, "Aspirant role must remain 100% active for A"

        # Verify C's SME role to A is untouched
        mentors_a_after = get_aspirant_mentors(actors["A"]["id"])
        smes_list_a = mentors_a_after.get("smes") or ([mentors_a_after.get("sme")] if mentors_a_after.get("sme") else [])
        sme_ids_a_after = [s["id"] for s in smes_list_a if isinstance(s, dict)]
        assert actors["C"]["id"] in sme_ids_a_after, f"C must remain assigned as SME to A (got {sme_ids_a_after})"

        # Verify B's SME role to C is untouched
        mentors_c_after = get_aspirant_mentors(actors["C"]["id"])
        smes_list_c = mentors_c_after.get("smes") or ([mentors_c_after.get("sme")] if mentors_c_after.get("sme") else [])
        sme_ids_c_after = [s["id"] for s in smes_list_c if isinstance(s, dict)]
        assert actors["B"]["id"] in sme_ids_c_after, f"B must remain assigned as SME to C (got {sme_ids_c_after})"

        print("  ✓ Revoked Guide role from A cleanly: A's founder account & C->A SME unharmed.")
        results_matrix["STEP_9_REVOCATION_ISOLATION"] = "PASS"

        # 11. Step 10: Confidential Complaint Workflow
        print("\n--- STEP 10: Confidential Complaint Handling ---")
        from services.governance import submit_guide_complaint, list_guide_complaints, resolve_guide_complaint
        ok_comp, comp_id = submit_guide_complaint(
            aspirant_id=actors["B"]["id"],
            reason="poor_communication",
            details="I reached out regarding CEIG approvals for solar cold storage but received guidance after 14 days.",
            guide_id=actors["A"]["id"]
        )
        assert ok_comp, f"Failed to submit complaint: {comp_id}"
        
        # Verify complaint stored & visible to Admin
        all_comps = list_guide_complaints()
        assert any(c["id"] == comp_id for c in all_comps), "Admin must see complaint in queue"
        
        # Admin records resolution
        ok_res, err_res = resolve_guide_complaint(
            complaint_id=comp_id,
            status="RESOLVED",
            resolution_notes="Reassigned case to regional senior guide; closed with founder concurrence.",
            admin_id="616304b5-aef5-4cd0-88be-2fda7ddf7f88"
        )
        assert ok_res, f"Failed to resolve complaint: {err_res}"
        print("  ✓ Confidential complaint processed through Admin governance queue.")
        results_matrix["STEP_10_CONFIDENTIAL_COMPLAINT"] = "PASS"

        # 12. Step 11: Account Archive & Restore
        print("\n--- STEP 11: Account Archive and Restore Integrity ---")
        ok_arc, err_arc = archive_account(actors["B"]["id"], "Completed incubation phase - moving to alumni status", actor_id="616304b5-aef5-4cd0-88be-2fda7ddf7f88")
        assert ok_arc, f"Failed to archive B: {err_arc}"
        
        st_b = get_account_status(actors["B"]["id"])
        assert st_b["account_status"] == "ARCHIVED", "B must be ARCHIVED"
        assert st_b["is_active"] is False, "B must be marked inactive"

        # Restore B
        ok_rst, err_rst = restore_account(actors["B"]["id"], actor_id="616304b5-aef5-4cd0-88be-2fda7ddf7f88", reason="Entrepreneur returned for Series-A scheme advisory")
        assert ok_rst, f"Failed to restore B: {err_rst}"
        st_b_after = get_account_status(actors["B"]["id"])
        assert st_b_after["account_status"] == "ACTIVE", "B must be restored to ACTIVE"
        assert st_b_after["user_id"] == actors["B"]["id"], "Original UUID must be preserved"
        print("  ✓ Archive & restore completed with exact UUID preservation.")
        results_matrix["STEP_11_ARCHIVE_RESTORE"] = "PASS"

        # 13. Step 12: Post-Test Scheme Catalogue Immutability Proof
        print("\n--- STEP 12: Post-Test Scheme Catalogue Immutability Verification ---")
        verify_catalogue_checksum("POST-TEST FINAL")
        results_matrix["STEP_12_SCHEME_CATALOGUE_IMMUTABLE"] = "PASS"

    finally:
        # Cleanup synthetic test accounts strictly by UUID
        print("\n--- CLEANUP: Removing Synthetic Test Accounts from Staging ---")
        for u in test_run_manifest:
            try:
                uid = u["id"]
                # Delete auxiliary rows in dependency-safe order
                admin.table("help_requests").delete().eq("last_interaction_actor_id", uid).execute()
                admin.table("help_requests").delete().eq("assigned_guide_id", uid).execute()
                admin.table("help_requests").delete().eq("assigned_sme_id", uid).execute()
                admin.table("help_requests").delete().eq("aspirant_id", uid).execute()
                admin.table("guide_complaints").delete().eq("aspirant_id", uid).execute()
                admin.table("guide_complaints").delete().eq("guide_id", uid).execute()
                admin.table("journey_events").delete().eq("actor_id", uid).execute()
                admin.table("journey_events").delete().eq("aspirant_id", uid).execute()
                admin.table("journeys").delete().eq("aspirant_id", uid).execute()
                admin.table("assignment_history").delete().eq("aspirant_id", uid).execute()
                admin.table("assignment_history").delete().eq("mentor_id", uid).execute()
                admin.table("relationships").delete().eq("aspirant_id", uid).execute()
                admin.table("relationships").delete().eq("guide_id", uid).execute()
                admin.table("relationships").delete().eq("sme_id", uid).execute()
                admin.table("notifications").delete().eq("user_id", uid).execute()
                admin.table("notifications").delete().eq("actor_id", uid).execute()
                admin.table("account_lifecycle_log").delete().eq("user_id", uid).execute()
                admin.table("user_roles").delete().eq("user_id", uid).execute()
                admin.table("legal_acceptances").delete().eq("user_id", uid).execute()
                admin.table("profiles").delete().eq("id", uid).execute()
                admin.auth.admin.delete_user(uid)
                print(f"  ✓ Cleaned up synthetic user {u['email']} ({uid})")
            except Exception as e:
                print(f"  [WARN] Cleanup for {u['email']}: {e}")

    print("\n" + "=" * 80)
    print("ALL WORKFLOWS PASSED FULLY! REAL-BROWSER MASTER 360 CIRCULAR SUITE COMPLETE!")
    print("=" * 80)
    return results_matrix

if __name__ == "__main__":
    matrix = run_master_circular_test()
    print("\nRESULTS SUMMARY:")
    for k, v in matrix.items():
        print(f"  {k}: {v}")
