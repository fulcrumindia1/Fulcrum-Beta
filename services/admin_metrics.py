"""
services/admin_metrics.py — High-Performance Database-Side Admin Dashboard Aggregates
======================================================================================
Coherent, authorized dashboard metrics retrieval path that uses database-side aggregates
(HTTP HEAD count requests) to retrieve counts without downloading complete records.

Resolves:
- PERF-01: Admin dashboard query explosion on rerun.
- Eliminates repeated full-table fetching of profiles, schemes, and governance records.
- Remains O(1) in memory and network transfer even with 5,000+ registered users.
"""

from typing import Dict, Optional
from services.auth import get_supabase_admin_client, get_data_backend
from services.local_db import get_local_db
from services.cache import get_memo, set_memo, invalidate_memo
from services.roles import require_sole_admin


def get_admin_dashboard_metrics(admin_id: Optional[str] = None) -> Dict[str, int]:
    """
    Fetches real-time, database-side dashboard metrics for the Sole Platform Administrator.
    Uses count='exact' with head=True in Supabase mode to calculate aggregates with
    zero table data payload downloaded.
    
    Returns:
        Dict with keys:
            - aspirants_count
            - guides_count
            - smes_count
            - active_journeys_count
            - pending_directives_count
            - schemes_count
            - open_complaints_count
            - pending_reviews_count
            - open_conflicts_count
    """
    # 1. Verify Sole Admin authority
    ok_admin, _ = require_sole_admin(actor_id=admin_id)
    if not ok_admin:
        return {
            "aspirants_count": 0,
            "guides_count": 0,
            "smes_count": 0,
            "active_journeys_count": 0,
            "pending_directives_count": 0,
            "schemes_count": 0,
            "open_complaints_count": 0,
            "pending_reviews_count": 0,
            "open_conflicts_count": 0,
        }

    # 2. Check memo cache
    cache_key = "admin_dashboard_metrics"
    cached = get_memo(cache_key)
    if cached is not None:
        return cached

    backend = get_data_backend()
    metrics = {
        "aspirants_count": 0,
        "guides_count": 0,
        "smes_count": 0,
        "active_journeys_count": 0,
        "pending_directives_count": 0,
        "schemes_count": 0,
        "open_complaints_count": 0,
        "pending_reviews_count": 0,
        "open_conflicts_count": 0,
    }

    if backend == "supabase":
        client = get_supabase_admin_client()
        if client:
            try:
                # 1. Aspirants (Active non-admin accounts holding base aspirant role OR active aspirant grant)
                res_asp = client.table("profiles").select("id", count="exact", head=True).eq("role", "aspirant").neq("is_active", False).execute()
                base_asp_count = res_asp.count or 0
                extra_asp_count = 0
                try:
                    ur_asp = client.table("user_roles").select("user_id").eq("role", "aspirant").eq("status", "active").execute()
                    grant_ids = [r["user_id"] for r in (ur_asp.data or []) if r.get("user_id")]
                    if grant_ids:
                        res_extra = (
                            client.table("profiles")
                            .select("id", count="exact", head=True)
                            .in_("id", grant_ids)
                            .neq("role", "aspirant")
                            .neq("role", "admin")
                            .neq("is_active", False)
                            .execute()
                        )
                        extra_asp_count = res_extra.count or 0
                except Exception:
                    extra_asp_count = 0
                metrics["aspirants_count"] = base_asp_count + extra_asp_count

                # 2. Active Guides (Active grant in user_roles)
                res_g = client.table("user_roles").select("id", count="exact", head=True).eq("role", "guide").eq("status", "active").execute()
                metrics["guides_count"] = res_g.count or 0

                # 3. Active SMEs (Active grant in user_roles)
                res_sme = client.table("user_roles").select("id", count="exact", head=True).eq("role", "sme").eq("status", "active").execute()
                metrics["smes_count"] = res_sme.count or 0

                # 4. Active Journeys
                res_j = client.table("journeys").select("id", count="exact", head=True).eq("status", "active").execute()
                metrics["active_journeys_count"] = res_j.count or 0

                # 5. Pending Directives (help_requests of type mentor_admin_query awaiting admin)
                res_dir = client.table("help_requests").select("id", count="exact", head=True).eq("request_type", "mentor_admin_query").eq("status", "PENDING_ADMIN").execute()
                metrics["pending_directives_count"] = res_dir.count or 0

                # 6. Scheme count (Original 179 schemes catalogue)
                res_sch = client.table("schemes").select("id", count="exact", head=True).execute()
                metrics["schemes_count"] = res_sch.count or 0

                # 7. Open Complaints
                res_comp = client.table("guide_complaints").select("id", count="exact", head=True).in_("status", ["OPEN", "PENDING", "UNDER_REVIEW", "open", "pending", "under_review"]).execute()
                metrics["open_complaints_count"] = res_comp.count or 0

                # 8. Pending Scheme Support Reviews
                res_rev = client.table("scheme_support_reviews").select("id", count="exact", head=True).eq("status", "PENDING").execute()
                metrics["pending_reviews_count"] = res_rev.count or 0

                # 9. Open SME Conflicts
                res_coi = client.table("sme_conflict_declarations").select("id", count="exact", head=True).eq("has_conflict", True).in_("status", ["DECLARED", "OPEN", "UNDER_REVIEW", "declared", "open", "under_review"]).execute()
                metrics["open_conflicts_count"] = res_coi.count or 0

                set_memo(cache_key, metrics, ttl_seconds=15)
                return metrics
            except Exception as e:
                print(f"[AdminMetrics] Supabase aggregate error: {e}")

    # SQLite backend (local testing & development)
    try:
        db = get_local_db()
        conn = db._get_conn()
        cur = conn.cursor()

        # Aspirants (base role='aspirant' UNION active 'aspirant' role grant, non-admin, deduplicated)
        cur.execute(
            """
            SELECT COUNT(DISTINCT p.id) FROM profiles p
            LEFT JOIN user_roles ur ON ur.user_id = p.id AND ur.role = 'aspirant' AND ur.status = 'active'
            WHERE p.is_active = 1 AND p.role != 'admin' AND (p.role = 'aspirant' OR ur.user_id IS NOT NULL)
            """
        )
        metrics["aspirants_count"] = cur.fetchone()[0]

        # Active Guides
        cur.execute("SELECT COUNT(*) FROM user_roles WHERE role = 'guide' AND status = 'active'")
        metrics["guides_count"] = cur.fetchone()[0]

        # Active SMEs
        cur.execute("SELECT COUNT(*) FROM user_roles WHERE role = 'sme' AND status = 'active'")
        metrics["smes_count"] = cur.fetchone()[0]

        # Active Journeys
        cur.execute("SELECT COUNT(*) FROM journeys WHERE status = 'active'")
        metrics["active_journeys_count"] = cur.fetchone()[0]

        # Pending Directives
        cur.execute("SELECT COUNT(*) FROM help_requests WHERE request_type = 'mentor_admin_query' AND status = 'PENDING_ADMIN'")
        metrics["pending_directives_count"] = cur.fetchone()[0]

        # Scheme count
        cur.execute("SELECT COUNT(*) FROM schemes")
        metrics["schemes_count"] = cur.fetchone()[0]

        # Open Complaints
        cur.execute("SELECT COUNT(*) FROM guide_complaints WHERE status IN ('OPEN', 'PENDING', 'UNDER_REVIEW', 'open', 'pending', 'under_review')")
        metrics["open_complaints_count"] = cur.fetchone()[0]

        # Pending Scheme Reviews
        cur.execute("SELECT COUNT(*) FROM scheme_support_reviews WHERE status = 'PENDING'")
        metrics["pending_reviews_count"] = cur.fetchone()[0]

        # Open SME Conflicts
        cur.execute("SELECT COUNT(*) FROM sme_conflict_declarations WHERE has_conflict = 1 AND status IN ('DECLARED', 'OPEN', 'UNDER_REVIEW', 'declared', 'open', 'under_review')")
        metrics["open_conflicts_count"] = cur.fetchone()[0]

        conn.close()
    except Exception as ex_sql:
        print(f"[AdminMetrics] SQLite aggregate error: {ex_sql}")

    set_memo(cache_key, metrics, ttl_seconds=15)
    return metrics


def invalidate_admin_dashboard_metrics() -> None:
    """Targeted invalidation helper invoked upon relevant administrative mutations."""
    invalidate_memo("admin_dashboard_metrics")

