"""
services/pagination.py — High-Performance Server-Side Pagination Engine
========================================================================
Implements safe database-side pagination, sorting, and filtering for:
- Entrepreneurs Directory
- Guide Management
- SME Management
- Multi-Role Grants
- Account Lifecycle & Archive
- Consultation Histories
- Journey Records
- Notification and Administrative History

Uses PostgREST .range(offset, offset + page_size - 1) and count='exact' in Supabase mode.
Preserves default page size of 25 records and bounded memory usage for 5,000+ accounts.
"""

from typing import Dict, List, Optional, Tuple, Any
from services.auth import get_supabase_admin_client, get_supabase_client, get_data_backend
from services.local_db import get_local_db
from services.cache import get_memo, set_memo
from services.profiles import calculate_completion, get_profiles_batch


DEFAULT_PAGE_SIZE = 25


def paginate_profiles(
    role: str = "aspirant",
    page: int = 1,
    page_size: int = DEFAULT_PAGE_SIZE,
    search: str = "",
    district: str = "ALL",
    sort_by: str = "created_at",
    sort_desc: bool = True
) -> Tuple[List[Dict], int]:
    """
    Server-side paginated retrieval of active profiles.
    Returns (records_for_page, total_matching_records).
    """
    page = max(1, page)
    offset = (page - 1) * page_size
    backend = get_data_backend()

    if backend == "supabase":
        client = get_supabase_admin_client() or get_supabase_client()
        if client:
            try:
                grant_uids: List[str] = []
                if role == "aspirant":
                    try:
                        ur_res = (
                            client.table("user_roles")
                            .select("user_id")
                            .eq("role", "aspirant")
                            .eq("status", "active")
                            .execute()
                        )
                        grant_uids = [r["user_id"] for r in (ur_res.data or []) if r.get("user_id")]
                    except Exception:
                        grant_uids = []

                def _apply_profile_filters(qb):
                    if search and search.strip():
                        s = search.strip()
                        qb = qb.or_(f"full_name.ilike.%{s}%,email.ilike.%{s}%")
                    if district and district != "ALL":
                        qb = qb.eq("district", district)
                    return qb

                q = _apply_profile_filters(
                    client.table("profiles").select("*", count="exact").eq("role", role).neq("is_active", False)
                )
                if role == "aspirant":
                    q = q.neq("role", "admin")
                q = q.order(sort_by, desc=sort_desc)
                fetch_start = 0 if grant_uids else offset
                res = q.range(fetch_start, offset + page_size - 1).execute()
                total = res.count or 0
                rows = res.data or []

                if grant_uids and role == "aspirant":
                    q_extra = _apply_profile_filters(
                        client.table("profiles")
                        .select("*")
                        .in_("id", grant_uids)
                        .neq("role", "aspirant")
                        .neq("role", "admin")
                        .neq("is_active", False)
                    )
                    extra_rows = q_extra.execute().data or []
                    if extra_rows:
                        by_id = {r["id"]: r for r in rows if r.get("id")}
                        for er in extra_rows:
                            if er.get("id") and er["id"] not in by_id:
                                by_id[er["id"]] = er
                        total = total + len(extra_rows)
                        merged = list(by_id.values())
                        merged.sort(key=lambda r: str(r.get(sort_by) or ""), reverse=sort_desc)
                        rows = merged[offset:offset + page_size]
                    else:
                        rows = rows[offset:offset + page_size]

                for r in rows:
                    r["completion_pct"] = calculate_completion(r)
                return rows, total
            except Exception as e:
                print(f"[Pagination] Supabase profiles query error: {e}")
                return [], 0

    # SQLite backend
    try:
        db = get_local_db()
        conn = db._get_conn()
        cur = conn.cursor()

        safe_sort = sort_by if sort_by in ("created_at", "updated_at", "full_name", "email", "district") else "created_at"
        if role == "aspirant":
            where_clauses = [
                "(role = 'aspirant' OR EXISTS (SELECT 1 FROM user_roles ur WHERE ur.user_id = profiles.id AND ur.role = 'aspirant' AND ur.status = 'active'))",
                "role != 'admin'",
                "is_active = 1",
            ]
            params: List[Any] = []
        else:
            where_clauses = ["role = ?", "is_active = 1"]
            params = [role]
        if search and search.strip():
            where_clauses.append("(full_name LIKE ? OR email LIKE ?)")
            params.extend([f"%{search.strip()}%", f"%{search.strip()}%"])
        if district and district != "ALL":
            where_clauses.append("district = ?")
            params.append(district)

        where_sql = " AND ".join(where_clauses)
        cur.execute(f"SELECT COUNT(*) FROM profiles WHERE {where_sql}", params)
        total = cur.fetchone()[0]

        order_dir = "DESC" if sort_desc else "ASC"
        cur.execute(
            f"SELECT * FROM profiles WHERE {where_sql} ORDER BY {safe_sort} {order_dir} LIMIT ? OFFSET ?",
            params + [page_size, offset]
        )
        col_names = [d[0] for d in cur.description]
        rows = [dict(zip(col_names, row)) for row in cur.fetchall()]
        conn.close()

        import json
        for r in rows:
            pd = r.get("profile_data")
            if isinstance(pd, str):
                try:
                    r["profile_data"] = json.loads(pd) if pd.strip() else {}
                except Exception:
                    r["profile_data"] = {}
            elif pd is None:
                r["profile_data"] = {}
            r["completion_pct"] = calculate_completion(r)
        return rows, total
    except Exception as ex_sql:
        print(f"[Pagination] SQLite profiles query error: {ex_sql}")
        return [], 0


