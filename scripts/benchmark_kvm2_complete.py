"""
scripts/benchmark_kvm2_complete.py
==================================
Comprehensive automated benchmark harness for KVM 2 optimization:
- Admin dashboard aggregate queries vs legacy full-table fetching
- Server-side pagination performance across entities
- PDF generation under 1, 2, and 3 concurrent workers
- Cache hit latency and invalidation
- Scheme matching determinism and performance
"""

import os
import sys
import time
import json
import psutil
import statistics
import threading
from concurrent.futures import ThreadPoolExecutor

# Ensure root is on PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.auth import get_supabase_admin_client, get_data_backend
from services.roles import SOLE_ADMIN_UUID
from services.admin_metrics import get_admin_dashboard_metrics
from services.pagination import (
    paginate_profiles,
    paginate_guides,
    paginate_smes,
    paginate_accounts,
)
from services.pdf_generator import generate_aspirant_dossier_pdf
from services.schemes import list_schemes, match_schemes_for_aspirant
from services.cache import get_memo, set_memo, invalidate_memo

def run_admin_metrics_benchmark():
    print("\n--- [BENCHMARK 1] Admin Dashboard Metrics ---")
    admin_id = SOLE_ADMIN_UUID

    # New Optimized Metrics (PostgREST HEAD requests)
    times_opt = []
    for _ in range(5):
        t0 = time.perf_counter()
        metrics = get_admin_dashboard_metrics(admin_id)
        times_opt.append((time.perf_counter() - t0) * 1000)

    p50_opt = statistics.median(times_opt)
    mean_opt = statistics.mean(times_opt)
    print(f"Optimized get_admin_dashboard_metrics: p50={p50_opt:.2f}ms, mean={mean_opt:.2f}ms")
    print(f"Metrics Output: {json.dumps(metrics, indent=2)}")

    # Legacy simulated full-table retrieval
    client = get_supabase_admin_client()
    t0 = time.perf_counter()
    p_res = client.table("profiles").select("*").execute()
    r_res = client.table("relationships").select("*").execute()
    h_res = client.table("help_requests").select("*").execute()
    s_res = client.table("schemes").select("*").execute()
    legacy_time = (time.perf_counter() - t0) * 1000
    legacy_rows = len(p_res.data or []) + len(r_res.data or []) + len(h_res.data or []) + len(s_res.data or [])
    print(f"Legacy Full Table Fetch: latency={legacy_time:.2f}ms, downloaded_rows={legacy_rows} (Estimated {legacy_rows * 1.5:.1f} KB transferred)")

    return {
        "optimized_p50_ms": round(p50_opt, 2),
        "optimized_mean_ms": round(mean_opt, 2),
        "legacy_ms": round(legacy_time, 2),
        "metrics": metrics,
        "payload_bytes_optimized": 0, # HEAD requests download 0 bytes payload
        "rows_downloaded_legacy": legacy_rows,
    }

def run_pagination_benchmark():
    print("\n--- [BENCHMARK 2] Server-Side Pagination ---")
    results = {}

    # Aspirants
    t0 = time.perf_counter()
    rows, total = paginate_profiles(role="aspirant", page=1, page_size=25)
    lat_asp = (time.perf_counter() - t0) * 1000
    results["aspirants_p1"] = {"latency_ms": round(lat_asp, 2), "returned_rows": len(rows), "total_in_db": total}
    print(f"paginate_profiles(aspirant, p1, 25): {lat_asp:.2f}ms, count={len(rows)}/{total}")

    # Guides
    t0 = time.perf_counter()
    g_rows, g_total = paginate_guides(page=1, page_size=25)
    lat_g = (time.perf_counter() - t0) * 1000
    results["guides_p1"] = {"latency_ms": round(lat_g, 2), "returned_rows": len(g_rows), "total_in_db": g_total}
    print(f"paginate_guides(p1, 25): {lat_g:.2f}ms, count={len(g_rows)}/{g_total}")

    # SMEs
    t0 = time.perf_counter()
    s_rows, s_total = paginate_smes(page=1, page_size=25)
    lat_s = (time.perf_counter() - t0) * 1000
    results["smes_p1"] = {"latency_ms": round(lat_s, 2), "returned_rows": len(s_rows), "total_in_db": s_total}
    print(f"paginate_smes(p1, 25): {lat_s:.2f}ms, count={len(s_rows)}/{s_total}")

    # Accounts
    t0 = time.perf_counter()
    a_rows, a_total = paginate_accounts(status="active_and_paused", page=1, page_size=25)
    lat_a = (time.perf_counter() - t0) * 1000
    results["accounts_active"] = {"latency_ms": round(lat_a, 2), "returned_rows": len(a_rows), "total_in_db": a_total}
    print(f"paginate_accounts(active_and_paused, p1, 25): {lat_a:.2f}ms, count={len(a_rows)}/{a_total}")

    return results

