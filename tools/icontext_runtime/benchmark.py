"""Read-only reproducible timing samples; no assertions about LLM inference speed."""
import statistics
import subprocess
import sys
import time
import tempfile
from pathlib import Path

from context_runtime import inventory, read_json, iter_files, atomic_write, estimated_tokens


def percentile(values, fraction):
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, max(0, int(len(ordered) * fraction + 0.9999) - 1))]


def benchmark(root, samples=7):
    from icontext_cli import pack
    full, incremental, query, process_times = [], [], [], []
    reads, parses, full_reads, full_parses, token_samples = [], [], [], [], []
    for _ in range(samples):
        started = time.perf_counter()
        _, complete_stats = inventory(root, full=True)
        full.append((time.perf_counter() - started) * 1000)
        full_reads.append(complete_stats["files_read"])
        full_parses.append(complete_stats["ast_parses"])
        started = time.perf_counter()
        _, delta = inventory(root)
        incremental.append((time.perf_counter() - started) * 1000)
        reads.append(delta["files_read"])
        parses.append(delta["ast_parses"])
        started = time.perf_counter()
        payload = pack(root)
        query.append((time.perf_counter() - started) * 1000)
        token_samples.append(estimated_tokens(payload))
        started = time.perf_counter()
        child = subprocess.run([sys.executable, "-B", str(Path(__file__).parent / "icontext_cli.py"),
                                "pack", "--target", str(root), "--json"], capture_output=True, timeout=30)
        if child.returncode:
            raise RuntimeError(child.stderr.decode(errors="replace"))
        process_times.append((time.perf_counter() - started) * 1000)
    result = {"project": Path(root).name, "samples": samples, "state": "measured",
            "query_p50_ms": statistics.median(query), "query_p95_ms": percentile(query, .95),
            "process_query_p50_ms": statistics.median(process_times), "process_query_p95_ms": percentile(process_times, .95),
            "full_inventory_p50_ms": statistics.median(full), "incremental_inventory_p50_ms": statistics.median(incremental),
            "full_inventory_p95_ms": percentile(full, .95), "incremental_inventory_p95_ms": percentile(incremental, .95),
            "incremental_files_read": reads, "incremental_ast_parses": parses,
            "full_files_read": full_reads, "full_ast_parses": full_parses,
            "context_pack_estimated_tokens": token_samples,
            "token_method": "heuristic, not provider token accounting", "includes_llm_inference": False}
    # Audit comparisons run in a verified temporary clone. The target repository
    # stays read-only, including its reports and caches.
    try:
        from metricsthinking.engine import run_audit
    except ImportError:
        result["audit_measurement"] = "unavailable: optional audit dependencies missing"
        return result
    with tempfile.TemporaryDirectory(prefix="icontext_benchmark_") as temporary:
        fixture = Path(temporary).resolve()
        fixture.relative_to(Path(tempfile.gettempdir()).resolve())
        for source in iter_files(root):
            atomic_write(fixture / source.relative_to(root), source.read_bytes())
        full_audits, warm_audits = [], []
        for _ in range(3):
            started = time.perf_counter()
            run_audit(str(fixture), quiet=True, full=True, reconcile_plans=False)
            full_audits.append((time.perf_counter() - started) * 1000)
            started = time.perf_counter()
            run_audit(str(fixture), quiet=True, reconcile_plans=False)
            warm_audits.append((time.perf_counter() - started) * 1000)
        result["full_audit_p50_ms"] = statistics.median(full_audits)
        result["incremental_audit_p50_ms"] = statistics.median(warm_audits)
        result["audit_samples"] = len(full_audits)
        result["full_audit_p95_ms"] = percentile(full_audits, .95)
        result["incremental_audit_p95_ms"] = percentile(warm_audits, .95)
        result["incremental_audit_reduction_pct"] = 100 * (1 - statistics.median(warm_audits) / statistics.median(full_audits))
        result["audit_fixture"] = "governed files in temporary clone; no Git internals"
    return result
