"""
services/auth.py — Authentication & RBAC Service for FULCRUM-INDIA
===================================================================
Manages Supabase Auth, session tokens, and database-driven user roles.
Supports dual backend architecture:
- Primary: Supabase Auth & PostgreSQL with RLS (Production & Cloud Dev)
- Fallback: SQLite cluster_a.db (Explicit Local Dev & Offline Testing Only)
No hardcoded secrets. Deterministic backend selection via DATA_BACKEND.
"""

import os
import json
import streamlit as st
from datetime import datetime, timezone
from typing import Optional, Tuple, Dict, Any, List

try:
    from supabase import create_client, Client, ClientOptions
except ImportError:
    create_client = None
    ClientOptions = None

# Local fallback SQLite store for explicit offline development
from services.local_db import get_local_db

def _get_secrets() -> Tuple[str, str, str]:
    """
    Retrieves Supabase URL, Publishable/Anon Key, and Secret/Service-Role Key.
    Resolution priority:
      1. FULCRUM_SUPABASE_* overrides (immune to Streamlit's secrets.toml os.environ clobbering)
      2. Process environment variables (SUPABASE_*)
      3. st.secrets fallback
    If FULCRUM_FORBID_PRODUCTION=1 is set (isolated staging/local tests), refuses
    to return the known production Supabase URL.
    """
    isolated = bool(os.environ.get("FULCRUM_SUPABASE_URL", "").strip())

    # 1. Explicit isolated/staging prefix overrides (Streamlit cannot overwrite these)
    url = os.environ.get("FULCRUM_SUPABASE_URL", "") or os.environ.get("SUPABASE_URL", "")
    pub_key = (
        os.environ.get("FULCRUM_SUPABASE_PUBLISHABLE_KEY", "")
        or os.environ.get("SUPABASE_PUBLISHABLE_KEY", "")
        or os.environ.get("SUPABASE_ANON_KEY", "")
    )
    sec_key = (
        os.environ.get("FULCRUM_SUPABASE_SECRET_KEY", "")
        or os.environ.get("SUPABASE_SECRET_KEY", "")
        or os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    )

    # 2. Streamlit secrets fallback (skipped if FULCRUM_SUPABASE_URL was explicitly injected)
    if not isolated:
        try:
            if hasattr(st, "secrets"):
                if not url:
                    url = st.secrets.get("SUPABASE_URL", "")
                if not pub_key:
                    pub_key = st.secrets.get("SUPABASE_PUBLISHABLE_KEY", "") or st.secrets.get("SUPABASE_ANON_KEY", "")
                if not sec_key:
                    sec_key = st.secrets.get("SUPABASE_SECRET_KEY", "") or st.secrets.get("SUPABASE_SERVICE_ROLE_KEY", "")
        except Exception:
            pass

    url_clean = url.strip()
    if os.environ.get("FULCRUM_FORBID_PRODUCTION", "").strip() == "1":
        if "bhaqaawsufwtjeqfifbv" in url_clean.lower():
            raise RuntimeError(
                "ISOLATION GUARD TRIGGERED: Production Supabase project blocked while FULCRUM_FORBID_PRODUCTION=1."
            )

    return url_clean, pub_key.strip(), sec_key.strip()

def get_data_backend() -> str:
    """
    Determines the active backend: 'supabase' or 'sqlite'.
    Checks FULCRUM_DATA_BACKEND first (immune to Streamlit's startup secrets.toml
    injection into os.environ), then DATA_BACKEND, then st.secrets.
    """
    backend = os.environ.get("FULCRUM_DATA_BACKEND", "") or os.environ.get("DATA_BACKEND", "")
    if not backend:
        try:
            if hasattr(st, "secrets"):
                backend = st.secrets.get("DATA_BACKEND", "")
        except Exception:
            pass

    backend = backend.strip().lower()
    if backend in ("supabase", "sqlite"):
        return backend

    url, pub_key, _ = _get_secrets()
    if url and pub_key:
        return "supabase"
    return "sqlite"

def get_app_base_url() -> str:
    """
    Returns the application base URL for auth redirects.
    Checks FULCRUM_APP_URL first (immune to secrets.toml), then os.environ['APP_URL'],
    then st.secrets['APP_URL'], defaulting to https://app.fulcrumindia.online.
    """
    url = os.environ.get("FULCRUM_APP_URL", "") or os.environ.get("APP_URL", "")
    if not url:
        try:
            if hasattr(st, "secrets"):
                url = st.secrets.get("APP_URL", "")
        except Exception:
            pass
    if not url:
        url = "https://app.fulcrumindia.online"
    return url.strip().rstrip("/")

def validate_production_configuration() -> Tuple[bool, Optional[str]]:
    """
    PART 3 — FAIL FAST ON PRODUCTION CONFIGURATION
    When DATA_BACKEND=supabase, verifies that all required production secrets
    (SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY/ANON_KEY, SUPABASE_SECRET_KEY/SERVICE_ROLE_KEY)
    are configured. Raises RuntimeError if any secret is missing.
    """
    backend = get_data_backend()
    if backend == "supabase":
        url, pub_key, sec_key = _get_secrets()
        missing = []
        if not url:
            missing.append("SUPABASE_URL")
        if not pub_key:
            missing.append("SUPABASE_PUBLISHABLE_KEY (or SUPABASE_ANON_KEY)")
        if not sec_key:
            missing.append("SUPABASE_SECRET_KEY (or SUPABASE_SERVICE_ROLE_KEY)")
        if missing:
            err = f"FATAL PRODUCTION CONFIGURATION ERROR: DATA_BACKEND=supabase but missing required secrets: {', '.join(missing)}. Refusing to start or silently fall back to SQLite."
            try:
                from services.logger import app_logger
                app_logger.error("auth", "startup_validation", err)
            except Exception:
                pass
            raise RuntimeError(err)
    return True, None

