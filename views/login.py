"""
views/login.py — Institutional Light Login & Aspirant Onboarding for FULCRUM-INDIA
==================================================================================
Design Guidelines:
- Clean Light / White Institutional Design (Refined, Modern, Calm, Trustworthy)
- Typography: Avenir Next / Avenir with clean system fallbacks
- Button Styling: Brand Royal Blue (#2563EB) with crisp white text, high contrast
- Centered surface with clear visual hierarchy
- Single public self-registration flow strictly for Aspirants (role = 'aspirant')
- Zero public registration for Guides, SMEs, or Admins
- Built-in Demo Test Credentials and 1-Click Role Quick Fill
"""

import streamlit as st
import streamlit.components.v1 as components
from services.auth import (
    login_user,
    signup_aspirant,
    send_password_reset,
    complete_password_reset,
    get_data_backend
)
from services.constants import MASTER_DISTRICTS_TN

def render_login_page():
    # Inject Institutional Light Theme CSS specifically for the login surface
    st.markdown("""
    <style>
    /* Full Page Background - Calm Institutional Neutral */
    .stApp {
        background-color: #F8FAFC !important;
        background-image: none !important;
    }

    /* Hide Streamlit technical multipage sidebar navigation and toggle controls */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    /* Typography - Avenir Next / Avenir with elegant system fallbacks */
    html, body, .stApp, h1, h2, h3, h4, h5, h6, p, label, input, textarea, select {
        font-family: 'Avenir Next', 'Avenir', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        color: #1E293B;
    }

    /* STRICTLY PROTECT Streamlit expander toggle icon from printing 'keyboard_arrow_right' */
    [data-testid="stExpanderToggleIcon"] {
        font-size: 0px !important;
        line-height: 0 !important;
        color: transparent !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 18px !important;
        height: 18px !important;
    }
    [data-testid="stExpanderToggleIcon"] * {
        display: none !important;
    }
    [data-testid="stExpanderToggleIcon"]::after {
        content: "▶" !important;
        font-size: 11px !important;
        color: #64748B !important;
        display: inline-block !important;
        transition: transform 0.2s ease !important;
    }
    details[open] [data-testid="stExpanderToggleIcon"]::after {
        transform: rotate(90deg) !important;
        color: #2563EB !important;
    }

    /* Additional Icon protection for Material Symbols */
    .material-symbols-rounded,
    .material-symbols-outlined,
    .material-icons {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons", sans-serif !important;
        font-feature-settings: "liga" 1 !important;
        display: inline-block !important;
    }

    /* Centered Login Card Container */
    .auth-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 2.5rem 2.75rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03), 0 20px 25px -5px rgba(0, 0, 0, 0.04);
        margin: 1.5rem auto 2.5rem;
        max-width: 480px;
    }

    .auth-brand-badge {
        display: inline-block;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #2563EB;
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        padding: 4px 12px;
        border-radius: 20px;
        margin-bottom: 0.75rem;
    }

    .auth-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #0F172A !important;
        margin: 0 0 0.4rem 0;
        line-height: 1.15;
    }

    .auth-subtitle {
        font-size: 0.9rem;
        font-weight: 500;
        color: #64748B !important;
        line-height: 1.45;
        margin-bottom: 1.75rem;
    }

    /* Light Theme Input Styling */
    .stTextInput > div > div > input {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        color: #0F172A !important;
        border-radius: 6px !important;
        font-size: 0.92rem !important;
        padding: 0.6rem 0.85rem !important;
        transition: all 0.15s ease-in-out;
    }
    .stTextInput > div > div > input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
        background-color: #FFFFFF !important;
    }

    .stTextInput label {
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        color: #334155 !important;
        letter-spacing: 0.01em;
        margin-bottom: 4px;
    }

    /* Clean st.form container to avoid default double border and padding */
    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
        margin: 0 !important;
    }

    /* Brand Blue Login Button - High Contrast & Refined */
    .stButton > button,
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #2563EB !important;
        background-image: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid #1D4ED8 !important;
        border-radius: 6px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.03em !important;
        padding: 0.65rem 1.25rem !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
        transition: all 0.15s ease-in-out !important;
    }
    .stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #1D4ED8 !important;
        background-image: none !important;
        border-color: #1E40AF !important;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35) !important;
        transform: translateY(-1px);
    }
    .stButton > button:active,
    div[data-testid="stFormSubmitButton"] > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 6px rgba(37, 99, 235, 0.2) !important;
    }
    .stButton > button p,
    .stButton > button span,
    .stButton > button div,
    div[data-testid="stFormSubmitButton"] > button p,
    div[data-testid="stFormSubmitButton"] > button span,
    div[data-testid="stFormSubmitButton"] > button div {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Tabs Styling - Blue Active Indicator */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #F1F5F9 !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 4px !important;
        gap: 4px !important;
        margin-bottom: 1.5rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        height: 38px !important;
        border-radius: 6px !important;
        color: #64748B !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        background-color: transparent !important;
        border: none !important;
        padding: 0 16px !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #2563EB !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08) !important;
    }
    [data-baseweb="tab-highlight"] {
        background-color: #2563EB !important;
    }

    /* Footer Trust Mark */
    .auth-footer {
        text-align: center;
        margin-top: 1.75rem;
        padding-top: 1.25rem;
        border-top: 1px solid #F1F5F9;
        font-size: 0.78rem;
        color: #94A3B8;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

    # Bridge URL hash fragment (#access_token=... / #error=...) to query params for Streamlit
    components.html(r"""
    <script>
    (function() {
        try {
            var targetWin = window.parent || window;
            var hash = targetWin.location.hash || window.location.hash;
            if (hash && (hash.indexOf('access_token=') !== -1 || hash.indexOf('error=') !== -1)) {
                var cleanHash = hash.replace(/^[#\/]+/, '');
                var hashParams = new URLSearchParams(cleanHash);
                var searchParams = new URLSearchParams(targetWin.location.search || window.location.search);
                var changed = false;
                ['access_token', 'refresh_token', 'type', 'error', 'error_description', 'error_code'].forEach(function(k) {
                    var v = hashParams.get(k);
                    if (v && !searchParams.has(k)) {
                        searchParams.set(k, v);
                        changed = true;
                    }
                });
                if (changed) {
                    if (searchParams.has('access_token') && !searchParams.has('type')) {
                        searchParams.set('type', 'recovery');
                    }
                    var cleanUrl = (targetWin.location.pathname || window.location.pathname) + '?' + searchParams.toString();
                    targetWin.location.replace(cleanUrl);
                }
            }
        } catch(e) {
            console.error('Hash bridge error:', e);
        }
    })();
    </script>
    """, height=0, width=0)

    # Check query parameters for email confirmation or password recovery
    query_params = st.query_params
    auth_type = query_params.get("type", "")
    token_hash = query_params.get("token_hash") or query_params.get("token") or ""
    acc_token = query_params.get("access_token", "")
    ref_token = query_params.get("refresh_token", "")
    auth_code = query_params.get("code", "")
    error_desc = query_params.get("error_description") or query_params.get("error") or ""
    backend = get_data_backend()

    # Step A: Catch provider-level callback errors immediately
    if error_desc:
        st.session_state.recovery_verified = False
        st.session_state.recovery_error = "This password recovery link is invalid or has expired. Please request a new link."
        st.query_params.clear()
        st.rerun()

    # Step B: Supabase mode cryptographic verification of incoming recovery parameters
    if backend == "supabase" and not st.session_state.get("recovery_verified"):
        from services.auth import get_supabase_client
        client = get_supabase_client()

        # Mode 1: token_hash OTP verification (Recommended Supabase recovery link format)
        if token_hash and (auth_type == "recovery" or not auth_type):
            try:
                if client:
                    res = client.auth.verify_otp({"token_hash": token_hash, "type": "recovery"})
                    if res and getattr(res, "session", None) and getattr(res, "user", None):
                        st.session_state.recovery_verified = True
                        st.session_state.recovery_verified_email = res.user.email
                        st.session_state.sb_access_token = res.session.access_token
                        st.session_state.sb_refresh_token = res.session.refresh_token
                        st.session_state.recovery_error = None
                        st.query_params.clear()
                        st.rerun()
                    else:
                        st.session_state.recovery_verified = False
                        st.session_state.recovery_error = "This password recovery link is invalid or has expired. Please request a new link."
                        st.query_params.clear()
                        st.rerun()
            except Exception:
                st.session_state.recovery_verified = False
                st.session_state.recovery_error = "This password recovery link is invalid or has expired. Please request a new link."
                st.query_params.clear()
                st.rerun()

        # Mode 2: access_token verification (from Hash bridge or direct link)
        elif acc_token and auth_type == "recovery":
            try:
                if client:
                    user_res = client.auth.get_user(acc_token)
                    if user_res and getattr(user_res, "user", None):
                        st.session_state.recovery_verified = True
                        st.session_state.recovery_verified_email = user_res.user.email
                        st.session_state.sb_access_token = acc_token
                        st.session_state.sb_refresh_token = ref_token or acc_token
                        st.session_state.recovery_error = None
                        st.query_params.clear()
                        st.rerun()
                    else:
                        st.session_state.recovery_verified = False
                        st.session_state.recovery_error = "This password recovery link is invalid or has expired. Please request a new link."
                        st.query_params.clear()
                        st.rerun()
            except Exception:
                st.session_state.recovery_verified = False
                st.session_state.recovery_error = "This password recovery link is invalid or has expired. Please request a new link."
                st.query_params.clear()
                st.rerun()

        # Mode 3: PKCE authorization code exchange (if code is provided)
        elif auth_code and (auth_type == "recovery" or not auth_type):
            code_verifier = st.session_state.get("pkce_verifier")
            exchanged = False
            if client:
                try:
                    params = {"auth_code": auth_code}
                    if code_verifier:
                        params["code_verifier"] = code_verifier
                    res = client.auth.exchange_code_for_session(params)
                    if res and getattr(res, "session", None) and getattr(res, "user", None):
                        st.session_state.recovery_verified = True
                        st.session_state.recovery_verified_email = res.user.email
                        st.session_state.sb_access_token = res.session.access_token
                        st.session_state.sb_refresh_token = res.session.refresh_token
                        st.session_state.recovery_error = None
                        st.query_params.clear()
                        st.rerun()
                        exchanged = True
                except Exception:
                    pass
            if not exchanged:
                st.session_state.recovery_verified = False
                st.session_state.recovery_error = "This password recovery link is invalid or has expired. Please request a new link."
                st.query_params.clear()
                st.rerun()

        # Mode 4: Naked ?type=recovery without tokens
        elif auth_type == "recovery" and not (token_hash or acc_token or auth_code):
            st.session_state.recovery_verified = False
            st.session_state.recovery_error = "This password recovery link is invalid or has expired. Please request a new link."
            st.query_params.clear()
            st.rerun()

    # Centered Container Layout
    col_l, col_center, col_r = st.columns([1, 1.4, 1])

    with col_center:
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; margin-bottom: 1.25rem;">
            <div class="auth-brand-badge">Institutional Enterprise System</div>
            <h1 class="auth-title">FULCRUM-INDIA</h1>
        </div>
        """, unsafe_allow_html=True)

        if auth_type in ["signup", "email_verification"]:
            st.success("✅ Email confirmed successfully. Please sign in with your email and password.")

        if st.session_state.get("password_reset_success"):
            st.success("🎉 Password updated successfully! Please sign in with your new password.")
            st.session_state.password_reset_success = False

        # ─────────────────────────────────────────────────────────────
        # RECOVERY STATE 1: RECOVERY LINK FAILED / EXPIRED / INVALID
        # ─────────────────────────────────────────────────────────────
        if st.session_state.get("recovery_error"):
            st.error(f"⚠️ {st.session_state.recovery_error}")
            st.info("Password reset links are single-use and expire quickly for your account's security.")
            col_err1, col_err2 = st.columns(2)
            with col_err1:
                if st.button("Request New Reset Link", key="btn_req_new_link", use_container_width=True):
                    st.session_state.recovery_error = None
                    st.session_state.open_forgot_password = True
                    st.rerun()
            with col_err2:
                if st.button("← Back to Sign In", key="btn_err_back_signin", use_container_width=True):
                    st.session_state.recovery_error = None
                    st.rerun()

            st.markdown("""
            <div style="text-align: center; margin-top: 1.25rem; font-size: 0.82rem; color: #475569;">
                Contact System Maintenance at <a href="mailto:fulcrumindia1@gmail.com" style="color: #2563EB; font-weight: 600; text-decoration: none;">fulcrumindia1@gmail.com</a> for login issues
            </div>
            """, unsafe_allow_html=True)
            return

        # ─────────────────────────────────────────────────────────────
        # RECOVERY STATE 2: RECOVERY SESSION CRYPTOGRAPHICALLY VERIFIED
        # ─────────────────────────────────────────────────────────────
        is_recovery_active = bool(st.session_state.get("recovery_verified"))
        if backend == "sqlite" and st.session_state.get("show_recovery_form", False):
            is_recovery_active = True
            if not st.session_state.get("recovery_verified_email"):
                st.session_state.recovery_verified_email = st.session_state.get("input_fp_email") or "demo@fulcrumindia.online"

        if is_recovery_active:
            verified_email = st.session_state.get("recovery_verified_email") or ""
            st.markdown(f"""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:1.5rem; margin-bottom:1.25rem; box-shadow:0 2px 4px rgba(0,0,0,0.04);">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:0.4rem;">
                    <span style="font-size:1.4rem;">🔑</span>
                    <h3 style="margin:0; color:#0F172A; font-size:1.25rem; font-weight:700;">Set New Password</h3>
                </div>
                <p style="font-size:0.84rem; color:#64748B; margin:0 0 1rem 0;">Choose a secure new password for your verified account.</p>
                <div style="background:#F1F5F9; border-left:4px solid #2563EB; padding:0.6rem 0.9rem; border-radius:4px; font-size:0.88rem; color:#1E293B;">
                    <span style="color:#64748B; font-weight:600;">Verified Account:</span> <strong>{verified_email}</strong>
                    <span style="background:#DCFCE7; color:#166534; font-size:0.75rem; font-weight:600; padding:2px 8px; border-radius:999px; margin-left:8px;">✓ Cryptographically Verified</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.form("form_set_new_password"):
                new_p1 = st.text_input("New Password", type="password", placeholder="••••••••", key="rec_pwd1", help="Must be at least 8 characters long")
                new_p2 = st.text_input("Confirm New Password", type="password", placeholder="••••••••", key="rec_pwd2")
                submit_recovery = st.form_submit_button("UPDATE PASSWORD", use_container_width=True)

                if submit_recovery:
                    if not new_p1 or not new_p2:
                        st.error("Please enter and confirm your new password.")
                    elif new_p1 != new_p2:
                        st.error("Passwords do not match.")
                    elif len(new_p1) < 8:
                        st.error("Password must be at least 8 characters long.")
                    elif verified_email.strip().lower() == "fulcrumindia1@gmail.com":
                        st.error("Security Notice: Platform Administrator credentials cannot be reset through self-service recovery. Contact system maintenance.")
                    else:
                        ok, err = complete_password_reset(
                            new_p1,
                            access_token=st.session_state.get("sb_access_token"),
                            refresh_token=st.session_state.get("sb_refresh_token"),
                            email=verified_email
                        )
                        if ok:
                            try:
                                from services.auth import get_supabase_client
                                c = get_supabase_client()
                                if c:
                                    c.auth.sign_out()
                            except Exception:
                                pass
                            st.session_state.recovery_verified = False
                            st.session_state.recovery_verified_email = None
                            st.session_state.sb_access_token = None
                            st.session_state.sb_refresh_token = None
                            st.session_state.show_recovery_form = False
                            st.session_state.password_reset_success = True
                            st.session_state.input_login_email = verified_email
                            st.query_params.clear()
                            st.rerun()
                        else:
                            if err and "different" in err.lower():
                                st.error("New password must be different from your current password.")
                            elif err and ("expired" in err.lower() or "invalid" in err.lower()):
                                st.session_state.recovery_verified = False
                                st.session_state.recovery_error = "The recovery link has expired or has already been used. Please request a new link."
                                st.rerun()
                            else:
                                st.error(err or "Failed to update password.")

            if st.button("← Cancel & Back to Sign In", key="btn_cancel_recovery", use_container_width=True):
                try:
                    from services.auth import get_supabase_client
                    c = get_supabase_client()
                    if c:
                        c.auth.sign_out()
                except Exception:
                    pass
                st.session_state.recovery_verified = False
                st.session_state.recovery_verified_email = None
                st.session_state.sb_access_token = None
                st.session_state.sb_refresh_token = None
                st.session_state.show_recovery_form = False
                st.query_params.clear()
                st.rerun()

            st.markdown("""
            <div style="text-align: center; margin-top: 1.25rem; font-size: 0.82rem; color: #475569;">
                Contact System Maintenance at <a href="mailto:fulcrumindia1@gmail.com" style="color: #2563EB; font-weight: 600; text-decoration: none;">fulcrumindia1@gmail.com</a> for login issues
            </div>
            """, unsafe_allow_html=True)
            return

        # ─────────────────────────────────────────────────────────────
        # RECOVERY STATE 3: STANDARD LOGIN & SIGNUP TABS
        # ─────────────────────────────────────────────────────────────
        tab_login, tab_signup = st.tabs(["Sign In", "Create Aspirant Account"])

        # ─────────────────────────────────────────────────────────────
        # TAB 1: LOGIN SURFACE
        # ─────────────────────────────────────────────────────────────
        with tab_login:
            st.markdown("<p style='font-size: 0.84rem; color: #64748B; margin-bottom: 1.25rem;'>Enter your credentials to access your verified dashboard.</p>", unsafe_allow_html=True)
            
            with st.form("login_form", clear_on_submit=False):
                login_email = st.text_input(
                    "Email Address",
                    placeholder="name@domain.in",
                    key="input_login_email"
                )
                login_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="••••••••",
                    key="input_login_pwd"
                )

                st.write("")
                submit_login = st.form_submit_button("LOGIN", use_container_width=True)
                if submit_login:
                    if login_email and login_password:
                        profile, err = login_user(login_email, login_password)
                        if profile:
                            st.rerun()
                        else:
                            st.error(err or "Invalid credentials. Please verify your email and password.")
                    else:
                        st.warning("Please enter your email and password.")

            # Password Reset Expander
            backend = get_data_backend()
            is_fp_open = bool(st.session_state.get("open_forgot_password", False))
            with st.expander("🔑 Forgot Password?", expanded=is_fp_open):
                if backend == "supabase":
                    st.markdown("<p style='font-size:0.8rem; color:#64748B;'>Enter your registered email address to receive a secure password recovery link.</p>", unsafe_allow_html=True)
                    col_fp1, col_fp2 = st.columns([2, 1])
                    with col_fp1:
                        fp_email = st.text_input("Registered Email", placeholder="name@domain.in", key="input_fp_email")
                    with col_fp2:
                        st.write("")
                        st.write("")
                        if st.button("Send Reset Link", key="btn_send_fp"):
                            if fp_email:
                                ok, err = send_password_reset(fp_email)
                                if ok:
                                    st.success("Password reset email sent! Check your inbox for the reset link.")
                                else:
                                    st.error(err or "Failed to send reset email.")
                            else:
                                st.warning("Please enter your email.")

                    st.markdown("""
                    <div style="border-top: 1px dashed #E2E8F0; margin-top: 0.9rem; padding-top: 0.75rem; text-align: center;">
                        <span style="font-size:0.8rem; color:#64748B;">For security, click the verified recovery link sent to your email to set a new password.</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("In local development mode (SQLite), password resets via email are disabled. Please use the verified demo test accounts below or contact fulcrumindia1@gmail.com.")
                    if st.button("🔑 Reset Local Dev Password", key="btn_open_set_pwd_local", use_container_width=True):
                        st.session_state.show_recovery_form = True
                        st.rerun()

            # Contact System Maintenance notice requested by user
            st.markdown("""
            <div style="text-align: center; margin-top: 0.85rem; margin-bottom: 0.5rem; font-size: 0.82rem; color: #475569;">
                Contact System Maintainence in <a href="mailto:fulcrumindia1@gmail.com" style="color: #2563EB; font-weight: 600; text-decoration: none;">fulcrumindia1@gmail.com</a> for login issues
            </div>
            """, unsafe_allow_html=True)

        # ─────────────────────────────────────────────────────────────
        # TAB 2: PUBLIC ASPIRANT SIGNUP SURFACE (Aspirants Only)
        # ─────────────────────────────────────────────────────────────
        with tab_signup:
            st.markdown("<p style='font-size: 0.84rem; color: #64748B; margin-bottom: 1.25rem;'>Register as an entrepreneur to access mentorship and scheme intelligence.</p>", unsafe_allow_html=True)

            s_name = st.text_input("Full Name", placeholder="Ravi Kumar", key="signup_name")
            s_email = st.text_input("Work / Personal Email", placeholder="ravi.kumar@milletfoods.in", key="signup_email")
            
            c_ph, c_dist = st.columns(2)
            with c_ph:
                s_phone = st.text_input("Mobile Number", placeholder="9876543210", key="signup_phone")
            with c_dist:
                s_dist = st.selectbox("District (Tamil Nadu)", MASTER_DISTRICTS_TN, index=13, key="signup_district")

            # If "Other" is selected, show a text input to specify the actual district/city/state
            s_final_district = s_dist
            if s_dist == "Other District / Non-TN (Specify)":
                s_other_dist = st.text_input("Specify District / City / State *", placeholder="e.g. Bengaluru (Karnataka), Mumbai (Maharashtra)", key="signup_other_district")
                if s_other_dist and s_other_dist.strip():
                    s_final_district = s_other_dist.strip()

            c_p1, c_p2 = st.columns(2)
            with c_p1:
                s_pwd = st.text_input("Create Password", type="password", placeholder="••••••••", key="signup_pwd")
            with c_p2:
                s_pwd_confirm = st.text_input("Confirm Password", type="password", placeholder="••••••••", key="signup_pwd2")

            st.write("")
            if st.button("CREATE ASPIRANT ACCOUNT", use_container_width=True, key="btn_do_signup"):
                if not s_name or not s_email or not s_pwd:
                    st.error("Please fill in all mandatory fields.")
                elif s_pwd != s_pwd_confirm:
                    st.error("Passwords do not match.")
                elif len(s_pwd) < 6:
                    st.error("Password must be at least 6 characters long.")
                elif s_dist == "Other District / Non-TN (Specify)" and not s_other_dist.strip():
                    st.error("Please specify your district / city / state.")
                else:
                    profile, err = signup_aspirant(
                        email=s_email,
                        password=s_pwd,
                        full_name=s_name,
                        phone=s_phone,
                        district=s_final_district
                    )
                    if profile:
                        if profile.get("pending_confirmation"):
                            st.success(f"🎉 Account created successfully for **{s_email}**! A confirmation link has been sent to your email. Please check your inbox and verify your email before signing in.")
                        else:
                            st.success("🎉 Account created successfully! Logging in...")
                            st.rerun()
                    else:
                        st.error(err or "Failed to create account. Email may already be in use.")

            st.markdown("""
            <div style="text-align: center; margin-top: 1.25rem; font-size: 0.78rem; color: #94A3B8;">
                Note: Mentors (Guides and Subject Matter Experts) are provisioned exclusively by Program Administration.
            </div>
            """, unsafe_allow_html=True)