def _paginate_role_holders(
    target_role: str,
    page: int = 1,
    page_size: int = DEFAULT_PAGE_SIZE,
    search: str = "",
    district: str = "ALL",
) -> Tuple[List[Dict], int]:
    """
    Server-side paginated retrieval of active AND pending-NDA mentors holding
    verified user_roles grants (with `role_grant_status` attached).
    """
    page = max(1, page)
    offset = (page - 1) * page_size
    backend = get_data_backend()

    if backend == "supabase":
        client = get_supabase_admin_client() or get_supabase_client()
        if client:
            try:
                ur_res = (
                    client.table("user_roles")
                    .select("user_id, status", count="exact")
                    .eq("role", target_role)
                    .in_("status", ["active", "pending_nda"])
                    .order("created_at", desc=True)
                    .range(offset, offset + page_size - 1)
                    .execute()
                )
                total = ur_res.count or 0
                status_by_uid = {
                    r["user_id"]: r.get("status", "active")
                    for r in (ur_res.data or [])
                    if r.get("user_id")
                }
                uids = list(status_by_uid.keys())
                if not uids:
                    return [], total

                profiles_map = get_profiles_batch(uids, is_system=True)
                rows = []
                for uid in uids:
                    prof = profiles_map.get(uid)
                    if not prof:
                        continue
                    prof_copy = dict(prof)
                    prof_copy["role_grant_status"] = status_by_uid[uid]
                    rows.append(prof_copy)
                if search and search.strip():
                    s = search.strip().lower()
                    rows = [r for r in rows if s in r.get("full_name", "").lower() or s in r.get("email", "").lower()]
                if district and district != "ALL":
                    rows = [r for r in rows if r.get("district") == district]
                return rows, total
            except Exception as e:
                print(f"[Pagination] Supabase {target_role}s query error: {e}")
                return [], 0

    # SQLite: include active AND pending_nda mentor grants cleanly
    from services.roles import list_users_with_multi_roles
    from services.profiles import get_profile
    rows_by_id: Dict[str, Dict] = {}
    for u in list_users_with_multi_roles():
        uid = str(u.get("id") or "")
        if not uid:
            continue
        status = None
        if target_role in u.get("active_roles", []):
            status = "active"
        elif target_role in u.get("pending_nda_roles", []):
            status = "pending_nda"
        if not status:
            continue
        prof = get_profile(uid)
        if prof:
            prof_copy = dict(prof)
            prof_copy["role_grant_status"] = status
            rows_by_id[uid] = prof_copy

    all_rows = list(rows_by_id.values())
    all_rows.sort(key=lambda x: str(x.get("created_at") or ""), reverse=True)
    if search and search.strip():
        s = search.strip().lower()
        all_rows = [r for r in all_rows if s in r.get("full_name", "").lower() or s in r.get("email", "").lower()]
    if district and district != "ALL":
        all_rows = [r for r in all_rows if r.get("district") == district]
    total = len(all_rows)
    return all_rows[offset:offset + page_size], total


def paginate_guides(
    page: int = 1,
    page_size: int = DEFAULT_PAGE_SIZE,
    search: str = "",
    district: str = "ALL"
) -> Tuple[List[Dict], int]:
    """Server-side paginated retrieval of active and pending-NDA Guides."""
    return _paginate_role_holders("guide", page=page, page_size=page_size, search=search, district=district)


def paginate_smes(
    page: int = 1,
    page_size: int = DEFAULT_PAGE_SIZE,
    search: str = "",
    district: str = "ALL"
) -> Tuple[List[Dict], int]:
    """Server-side paginated retrieval of active and pending-NDA Domain SMEs."""
    return _paginate_role_holders("sme", page=page, page_size=page_size, search=search, district=district)


