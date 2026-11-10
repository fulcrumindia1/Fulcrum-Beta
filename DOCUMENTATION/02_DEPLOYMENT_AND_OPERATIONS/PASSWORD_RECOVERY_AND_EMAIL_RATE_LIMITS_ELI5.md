# FULCRUM-INDIA — PASSWORD RECOVERY & EMAIL RATE LIMITING GUIDE (ELI5)

**Target Audience:** Non-technical operators, administrators, and developers  
**System:** FULCRUM-BETA (Production Cluster B)  
**Last Updated:** November 10, 2026  

---

## 1. THE BIG PICTURE (ELI5 EXPLANATION)

### How Password Reset Works in Fulcrum
1. A user enters their email address and clicks **"Send Reset Link"**.
2. Fulcrum sends a request to **Supabase Auth**.
3. Supabase sends an email to the user with a special one-time security link.
4. The user opens the email in Gmail/Outlook and clicks the link.
5. The link opens `https://app.fulcrumindia.online`, where Fulcrum cryptographically verifies the link.
6. Fulcrum displays the **"Set New Password"** screen with the user's email locked in (they cannot accidentally mistype it).
7. The user enters a new password, clicks **"UPDATE PASSWORD"**, and can immediately log in!

---

## 2. WHY DID "EMAIL RATE LIMIT EXCEEDED" HAPPEN?

When you saw the error:
> `Password reset request failed: email rate limit exceeded`

Here is what happened under the hood:

### 1. Supabase's Built-in Mailer Quota
* Every Supabase project comes with a **free built-in email service** meant only for basic initial testing.
* Because this mail service is shared across thousands of users, Supabase enforces a strict limit: **only 2 to 3 emails per hour**.
* If you click "Send Reset Link" 3 times in a row while testing, Supabase temporarily blocks automated emails for about 1 hour to prevent spam.

### 2. The 60-Second Cooldown Timer
* Supabase also enforces an anti-spam cooldown: the same email address cannot request a reset email more than once every **60 seconds**.
* If you click "Send Reset Link" immediately after sending one, it will say: *"For security purposes, you can only request this after XX seconds."*

> [!NOTE]
> **This is NOT a bug in Fulcrum code.** It is a built-in safety rate limit on Supabase's free shared email server.

---

## 3. HOW TO BYPASS THE RATE LIMIT DURING TESTING (ADMIN DIRECT LINK)

If you need to test password reset right now without waiting 1 hour for Supabase's quota to reset:

You can generate a direct recovery link from the server using the Supabase Admin API. This bypasses the email mailer completely.

### The Direct URL Format
```text
https://app.fulcrumindia.online/?token_hash=<TOKEN_HASH>&type=recovery
```

When you paste this URL directly into your browser:
* Fulcrum connects directly to Supabase via `verify_otp`.
* The session is verified in 1 millisecond.
* The Set New Password form opens immediately!

---

## 4. HOW TO REMOVE THE EMAIL LIMIT PERMANENTLY FOR PRODUCTION

For your real production launch with multiple users, you should connect a free **Custom SMTP** provider in Supabase. This permanently removes the 3-emails/hour restriction and allows thousands of emails per month.

### Recommended Free Email Providers:
1. **Resend** ([resend.com](https://resend.com)) — Free tier gives 3,000 emails/month (takes 2 minutes to set up).
2. **Brevo / Sendinblue** ([brevo.com](https://brevo.com)) — Free tier gives 300 emails/day (9,000/month).
3. **Google Workspace SMTP** — If you already have `fulcrumindia1@gmail.com` or custom Google domain.

### Step-by-Step Setup in Supabase:
1. Create a free account at [Resend.com](https://resend.com) and get your **API Key / SMTP credentials**:
   * **Host:** `smtp.resend.com`
   * **Port:** `465` (or `587`)
   * **Username:** `resend`
   * **Password:** `re_your_api_key_here`
2. Open your **Supabase Dashboard** ➔ Go to **Authentication** ➔ **Providers** ➔ Click **Email**.
3. Scroll down to **Custom SMTP** and toggle it **ON**.
4. Fill in the Host, Port, Username, and Password.
5. Set **Sender Email** to your domain (e.g., `support@fulcrumindia.online`).
6. Click **Save changes**.

> [!TIP]
> Once Custom SMTP is connected, the `email rate limit exceeded` error will disappear completely for all users!

---

## 5. TECHNICAL DEEP DIVE: PKCE VS. IMPLICIT VS. TOKEN HASH

For technical operators and developers, here is why password resets previously broke and how the architecture was redesigned:

### 1. The PKCE "New Browser Tab" Breakdown
* Modern Supabase defaults to `flow_type="pkce"`.
* When a user requests a password reset, a `code_verifier` is stored in the browser/client memory.
* When the user clicks the reset link in their email client (like Gmail or mobile mail), it opens in a **new browser tab / new session**.
* In a server-rendered app like Streamlit, that new tab starts with a **blank session state** without the originating `code_verifier`.
* Calling `exchange_code_for_session({"auth_code": code})` without a verifier throws HTTP 400: `both auth code and code verifier should be non-empty`.

### 2. The Hash Fragment Problem (RFC 3986)
* When Supabase uses implicit redirect flow, it redirects to `https://app.fulcrumindia.online/#access_token=...`.
* Under HTTP/RFC 3986, web browsers **never send `#...` fragments to web servers**.
* Streamlit Python only saw an empty query string.

### 3. How Fulcrum 2.1 Resolved Both:
1. **Implicit Flow Client:** In `services/auth.py`, `get_supabase_client()` explicitly sets `ClientOptions(flow_type="implicit")`. This prevents Supabase from generating PKCE code challenges for password resets.
2. **Iframe Hash Fragment Bridge:** In `views/login.py`, `streamlit.components.v1.html` runs a tiny client-side JavaScript snippet in an iframe that reads `window.parent.location.hash`, extracts `access_token`, and seamlessly replaces it with query parameters (`?access_token=...`) so Streamlit Python receives it.
3. **Stateless `token_hash` Verification:** Fulcrum supports direct OTP verification via `client.auth.verify_otp({"token_hash": token_hash, "type": "recovery"})`, which is completely stateless and works across any device or private window.
4. **UI Guardrail:** The "Set New Password" form renders **ONLY** if `st.session_state.recovery_verified is True`. The email is shown as a read-only verified badge (no editable email field).
5. **Token Purging:** Once verified, `st.query_params.clear()` immediately purges all sensitive tokens from the browser URL bar.
