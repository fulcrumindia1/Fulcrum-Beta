# FULCRUM-INDIA: AGY ARGON — GATE 0 ROLE AUTHORIZATION MATRIX

## 1. Actor Classification & Identity Invariants

| Actor Category | Permitted Roles & Multi-Role Combination | Supabase Auth UUID | Single Admin Invariant Rule |
| :--- | :--- | :--- | :--- |
| **Platform Administrator** | `admin` exclusively | Dedicated Admin UUID (`fulcrumindia1@gmail.com`) | Exactly ONE account. Cannot hold `aspirant`, `guide`, or `sme`. Excluded from ordinary candidate lists. |
| **Aspirant / Entrepreneur** | `aspirant` | Unique User UUID | Base registered role. Cannot be administratively revoked. Zero NDA requirement. |
| **Dedicated Guide** | `guide` (or `aspirant + guide`) | Same User UUID | Requires active status & valid accepted Guide NDA. Gated from cases until NDA signed. |
| **Domain SME** | `sme` (or `aspirant + sme`) | Same User UUID | Requires active status & valid accepted SME NDA. Gated from cases until NDA signed. |
| **Dual Mentor** | `guide + sme` (or `aspirant + guide + sme`) | Same User UUID | Independent role statuses. Requires dual/role-specific NDA acceptances. |
| **Unassigned Mentor** | Valid `guide` / `sme` without case assignment | Same User UUID | Can view own profile and directory, but strictly denied private case discussions & photos. |
| **Unauthenticated Visitor** | None | Anonymous / No session | Gated strictly to Login and Aspirant Signup. All API and profile routes fail closed. |

---

## 2. Granular Resource & Action Permission Matrix

| Capability / Resource Action | Admin (`admin`) | Aspirant (`aspirant`) | Assigned Guide | Assigned SME | Unassigned Mentor | Unauthenticated |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Self-Service Password Reset** | ❌ Blocked (CLI/Console only) | ✅ Verified Token Only | ✅ Verified Token Only | ✅ Verified Token Only | ✅ Verified Token Only | ❌ Blocked |
| **Update Own Profile Data** | ✅ Full Access | ✅ Self-Owner Only | ✅ Self-Owner Only | ✅ Self-Owner Only | ✅ Self-Owner Only | ❌ Blocked |
| **Update Other User's Profile** | ✅ Full Access | ❌ Blocked (403) | ❌ Blocked (403) | ❌ Blocked (403) | ❌ Blocked (403) | ❌ Blocked |
| **Upload Aspirant Headshot** | ✅ Full Access | ✅ Self-Owner Only | ❌ Blocked | ❌ Blocked | ❌ Blocked | ❌ Blocked |
| **View Aspirant Headshot** | ✅ Full Access | ✅ Self-Owner Only | ✅ (If Active & NDA) | ✅ (If Active & NDA) | ❌ Blocked (None) | ❌ Blocked (None) |
| **View Aspirant Profile & Schemes**| ✅ Full Access | ✅ Self-Owner Only | ✅ (If Assigned) | ✅ (If Assigned) | ❌ Blocked | ❌ Blocked |
| **Post Open Case Discussion** | ✅ Full Access | ✅ Full Access | ✅ Full Access | ✅ Full Access | ❌ Blocked | ❌ Blocked |
| **Post Private Mentor Note** | ✅ Full Access | ❌ Blocked | ✅ (If Active & NDA) | ✅ (If Active & NDA) | ❌ Blocked | ❌ Blocked |
| **Read Private Mentor Note** | ✅ Full Access | ❌ Blocked (Filtered) | ✅ (If Active & NDA) | ✅ (If Active & NDA) | ❌ Blocked (Filtered) | ❌ Blocked (Filtered) |
| **Grant Role (Guide / SME)** | ✅ Full Access | ❌ Blocked | ❌ Blocked | ❌ Blocked | ❌ Blocked | ❌ Blocked |
| **Grant Role (`admin`)** | ❌ Hard Rejection | ❌ Hard Rejection | ❌ Hard Rejection | ❌ Hard Rejection | ❌ Hard Rejection | ❌ Hard Rejection |
| **Verify & Activate Mentor Role**| ✅ Full Access | ❌ Blocked | ❌ Blocked | ❌ Blocked | ❌ Blocked | ❌ Blocked |
| **Sign Mentor NDA** | ❌ N/A | ❌ N/A | ✅ (Mandatory Gate) | ✅ (Mandatory Gate) | ✅ (Mandatory Gate) | ❌ Blocked |
| **Assign Guide to Case** | ✅ Full Access | ❌ Blocked | ❌ Blocked | ❌ Blocked | ❌ Blocked | ❌ Blocked |
| **Assign SME to Advisory Panel** | ✅ Full Access | ❌ Blocked | ❌ Blocked | ❌ Blocked | ❌ Blocked | ❌ Blocked |

---

## 3. Defense-in-Depth Mechanisms

1. **Service Layer Gating**: Every service routine (`services/collaboration.py`, `services/aspirant_photos.py`, `services/roles.py`, `services/profiles.py`) resolves caller identity from verified session state and enforces checks independently of client arguments.
2. **Database Row Level Security (RLS)**: Staging and proposed production migrations enforce identical row-level security policies directly in PostgreSQL.
3. **Fail-Closed Default**: In the absence of an authenticated session or verified role grant, all endpoints return empty lists, `None`, or explicit access-denied errors.