def is_supabase_enabled() -> bool:
    """Returns True if DATA_BACKEND is configured for Supabase and credentials exist."""
    if get_data_backend() != "supabase":
        return False
    url, pub_key, _ = _get_secrets()
    return bool(url and pub_key and create_client)

def get_supabase_client() -> Optional[Client]:
    """Returns a per-session Supabase public client with auth state."""
    url, pub_key, _ = _get_secrets()
    if not url or not pub_key or not create_client:
        return None

    try:
        client_opts = ClientOptions(flow_type="implicit") if ClientOptions else None
        if "supabase_client" not in st.session_state or st.session_state.supabase_client is None:
            if client_opts:
                st.session_state.supabase_client = create_client(url, pub_key, options=client_opts)
            else:
                st.session_state.supabase_client = create_client(url, pub_key)

        client = st.session_state.supabase_client

        # Synchronize active tokens if present in session state
        token = st.session_state.get("sb_access_token")
        refresh_token = st.session_state.get("sb_refresh_token")
        if client and token and refresh_token:
            try:
                curr = client.auth.get_session()
                if not curr or curr.access_token != token:
                    client.auth.set_session(token, refresh_token)
            except Exception:
                pass

        return client
    except Exception:
        try:
            client_opts = ClientOptions(flow_type="implicit") if ClientOptions else None
            if client_opts:
                return create_client(url, pub_key, options=client_opts)
            return create_client(url, pub_key)
        except Exception:
            return None

@st.cache_resource
def get_supabase_admin_client() -> Optional[Client]:
    """Returns trusted server-side Supabase client with secret/service_role privileges.
    Cached as a process-level singleton — the service-role client is stateless."""
    url, _, sec_key = _get_secrets()
    if not url or not sec_key or not create_client:
        return None
    try:
        return create_client(url, sec_key)
    except Exception:
        return None


def _create_ephemeral_supabase_client() -> Optional[Client]:
    """Creates an isolated transient Supabase client with implicit flow for recovery verification
    so temporary recovery auth operations never mutate the app's session client."""
    url, pub_key, _ = _get_secrets()
    if not url or not pub_key or not create_client:
        return None
    try:
        client_opts = ClientOptions(flow_type="implicit") if ClientOptions else None
        if client_opts:
            return create_client(url, pub_key, options=client_opts)
        return create_client(url, pub_key)
    except Exception:
        return None


def _classify_recovery_error(err: Exception) -> Tuple[str, str]:
    """
    Maps raw Supabase Auth / network exceptions into distinct, sanitized diagnostics.
    Never exposes access tokens, refresh tokens, passwords, or raw stack traces.
    """
    msg = str(err or "").lower()
    if any(k in msg for k in ("timed out", "timeout", "connecterror", "readerror", "connection", "unreachable", "handshake")):
        return (
            "timeout",
            "Network timeout while verifying your recovery link with the authentication service. Please try again in a moment."
        )
    if "verifier" in msg:
        return (
            "missing_verifier",
            "This link requires the original browser session where the reset was requested (missing PKCE verifier). Please request a new reset link."
        )
    if any(k in msg for k in ("otp_expired", "expired")):
        return (
            "expired",
            "This password recovery link has expired. Reset links are single-use and time-limited. Please request a new link."
        )
    if any(k in msg for k in ("session_not_found", "already", "used", "invalid claim", "invalid grant", "invalid_grant")):
        return (
            "used_or_invalid",
            "This password recovery link has already been used or is invalid. Please request a new reset link."
        )
    if "different" in msg:
        return (
            "same_password",
            "New password must be different from your current password."
        )
    if any(k in msg for k in ("rate limit", "over_email_send_rate_limit", "429", "only request this after")):
        return (
            "rate_limit",
            "Too many password reset requests in a short period. Please wait a minute before trying again."
        )
    if any(k in msg for k in ("weak", "at least")):
        return (
            "weak_password",
            "Password must be at least 8 characters long and meet strength requirements."
        )
    if "invalid" in msg or "jwt" in msg:
        return (
            "used_or_invalid",
            "This password recovery link is invalid or has already been used. Please request a new link."
        )
    return (
        "supabase_error",
        "Unable to verify recovery session with the authentication provider. Please request a new reset link."
    )

def sync_user_phone_if_missing(user_id: str, phone: str, district: Optional[str] = None) -> bool:
    """Self-healing utility: updates missing phone/district in profiles table and profile_data."""
    if not user_id or not phone:
        return False
    backend = get_data_backend()
    if backend == "supabase":
        client = get_supabase_admin_client() or get_supabase_client()
        if client:
            try:
                upd = {"phone": phone}
                if district:
                    upd["district"] = district
                client.table("profiles").update(upd).eq("id", user_id).execute()
                return True
            except Exception as e:
                try:
                    from services.logger import app_logger
                    app_logger.warning("auth", "sync_user_phone", f"Could not sync phone in Supabase for user {user_id}: {e}")
                except Exception:
                    pass
        return False

    # SQLite local mode ONLY (when DATA_BACKEND=sqlite)
    try:
        from services.local_db import get_local_db
        db = get_local_db()
        p = db.get_profile_by_id(user_id)
        if p:
            p_data = p.get("profile_data") or {}
            if isinstance(p_data, str):
                import json
                try:
                    p_data = json.loads(p_data)
                except Exception:
                    p_data = {}
            p_pers = p_data.setdefault("personal", {})
            p_pers["phone"] = phone
            if district:
                p_pers["district"] = district
            p["phone"] = phone
            if district:
                p["district"] = district
            p["profile_data"] = p_data
            db.upsert_profile(p)
            return True
    except Exception as e:
        print(f"[Auth] sync_user_phone error: {e}")
    return False