def paginate_accounts(
    status: str = "ACTIVE",
    page: int = 1,
    page_size: int = DEFAULT_PAGE_SIZE,
    search: str = ""
) -> Tuple[List[Dict], int]:
    """
    Server-side paginated retrieval of accounts for Account Lifecycle & Archive Console.
    Supports status filters: 'ALL', 'ACTIVE', 'TEMPORARILY_SUSPENDED', 'ARCHIVED',
    'PENDING_DELETION', or composite 'active_and_paused'.
    """
    page = max(1, page)
    offset = (page - 1) * page_size
    backend = get_data_backend()

    if backend == "supabase":
        client = get_supabase_admin_client() or get_supabase_client()
        if client:
            try:
                q = client.table("profiles").select("*", count="exact")
                if status == "active_and_paused":
                    q = q.in_("account_status", ["ACTIVE", "TEMPORARILY_SUSPENDED"])
                elif status and status != "ALL":
                    q = q.eq("account_status", status.upper())
                if search and search.strip():
                    s = search.strip()
                    q = q.or_(f"full_name.ilike.%{s}%,email.ilike.%{s}%")

                q = q.order("created_at", desc=True)
                res = q.range(offset, offset + page_size - 1).execute()
                total = res.count or 0
                rows = res.data or []
                for r in rows:
                    r["completion_pct"] = calculate_completion(r)
                return rows, total
            except Exception as e:
                print(f"[Pagination] Supabase accounts query error: {e}")
                return [], 0

    # SQLite
    from services.account_lifecycle import list_accounts_by_status
    if status == "active_and_paused":
        all_acc = [
            u for u in list_accounts_by_status(status_filter=None)
            if str(u.get("account_status", "ACTIVE")).upper() in ("ACTIVE", "TEMPORARILY_SUSPENDED")
        ]
    else:
        all_acc = list_accounts_by_status(status_filter=status if status != "ALL" else None)

    if search and search.strip():
        s = search.strip().lower()
        all_acc = [a for a in all_acc if s in a.get("full_name", "").lower() or s in a.get("email", "").lower()]
    total = len(all_acc)
    return all_acc[offset:offset + page_size], total


def paginate_journey_events(
    aspirant_id: str,
    page: int = 1,
    page_size: int = DEFAULT_PAGE_SIZE
) -> Tuple[List[Dict], int]:
    """
    Server-side paginated retrieval of Journey events for an entrepreneur.
    """
    if not aspirant_id:
        return [], 0

    page = max(1, page)
    offset = (page - 1) * page_size
    backend = get_data_backend()

    if backend == "supabase":
        client = get_supabase_admin_client() or get_supabase_client()
        if client:
            try:
                q = client.table("journeys").select("*", count="exact").eq("aspirant_id", aspirant_id).eq("status", "active")
                res = q.order("event_date", desc=True).range(offset, offset + page_size - 1).execute()
                total = res.count or 0
                return res.data or [], total
            except Exception as e:
                print(f"[Pagination] Supabase journey events error: {e}")
                return [], 0

    # SQLite
    from services.journey import get_journey_timeline
    all_events = get_journey_timeline(aspirant_id)
    total = len(all_events)
    return all_events[offset:offset + page_size], total


def paginate_notifications(
    user_id: str,
    unread_only: bool = False,
    page: int = 1,
    page_size: int = DEFAULT_PAGE_SIZE
) -> Tuple[List[Dict], int]:
    """
    Server-side paginated retrieval of notifications.
    """
    if not user_id:
        return [], 0

    page = max(1, page)
    offset = (page - 1) * page_size
    backend = get_data_backend()

    if backend == "supabase":
        client = get_supabase_admin_client() or get_supabase_client()
        if client:
            try:
                q = client.table("notifications").select("*", count="exact").eq("user_id", user_id)
                if unread_only:
                    q = q.eq("is_read", False)
                res = q.order("created_at", desc=True).range(offset, offset + page_size - 1).execute()
                total = res.count or 0
                return res.data or [], total
            except Exception as e:
                print(f"[Pagination] Supabase notifications error: {e}")
                return [], 0

    # SQLite
    from services.notifications import list_notifications
    all_notifs = list_notifications(user_id=user_id, unread_only=unread_only)
    total = len(all_notifs)
    return all_notifs[offset:offset + page_size], total


def render_pagination_controls(
    total_records: int,
    current_page: int,
    page_size: int = DEFAULT_PAGE_SIZE,
    key_prefix: str = "pag"
) -> int:
    """
    Renders clean, accessible pagination controls in Streamlit.
    Preserves page state in st.session_state and returns the current active page.
    """
    import streamlit as st

    total_pages = max(1, (total_records + page_size - 1) // page_size)
    if total_pages <= 1:
        return 1

    col_info, col_prev, col_num, col_next = st.columns([3, 1, 1.5, 1])
    with col_info:
        start_idx = (current_page - 1) * page_size + 1
        end_idx = min(total_records, current_page * page_size)
        st.caption(f"Showing **{start_idx}–{end_idx}** of **{total_records}** records (Page **{current_page}** of **{total_pages}**)")

    with col_prev:
        if st.button("◀ Prev", key=f"{key_prefix}_prev", disabled=(current_page <= 1), use_container_width=True):
            current_page = max(1, current_page - 1)
            st.session_state[f"{key_prefix}_page"] = current_page
            st.rerun()

    with col_num:
        new_page = st.number_input(
            "Page",
            min_value=1,
            max_value=total_pages,
            value=current_page,
            key=f"{key_prefix}_num",
            label_visibility="collapsed"
        )
        if new_page != current_page:
            st.session_state[f"{key_prefix}_page"] = int(new_page)
            st.rerun()

    with col_next:
        if st.button("Next ▶", key=f"{key_prefix}_next", disabled=(current_page >= total_pages), use_container_width=True):
            current_page = min(total_pages, current_page + 1)
            st.session_state[f"{key_prefix}_page"] = current_page
            st.rerun()

    return current_page
