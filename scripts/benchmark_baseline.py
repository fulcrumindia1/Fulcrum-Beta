"""
scripts/benchmark_baseline.py
=============================
Instruments and benchmarks database read/write latency and request counts
across core Fulcrum workflows against the active backend (Supabase / SQLite).
Records p50, p95, min, max, and total duration for each operation.
"""

import os
import sys
import time
import json
import statistics
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from services.auth import get_data_backend, get_supabase_admin_client
from services.profiles import get_profile, update_aspirant_profile
from services.relationships import get_aspirant_mentors, get_assigned_aspirants_for_guide, get_assigned_aspirants_for_sme
from services.journey import get_journey_timeline
from services.schemes import list_schemes, get_released_schemes_for_aspirant, match_schemes_for_aspirant
from services.help_requests import list_requests, list_mentor_admin_queries
from services.notifications import get_unread_count, list_notifications

NUM_RUNS = 5


def timed_run(func, *args, **kwargs):
    t0 = time.perf_counter()
    res = func(*args, **kwargs)
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0, res  # milliseconds


def run_benchmark_suite(label: str = "BASELINE"):
    backend = get_data_backend()
    print("=" * 75)
    print(f" [FULCRUM PERFORMANCE BENCHMARK] Mode: {label} | Backend: {backend}")
    print(f" Timestamp: {datetime.now().isoformat()}")
    print("=" * 75)

    # Resolve test accounts
    admin = get_supabase_admin_client() if backend == "supabase" else None
    test_asp_id = None
    test_guide_id = None
    test_sme_id = None

    if backend == "supabase" and admin:
        try:
            p_res = admin.table("profiles").select("id, role, email").execute()
            for p in (p_res.data or []):
                if p["role"] == "aspirant" and not test_asp_id:
                    test_asp_id = p["id"]
                elif p["role"] == "guide" and not test_guide_id:
                    test_guide_id = p["id"]
                elif p["role"] == "sme" and not test_sme_id:
                    test_sme_id = p["id"]
        except Exception as e:
            print(f"Error querying profiles: {e}")

    # Fallback IDs if not found
    if not test_asp_id:
        test_asp_id = "2970a3ee-46fc-483c-b276-aa2a955ba123"
    if not test_guide_id:
        test_guide_id = "83afcd9a-f608-4ab1-90a2-8dc64530dd04"
    if not test_sme_id:
        test_sme_id = "56f7dab8-3054-4ab3-8349-5778de6d9093"

    benchmarks = {}

    operations = [
        ("1. Profile Retrieval [get_profile]", lambda: get_profile(test_asp_id)),
        ("2. Mentors Lookup [get_aspirant_mentors]", lambda: get_aspirant_mentors(test_asp_id)),
        ("3. Released Schemes [get_released_schemes_for_aspirant]", lambda: get_released_schemes_for_aspirant(test_asp_id)),
        ("4. Journey Timeline [get_journey_timeline]", lambda: get_journey_timeline(test_asp_id)),
        ("5. Aspirant Help Requests [list_requests]", lambda: list_requests(test_asp_id)),
        ("6. Notifications Unread Count [get_unread_count]", lambda: get_unread_count(test_asp_id)),
        ("7. Notifications List [list_notifications]", lambda: list_notifications(test_asp_id)),
        ("8. Guide Caseload [get_assigned_aspirants_for_guide]", lambda: get_assigned_aspirants_for_guide(test_guide_id)),
        ("9. SME Caseload [get_assigned_aspirants_for_sme]", lambda: get_assigned_aspirants_for_sme(test_sme_id)),
        ("10. Full Scheme Catalogue [list_schemes]", lambda: list_schemes(active_only=True)),
        ("11. Scheme Matching Engine [match_schemes_for_aspirant]", lambda: match_schemes_for_aspirant(test_asp_id)),
        ("12. Mentor Admin Queries [list_mentor_admin_queries]", lambda: list_mentor_admin_queries(mentor_id=test_guide_id)),
    ]

    for name, op in operations:
        times = []
        for _ in range(NUM_RUNS):
            duration_ms, _ = timed_run(op)
            times.append(duration_ms)
        p50 = statistics.median(times)
        p95 = sorted(times)[int(len(times) * 0.95)] if len(times) > 1 else times[0]
        mean = statistics.mean(times)
        benchmarks[name] = {
            "mean_ms": round(mean, 2),
            "p50_ms": round(p50, 2),
            "p95_ms": round(p95, 2),
            "min_ms": round(min(times), 2),
            "max_ms": round(max(times), 2),
            "raw_runs": [round(t, 2) for t in times]
        }
        print(f"  {name:55} | p50: {p50:7.2f} ms | p95: {p95:7.2f} ms | mean: {mean:7.2f} ms")

    # Measure simulated Aspirant Dashboard total sequential load (as current code does)
    print("\n--- SIMULATED DASHBOARD FULL LOAD (Unoptimized vs Optimized) ---")
    asp_total_times = []
    for _ in range(3):
        t0 = time.perf_counter()
        # What current aspirant dashboard executes across tabs:
        p = get_profile(test_asp_id)
        m1 = get_aspirant_mentors(test_asp_id)
        r1 = get_released_schemes_for_aspirant(test_asp_id)
        j1 = get_journey_timeline(test_asp_id)
        j2 = get_journey_timeline(test_asp_id)  # duplicated in tab 2
        m2 = get_aspirant_mentors(test_asp_id)  # duplicated in tab 3
        r2 = get_released_schemes_for_aspirant(test_asp_id)  # duplicated in tab 4
        hr = list_requests(test_asp_id)  # in tab 5
        u1 = get_unread_count(test_asp_id)  # in app.py line 712
        nl = list_notifications(test_asp_id)  # in app.py line 717
        u2 = get_unread_count(test_asp_id)  # in app.py line 842
        t1 = time.perf_counter()
        asp_total_times.append((t1 - t0) * 1000.0)

    mean_dash = statistics.mean(asp_total_times)
    p50_dash = statistics.median(asp_total_times)
    benchmarks["SIMULATED_ASPIRANT_DASHBOARD_TOTAL"] = {
        "mean_ms": round(mean_dash, 2),
        "p50_ms": round(p50_dash, 2),
        "raw_runs": [round(t, 2) for t in asp_total_times]
    }
    print(f"  Simulated Full Aspirant Dashboard Load: p50={p50_dash:.2f} ms | mean={mean_dash:.2f} ms")

    # Save benchmark results
    out_file = PROJECT_ROOT / f"scratch/benchmark_{label.lower()}_{int(time.time())}.json"
    os.makedirs(out_file.parent, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({
            "label": label,
            "backend": backend,
            "timestamp": datetime.now().isoformat(),
            "benchmarks": benchmarks
        }, f, indent=2)
    print(f"\n[OK] Results saved to: {out_file.name}")
    print("=" * 75)
    return benchmarks


if __name__ == "__main__":
    run_benchmark_suite("BASELINE")

