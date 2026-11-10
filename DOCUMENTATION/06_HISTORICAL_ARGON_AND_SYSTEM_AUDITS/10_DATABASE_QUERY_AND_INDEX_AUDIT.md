# 10 — DATABASE QUERY AND INDEX AUDIT
**Phase K Deliverable | Target: PostgreSQL / Supabase (`bhaqaawsufwtjeqfifbv.supabase.co`)**

---

## 1. Query Execution & N+1 Pattern Audit

Empirical analysis of the Fulcrum-Beta codebase and PostgREST execution profiles identified four primary database access patterns:

| Query Type | Pattern Identified | Pre-Fix Cost | Post-Fix Optimization | Benefit |
| :--- | :--- | :---: | :---: | :---: |
| **User Role Resolution** | Repeated N+1 loop in [`list_users_with_multi_roles()`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/roles.py#L366) | 190 sequential HTTP calls (`21,565 ms`) | 2 batch queries joined in-memory (`345 ms`) | **62.4× faster** |
| **Active Aspirant Profiles** | Repeated calls to `get_active_roles(user_id)` inside directory loop | 196 sequential queries (`18,324 ms`) | 1 batch query with in-memory role map (`738 ms`) | **24.8× faster** |
| **Relationship Map Lookup** | Per-aspirant `get_aspirant_mentors(asp_id)` inside Admin loop | 32 separate queries (`2,403 ms`) | 1 batch query via [`get_all_relationships()`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/relationships.py#L604) (`98.3 ms`) | **24.4× faster** |
| **Government Schemes Read** | Full scan of 179 rows on `public.schemes` (`146.5 ms` per call) | Cold fetch on every tab (`1,372 ms`) | Global in-memory cache with write invalidation (`0.0 ms` warm) | **Instantaneous** |

---

## 2. Existing vs. Recommended PostgreSQL Indexes (Verified Against Actual Schema)

### A. Indexes Already Provisioned in [`supabase_setup.sql`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/supabase_setup.sql#L254-L295) & [`migrations/001_multi_role_and_legal.sql`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/migrations/001_multi_role_and_legal.sql#L24-L108)
- `public.profiles`: `idx_profiles_role ON public.profiles(role)`
- `public.user_roles`: `idx_user_roles_user_id ON public.user_roles(user_id)`, `idx_user_roles_role_status ON public.user_roles(role, status)`
- `public.relationships`: `idx_relationships_aspirant (aspirant_id)`, `idx_relationships_guide (guide_id)`, `idx_relationships_sme (sme_id)`
- `public.journeys`: `idx_journeys_aspirant (aspirant_id)`
- `public.journey_events`: `idx_journey_events_journey (journey_id, event_date DESC)`, `idx_journey_events_aspirant (aspirant_id)`
- `public.help_requests`: `idx_help_requests_aspirant (aspirant_id)`, `idx_help_requests_status (status)`, `idx_help_requests_assigned_guide (assigned_guide_id)`, `idx_help_requests_assigned_sme (assigned_sme_id)`, `idx_help_requests_status_created (status, created_at)`
- `public.notifications`: `idx_notifications_user_id (user_id)`, `idx_notifications_created_at (created_at DESC)`, `idx_notifications_user_unread (user_id, is_read)`
- `public.schemes`: `idx_schemes_active (is_active)`
- `public.scheme_releases`: `idx_scheme_releases_aspirant (aspirant_id)`, `idx_scheme_releases_guide (guide_id)`, `idx_scheme_releases_scheme (scheme_id)`, `idx_scheme_releases_status (status)`

### B. Additional Composite & GIN Indexes Recommended for Scale (`> 1,000` Users)
Every table and column name below is strictly verified against [`supabase_setup.sql`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/supabase_setup.sql) and [`migrations/001_multi_role_and_legal.sql`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/migrations/001_multi_role_and_legal.sql) (**Status: `NOT APPROVED — Awaiting Owner Decision`**):

```sql
-- 1. Composite index on public.profiles(role, is_active) for active directory filtering
CREATE INDEX IF NOT EXISTS idx_profiles_role_is_active
ON public.profiles(role, is_active);

-- 2. Composite index on public.user_roles(user_id, status) for per-user active role checks
CREATE INDEX IF NOT EXISTS idx_user_roles_user_id_status
ON public.user_roles(user_id, status);

-- 3. Composite & GIN indexes on public.relationships for active multi-mentor rosters
CREATE INDEX IF NOT EXISTS idx_relationships_status_aspirant
ON public.relationships(status, aspirant_id);

CREATE INDEX IF NOT EXISTS idx_relationships_guide_ids_gin
ON public.relationships USING GIN (guide_ids);

CREATE INDEX IF NOT EXISTS idx_relationships_sme_ids_gin
ON public.relationships USING GIN (sme_ids);

-- 4. Composite triage indexes on public.help_requests for Guide & SME queues
CREATE INDEX IF NOT EXISTS idx_help_requests_guide_status_updated
ON public.help_requests(assigned_guide_id, status, updated_at DESC);

CREATE INDEX IF NOT EXISTS idx_help_requests_sme_status_updated
ON public.help_requests(assigned_sme_id, status, updated_at DESC);

-- 5. Partial index on active (non-deleted) chronological journey events
CREATE INDEX IF NOT EXISTS idx_journey_events_aspirant_active_date
ON public.journey_events(aspirant_id, event_date DESC)
WHERE deleted_at IS NULL;
```

### C. Server-Side Pagination Recommendation for Future Scale (`> 2,000` Users)
In [`services/profiles.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/profiles.py) and [`views/admin.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py), replace unbounded `select("*")` directory fetches with PostgREST range pagination when the registered user base grows past 2,000 accounts:
```python
client.table("profiles").select("*").range(offset, offset + limit - 1).execute()
```
