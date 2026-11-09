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
# Process-wide invalidation timestamps so mutations in one user's session (e.g. Admin revoking a role)
# immediately invalidate stale memo entries in another user's open browser session.
_INVALIDATION_TIMESTAMPS: Dict[str, float] = {}
_LAST_PRUNE_TIME: float = 0.0

MAX_GLOBAL_CACHE_SIZE = 1000
MAX_SESSION_CACHE_SIZE = 500
INVALIDATION_TTL_SECONDS = 3600.0  # Expire timestamps after 1 hour


def _prune_expired_entries() -> None:
    """Periodically purges expired invalidation timestamps and stale global cache entries."""
    global _LAST_PRUNE_TIME
    now = time.time()
    if now - _LAST_PRUNE_TIME < 60.0:
        return
    _LAST_PRUNE_TIME = now

    # Prune invalidation timestamps older than 1 hour
    stale_inv = [k for k, ts in list(_INVALIDATION_TIMESTAMPS.items()) if (now - ts) > INVALIDATION_TTL_SECONDS]
    for k in stale_inv:
        _INVALIDATION_TIMESTAMPS.pop(k, None)

    # Prune expired global cache items
    expired_global = [k for k, v in list(_GLOBAL_CACHE.items()) if now > v.get("expires_at", 0)]
    for k in expired_global:
        _GLOBAL_CACHE.pop(k, None)


def get_global_cache(key: str) -> Optional[Any]:
    """Retrieves an item from the shared in-memory cache if not expired."""
    _prune_expired_entries()
    entry = _GLOBAL_CACHE.get(key)
    if not entry:
        return None
    if time.time() > entry["expires_at"]:
        _GLOBAL_CACHE.pop(key, None)
        return None
    return entry["value"]


def set_global_cache(key: str, value: Any, ttl_seconds: int = 300) -> None:
    """Stores an item in the shared in-memory cache with bounded size and expiration."""
    now = time.time()
    if len(_GLOBAL_CACHE) >= MAX_GLOBAL_CACHE_SIZE:
        _prune_expired_entries()
        # If still at capacity, evict oldest 20%
        if len(_GLOBAL_CACHE) >= MAX_GLOBAL_CACHE_SIZE:
            oldest = sorted(_GLOBAL_CACHE.keys(), key=lambda k: _GLOBAL_CACHE[k].get("expires_at", 0))[:200]
            for k in oldest:
                _GLOBAL_CACHE.pop(k, None)

    _GLOBAL_CACHE[key] = {
        "value": value,
        "expires_at": now + ttl_seconds
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
    """Retrieves a cached value from the current request/session, respecting cross-session invalidations."""
    _prune_expired_entries()
    store = _get_session_store()
    entry = store.get(key)
    if not entry:
        return default
    now = time.time()
    if entry.get("expires_at") and now > entry["expires_at"]:
        store.pop(key, None)
        return default
    stored_at = entry.get("stored_at", 0.0)
    for prefix, inv_ts in list(_INVALIDATION_TIMESTAMPS.items()):
        if (not prefix or key.startswith(prefix)) and inv_ts >= stored_at:
            store.pop(key, None)
            return default
    return entry["value"]


def set_memo(key: str, value: Any, ttl_seconds: Optional[int] = 60) -> Any:
    """Stores a value in the current request/session cache with bounded capacity."""
    now = time.time()
    store = _get_session_store()

    # Bound session store size
    if len(store) >= MAX_SESSION_CACHE_SIZE:
        expired = [k for k, v in list(store.items()) if v.get("expires_at") and now > v["expires_at"]]
        for k in expired:
            store.pop(k, None)
        if len(store) >= MAX_SESSION_CACHE_SIZE:
            oldest = sorted(store.keys(), key=lambda k: store[k].get("stored_at", 0))[:100]
            for k in oldest:
                store.pop(k, None)

    store[key] = {
        "value": value,
        "stored_at": now,
        "expires_at": (now + ttl_seconds) if ttl_seconds else None
    }
    return value


def invalidate_memo(key_prefix: str = "") -> None:
    """Invalidates session memo entries matching a key prefix across all active sessions."""
    _INVALIDATION_TIMESTAMPS[key_prefix] = time.time()
    store = _get_session_store()
    if not key_prefix:
        store.clear()
        return
    keys_to_del = [k for k in store if k.startswith(key_prefix)]
    for k in keys_to_del:
        store.pop(k, None)


def is_tab_active(tab) -> bool:
    """Returns True if the tab container is currently open/selected."""
    val = getattr(tab, "open", None)
    if isinstance(val, bool):
        return val
    return True