def run_pdf_concurrency_benchmark():
    print("\n--- [BENCHMARK 3] PDF Generation Concurrency (1, 2, 3 workers) ---")
    proc = psutil.Process()
    results = {}

    # Find a valid aspirant ID
    aspirants, _ = paginate_profiles(role="aspirant", page=1, page_size=1)
    target_aid = aspirants[0]["id"] if aspirants else SOLE_ADMIN_UUID

    for concurrency in [1, 2, 3]:
        print(f"\nTesting {concurrency} concurrent PDF export(s)...")
        mem_before = proc.memory_info().rss / (1024 * 1024)
        cpu_before = psutil.cpu_percent(interval=None)

        def _worker(worker_id):
            t0 = time.perf_counter()
            pdf_data = generate_aspirant_dossier_pdf(target_aid)
            dur = time.perf_counter() - t0
            size = len(pdf_data) if pdf_data else 0
            return {"worker": worker_id, "duration": dur, "size": size, "valid": size > 1000}

        t_start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=concurrency) as ex:
            futs = [ex.submit(_worker, i) for i in range(concurrency)]
            worker_results = [f.result(timeout=120) for f in futs]
        total_wall_time = time.perf_counter() - t_start

        mem_after = proc.memory_info().rss / (1024 * 1024)
        cpu_after = psutil.cpu_percent(interval=None)
        mem_delta = mem_after - mem_before

        durations = [r["duration"] for r in worker_results]
        all_valid = all(r["valid"] for r in worker_results)

        results[f"concurrency_{concurrency}"] = {
            "wall_time_s": round(total_wall_time, 2),
            "p50_duration_s": round(statistics.median(durations), 2),
            "max_duration_s": round(max(durations), 2),
            "mem_before_mb": round(mem_before, 1),
            "mem_after_mb": round(mem_after, 1),
            "mem_delta_mb": round(mem_delta, 1),
            "all_valid_pdf": all_valid,
            "sizes_bytes": [r["size"] for r in worker_results]
        }
        print(f"Results for Concurrency {concurrency}: Wall Time={total_wall_time:.2f}s, Median Latency={statistics.median(durations):.2f}s, RAM Delta={mem_delta:.1f}MB, All Valid={all_valid}")

    return results

def run_cache_and_schemes_benchmark():
    print("\n--- [BENCHMARK 4] Cache Performance & Scheme Matching Consistency ---")
    # Cache hit speed
    set_memo("bench_key", {"data": "test_payload"}, ttl_seconds=60)
    t0 = time.perf_counter()
    for _ in range(1000):
        get_memo("bench_key")
    cache_lat_us = ((time.perf_counter() - t0) / 1000) * 1_000_000
    print(f"In-Memory Cache Read Latency: {cache_lat_us:.3f} microseconds per lookup")

    # Invalidation
    invalidate_memo("bench_key")
    is_none = get_memo("bench_key") is None
    print(f"Cache Invalidation verified: {is_none}")

    # Schemes catalogue count and matching
    schemes = list_schemes()
    print(f"Active Schemes in Database: {len(schemes)} (Expected: 179)")
    assert len(schemes) == 179, f"Catalogue size altered! Found {len(schemes)}"

    # Synthetic aspirant profile matching consistency
    aspirants, _ = paginate_profiles(role="aspirant", page=1, page_size=1)
    if aspirants:
        aid = aspirants[0]["id"]
        t0 = time.perf_counter()
        matches_run1 = match_schemes_for_aspirant(aid, limit=10)
        dur1 = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        matches_run2 = match_schemes_for_aspirant(aid, limit=10)
        dur2 = (time.perf_counter() - t0) * 1000

        # Verify determinism
        names1 = [m.get("scheme_name") or m.get("name") for m in matches_run1]
        names2 = [m.get("scheme_name") or m.get("name") for m in matches_run2]
        deterministic = (names1 == names2)
        print(f"Scheme Matching (179 schemes): Run1={dur1:.2f}ms, Run2={dur2:.2f}ms, Deterministic={deterministic}")
    else:
        dur1, dur2, deterministic = 0, 0, True

    return {
        "cache_lookup_us": round(cache_lat_us, 3),
        "invalidation_verified": is_none,
        "schemes_catalogue_count": len(schemes),
        "scheme_matching_deterministic": deterministic,
        "scheme_matching_latency_ms": round(dur1, 2)
    }

def main():
    print("=" * 60)
    print("FULCRUM-BETA: KVM 2 PRODUCTION HARDENING BENCHMARK HARNESS")
    print("=" * 60)

    summary = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "backend": get_data_backend(),
        "python_version": sys.version.split()[0],
    }

    summary["admin_metrics"] = run_admin_metrics_benchmark()
    summary["pagination"] = run_pagination_benchmark()
    summary["pdf_concurrency"] = run_pdf_concurrency_benchmark()
    summary["cache_and_schemes"] = run_cache_and_schemes_benchmark()

    out_path = os.path.join(os.path.dirname(__file__), "..", "artifacts", "kvm2_hardening_benchmark_results.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 60)
    print(f"Benchmarks successfully recorded to {out_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()

