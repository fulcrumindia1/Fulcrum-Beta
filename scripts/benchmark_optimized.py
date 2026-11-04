"""
scripts/benchmark_optimized.py — Measures post-optimization timings and generates before/after comparison
"""

import sys
import os
import time
import json
from statistics import median, mean

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.profiles import get_profile, get_profiles_batch
from services.relationships import get_aspirant_mentors, get_assigned_aspirants_for_guide, get_assigned_aspirants_for_sme
from services.schemes import list_schemes, match_schemes_for_aspirant, get_released_schemes_for_aspirant
from services.notifications import get_unread_count

TEST_ASPIRANT_ID = "6e667c86-84d3-4b65-b727-90f71f2b2875"
TEST_GUIDE_ID = "a21158e5-7850-4cad-94d2-1ef69e177765"
TEST_ADMIN_ID = "72655c43-9f13-4309-a8a0-194570a6c2aa"

def measure(fn, *args, iterations=5):
    timings = []
    for _ in range(iterations):
        t0 = time.perf_counter()
        fn(*args)
        t1 = time.perf_counter()
        timings.append((t1 - t0) * 1000)
    return {
        "p50_ms": round(median(timings), 2),
        "mean_ms": round(mean(timings), 2),
        "min_ms": round(min(timings), 2),
        "max_ms": round(max(timings), 2),
    }

print("Running Post-Optimization Benchmarks...")

# Baseline values recorded during Phase 0:
BASELINE = {
    "get_aspirant_mentors": {"p50": 2284.25, "mean": 2185.74},
    "get_profile": {"p50": 1877.41, "mean": 1944.59},
    "get_assigned_aspirants_for_guide": {"p50": 2015.40, "mean": 2049.20},
    "match_schemes_for_aspirant": {"p50": 2048.81, "mean": 2056.40},
    "list_schemes": {"p50": 655.25, "mean": 648.33},
    "get_unread_count": {"p50": 935.34, "mean": 948.71},
    "SIMULATED_ASPIRANT_DASHBOARD": {"p50": 7078.87, "mean": 9664.33}
}

res_mentors = measure(get_aspirant_mentors, TEST_ASPIRANT_ID)
res_profile = measure(get_profile, TEST_ASPIRANT_ID)
res_guide_asp = measure(get_assigned_aspirants_for_guide, TEST_GUIDE_ID)
res_match = measure(match_schemes_for_aspirant, TEST_ASPIRANT_ID)
res_schemes = measure(list_schemes, "", True)
res_unread = measure(get_unread_count, TEST_ASPIRANT_ID)

def simulate_aspirant_dashboard():
    p = get_profile(TEST_ASPIRANT_ID)
    m = get_aspirant_mentors(TEST_ASPIRANT_ID)
    r = get_released_schemes_for_aspirant(TEST_ASPIRANT_ID)
    u = get_unread_count(TEST_ASPIRANT_ID)
    return p, m, r, u

res_dash = measure(simulate_aspirant_dashboard)

CURRENT = {
    "get_aspirant_mentors": res_mentors,
    "get_profile": res_profile,
    "get_assigned_aspirants_for_guide": res_guide_asp,
    "match_schemes_for_aspirant": res_match,
    "list_schemes": res_schemes,
    "get_unread_count": res_unread,
    "SIMULATED_ASPIRANT_DASHBOARD": res_dash
}

print("\n" + "=" * 90)
print(f"{'OPERATION':<35} | {'BASELINE p50':<15} | {'OPTIMIZED p50':<15} | {'IMPROVEMENT':<15}")
print("=" * 90)

for op, base in BASELINE.items():
    curr = CURRENT[op]["p50_ms"]
    base_p50 = base["p50"]
    ratio = (base_p50 / curr) if curr > 0 else 999
    pct = ((base_p50 - curr) / base_p50) * 100
    print(f"{op:<35} | {base_p50:>10.2f} ms   | {curr:>10.2f} ms   | {pct:>6.1f}% ({ratio:.1f}x faster)")

print("=" * 90)

with open("benchmark_results.json", "w", encoding="utf-8") as f:
    json.dump({"baseline": BASELINE, "optimized": CURRENT}, f, indent=2)
print("Benchmark comparison saved to benchmark_results.json.")
