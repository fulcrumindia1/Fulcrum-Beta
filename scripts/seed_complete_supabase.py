"""
scripts/seed_complete_supabase.py
=============================================================================
Complete Seeding Script for New Supabase Instance (Fulcrum-Beta):
1. Creates/Syncs 4 Core User Accounts in Supabase Auth & public.profiles
2. Grants and Activates Multi-Role Assignments in public.user_roles
3. Signs Initial Platform Terms and Guide/SME NDA in public.legal_acceptances
4. Initializes Ravi Kumar's Entrepreneurial Journey and Relationship Roster
5. Synchronizes all 170 Public Schemes into public.schemes
=============================================================================
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timezone

# Ensure project root is on path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import dotenv
dotenv.load_dotenv(override=True)

from services.auth import get_supabase_admin_client

def main():
    admin = get_supabase_admin_client()
    if not admin:
        print("[ERROR] Supabase admin client not available. Please verify SUPABASE_URL and SUPABASE_SECRET_KEY.")
        sys.exit(1)

    print(f"[SEED] Connected to Supabase at {os.environ.get('SUPABASE_URL', 'bhaqaawsufwtjeqfifbv.supabase.co')}")
    now_iso = datetime.now(timezone.utc).isoformat()

    # 1. Accounts Configuration
    accounts = [
        {
            "email": "admin@fulcrum.in",
            "password": "Admin@123",
            "role": "admin",
            "full_name": "Fulcrum Administrator",
            "phone": "9876543213",
            "district": "Chennai",
            "profile_data": {}
        },
        {
            "email": "rajendran@fulcrum.in",
            "password": "Welcome@2026",
            "role": "guide",
            "full_name": "Rajendran Natarajan",
            "phone": "9840123456",
            "district": "Chennai",
            "profile_data": {
                "expertise": "Enterprise Strategy, Agribusiness Scaling",
                "bio": "Senior Enterprise Guide with 15+ years experience mentoring MSMEs.",
                "industry": "Agribusiness",
                "temp_password_issued": True
            }
        },
        {
            "email": "kumar.sme@fulcrum.in",
            "password": "Welcome@2026",
            "role": "sme",
            "full_name": "Kumar S.",
            "phone": "9840654321",
            "district": "Madurai",
            "profile_data": {
                "expertise": "GST, Indirect Taxation & FSSAI Compliance",
                "bio": "Specialized Chartered Accountant & Compliance Consultant.",
                "industry": "Taxation & Regulatory",
                "temp_password_issued": True
            }
        },
        {
            "email": "ravi.kumar@milletfoods.in",
            "password": "Aspirant@123",
            "role": "aspirant",
            "full_name": "Ravi Kumar",
            "phone": "9876543210",
            "district": "Madurai",
            "profile_data": {
                "personal": {
                    "full_name": "Ravi Kumar",
                    "email": "ravi.kumar@milletfoods.in",
                    "phone": "9876543210",
                    "district": "Madurai",
                    "state": "Tamil Nadu",
                    "gender": "Male",
                    "dob": "15-08-1995",
                    "address": "12 Main Road, Madurai"
                },
                "professional": {
                    "education": "B.Sc Agriculture",
                    "experience_years": 4,
                    "skills": ["Food Processing", "Supply Chain", "Retail"],
                    "current_status": "Full-time Founder",
                    "experience": "4 years in value-added millet processing and organic distribution"
                },
                "demographics": {
                    "category": "OBC",
                    "gender": "Male",
                    "differently_abled": "No",
                    "district": "Madurai",
                    "state": "Tamil Nadu"
                },
                "business": {
                    "business_name": "Madurai Millet Foods Pvt Ltd",
                    "industry": "Food Processing",
                    "sector": "Agribusiness / Value Addition",
                    "stage": "validation",
                    "entity_type": "Private Limited",
                    "turnover": 4500000,
                    "investment": 2500000,
                    "has_gst": True,
                    "gst_number": "33AABCM1234F1Z5",
                    "has_udyam": True,
                    "udyam_number": "UDYAM-TN-12-0012345",
                    "employees": 12,
                    "current_capital": 2500000,
                    "funding_needed": 5000000,
                    "capital_requirement": 5000000,
                    "district": "Madurai",
                    "state": "Tamil Nadu",
                    "products_services": "Traditional millet cookies, instant porridge mixes, ready-to-cook grains"
                }
            }
        }
    ]

    user_ids = {}

    print("\n--- STEP 1: AUTH USERS & PROFILES ---")
    for acc in accounts:
        email = acc["email"]
        role = acc["role"]
        try:
            # Check if user already exists
            user_list = admin.auth.admin.list_users()
            found = next((u for u in user_list if u.email == email), None)
            if not found:
                created = admin.auth.admin.create_user({
                    "email": email,
                    "password": acc["password"],
                    "email_confirm": True,
                    "user_metadata": {
                        "full_name": acc["full_name"],
                        "role": role,
                        "phone": acc["phone"],
                        "district": acc["district"]
                    }
                })
                user_ids[role] = created.user.id
                print(f"  [AUTH CREATED] {email} -> {created.user.id}")
            else:
                user_ids[role] = found.id
                print(f"  [AUTH EXISTS]  {email} -> {found.id}")
        except Exception as e:
            print(f"  [AUTH ERROR]   {email}: {e}")

        if role in user_ids:
            try:
                profile_record = {
                    "id": user_ids[role],
                    "email": email,
                    "role": role,
                    "full_name": acc["full_name"],
                    "phone": acc["phone"],
                    "district": acc["district"],
                    "state": "Tamil Nadu",
                    "profile_data": acc["profile_data"],
                    "is_active": True,
                    "updated_at": now_iso
                }
                admin.table("profiles").upsert(profile_record, on_conflict="id").execute()
                print(f"  [PROFILE SYNCED] {email}")
            except Exception as e:
                print(f"  [PROFILE ERROR]  {email}: {e}")

    print("\n--- STEP 2: MULTI-ROLE ASSIGNMENTS (user_roles) ---")
    for role, uid in user_ids.items():
        try:
            admin.table("user_roles").upsert({
                "user_id": uid,
                "role": role,
                "status": "active",
                "activated_at": now_iso,
                "created_at": now_iso,
                "updated_at": now_iso
            }, on_conflict="user_id, role").execute()
            print(f"  [ROLE ACTIVE] {role} for {uid}")

            if role != "aspirant":
                admin.table("user_roles").upsert({
                    "user_id": uid,
                    "role": "aspirant",
                    "status": "active",
                    "activated_at": now_iso,
                    "created_at": now_iso,
                    "updated_at": now_iso
                }, on_conflict="user_id, role").execute()
                print(f"  [BASE ROLE ACTIVE] aspirant for {uid}")
        except Exception as e:
            print(f"  [ROLE ERROR] {role}: {e}")

    print("\n--- STEP 3: PRE-SIGN LEGAL TERMS & NDA AUDIT ---")
    for role, uid in user_ids.items():
        try:
            # Terms and conditions
            admin.table("legal_acceptances").insert({
                "user_id": uid,
                "document_id": "terms_v1_0",
                "doc_type": "terms_and_conditions",
                "doc_version": "1.0.0",
                "doc_hash": "b8c9d2e1f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1",
                "user_email_snapshot": f"{role}@fulcrum.in",
                "typed_legal_name": f"Authorized {role.title()}",
                "typed_acceptance_phrase": "I ACCEPT TERMS AND CONDITIONS",
                "checkbox_confirmed": True,
                "roles_covered": ["aspirant", "guide", "sme", "admin"],
                "ip_address": "127.0.0.1",
                "user_agent": "Fulcrum System Seeder",
                "status": "ACCEPTED",
                "accepted_at": now_iso
            }).execute()

            # NDA for Guide and SME
            if role in ("guide", "sme"):
                admin.table("legal_acceptances").insert({
                    "user_id": uid,
                    "document_id": "nda_dual_v1_0",
                    "doc_type": "nda_dual",
                    "doc_version": "1.0.0",
                    "doc_hash": "c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8",
                    "user_email_snapshot": f"{role}@fulcrum.in",
                    "typed_legal_name": f"Certified {role.upper()}",
                    "typed_acceptance_phrase": "I AGREE TO MAINTAIN STRICT CONFIDENTIALITY",
                    "checkbox_confirmed": True,
                    "roles_covered": ["guide", "sme"],
                    "ip_address": "127.0.0.1",
                    "user_agent": "Fulcrum System Seeder",
                    "status": "ACCEPTED",
                    "accepted_at": now_iso
                }).execute()
                print(f"  [NDA ACCEPTED] {role} ({uid})")
        except Exception as e:
            print(f"  [LEGAL ACCEPTANCE NOTICE] {role}: {e}")

    print("\n--- STEP 4: JOURNEY & RELATIONSHIP ROSTER ---")
    asp_id = user_ids.get("aspirant")
    admin_id = user_ids.get("admin")
    guide_id = user_ids.get("guide")
    sme_id = user_ids.get("sme")

    if asp_id:
        try:
            admin.table("journeys").upsert({
                "aspirant_id": asp_id,
                "title": "Madurai Millet Foods — Value Addition Journey",
                "business_type": "Food Processing & Agribusiness",
                "stage": "validation",
                "status": "active",
                "updated_at": now_iso
            }, on_conflict="aspirant_id").execute()
            print("  [JOURNEY SYNCED]")
        except Exception as e:
            print(f"  [JOURNEY ERROR] {e}")

        try:
            admin.table("relationships").upsert({
                "aspirant_id": asp_id,
                "guide_id": guide_id,
                "sme_id": sme_id,
                "guide_ids": [guide_id] if guide_id else [],
                "sme_ids": [sme_id] if sme_id else [],
                "assigned_by": admin_id,
                "status": "active",
                "notes": "Dedicated Enterprise Guide (Rajendran) and Taxation SME (Kumar) assigned.",
                "updated_at": now_iso
            }, on_conflict="aspirant_id").execute()
            print("  [RELATIONSHIPS SYNCED]")
        except Exception as e:
            print(f"  [RELATIONSHIP ERROR] {e}")

    print("\n--- STEP 5: SYNCHRONIZING 170 SCHEMES ---")
    schemes_file = BASE_DIR / "seed" / "schemes.json"
    if schemes_file.exists():
        with open(schemes_file, "r", encoding="utf-8") as f:
            schemes_data = json.load(f)

        print(f"  Loaded {len(schemes_data)} schemes from {schemes_file.name}")
        batch_size = 25
        for i in range(0, len(schemes_data), batch_size):
            batch = schemes_data[i:i + batch_size]
            try:
                admin.table("schemes").upsert(batch, on_conflict="id").execute()
                print(f"  Upserted schemes batch {i // batch_size + 1}/{(len(schemes_data) + batch_size - 1) // batch_size} ({len(batch)} items)")
            except Exception as e:
                print(f"  [SCHEMES ERROR] Batch {i}: {e}")
        print("  [SCHEMES SYNC COMPLETED]")
    else:
        print("  [WARN] seed/schemes.json not found!")

    print("\n=======================================================")
    print("✅ SUCCESS: Supabase Database Seeding Completed!")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