def login_user(email: str, password: str) -> Tuple[Optional[Dict], Optional[str]]:
    """
    Authenticates user.
    When DATA_BACKEND=supabase: strictly uses Supabase Auth; respects email confirmation.
    When DATA_BACKEND=sqlite: authenticates against local SQLite.
    Returns (user_profile_dict, error_message).
    """
    from services.account_lifecycle import get_account_status

    email = email.strip().lower()
    password = password.strip()
    if not email or not password:
        return None, "Please provide both email and password."

    backend = get_data_backend()

    # ── SQLITE LOCAL MODE ──
    if backend == "sqlite":
        local_db = get_local_db()
        local_profile = local_db.get_profile_by_email(email)
        if local_profile and local_db.verify_password(email, password):
            if email != "fulcrumindia1@gmail.com" and str(local_profile.get("role") or "").strip().lower() in ("admin", "district_admin", "operational_admin"):
                local_profile["role"] = "aspirant"
                local_db.upsert_profile(local_profile)

            # Check Account Lifecycle Gate
            acc_st = get_account_status(local_profile["id"])
            st_val = str(acc_st.get("account_status") or "DENIED").strip().upper()
            if st_val == "DENIED" or not acc_st.get("exists", True) or acc_st.get("error"):
                return None, f"Account access denied: {acc_st.get('error') or 'Account record is invalid or inaccessible.'}"
            if st_val in ("TEMPORARILY_SUSPENDED", "ARCHIVED"):
                st_label = "temporarily suspended" if st_val == "TEMPORARILY_SUSPENDED" else "archived"
                reason_txt = acc_st.get("lifecycle_reason") or "Administrative compliance review"
                return None, f"Account access restricted: Account is {st_label} ({reason_txt}). Please contact fulcrumindia1@gmail.com."
            if st_val != "ACTIVE" and st_val != "PENDING_DELETION":
                return None, f"Account access denied: Restricted account status '{st_val}'."
            if not acc_st.get("is_active", True) and st_val != "PENDING_DELETION":
                return None, "Account access restricted: Account is marked inactive by administration."

            st.session_state.user = local_profile
            st.session_state.user_id = local_profile["id"]
            st.session_state.role = local_profile.get("role", "aspirant")
            return local_profile, None
        return None, "Invalid email or password (Local SQLite Mode)."

    # ── SUPABASE PRIMARY MODE ──
    from services.perf import get_active_tracker
    tracker = get_active_tracker("login")

    client = get_supabase_client()
    if not client:
        return None, "Supabase connection is not configured. Please check SUPABASE_URL and SUPABASE_PUBLISHABLE_KEY."

    user_id = None
    access_token = None
    refresh_token = None

    try:
        with tracker.stage("auth_signin_ms"):
            res = client.auth.sign_in_with_password({"email": email, "password": password})
        if res.user:
            user_id = res.user.id
            if res.session:
                access_token = res.session.access_token
                refresh_token = res.session.refresh_token
    except Exception as e:
        err_str = str(e)
        if "email not confirmed" in err_str.lower() or "unconfirmed" in err_str.lower():
            return None, "Your email address has not been confirmed yet. Please check your inbox for the confirmation email."
        if "invalid login credentials" in err_str.lower() or "invalid_grant" in err_str.lower():
            return None, "Invalid email or password."
        return None, f"Authentication error: {err_str}"

    if not user_id:
        return None, "Invalid email or password."

    # Retrieve profile from Supabase Database
    profile = None
    try:
        with tracker.stage("profile_fetch_ms"):
            res_p = client.table("profiles").select("*").eq("id", user_id).execute()
        if res_p.data and len(res_p.data) > 0:
            profile = res_p.data[0]
    except Exception as e:
        return None, f"Database profile error: {e}"

    # Auto-backfill profile if user exists in Supabase Auth but lacks a profiles row
    if not profile and user_id:
        admin_client = get_supabase_admin_client() or client
        try:
            with tracker.stage("profile_init_ms"):
                # Look up metadata from Auth user
                user_meta = {}
                if res.user and hasattr(res.user, "user_metadata"):
                    user_meta = res.user.user_metadata or {}

                full_name = user_meta.get("full_name") or email.split("@")[0].capitalize()
                role = str(user_meta.get("role", "aspirant")).strip().lower()
                if email.strip().lower() != "fulcrumindia1@gmail.com" and role in ("admin", "district_admin", "operational_admin"):
                    role = "aspirant"
                district = user_meta.get("district", "Tamil Nadu")

                new_profile = {
                    "id": user_id,
                    "email": email,
                    "full_name": full_name,
                    "phone": user_meta.get("phone", ""),
                    "role": role,
                    "district": district,
                    "state": "Tamil Nadu",
                    "profile_data": {
                        "personal": {"full_name": full_name, "email": email, "phone": user_meta.get("phone", ""), "district": district}
                    },
                    "is_active": True
                }
                admin_client.table("profiles").upsert(new_profile, on_conflict="id").execute()
                profile = new_profile

                if role == "aspirant":
                    admin_client.table("journeys").upsert({
                        "aspirant_id": user_id,
                        "title": f"{full_name}'s Enterprise Journey",
                        "business_type": "Entrepreneurship",
                        "stage": "idea",
                        "status": "active"
                    }, on_conflict="aspirant_id").execute()

                    admin_client.table("relationships").upsert({
                        "aspirant_id": user_id,
                        "status": "active"
                    }, on_conflict="aspirant_id").execute()
        except Exception as e:
            return None, f"Failed to initialize user profile: {e}"

    if not profile:
        return None, "User profile not found in Supabase database."

    # Single-Admin Enforcement Gate: No account other than fulcrumindia1@gmail.com may hold admin role
    prof_email = str(profile.get("email") or email or "").strip().lower()
    prof_role = str(profile.get("role") or "aspirant").strip().lower()
    if prof_email != "fulcrumindia1@gmail.com" and prof_role in ("admin", "district_admin", "operational_admin"):
        profile["role"] = "aspirant"
        try:
            admin_client = get_supabase_admin_client() or client
            admin_client.table("profiles").update({"role": "aspirant"}).eq("id", profile["id"]).execute()
        except Exception:
            pass

    # Self-heal phone number if missing in profile record but present in user metadata
    if profile and res.user:
        user_meta = getattr(res.user, "user_metadata", {}) or {}
        meta_phone = user_meta.get("phone")
        if meta_phone and not profile.get("phone"):
            profile["phone"] = meta_phone
            sync_user_phone_if_missing(user_id, meta_phone, user_meta.get("district"))

    # Account Lifecycle Gate: Enforce active status before granting session state
    with tracker.stage("account_lifecycle_ms"):
        acc_st = get_account_status(profile["id"], prefetched_profile=profile)
    st_val = str(acc_st.get("account_status") or "DENIED").strip().upper()
    if st_val == "DENIED" or not acc_st.get("exists", True) or acc_st.get("error"):
        try:
            client.auth.sign_out()
        except Exception:
            pass
        return None, f"Account access denied: {acc_st.get('error') or 'Account record is invalid or inaccessible.'}"
    if st_val in ("TEMPORARILY_SUSPENDED", "ARCHIVED"):
        st_label = "temporarily suspended" if st_val == "TEMPORARILY_SUSPENDED" else "archived"
        reason_txt = acc_st.get("lifecycle_reason") or "Administrative compliance review"
        try:
            client.auth.sign_out()
        except Exception:
            pass
        return None, f"Account access restricted: Account is {st_label} ({reason_txt}). Please contact fulcrumindia1@gmail.com."
    if st_val != "ACTIVE" and st_val != "PENDING_DELETION":
        try:
            client.auth.sign_out()
        except Exception:
            pass
        return None, f"Account access denied: Restricted account status '{st_val}'."
    if not acc_st.get("is_active", True) and st_val != "PENDING_DELETION":
        try:
            client.auth.sign_out()
        except Exception:
            pass
        return None, "Account access restricted: Account is marked inactive by administration."

    # Save authenticated session state
    st.session_state.user = profile
    # Save authenticated session state and pre-warm actor-scoped profile memo
    try:
        from services.profiles import calculate_completion
        from services.cache import set_memo
        p_copy = dict(profile)
        p_copy["completion_pct"] = calculate_completion(p_copy)
        set_memo(f"profile:{profile['id']}:{profile['id']}", p_copy, ttl_seconds=60)
        profile = p_copy
    except Exception:
        pass

    st.session_state.user = profile
    st.session_state.user_id = profile["id"]
    st.session_state.role = profile.get("role", "aspirant")
    if access_token:
        st.session_state.sb_access_token = access_token
        st.session_state.sb_refresh_token = refresh_token

    return profile, None

