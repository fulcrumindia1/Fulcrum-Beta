import sys
import os
sys.path.insert(0, os.path.abspath("."))
from services.auth import get_supabase_admin_client
from services.local_db import get_local_db

EMAILS_TO_REMOVE = [
    "e2e.guide@fulcrum-test.local",
    "e2e.sme@fulcrum-test.local",
    "austinthambi85@gmail.com",
    "ravi.kumar@milletfoods.in",
    "kumar.sme@fulcrum.in",
    "rajendran@fulcrum.in",
    "admin@fulcrum.in"
]

def remove_from_supabase():
    print("=" * 60)
    print("REMOVING ACCOUNTS FROM SUPABASE")
    print("=" * 60)
    client = get_supabase_admin_client()
    if not client:
        print("ERROR: Supabase admin client not available!")
        return

    # 1. Fetch user records from profiles
    res = client.table("profiles").select("id, email, full_name, role").in_("email", EMAILS_TO_REMOVE).execute()
    matched_profiles = res.data or []
    print(f"Found {len(matched_profiles)} matching profiles in Supabase.")
    user_ids = [p["id"] for p in matched_profiles]

    # Also check auth.users directly in case any profile is missing
    try:
        auth_users = client.auth.admin.list_users()
        matched_auth = [u for u in auth_users if u.email in EMAILS_TO_REMOVE]
        print(f"Found {len(matched_auth)} matching users in Supabase Auth.")
        for u in matched_auth:
            if u.id not in user_ids:
                user_ids.append(u.id)
    except Exception as e:
        print(f"Warning fetching auth users: {e}")

    if not user_ids:
        print("No users to remove in Supabase.")
        return

    print(f"Total distinct user IDs to remove: {len(user_ids)}")

    # Tables with cascade/foreign key references to delete first
    # (table_name, column_name)
    dependent_deletions = [
        ("journey_event_revisions", "user_id"),
        ("journey_event_revisions", "edited_by"),
        ("journey_events", "user_id"),
        ("journey_events", "author_id"),
        ("journeys", "user_id"),
        ("help_responses", "author_id"),
        ("help_requests", "aspirant_id"),
        ("help_requests", "assigned_to"),
        ("help_requests", "resolved_by"),
        ("mentor_relationships", "aspirant_id"),
        ("mentor_relationships", "guide_id"),
        ("mentor_relationships", "sme_id"),
        ("mentor_admin_queries", "mentor_id"),
        ("notifications", "user_id"),
        ("notifications", "actor_id"),
        ("legal_acceptances", "user_id"),
        ("guide_complaints", "guide_id"),
        ("guide_complaints", "aspirant_id"),
        ("sme_conflict_declarations", "sme_id"),
        ("user_roles", "user_id"),
    ]

    for tbl, col in dependent_deletions:
        for uid in user_ids:
            try:
                client.table(tbl).delete().eq(col, uid).execute()
            except Exception:
                pass
        print(f"  Cleaned {tbl} by user ID references.")

    # Also clean legal_acceptances by email
    for email in EMAILS_TO_REMOVE:
        try:
            client.table("legal_acceptances").delete().eq("user_email", email).execute()
        except Exception:
            pass

    # Delete from profiles
    for uid in user_ids:
        try:
            client.table("profiles").delete().eq("id", uid).execute()
        except Exception as e:
            print(f"  Error deleting profile {uid}: {e}")
    for email in EMAILS_TO_REMOVE:
        try:
            client.table("profiles").delete().eq("email", email).execute()
        except Exception as e:
            pass
    print("  Profiles deleted.")

    # Delete from Supabase Auth
    for uid in user_ids:
        try:
            client.auth.admin.delete_user(uid)
            print(f"  Deleted Supabase Auth user: {uid}")
        except Exception as e:
            print(f"  Warning deleting Auth user {uid}: {e}")

    print("Supabase cleanup completed successfully.\n")


def remove_from_sqlite():
    print("=" * 60)
    print("REMOVING ACCOUNTS FROM LOCAL SQLITE")
    print("=" * 60)
    db = get_local_db()
    conn = db._get_conn()
    cur = conn.cursor()

    placeholders = ",".join("?" for _ in EMAILS_TO_REMOVE)
    cur.execute(f"SELECT id, email FROM profiles WHERE email IN ({placeholders})", EMAILS_TO_REMOVE)
    rows = cur.fetchall()
    user_ids = [r["id"] for r in rows]
    print(f"Found {len(user_ids)} matching profiles in SQLite.")

    if not user_ids:
        print("No users to remove in SQLite.")
        return

    uid_placeholders = ",".join("?" for _ in user_ids)
    
    tables_cols = [
        ("journey_event_revisions", "user_id"),
        ("journey_event_revisions", "edited_by"),
        ("journey_events", "user_id"),
        ("journey_events", "author_id"),
        ("journeys", "user_id"),
        ("help_responses", "author_id"),
        ("help_requests", "aspirant_id"),
        ("help_requests", "assigned_to"),
        ("help_requests", "resolved_by"),
        ("mentor_relationships", "aspirant_id"),
        ("mentor_relationships", "guide_id"),
        ("mentor_relationships", "sme_id"),
        ("mentor_admin_queries", "mentor_id"),
        ("notifications", "user_id"),
        ("notifications", "actor_id"),
        ("legal_acceptances", "user_id"),
        ("guide_complaints", "guide_id"),
        ("guide_complaints", "aspirant_id"),
        ("sme_conflict_declarations", "sme_id"),
        ("user_roles", "user_id"),
    ]

    for tbl, col in tables_cols:
        try:
            cur.execute(f"DELETE FROM {tbl} WHERE {col} IN ({uid_placeholders})", user_ids)
        except Exception:
            pass

    # Delete legal acceptances by email
    try:
        cur.execute(f"DELETE FROM legal_acceptances WHERE user_email IN ({placeholders})", EMAILS_TO_REMOVE)
    except Exception:
        pass

    # Delete profiles
    cur.execute(f"DELETE FROM profiles WHERE id IN ({uid_placeholders})", user_ids)
    conn.commit()
    print("SQLite cleanup completed successfully.\n")


def print_remaining_users():
    print("=" * 60)
    print("REMAINING USERS IN DATABASE")
    print("=" * 60)
    client = get_supabase_admin_client()
    if client:
        res = client.table("profiles").select("id, email, full_name, role").order("role").execute()
        print(f"Supabase remaining profiles ({len(res.data)}):")
        for p in res.data:
            print(f"  [{p['role'].upper()}] {p['email']} ({p['full_name']})")
    
    db = get_local_db()
    conn = db._get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, email, full_name, role FROM profiles ORDER BY role")
    local_rows = cur.fetchall()
    print(f"\nSQLite remaining profiles ({len(local_rows)}):")
    for r in local_rows:
        print(f"  [{r['role'].upper()}] {r['email']} ({r['full_name']})")


if __name__ == "__main__":
    remove_from_supabase()
    remove_from_sqlite()
    print_remaining_users()

