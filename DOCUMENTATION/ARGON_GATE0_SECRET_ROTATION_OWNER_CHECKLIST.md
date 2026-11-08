# FULCRUM-INDIA: AGY ARGON — GATE 0 SECRET ROTATION OWNER CHECKLIST

> [!CAUTION]
> **Action Required by Platform Owner Only**: The legacy deployment archive `fulcrum_deploy.tar.gz` contained historical environment settings. It has been completely purged from git tracking and added to `.gitignore`. To ensure absolute perimeter security, the Platform Administrator must rotate API credentials. **Never paste secret values into chat, commit history, or public issue trackers.**

---

## 1. Credentials Requiring Rotation

| Service | Key / Credential | Scope & Impact | Rotation Priority |
| :--- | :--- | :--- | :--- |
| **Supabase Project** | `anon` public API Key | Browser client authentication & public endpoints | **P1 — High** |
| **Supabase Project** | `service_role` Secret Key | Administrative backend tasks & storage management | **P0 — Critical** |
| **Supabase Project** | Postgres Database Password | Direct PostgreSQL connection string | **P1 — High** |
| **Streamlit Community Cloud** | App Secrets (`secrets.toml`) | Cloud deployment runtime environment | **P0 — Critical** |

---

## 2. Step-by-Step Rotation Checklist for Owner

### Step A: Supabase Dashboard Key Rotation

1. Navigate to your [Supabase Dashboard](https://supabase.com/dashboard).
2. Select your production project (`fulcrum-beta` / `fulcrum-cluster-b`).
3. In the left sidebar, click **Project Settings** (gear icon) → **API**.
4. Scroll to **Project API Keys**:
   - Locate the **JWT Secret** section.
   - Click **Generate a new JWT secret**. *(Note: This immediately invalidates the existing `anon` and `service_role` keys).*
   - Confirm the rotation in the confirmation dialog.
5. Copy the newly generated:
   - `Project URL`
   - `anon` `public` key
   - `service_role` `secret` key

### Step B: Update Streamlit Cloud Application Secrets

1. Navigate to your [Streamlit Community Cloud Console](https://share.streamlit.io).
2. Locate the `fulcrum-beta` app.
3. Click the three dots `...` next to the app → **Settings**.
4. Select the **Secrets** tab.
5. Replace the secret entries with the new credentials:

```toml
[supabase]
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-new-anon-key"
SUPABASE_SERVICE_ROLE_KEY = "your-new-service-role-key"

[general]
DATA_BACKEND = "supabase"
```

6. Click **Save**. Streamlit Cloud will automatically reboot the application container with the clean credentials.

### Step C: Verify Local Staging & Environment Synchronization

1. In your local development environment:
   - Ensure `.env` and `.streamlit/secrets.toml` reflect the new credentials.
   - Verify that `.gitignore` prevents them from being staged:
     ```bash
     git status --ignored
     ```
   - Confirm that neither `secrets.toml`, `.env`, nor any `*.tar.gz` archive appears in `git status`.

---

## 3. Post-Rotation Verification

After updating secrets on Streamlit Cloud:
- [ ] Log in as Platform Administrator (`fulcrumindia1@gmail.com`).
- [ ] Log in as Aspirant, Guide, and SME.
- [ ] Verify that headshot uploads persist cleanly to Supabase Storage.
- [ ] Check `Legal Agreements & NDA Signature Audit Trail` to confirm connectivity.