def signup_aspirant(email: str, password: str, full_name: str, phone: str = "", district: str = "Madurai") -> Tuple[Optional[Dict], Optional[str]]:
    """
    Public Aspirant Signup. Strictly sets role = 'aspirant'.
    When DATA_BACKEND=supabase: uses Supabase Auth with email confirmation redirect.
    When DATA_BACKEND=sqlite: creates local SQLite account.
    """
    from services.account_lifecycle import get_account_status

    email = email.strip().lower()
    full_name = full_name.strip()
    if not email or not password or not full_name:
        return None, "Please fill in all required fields."

    if len(password) < 6:
        return None, "Password must be at least 6 characters long."

    backend = get_data_backend()

    # ── SQLITE LOCAL MODE ──
    if backend == "sqlite":
        local_db = get_local_db()
        existing = local_db.get_profile_by_email(email)
        if existing:
            return None, "An account with this email already exists in local database."

        import uuid
        user_id = str(uuid.uuid4())
        profile = {
            "id": user_id,
            "email": email,
            "full_name": full_name,
            "phone": phone,
            "role": "aspirant",
            "district": district,
            "state": "Tamil Nadu",
            "profile_data": {
                "personal": {"full_name": full_name, "email": email, "phone": phone, "district": district},
                "business": {"business_name": f"{full_name}'s Enterprise", "stage": "idea"},
                "demographics": {"district": district, "state": "Tamil Nadu"}
            },
            "is_active": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        local_db.create_user_with_password(email, password, profile)
        local_db.create_initial_journey(user_id, f"{full_name}'s Enterprise Journey")

        st.session_state.user = profile
        st.session_state.user_id = profile["id"]
        st.session_state.role = "aspirant"
        return profile, None

    # ── SUPABASE PRIMARY MODE ──
    client = get_supabase_client()
    if not client:
        return None, "Supabase client is not available. Please verify credentials."

    try:
        app_base = get_app_base_url()
        res = client.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "full_name": full_name,
                    "role": "aspirant",
                    "district": district,
                    "phone": phone
                },
                "email_redirect_to": app_base
            }
        })
    except Exception as e:
        err_str = str(e)
        if "already registered" in err_str.lower() or "user already exists" in err_str.lower():
            return None, "An account with this email already exists. Please sign in."
        return None, f"Signup failed: {err_str}"

    if not res.user:
        return None, "Failed to register account with Supabase Auth."

    user_id = res.user.id

    # If email confirmation is required, res.session is None
    if not res.session:
        # Pre-seed profile with phone so race condition doesn't drop it
        admin_client = get_supabase_admin_client()
        if admin_client:
            try:
                admin_client.table("profiles").upsert({
                    "id": user_id,
                    "email": email,
                    "full_name": full_name,
                    "phone": phone,
                    "role": "aspirant",
                    "district": district,
                    "state": "Tamil Nadu",
                    "profile_data": {
                        "personal": {"full_name": full_name, "email": email, "phone": phone, "district": district},
                        "business": {"business_name": f"{full_name}'s Enterprise", "stage": "idea"},
                        "demographics": {"district": district, "state": "Tamil Nadu"}
                    },
                    "is_active": True
                }, on_conflict="id").execute()
            except Exception:
                pass
        return {
            "id": user_id,
            "email": email,
            "pending_confirmation": True
        }, None

    # If email confirmation is disabled or user auto-confirmed:
    profile = {
        "id": user_id,
        "email": email,
        "full_name": full_name,
        "phone": phone,
        "role": "aspirant",
        "district": district,
        "state": "Tamil Nadu",
        "profile_data": {
            "personal": {"full_name": full_name, "email": email, "phone": phone, "district": district},
            "business": {"business_name": f"{full_name}'s Enterprise", "stage": "idea"},
            "demographics": {"district": district, "state": "Tamil Nadu"}
        },
        "is_active": True
    }

    try:
        client.table("profiles").upsert(profile, on_conflict="id").execute()
        client.table("journeys").upsert({
            "aspirant_id": user_id,
            "title": f"{full_name}'s Enterprise Journey",
            "business_type": "Entrepreneurship",
            "stage": "idea",
            "status": "active"
        }, on_conflict="aspirant_id").execute()
        client.table("relationships").upsert({
            "aspirant_id": user_id,
            "status": "active"
        }, on_conflict="aspirant_id").execute()
    except Exception:
        pass

    st.session_state.user = profile
    st.session_state.user_id = profile["id"]
    st.session_state.role = "aspirant"
    if res.session:
        st.session_state.sb_access_token = res.session.access_token
        st.session_state.sb_refresh_token = res.session.refresh_token

    return profile, None

