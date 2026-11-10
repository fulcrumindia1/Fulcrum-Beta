# How Fulcrum Email (Resend) & Forgot Password Work Together — ELI5 Step-by-Step Guide

> **Audience:** Non-technical operators & platform owners  
> **Domain Setup:** `notify.fulcrumindia.online` (via Hostinger DNS + Resend SMTP) connected to Supabase Auth and `https://app.fulcrumindia.online/`  
> **Code Version:** Includes the `FULCRUM-BETA` WebSocket `#hash` recovery fix and performance improvements.

---

## 1. The Big Picture (Explain Like I'm 5)

Imagine resetting a forgotten house key for a member:

1. **Fulcrum (`app.fulcrumindia.online`) = The Front Desk.**  
   The user asks for a password reset here, and later types in their new password here.
2. **Supabase Auth (`bhaqaawsufwtjeqfifbv`) = The Security Officer.**  
   The officer checks if the email exists, prints a one-time secret pass (`#access_token` + `#refresh_token`), and checks that pass before updating the password vault.
3. **Hostinger DNS (`fulcrumindia.online`) = The Official City Signboard.**  
   DNS records tell Gmail, Outlook, and Yahoo: *"Yes, `notify.fulcrumindia.online` genuinely belongs to Fulcrum-India — don't put these emails in Spam!"*
4. **Resend (`smtp.resend.com`) = The Dedicated Postman.**  
   Supabase hands the reset email to Resend, and Resend delivers it cleanly from **`no-reply@notify.fulcrumindia.online`**.

> **Key takeaway:** Resend is *only* the postman — it never checks passwords or sees who is allowed in. **Resend fixes email delivery** (and unlocks custom templates + higher Supabase email limits), while **Fulcrum's recovery callback code** verifies the secret link and opens the password-change screen.

---

## 2. Why We Used Resend Instead of Gmail or Supabase's Free Mailer

| Method | What Happened / Limitation | Why Resend Won |
| :--- | :--- | :--- |
| **Supabase Built-In Free Mailer** | Strict rate limit (**2–4 emails/hour**), locks email template editing, and is not meant for public production users. | Resend gives **3,000 free emails/month**, raises Supabase's Auth SMTP limit to **30+/hour**, and unlocks template editing. |
| **Gmail App Password** | Google blocked **"App passwords"** for the account (*"The setting you are looking for is not available for your account"*). | Resend is built specifically for app emails and doesn't rely on personal Gmail security settings. |
| **Hostinger + Resend Subdomain (`notify.fulcrumindia.online`)** | Uses DNS records once — zero changes needed on your website Caddy proxy, VPS `.env`, or Docker containers. | Branded `@notify.fulcrumindia.online` sender with full DKIM/SPF deliverability. |

---

## 3. Step-by-Step: How the Resend Integration Was Set Up

