"""
services/cache.py — Safe, High-Performance Request-Scoped & In-Memory Cache
==========================================================================
Provides:
1. Session/Request-Scoped Memoization (isolated per user session in st.session_state)
2. Safe TTL-bounded in-memory caching for stable read-only lookup data (e.g. Schemes)
3. Targeted Cache Invalidation (user profile updates, scheme changes, assignment changes)
4. Strict user/role isolation (never shares sensitive user records across sessions)
"""

import time
from typing import Any, Optional, Dict, Callable

# Global in-memory cache for shared, non-sensitive static data (e.g., active scheme catalogue)
_GLOBAL_CACHE: Dict[str, Dict[str, Any]] = {}


def get_global_cache(key: str) -> Optional[Any]:
    """Retrieves an item from the shared in-memory cache if not expired."""
    entry = _GLOBAL_CACHE.get(key)
    if not entry:
        return None
    if time.time() > entry["expires_at"]:
        _GLOBAL_CACHE.pop(key, None)
        return None
    return entry["value"]


def set_global_cache(key: str, value: Any, ttl_seconds: int = 300) -> None:
    """Stores an item in the shared in-memory cache with an expiration timestamp."""
    _GLOBAL_CACHE[key] = {
        "value": value,
        "expires_at": time.time() + ttl_seconds
    }


def invalidate_global_cache(key_prefix: str = "") -> None:
    """Invalidates entries matching a prefix from the global in-memory cache."""
    if not key_prefix:
        _GLOBAL_CACHE.clear()
        return
    keys_to_del = [k for k in _GLOBAL_CACHE if k.startswith(key_prefix)]
    for k in keys_to_del:
        _GLOBAL_CACHE.pop(k, None)


def _get_session_store() -> Dict[str, Any]:
    """Gets the session-local cache dictionary safely from st.session_state."""
    try:
        import streamlit as st
        if hasattr(st, "session_state"):
            if "_fulcrum_memo_store" not in st.session_state:
                st.session_state["_fulcrum_memo_store"] = {}
            return st.session_state["_fulcrum_memo_store"]
    except Exception:
        pass
    # Fallback for non-streamlit (e.g. CLI test scripts)
    if not hasattr(_get_session_store, "_cli_store"):
        _get_session_store._cli_store = {}
    return _get_session_store._cli_store


def get_memo(key: str, default: Any = None) -> Any:
    """Retrieves a cached value from the current request/session."""
    store = _get_session_store()
    entry = store.get(key)
    if not entry:
        return default
    if entry.get("expires_at") and time.time() > entry["expires_at"]:
        store.pop(key, None)
        return default
    return entry["value"]


def set_memo(key: str, value: Any, ttl_seconds: Optional[int] = 60) -> Any:
    """Stores a value in the current request/session cache."""
    store = _get_session_store()
    store[key] = {
        "value": value,
        "expires_at": (time.time() + ttl_seconds) if ttl_seconds else None
    }
    return value


def invalidate_memo(key_prefix: str = "") -> None:
    """Invalidates session memo entries matching a key prefix."""
    store = _get_session_store()
    if not key_prefix:
        store.clear()
        return
    keys_to_del = [k for k in store if k.startswith(key_prefix)]
    for k in keys_to_del:
        store.pop(k, None)


def is_tab_active(tab) -> bool:
    """Returns True if the tab container is currently open/selected (or if state tracking is not active)."""
    return getattr(tab, "open", True) is not False