def send_password_reset(email: str) -> Tuple[bool, Optional[str]]:
    """
    Triggers a password recovery email via Supabase Auth using implicit flow
    so default {{ .ConfirmationURL }} links work reliably across browser tabs,
    fresh sessions, and devices without needing a local PKCE verifier.
    """
    email = email.strip().lower()
    if not email:
        return False, "Please enter your registered email address."

    # Sole platform administrator credentials cannot be reset through self-service recovery
    if email == "fulcrumindia1@gmail.com":
        return False, "Security Notice: Platform Administrator credentials cannot be reset through self-service recovery. Contact system maintenance."

    if get_data_backend() == "sqlite":
        return False, "Password reset via email is only supported in Supabase mode."

    client = _create_ephemeral_supabase_client() or get_supabase_client()
    if not client:
        return False, "Supabase connection unavailable."

    try:
        app_base = get_app_base_url()
        client.auth.reset_password_for_email(
            email,
            {"redirect_to": f"{app_base}/?type=recovery"}
        )
        return True, None
    except Exception as e:
        err_code, clean_msg = _classify_recovery_error(e)
        if err_code == "rate_limit":
            return False, clean_msg
        if err_code == "timeout":
            return False, "Network timeout while requesting password reset email. Please try again."
        return False, f"Password reset request failed: {e}"


def verify_recovery_session_tokens(
    access_token: str,
    refresh_token: str
) -> Tuple[bool, Optional[str], Optional[str], Optional[str]]:
    """
    Cryptographically validates an implicit recovery callback's access_token + refresh_token
    against Supabase Auth using an isolated transient client.
    Never substitutes access_token for refresh_token.
    Returns (ok, verified_email, error_code, sanitized_error_message).
    """
    if not access_token or not str(access_token).strip():
        return False, None, "missing_tokens", "Invalid or missing recovery access token. Please request a new reset link."
    if not refresh_token or not str(refresh_token).strip():
        return False, None, "missing_refresh_token", "Incomplete recovery callback (missing refresh token). Please open the reset link directly from your email."

    rec_client = _create_ephemeral_supabase_client()
    if not rec_client:
        return False, None, "config_error", "Authentication service unavailable. Please try again later."

    try:
        user_res = rec_client.auth.get_user(access_token)
        user_obj = getattr(user_res, "user", None)
        verified_email = (getattr(user_obj, "email", "") or "").strip().lower() if user_obj else ""
        if not user_obj or not verified_email:
            return False, None, "used_or_invalid", "This password recovery link is invalid or has already been used. Please request a new link."

        if verified_email == "fulcrumindia1@gmail.com":
            try:
                rec_client.auth.sign_out()
            except Exception:
                pass
            return False, None, "admin_blocked", "Security Notice: Platform Administrator credentials cannot be reset through self-service recovery."

        return True, verified_email, None, None
    except Exception as e:
        err_code, clean_msg = _classify_recovery_error(e)
        return False, None, err_code, clean_msg