### Step 1 — Create Your Sending Domain in Resend
1. Create a free account at **Resend** (`https://resend.com`).
2. Go to **Domains → Add Domain** and enter:
   * **Name:** `notify.fulcrumindia.online` *(using a `notify.` subdomain keeps your live website `app.fulcrumindia.online` and Caddy SSL untouched)*
   * **Region:** `Tokyo` *(closest region in Resend's list; Singapore was not listed)*
   * **Custom Return-Path:** `send` *(default)*
   * **Tracking Subdomain:** `links` *(default)*
   * **Enable Click Tracking:** **OFF** *(very important — keep OFF! See Section 6)*
   * **Enable Open Tracking:** **OFF**
   * **Enable Receiving:** **OFF** *(Fulcrum only sends outgoing auth emails)*
3. Click **+ Add domain**. Resend displays **3 DNS records** (1 TXT DKIM + 2 CNAME records).

---

### Step 2 — Add the 3 DNS Records in Hostinger (`fulcrumindia.online`)
Open **Hostinger → Domains → `fulcrumindia.online` → DNS / Nameservers → Manage DNS Records**.

> ⚠️ **Hostinger Name Rule:** Hostinger automatically adds `.fulcrumindia.online` to the **Name** box!  
> So typing `send.notify` creates `send.notify.fulcrumindia.online`. Never type `.fulcrumindia.online` twice!

Add these exact 3 records (copying the full values from your Resend screen, not truncated `...` previews):

| # | Record Purpose | Type | Hostinger **Name** Field | Value / Target (Copy full text from Resend) | TTL |
| :-: | :--- | :---: | :--- | :--- | :---: |
| **1** | **DKIM** (Anti-forgery stamp) | `TXT` | `resend._domainkey.notify` | Full `p=MIGfMA...` string from Resend | `3600` |
| **2** | **SPF / Bounce Path** | `CNAME` | `rsend.notify` | Full `rsend-ap...` host from Resend | `3600` |
| **3** | **Sending Subdomain** | `CNAME` | `send.notify` | Full `send.for...` host from Resend | `3600` |

* **Leave everything else untouched:** Do **not** edit or delete your existing `@` (`A`), `app` (`A`), `www` (`CNAME`), or Google verification (`TXT`) records.
* Return to Resend and click **Verify / I've added the records** until the status shows **Verified**.

---

### Step 3 — Generate a Private Resend API Key
1. In Resend, go to **API Keys → Create API Key**.
2. Name it clearly (e.g., `Fulcrum Supabase Auth`), allow sending on `notify.fulcrumindia.online`.
3. Copy the secret key (`re_...`) into a secure password manager.
   * **Security rule:** Never paste API keys into Git commits, `.md` docs, or screenshots.

---

### Step 4 — Connect Resend SMTP Inside Supabase
Open your Supabase project → **Authentication → Emails → SMTP Settings**:

| Supabase Field | Value to Enter |
| :--- | :--- |
| **Enable custom SMTP** | **ON** (green) |
| **Sender email address** | `no-reply@notify.fulcrumindia.online` |
| **Sender name** | `FULCRUM-INDIA` |
| **Host** | `smtp.resend.com` |
| **Port number** | `465` |
| **Username** | `resend` |
| **Password** | Your private Resend API key (`re_...`) |

Click **Save changes**. Notice you do **not** have to modify Docker, Caddy, or `.env` on the VPS for Supabase to use Resend!

---

## 4. What Happens Step-by-Step When a User Clicks "Forgot Password?"

```
[1] User opens https://app.fulcrumindia.online/ -> expands "🔑 Forgot Password?" -> clicks "Send Reset Link"
        │
        ▼
[2] services/auth.py -> send_password_reset() uses an isolated ephemeral Supabase client
    (redirects back to https://app.fulcrumindia.online/?type=recovery)
        │
        ▼
[3] Supabase Auth creates a single-use recovery verification link ({{ .ConfirmationURL }})
    and passes the email to Resend SMTP (smtp.resend.com:465)
        │
        ▼
[4] Resend delivers the email from no-reply@notify.fulcrumindia.online to user's inbox
        │
        ▼
[5] User clicks "Reset password" -> browser opens:
    https://app.fulcrumindia.online/?type=recovery#access_token=...&refresh_token=...
        │
        ▼
[6] services/auth_callback_component.py (fulcrum_auth_callback_bridge) reads #access_token
    inside the browser, wipes it cleanly from the URL bar (history.replaceState), and sends
    the tokens securely over Streamlit's WSS WebSocket to views/login.py
        │
        ▼
[7] services/auth.py -> verify_recovery_session_tokens() checks BOTH access_token &
    refresh_token on a clean temporary Supabase client -> opens the verified password form
        │
        ▼
[8] User sets new password -> complete_password_reset() updates password in Supabase Auth,
    signs out the temporary recovery session, and user signs in with the new password
```

### Why Did It Used to Say `"expired or already used"` Before the Code Fix?
* Web browsers **never send anything after `#`** (`#access_token=...`) to the server — only JavaScript running in the browser can read `#`.
* Previously, `views/login.py` saw `?type=recovery` arrive with no visible token and immediately threw `"expired or already used"` *before* the browser JavaScript helper could read `#access_token`, wiping the URL and refreshing the page.
* Replacing that with [`read_auth_callback`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/auth_callback_component.py#L80-L97) (Streamlit Components v2 WebSocket bridge) fixed it cleanly without even needing to customize Supabase's default `{{ .ConfirmationURL }}` email template!

---

## 5. What Other Emails Does This Power?

Now that Supabase Auth is wired to Resend (`smtp.resend.com:465`), **every** Supabase Auth email automatically sends through Resend from `no-reply@notify.fulcrumindia.online`:
* New Aspirant signup confirmation links
* Forgot Password reset links
* Email-change verification links
* Mentor / Guide / SME invite emails (when initiated via Supabase Auth)

---

## 6. Operational Checklist & Gotchas (Save Yourself Future Headaches)

1. **Keep Resend Click Tracking & Open Tracking OFF:**  
   Turning Click Tracking ON makes Resend wrap links in a tracking redirect (`links.notify.fulcrumindia.online/...`). Email scanners or tracking redirects can break or consume single-use Supabase recovery tokens (`#access_token=...`) before Fulcrum ever sees them.
2. **Check Redirect URLs in Supabase (`Authentication → URL Configuration`):**  
   Ensure `https://app.fulcrumindia.online/**` is listed under **Redirect URLs**. (If you ever run an isolated staging or local test at `http://localhost:8501`, add `http://localhost:8501/**` on your *staging* Supabase project — never rely on production for staging tests.)
3. **Where to Check If an Email Failed or Bounced:**  
   Open **Resend Dashboard → Emails / Logs** to see exact timestamps (`Delivered`, `Bounced`, or `Suppressed`).
4. **If You Create a Separate Staging Supabase Project Later:**  
   You don't need to re-verify DNS in Hostinger! Reuse the same verified `notify.fulcrumindia.online` domain in Resend, generate a second API key (e.g. `Fulcrum Staging Auth`), and paste the same **Step 4** settings into the staging Supabase project.
5. **Rotating Your API Key:**  
   Create a new key in **Resend → API Keys**, paste it into **Supabase → SMTP Settings → Password**, click **Save changes**, test one email, and then revoke the old key in Resend.

