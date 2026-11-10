"""
services/auth_callback_component.py — Secure Same-Origin Hash Fragment Reader (WebSocket-Only)
=============================================================================================
Uses Streamlit Components v2 (`st.components.v2.component`) to read Supabase Auth
hash-fragment callbacks (`#access_token=...`, `#refresh_token=...`, `#error=...`)
directly from `window.location.hash` in the host document:
- ZERO URL query-parameter exposure (`?access_token=` is NEVER written to the URL bar or HTTP logs)
- Immediately scrubs `#...` and callback query params via `window.history.replaceState`
- Transfers the callback payload strictly over Streamlit's encrypted WSS WebSocket
"""

from typing import Optional, Dict, Any
import streamlit as st

_CALLBACK_JS = """
export default function(component) {
    const { data, setTriggerValue } = component;
    const expectHash = Boolean(data && data.expect_hash);
    const hash = window.location.hash || "";
    const hasAuthHash = Boolean(
        hash && (
            hash.includes("access_token=") ||
            hash.includes("error=") ||
            hash.includes("error_code=") ||
            hash.includes("type=recovery") ||
            hash.includes("type=signup")
        )
    );

    if (hasAuthHash) {
        if (window.__fulcrumLastAuthHash === hash) {
            return;
        }
        window.__fulcrumLastAuthHash = hash;

        const cleanHash = hash.replace(/^[#\\/]+/, "");
        const params = new URLSearchParams(cleanHash);
        const payload = {
            status: (params.get("error") || params.get("error_code")) ? "error" : "found",
            access_token: params.get("access_token") || "",
            refresh_token: params.get("refresh_token") || "",
            type: params.get("type") || "",
            error: params.get("error") || "",
            error_code: params.get("error_code") || "",
            error_description: params.get("error_description") || "",
            expires_in: params.get("expires_in") || ""
        };

        try {
            window.history.replaceState(null, "", window.location.pathname || "/");
        } catch (e) {}

        setTriggerValue("callback", payload);
    } else if (expectHash) {
        if (window.__fulcrumEmptyHashReported) {
            return;
        }
        window.__fulcrumEmptyHashReported = true;
        try {
            window.history.replaceState(null, "", window.location.pathname || "/");
        } catch (e) {}
        setTriggerValue("callback", { status: "empty" });
    }
}
"""

_AUTH_CALLBACK_COMPONENT = None
if hasattr(st, "components") and hasattr(st.components, "v2"):
    _AUTH_CALLBACK_COMPONENT = st.components.v2.component(
        "fulcrum_auth_callback_bridge",
        js=_CALLBACK_JS,
        isolate_styles=False,
    )


def _noop_callback() -> None:
    pass


def read_auth_callback(expect_hash: bool = False) -> Optional[Dict[str, Any]]:
    """
    Mounts the non-visual Components v2 hash-bridge when needed and returns the
    extracted callback dict (`{status, access_token, refresh_token, type, error, ...}`)
    over WebSocket, or None if no callback payload arrived in this rerun.
    """
    if _AUTH_CALLBACK_COMPONENT is None:
        return None

    result = _AUTH_CALLBACK_COMPONENT(
        data={"expect_hash": bool(expect_hash)},
        on_callback_change=_noop_callback,
        key="fulcrum_auth_callback_bridge_instance",
    )
    payload = getattr(result, "callback", None)
    if isinstance(payload, dict) and payload.get("status"):
        return payload
    return None