def verify_recovery_token_hash(
    token_hash: str
) -> Tuple[bool, Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]:
    """
    Statelessly verifies a Supabase recovery token_hash via verify_otp in an isolated client.
    Returns (ok, verified_email, access_token, refresh_token, error_code, sanitized_error_message).
    """
    if not token_hash or not str(token_hash).strip():
        return False, None, None, None, "missing_tokens", "Missing recovery verification token. Please request a new reset link."

    rec_client = _create_ephemeral_supabase_client()
    if not rec_client:
        return False, None, None, None, "config_error", "Authentication service unavailable. Please try again later."

    try:
        res = rec_client.auth.verify_otp({"token_hash": token_hash.strip(), "type": "recovery"})
        sess = getattr(res, "session", None)
        user_obj = getattr(res, "user", None)
        verified_email = (getattr(user_obj, "email", "") or "").strip().lower() if user_obj else ""
        acc_tok = getattr(sess, "access_token", None) if sess else None
        ref_tok = getattr(sess, "refresh_token", None) if sess else None

        if not sess or not acc_tok or not ref_tok or not verified_email:
            return False, None, None, None, "used_or_invalid", "This password recovery link is invalid or has already been used. Please request a new link."

        if verified_email == "fulcrumindia1@gmail.com":
            try:
                rec_client.auth.sign_out()
            except Exception:
                pass
            return False, None, None, None, "admin_blocked", "Security Notice: Platform Administrator credentials cannot be reset through self-service recovery."

        return True, verified_email, acc_tok, ref_tok, None, None
    except Exception as e:
        err_code, clean_msg = _classify_recovery_error(e)
        return False, None, None, None, err_code, clean_msg


