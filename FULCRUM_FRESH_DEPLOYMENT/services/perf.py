"""
services/perf.py — Sanitized Stage-Level Timing Instrumentation for FULCRUM-INDIA
================================================================================
Measures latency across app initialization, auth, DB lookups, and dashboard rendering.
NEVER logs passwords, tokens, emails, or identifiable personal data.
"""

import time
import logging
from contextlib import contextmanager
from typing import Dict, Any

_logger = logging.getLogger("fulcrum.perf")
if not _logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter("[PERF] %(message)s"))
    _logger.addHandler(_handler)
    _logger.setLevel(logging.INFO)


class PerfTracker:
    """Collects non-sensitive millisecond stage timings for a single Streamlit script run."""

    def __init__(self, flow_name: str = "request"):
        self.flow_name = flow_name
        self.started_at = time.perf_counter()
        self.stages: Dict[str, float] = {}

    @contextmanager
    def stage(self, name: str):
        t0 = time.perf_counter()
        try:
            yield
        finally:
            elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 2)
            self.stages[name] = self.stages.get(name, 0.0) + elapsed_ms

    def record(self, name: str, elapsed_ms: float) -> None:
        self.stages[name] = round(self.stages.get(name, 0.0) + elapsed_ms, 2)

    def summary(self) -> Dict[str, Any]:
        total_ms = round((time.perf_counter() - self.started_at) * 1000.0, 2)
        return {
            "flow": self.flow_name,
            "total_ms": total_ms,
            "stages": dict(self.stages),
        }

    def persist_to_session(self) -> Dict[str, Any]:
        snap = self.summary()
        try:
            import streamlit as st
            if hasattr(st, "session_state"):
                st.session_state["_last_perf_metrics"] = snap
        except Exception:
            pass
        return snap


def get_active_tracker(flow_name: str = "request") -> PerfTracker:
    """Returns or creates the current script run's PerfTracker in session_state."""
    try:
        import streamlit as st
        if hasattr(st, "session_state"):
            tracker = st.session_state.get("_current_perf_tracker")
            if isinstance(tracker, PerfTracker):
                return tracker
            tracker = PerfTracker(flow_name)
            st.session_state["_current_perf_tracker"] = tracker
            return tracker
    except Exception:
        pass
    return PerfTracker(flow_name)


def reset_tracker(flow_name: str = "request") -> PerfTracker:
    tracker = PerfTracker(flow_name)
    try:
        import streamlit as st
        if hasattr(st, "session_state"):
            st.session_state["_current_perf_tracker"] = tracker
    except Exception:
        pass
    return tracker

