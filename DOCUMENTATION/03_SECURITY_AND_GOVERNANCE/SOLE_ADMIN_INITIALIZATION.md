# SOLE PLATFORM ADMINISTRATOR INITIALIZATION RUNBOOK
**Platform:** Fulcrum India (Cluster A / Fulcrum-Beta)  
**Authoritative Sole Admin Email:** `fulcrumindia1@gmail.com`  
**Target Architecture:** Fresh Supabase Project (Clean Slate)  
**Date:** 2026-11-10  

---

## 1. Architectural Policy: Exactly One Platform Admin

Fulcrum enforces a **strict single-administrator governance model**:
- There is **exactly one** authorized platform administrator.
- The platform administrator identity is permanently tied to:  
  **`fulcrumindia1@gmail.com`**
- All other accounts are strictly Aspirants, Guides, or SMEs.
- Administrative mutations, multi-role promotions, NDA clearances, and account lifecycle suspensions require cryptographic verification of this sole admin identity.

---

## 2. The Fresh Supabase Project Challenge

When you provision a fresh Supabase project:
1. Supabase Auth will assign a **new random UUID** to `fulcrumindia1@gmail.com` upon signup.
2. In earlier versions of Fulcrum, the admin UUID was hardcoded to `616304b5-aef5-4cd0-88be-2fda7ddf7f88`.
3. If the hardcoded UUID does not match the new Supabase Auth UUID, the admin would be locked out of administrative tabs.

### How Fulcrum-Beta Solves This Dynamically
The codebase in `services/roles.py` has been updated with `get_configured_admin_uuid()`:
- It checks `os.environ.get("SOLE_ADMIN_UUID")` passed from `.env` via `docker-compose.yml`.
- If set, it dynamically binds the sole admin authority to the new UUID.
- If not set, it safely falls back to `616304b5-aef5-4cd0-88be-2fda7ddf7f88`.
- In all cases, the actor's email MUST also strictly match `fulcrumindia1@gmail.com`.

---

## 3. Step-by-Step Initialization Procedure

### Step 3.1: Create Admin Account in Supabase Auth
1. Go to your fresh Supabase Dashboard -> **Authentication -> Users**.
2. Click **Add User -> Create User**.
3. **Email:** `fulcrumindia1@gmail.com`
4. **Password:** Generate a strong production password.
5. **Auto Confirm User:** Toggle **ON** (so the account is immediately verified).
6. Click **Create User**.

### Step 3.2: Copy the New User UUID
1. Find `fulcrumindia1@gmail.com` in the user table.
2. Under the **User UID** column, copy the 36-character UUID string (e.g. `a1b2c3d4-e5f6-7890-abcd-ef1234567890`).

### Step 3.3: Elevate the New User in PostgreSQL (SQL Editor)
Open the **SQL Editor** in your Supabase Dashboard and run the following script (replace `<NEW_ADMIN_UUID>` with your copied UUID):

```sql
-- =============================================================================
-- ELEVATE SOLE ADMIN IDENTITY (fulcrumindia1@gmail.com)
-- =============================================================================
DO $$
DECLARE
    v_admin_uuid UUID := '<NEW_ADMIN_UUID>'::uuid;
    v_admin_email TEXT := 'fulcrumindia1@gmail.com';
BEGIN
    -- 1. Ensure profile exists and set role to admin
    INSERT INTO public.profiles (id, email, full_name, role, is_active, account_status)
    VALUES (
        v_admin_uuid,
        v_admin_email,
        'Platform Administrator',
        'admin',
        TRUE,
        'ACTIVE'
    )
    ON CONFLICT (id) DO UPDATE SET
        role = 'admin',
        is_active = TRUE,
        account_status = 'ACTIVE',
        updated_at = NOW();

    -- 2. Grant normalized admin role in user_roles table
    INSERT INTO public.user_roles (user_id, role, status)
    VALUES (v_admin_uuid, 'admin', 'active')
    ON CONFLICT (user_id, role) DO UPDATE SET
        status = 'active';

    -- 3. Safety Lock: Demote any other user if mistakenly set as admin
    UPDATE public.profiles
    SET role = 'aspirant', updated_at = NOW()
    WHERE lower(email) <> v_admin_email
      AND lower(role) IN ('admin', 'district_admin', 'operational_admin');

    DELETE FROM public.user_roles
    WHERE lower(role) IN ('admin', 'district_admin', 'operational_admin')
      AND user_id <> v_admin_uuid;

    RAISE NOTICE 'Sole Admin successfully elevated for UUID: %', v_admin_uuid;
END $$;
```

### Step 3.4: Configure `.env` on the Hostinger VPS
SSH into your Hostinger KVM 2 VPS and edit `/opt/fulcrum/.env`:

```bash
nano /opt/fulcrum/.env
```

Add or update the `SOLE_ADMIN_UUID` line:
```ini
DATA_BACKEND=supabase
SUPABASE_URL=https://your-fresh-id.supabase.co
SUPABASE_PUBLISHABLE_KEY=your_anon_key
SUPABASE_SECRET_KEY=your_service_role_key
SOLE_ADMIN_UUID=<NEW_ADMIN_UUID>
DOMAIN=app.fulcrumindia.online
APP_URL=https://app.fulcrumindia.online
```

Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

### Step 3.5: Restart Fulcrum Container
Apply the environment update without interrupting Caddy:

```bash
cd /opt/fulcrum
./scripts/restart.sh
```

---

## 4. Verification & Testing

### Verification 1: Command Line Check
Run this inside the container to verify the admin binding:

```bash
docker compose exec -T fulcrum python -c "
from services.roles import is_strict_admin, get_configured_admin_uuid, SOLE_ADMIN_EMAIL
admin_uuid = get_configured_admin_uuid()
print('Configured Admin UUID:', admin_uuid)
print('Strict Admin Check:   ', is_strict_admin(user_id=admin_uuid, email=SOLE_ADMIN_EMAIL))
assert is_strict_admin(user_id=admin_uuid, email=SOLE_ADMIN_EMAIL), 'Admin check failed!'
print('VERIFICATION PASSED: Sole Admin identity successfully locked.')
"
```

### Verification 2: Web Browser UI Check
1. Open `https://app.fulcrumindia.online` in your web browser.
2. Sign in with `fulcrumindia1@gmail.com` and your password.
3. Confirm that you are landed directly in the **Admin Command Center**.
4. Confirm visibility of all 13 tabs:
   - Dashboard & Metrics
   - Entrepreneurs Directory
   - Guide Management
   - SME Management
   - Mentor Assignments
   - Multi-Role Grants
   - Legal Terms & NDA
   - System Governance & Directives
   - Scheme Reviews
   - SME Conflicts & Direct Access
   - Account Lifecycle & Archive
   - Notifications & Audit Log
   - System Diagnostics