def complete_password_reset(
    new_password: str,
    access_token: Optional[str] = None,
    refresh_token: Optional[str] = None,
    email: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """
    Updates user password following a verified Supabase Auth recovery link.
    Strictly requires genuine access_token + refresh_token proof and executes
    update_user inside an isolated ephemeral client, terminating the recovery
    session immediately upon success. Never uses Admin API overrides (CWE-640).
    """
    if not new_password or len(new_password) < 8:
        return False, "Password must be at least 8 characters long."

    clean_email = (email or "").strip().lower()

    # The Single Platform Administrator credentials can NEVER be reset via public self-serve flow
    if clean_email == "fulcrumindia1@gmail.com":
        return False, "Security Notice: Platform Administrator credentials cannot be reset through self-service recovery. Contact system maintenance."

    backend = get_data_backend()

    if backend == "sqlite":
        # In local SQLite development mode only, require verified registered account
        if not clean_email:
            return False, "Please enter your registered email address."
        from services.local_db import get_local_db_conn
        import hashlib
        pwd_hash = hashlib.sha256(new_password.encode("utf-8")).hexdigest()
        try:
            conn = get_local_db_conn()
            cur = conn.cursor()
            cur.execute("SELECT id FROM profiles WHERE LOWER(email) = ?", (clean_email,))
            row = cur.fetchone()
            if not row:
                conn.close()
                return False, f"No registered account found with email: {clean_email}"
            cur.execute("UPDATE profiles SET password_hash = ? WHERE LOWER(email) = ?", (pwd_hash, clean_email))
            conn.commit()
            conn.close()
            return True, None
        except Exception as e:
            return False, f"Failed to update local password: {e}"

    # Supabase Mode: STRICTLY REQUIRE GENUINE ACCESS + REFRESH RECOVERY CREDENTIALS
    token = access_token or st.session_state.get("_recovery_access_token")
    ref_token = refresh_token or st.session_state.get("_recovery_refresh_token")

    if not token or not ref_token:
        return False, "Invalid or missing recovery credentials. Please use the secure reset link sent to your registered email."

    rec_client = _create_ephemeral_supabase_client()
    if not rec_client:
        return False, "Authentication service unavailable. Please try again later."

    try:
        # Establish isolated recovery session with genuine access + refresh tokens
        sess = rec_client.auth.set_session(token, ref_token)
        if not sess or not getattr(sess, "user", None):
            return False, "Recovery session has expired or is invalid. Please request a new password reset link."

        # Verify target user matches recovery session if email was provided
        sess_email = getattr(sess.user, "email", "") or ""
        if clean_email and sess_email.lower() != clean_email:
            return False, "Security violation: Recovery token does not match the verified email address."

        # Double check: Admin account protection
        if sess_email.lower() == "fulcrumindia1@gmail.com":
            return False, "Security Notice: Platform Administrator credentials cannot be reset through self-service recovery."

        # Perform password update within the verified recovery session context
        res = rec_client.auth.update_user({"password": new_password})
        if not res or not getattr(res, "user", None):
            return False, "Password update failed. Please request a new recovery link."

        # Immediately terminate the temporary recovery session
        try:
            rec_client.auth.sign_out()
        except Exception:
            pass

        return True, None
    except Exception as e:
        err_code, clean_msg = _classify_recovery_error(e)
        if err_code in ("same_password", "weak_password", "timeout"):
            return False, clean_msg
        if err_code in ("expired", "used_or_invalid"):
            return False, "The recovery link has expired or has already been used. Please request a new reset link."
        return False, clean_msg


def complete_first_login_password_change(
    user_id: str,
    new_password: str
) -> Tuple[bool, Optional[str]]:
    """
    Enforces the first-login permanent password change for accounts provisioned with a temporary password.
    Updates the password in Supabase Auth or SQLite local DB, and sets temp_password_issued: False in profile_data.
    Requires caller to be authenticated as the target user.
    """
    if not new_password or len(new_password) < 8:
        return False, "Password must be at least 8 characters long."

    # Verify session authorization: caller MUST be authenticated as user_id
    session_user = st.session_state.get("user")
    if not session_user or str(session_user.get("id")) != str(user_id):
        if str(st.session_state.get("user_id")) != str(user_id):
            return False, "Unauthorized: Session user does not match target account."

    backend = get_data_backend()
    from services.profiles import get_profile, update_profile

    if backend == "sqlite":
        db = get_local_db()
        success = db.update_user_password(user_id, new_password)
        if not success:
            return False, "Failed to update password in local database."
        prof = get_profile(user_id)
        prof_data = (prof.get("profile_data") or {}) if prof else {}
        if isinstance(prof_data, str):
            try: prof_data = json.loads(prof_data)
            except Exception: prof_data = {}
        prof_data["temp_password_issued"] = False
        try:
            conn = db._get_conn()
            cur = conn.cursor()
            cur.execute("UPDATE profiles SET profile_data = ?, updated_at = ? WHERE id = ?", (
                json.dumps(prof_data),
                datetime.now(timezone.utc).isoformat(),
                user_id
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[Auth] Local DB profile update error: {e}")

        fresh_prof = get_profile(user_id)
        if fresh_prof and "user" in st.session_state:
            st.session_state.user = fresh_prof
        elif st.session_state.get("user") and st.session_state.user.get("id") == user_id:
            st.session_state.user["profile_data"] = prof_data
        return True, None

    # Supabase mode
    admin_client = get_supabase_admin_client()
    client = get_supabase_client()
    updated = False

    if client and st.session_state.get("sb_access_token"):
        try:
            client.auth.set_session(st.session_state.sb_access_token, st.session_state.get("sb_refresh_token") or st.session_state.sb_access_token)
            client.auth.update_user({"password": new_password})
            updated = True
        except Exception as e:
            print(f"[Auth] Client password update notice: {e}")

    if not updated and admin_client:
        try:
            admin_client.auth.admin.update_user_by_id(user_id, {"password": new_password})
            updated = True
        except Exception as e:
            return False, f"Failed to update password in Supabase Auth: {e}"

    if not updated:
        return False, "Authentication client unavailable to update password."

    prof = get_profile(user_id)
    prof_data = (prof.get("profile_data") or {}) if prof else {}
    if isinstance(prof_data, str):
        try: prof_data = json.loads(prof_data)
        except Exception: prof_data = {}
    prof_data["temp_password_issued"] = False

    if admin_client:
        try:
            upd_res = admin_client.table("profiles").update({
                "profile_data": prof_data,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }).eq("id", user_id).execute()
            if not upd_res.data and hasattr(upd_res, "error") and upd_res.error:
                return False, f"Password updated in Auth, but profile update failed: {upd_res.error}"
        except Exception as e:
            return False, f"Password updated in Auth, but failed to persist permanent status in profile: {e}"

    # Synchronize SQLite Database
    try:
        local_db = get_local_db()
        local_db.update_user_password(user_id, new_password)
        conn = local_db._get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE profiles SET profile_data = ?, updated_at = ? WHERE id = ?", (
            json.dumps(prof_data),
            datetime.now(timezone.utc).isoformat(),
            user_id
        ))
        conn.commit()
        conn.close()
    except Exception:
        pass

    fresh_prof = get_profile(user_id)
    if fresh_prof and "user" in st.session_state:
        st.session_state.user = fresh_prof
    elif st.session_state.get("user") and st.session_state.user.get("id") == user_id:
        st.session_state.user["profile_data"] = prof_data

    return True, None

def admin_create_mentor(admin_user_id: str, role: str, full_name: str, email: str, phone: str, location: str, expertise: str, temp_password: Optional[str] = None, bio: str = "", industry: str = "") -> Tuple[Optional[Dict], Optional[str]]:
    """
    Administrative creation of Guide or SME accounts.
    Strictly restricted to Admin. No public signup allowed for these roles.
    Uses cryptographically strong random temporary passwords by default.
    """
    if role not in ("guide", "sme"):
        return None, f"Invalid mentor role: {role}"

    email = email.strip().lower()
    full_name = full_name.strip()
    if not email or not full_name:
        return None, "Name and email are required."

    import secrets
    effective_temp_password = temp_password if temp_password and len(temp_password) >= 8 else secrets.token_urlsafe(12)

    backend = get_data_backend()

    if backend == "sqlite":
        local_db = get_local_db()
        import uuid
        mentor_user_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()
        profile = {
            "id": mentor_user_id,
            "email": email,
            "full_name": full_name,
            "phone": phone,
            "role": role,
            "district": location,
            "state": "Tamil Nadu",
            "profile_data": {
                "expertise": expertise,
                "bio": bio,
                "industry": industry,
                "temp_password_issued": True
            },
            "is_active": True,
            "created_at": now_iso
        }
        local_db.create_user_with_password(email, effective_temp_password, profile)
        if hasattr(local_db, "upsert_user_role"):
            local_db.upsert_user_role({
                "user_id": mentor_user_id,
                "role": role,
                "status": "pending_nda",
                "granted_by": admin_user_id,
                "granted_at": now_iso,
                "activated_at": None,
                "suspended_at": None,
                "revoked_at": None,
                "revocation_reason": None,
                "updated_at": now_iso,
            })
        try:
            from services.cache import invalidate_memo
            invalidate_memo()
        except Exception:
            pass
        local_db.log_activity(admin_user_id, f"create_{role}", "profiles", mentor_user_id, {"full_name": full_name, "email": email})
        return profile, None

    # Supabase mode
    admin_client = get_supabase_admin_client()
    if not admin_client:
        return None, "Supabase admin client (SUPABASE_SECRET_KEY) is required to create mentor accounts."

    mentor_user_id = None
    try:
        res = admin_client.auth.admin.create_user({
            "email": email,
            "password": effective_temp_password,
            "email_confirm": True,
            "user_metadata": {
                "full_name": full_name,
                "role": role,
                "district": location,
                "phone": phone
            }
        })
        if res.user:
            mentor_user_id = res.user.id
    except Exception as e:
        err_str = str(e)
        if "already registered" in err_str.lower() or "user already exists" in err_str.lower():
            return None, "A user with this email already exists in Supabase Auth."
        return None, f"Failed to create mentor in Supabase Auth: {err_str}"

    if not mentor_user_id:
        return None, "Failed to obtain mentor user ID."

    profile = {
        "id": mentor_user_id,
        "email": email,
        "full_name": full_name,
        "phone": phone,
        "role": role,
        "district": location,
        "state": "Tamil Nadu",
        "profile_data": {
            "expertise": expertise,
            "bio": bio,
            "industry": industry,
            "temp_password_issued": True
        },
        "is_active": True
    }

    try:
        admin_client.table("profiles").upsert(profile, on_conflict="id").execute()
    except Exception as e:
        return None, f"Failed to save mentor profile in Supabase database: {e}"

    now_iso = datetime.now(timezone.utc).isoformat()
    try:
        admin_client.table("user_roles").upsert({
            "user_id": mentor_user_id,
            "role": role,
            "status": "pending_nda",
            "granted_by": admin_user_id,
            "granted_at": now_iso,
            "activated_at": None,
            "suspended_at": None,
            "revoked_at": None,
            "revocation_reason": None,
            "updated_at": now_iso,
        }, on_conflict="user_id, role").execute()
        from services.cache import invalidate_memo
        invalidate_memo()
    except Exception as e:
        return None, f"Mentor profile saved, but failed to initialize role grant in user_roles: {e}"

    return profile, None

def backfill_auth_users(default_admin_email: Optional[str] = None) -> Dict[str, Any]:
    """
    Safely backfills missing profiles, journeys, and relationship records in Supabase
    for existing Supabase Auth users (e.g. users registered before triggers were installed).
    Idempotent: does not delete or duplicate any records.
    """
    admin_client = get_supabase_admin_client()
    if not admin_client:
        return {"error": "Supabase admin client unavailable."}

    try:
        users = admin_client.auth.admin.list_users()
    except Exception as e:
        return {"error": f"Failed to list Supabase Auth users: {e}"}

    SOLE_ADMIN_EMAIL = "fulcrumindia1@gmail.com"
    results = {"total_auth_users": len(users), "backfilled": 0, "already_existing": 0, "errors": []}

    for u in users:
        try:
            u_email_clean = (u.email or "").strip().lower()
            p_res = admin_client.table("profiles").select("id, role").eq("id", u.id).execute()
            if p_res.data and len(p_res.data) > 0:
                results["already_existing"] += 1
                existing_role = str(p_res.data[0].get("role") or "aspirant").strip().lower()
                # Strictly enforce Single-Admin rule: only fulcrumindia1@gmail.com may be admin
                if u_email_clean == SOLE_ADMIN_EMAIL and existing_role != "admin":
                    admin_client.table("profiles").update({"role": "admin"}).eq("id", u.id).execute()
                elif u_email_clean != SOLE_ADMIN_EMAIL and existing_role in ("admin", "district_admin", "operational_admin"):
                    admin_client.table("profiles").update({"role": "aspirant"}).eq("id", u.id).execute()
                continue

            # Missing profile: generate and insert
            meta = u.user_metadata or {}
            full_name = meta.get("full_name") or (u.email.split("@")[0].capitalize() if u.email else "User")
            role = str(meta.get("role", "aspirant")).strip().lower()
            if u_email_clean == SOLE_ADMIN_EMAIL:
                role = "admin"
            elif role in ("admin", "district_admin", "operational_admin"):
                role = "aspirant"

            district = meta.get("district", "Tamil Nadu")

            profile_record = {
                "id": u.id,
                "email": u.email,
                "full_name": full_name,
                "role": role,
                "district": district,
                "state": "Tamil Nadu",
                "profile_data": {},
                "is_active": True
            }
            admin_client.table("profiles").upsert(profile_record, on_conflict="id").execute()

            if role == "aspirant":
                admin_client.table("journeys").upsert({
                    "aspirant_id": u.id,
                    "title": f"{full_name}'s Enterprise Journey",
                    "business_type": "Entrepreneurship",
                    "stage": "idea",
                    "status": "active"
                }, on_conflict="aspirant_id").execute()

                admin_client.table("relationships").upsert({
                    "aspirant_id": u.id,
                    "status": "active"
                }, on_conflict="aspirant_id").execute()

            results["backfilled"] += 1
        except Exception as e:
            results["errors"].append({"email": u.email, "error": str(e)})

    return results

def promote_user_to_admin(email: str) -> Tuple[bool, Optional[str]]:
    """Promotes an existing user profile to 'admin' role in Supabase. Locked strictly to fulcrumindia1@gmail.com."""
    clean_email = (email or "").strip().lower()
    if not clean_email:
        return False, "Email is required."
    if clean_email != "fulcrumindia1@gmail.com":
        return False, "Security Violation: Only fulcrumindia1@gmail.com is permitted as Platform Administrator."

    if get_data_backend() == "sqlite":
        db = get_local_db()
        p = db.get_profile_by_email(clean_email)
        if not p:
            return False, f"User {clean_email} not found in local database."
        p["role"] = "admin"
        db.upsert_profile(p)
        return True, None

    admin_client = get_supabase_admin_client()
    if not admin_client:
        return False, "Supabase admin client unavailable."

    try:
        res = admin_client.table("profiles").update({"role": "admin"}).eq("email", clean_email).execute()
        if res.data and len(res.data) > 0:
            return True, None
        return False, f"No profile found with email '{clean_email}' in Supabase database."
    except Exception as e:
        return False, f"Promotion failed: {e}"

def logout_user():
    """Clears Supabase session and resets Streamlit session state."""
    client = get_supabase_client()
    if client:
        try:
            client.auth.sign_out()
        except Exception:
            pass

    for key in ["user", "user_id", "role", "sb_access_token", "sb_refresh_token", "selected_aspirant_id", "supabase_client", "auth_mode"]:
        st.session_state.pop(key, None)
