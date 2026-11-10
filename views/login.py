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
from services.auth import (
    login_user,
    signup_aspirant,
    send_password_reset,
    complete_password_reset,
    verify_recovery_session_tokens,
    verify_recovery_token_hash,
    _classify_recovery_error,
    get_data_backend,
)
from services.auth_callback_component import read_auth_callback
from services.constants import MASTER_DISTRICTS_TN
from services.perf import get_active_tracker

def render_login_page():
    tracker = get_active_tracker("login_page")
    with tracker.stage("login_render_ms"):
        _render_login_page_impl()
    tracker.persist_to_session()


def _render_login_page_impl():
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

    # Check query parameters for email confirmation or password recovery
    query_params = st.query_params
    auth_type = str(query_params.get("type", "") or "").strip().lower()
    token_hash = str(query_params.get("token_hash") or query_params.get("token") or "").strip()
    acc_token_qp = str(query_params.get("access_token", "") or "").strip()
    ref_token_qp = str(query_params.get("refresh_token", "") or "").strip()
    auth_code = str(query_params.get("code", "") or "").strip()
    error_desc = str(query_params.get("error_description") or query_params.get("error_code") or query_params.get("error") or "").strip()
    backend = get_data_backend()

    # Security guardrail: reject & purge session tokens passed via browser query parameters
    if acc_token_qp or ref_token_qp:
        st.session_state.recovery_verified = False
        st.session_state.recovery_error = "Invalid callback format: session tokens cannot be passed in URL query parameters. Please open the link directly from your email."
        st.query_params.clear()
        st.rerun()

    # Step A: Catch provider-level callback errors immediately with distinct diagnostics
    if error_desc:
        st.session_state.recovery_verified = False
        _, clean_msg = _classify_recovery_error(Exception(error_desc))
        st.session_state.recovery_error = clean_msg
        st.query_params.clear()
        st.rerun()

    # Step B: Mount WebSocket-only Components v2 hash bridge (reads #access_token/#error without query params)
    waiting_for_hash_bridge = bool(
        backend == "supabase"
        and auth_type == "recovery"
        and not token_hash
        and not auth_code
        and not st.session_state.get("recovery_verified")
        and not st.session_state.get("recovery_error")
        and not st.session_state.get("_pending_recovery_token_hash")
    )
    cb_payload = None
    if backend == "supabase" and not st.session_state.get("recovery_verified"):
        cb_payload = read_auth_callback(expect_hash=waiting_for_hash_bridge)

    # Step C: Handle incoming WebSocket hash-fragment payload (default Supabase implicit confirmation/recovery)
    if backend == "supabase" and isinstance(cb_payload, dict):
        cb_status = cb_payload.get("status")
        cb_type = str(cb_payload.get("type") or auth_type or "").strip().lower()

        if cb_status == "error":
            raw_err = " ".join([
                str(cb_payload.get("error_code") or ""),
                str(cb_payload.get("error_description") or ""),
                str(cb_payload.get("error") or ""),
            ]).strip()
            _, clean_msg = _classify_recovery_error(Exception(raw_err or "invalid"))
            st.session_state.recovery_verified = False
            st.session_state.recovery_error = clean_msg
            st.query_params.clear()
            st.rerun()

        elif cb_status == "empty":
            st.session_state.recovery_verified = False
            st.session_state.recovery_error = "Missing recovery verification proof in the callback URL. Please open the password reset link directly from your email."
            st.query_params.clear()
            st.rerun()

        elif cb_status == "found":
            if cb_type in ("signup", "email", "email_change", "email_verification"):
                st.session_state.email_confirmed_notice = True
                st.query_params.clear()
                st.rerun()
            else:
                ok, verified_email, _, err_msg = verify_recovery_session_tokens(
                    cb_payload.get("access_token", ""),
                    cb_payload.get("refresh_token", ""),
                )
                if ok and verified_email:
                    st.session_state.recovery_verified = True
                    st.session_state.recovery_verified_email = verified_email
                    st.session_state._recovery_access_token = cb_payload.get("access_token", "")
                    st.session_state._recovery_refresh_token = cb_payload.get("refresh_token", "")
                    st.session_state.recovery_error = None
                    st.query_params.clear()
                    st.rerun()
                else:
                    st.session_state.recovery_verified = False
                    st.session_state.recovery_error = err_msg or "Recovery verification failed. Please request a new link."
                    st.query_params.clear()
                    st.rerun()

    # Step D: Handle query-param token_hash or PKCE code (if provided)
    if backend == "supabase" and not st.session_state.get("recovery_verified"):
        if token_hash and (auth_type == "recovery" or not auth_type):
            # Hold token_hash for deliberate user click so email scanners/prefetchers cannot burn single-use OTPs
            st.session_state._pending_recovery_token_hash = token_hash
            st.session_state.recovery_error = None
            st.query_params.clear()
            st.rerun()

        elif auth_code and (auth_type == "recovery" or not auth_type):
            # Strict PKCE check: NEVER exchange an authorization code without its matching verifier
            code_verifier = st.session_state.get("pkce_verifier")
            if not code_verifier:
                st.session_state.recovery_verified = False
                st.session_state.recovery_error = (
                    "This link uses a session-bound verification code whose browser verifier is missing "
                    "(this occurs when opening a PKCE link in a new tab, different browser, or mobile app). "
                    "Please request a new password reset link."
                )
                st.query_params.clear()
                st.rerun()
            else:
                from services.auth import _create_ephemeral_supabase_client
                rec_cli = _create_ephemeral_supabase_client()
                exchanged = False
                if rec_cli:
                    try:
                        res = rec_cli.auth.exchange_code_for_session({
                            "auth_code": auth_code,
                            "code_verifier": code_verifier,
                        })
                        sess = getattr(res, "session", None)
                        user_obj = getattr(res, "user", None)
                        if sess and user_obj and getattr(sess, "access_token", None) and getattr(sess, "refresh_token", None):
                            st.session_state.recovery_verified = True
                            st.session_state.recovery_verified_email = user_obj.email
                            st.session_state._recovery_access_token = sess.access_token
                            st.session_state._recovery_refresh_token = sess.refresh_token
                            st.session_state.recovery_error = None
                            st.query_params.clear()
                            exchanged = True
                            st.rerun()
                    except Exception as ex:
                        _, clean_msg = _classify_recovery_error(ex)
                        st.session_state.recovery_verified = False
                        st.session_state.recovery_error = clean_msg
                        st.query_params.clear()
                        st.rerun()
                if not exchanged:
                    st.session_state.recovery_verified = False
                    st.session_state.recovery_error = "Failed to verify authorization code. Please request a new reset link."
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

        if waiting_for_hash_bridge and not cb_payload:
            st.info("🔐 Verifying your password recovery link securely...")
            return

        if st.session_state.get("_pending_recovery_token_hash"):
            st.info("🔐 Confirm below to verify your one-time recovery link and proceed to password reset.")
            col_th1, col_th2 = st.columns(2)
            with col_th1:
                if st.button("Verify & Continue", key="btn_verify_token_hash", use_container_width=True):
                    pending_th = st.session_state.pop("_pending_recovery_token_hash", "")
                    ok, v_email, acc_t, ref_t, _, err_msg = verify_recovery_token_hash(pending_th)
                    if ok and v_email:
                        st.session_state.recovery_verified = True
                        st.session_state.recovery_verified_email = v_email
                        st.session_state._recovery_access_token = acc_t
                        st.session_state._recovery_refresh_token = ref_t
                        st.session_state.recovery_error = None
                    else:
                        st.session_state.recovery_verified = False
                        st.session_state.recovery_error = err_msg or "Recovery token verification failed."
                    st.rerun()
            with col_th2:
                if st.button("← Cancel", key="btn_cancel_token_hash", use_container_width=True):
                    st.session_state.pop("_pending_recovery_token_hash", None)
                    st.rerun()
            return

        if auth_type in ["signup", "email_verification"] or st.session_state.get("email_confirmed_notice"):
            st.success("✅ Email confirmed successfully. Please sign in with your email and password.")
            st.session_state.email_confirmed_notice = False

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
                            access_token=st.session_state.get("_recovery_access_token"),
                            refresh_token=st.session_state.get("_recovery_refresh_token"),
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
                            st.session_state._recovery_access_token = None
                            st.session_state._recovery_refresh_token = None
                            st.session_state.sb_access_token = None
                            st.session_state.sb_refresh_token = None
                            st.session_state.supabase_client = None
                            st.session_state.show_recovery_form = False
                            st.session_state.password_reset_success = True
                            st.session_state.input_login_email = verified_email
                            st.query_params.clear()
                            st.rerun()
                        else:
                            if err and "different" in err.lower():
                                st.error("New password must be different from your current password.")
                            elif err and "network timeout" in err.lower():
                                st.error(err)
                            elif err and ("expired" in err.lower() or "invalid" in err.lower() or "already been used" in err.lower()):
                                st.session_state.recovery_verified = False
                                st.session_state._recovery_access_token = None
                                st.session_state._recovery_refresh_token = None
                                st.session_state.recovery_error = err
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
                st.session_state._recovery_access_token = None
                st.session_state._recovery_refresh_token = None
                st.session_state.sb_access_token = None
                st.session_state.sb_refresh_token = None
                st.session_state.supabase_client = None
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

            # Password Reset Expander (wrapped in st.form to prevent unnecessary reruns)
            backend = get_data_backend()
            is_fp_open = bool(st.session_state.get("open_forgot_password", False))
            with st.expander("🔑 Forgot Password?", expanded=is_fp_open):
                if backend == "supabase":
                    st.markdown("<p style='font-size:0.8rem; color:#64748B;'>Enter your registered email address to receive a secure password recovery link.</p>", unsafe_allow_html=True)
                    with st.form("forgot_pwd_form", clear_on_submit=False):
                        col_fp1, col_fp2 = st.columns([2, 1])
                        with col_fp1:
                            fp_email = st.text_input("Registered Email", placeholder="name@domain.in", key="input_fp_email")
                        with col_fp2:
                            st.write("")
                            st.write("")
                            submit_fp = st.form_submit_button("Send Reset Link", use_container_width=True)

                        if submit_fp:
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
        # TAB 2: PUBLIC ASPIRANT SIGNUP SURFACE (Aspirants Only — inside st.form)
        # ─────────────────────────────────────────────────────────────
        with tab_signup:
            st.markdown("<p style='font-size: 0.84rem; color: #64748B; margin-bottom: 1.25rem;'>Register as an entrepreneur to access mentorship and scheme intelligence.</p>", unsafe_allow_html=True)

            with st.form("signup_form", clear_on_submit=False):
                s_name = st.text_input("Full Name", placeholder="Ravi Kumar", key="signup_name")
                s_email = st.text_input("Work / Personal Email", placeholder="ravi.kumar@milletfoods.in", key="signup_email")
                
                c_ph, c_dist = st.columns(2)
                with c_ph:
                    s_phone = st.text_input("Mobile Number", placeholder="9876543210", key="signup_phone")
                with c_dist:
                    s_dist = st.selectbox("District (Tamil Nadu)", MASTER_DISTRICTS_TN, index=13, key="signup_district")

                s_other_dist = st.text_input(
                    "If 'Other District / Non-TN', specify District / City / State",
                    placeholder="e.g. Bengaluru (Karnataka), Mumbai (Maharashtra)",
                    key="signup_other_district"
                )

                c_p1, c_p2 = st.columns(2)
                with c_p1:
                    s_pwd = st.text_input("Create Password", type="password", placeholder="••••••••", key="signup_pwd")
                with c_p2:
                    s_pwd_confirm = st.text_input("Confirm Password", type="password", placeholder="••••••••", key="signup_pwd2")

                st.write("")
                submit_signup = st.form_submit_button("CREATE ASPIRANT ACCOUNT", use_container_width=True)

                if submit_signup:
                    s_final_district = s_dist
                    if s_dist == "Other District / Non-TN (Specify)":
                        s_final_district = (s_other_dist or "").strip()

                    if not s_name or not s_email or not s_pwd:
                        st.error("Please fill in all mandatory fields.")
                    elif s_pwd != s_pwd_confirm:
                        st.error("Passwords do not match.")
                    elif len(s_pwd) < 6:
                        st.error("Password must be at least 6 characters long.")
                    elif s_dist == "Other District / Non-TN (Specify)" and not s_final_district:
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


