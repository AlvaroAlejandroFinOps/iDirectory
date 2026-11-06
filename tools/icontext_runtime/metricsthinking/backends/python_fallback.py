"""
Pure Python High-Efficiency Fallback Backend for MetricsThinking™ v4.0.

Provides single-pass directory scanning with incremental SHA-256 caching,
AST dependency coupling (Ca, Ce, Instability, SPOFs), Shannon entropy,
and k-shingle Jaccard overlap when native Rust extension is not available.
"""

from collections import Counter
import hashlib
import json
import math
import os
from pathlib import Path
import re
from typing import Any

DEFAULT_EXCLUDED_DIRS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__",
    ".pytest_cache", ".ruff_cache", ".mypy_cache", "dist", "build",
    ".egg-info", "data/raw", "data/processed", "data/sandbox", ".system_generated"
}

_MEMORY_CONTENT_CACHE: dict[tuple[str, float, int], str] = {}


def fast_shannon_entropy(data: str) -> float:
    """Computes Shannon entropy in bits per symbol."""
    if not data:
        return 0.0
    length = len(data)
    counts = Counter(data)
    return -sum((count / length) * math.log2(count / length) for count in counts.values())


def calculate_shingling_jaccard(a: str, b: str, k: int = 3) -> float:
    """Computes k-shingle Jaccard similarity between two texts."""
    words_a = re.findall(r"\w+", a.lower())
    words_b = re.findall(r"\w+", b.lower())

    if len(words_a) < k:
        shingles_a = set(words_a)
    else:
        shingles_a = {" ".join(words_a[i:i+k]) for i in range(len(words_a) - k + 1)}

    if len(words_b) < k:
        shingles_b = set(words_b)
    else:
        shingles_b = {" ".join(words_b[i:i+k]) for i in range(len(words_b) - k + 1)}

    union = len(shingles_a.union(shingles_b))
    if union == 0:
        return 0.0
    intersection = len(shingles_a.intersection(shingles_b))
    return round(intersection / union, 4)


def scan_directory(path, ignore_patterns=None, include_content=True, cache_path=None, persist=False, full=False):
    from ..runtime import iter_files, read_json, write_json, digest
    root = Path(path).resolve()
    cache_file = Path(cache_path) if cache_path else root / ".context/cache/scan_cache_v6.json"
    previous = read_json(cache_file)
    records, stored = [], {}
    for file_path in iter_files(root, ignore_patterns):
        relative = file_path.relative_to(root).as_posix()
        if file_path.resolve() == cache_file.resolve():
            continue
        st = file_path.stat()
        stamp = [st.st_size, st.st_mtime_ns]
        cached = previous.get(relative, {})
        if not full and cached.get("stat") == stamp:
            record = dict(cached["record"])
        else:
            raw = file_path.read_bytes()
            binary = b"\0" in raw[:1024] or file_path.suffix.lower() in {".png", ".jpg", ".pdf", ".zip", ".exe", ".dll", ".parquet"}
            content = raw.decode("utf-8", errors="replace") if not binary and len(raw) < 2 * 1024 * 1024 else None
            record = {"path": relative, "size_bytes": len(raw), "sha256": digest(raw),
                      "line_count": len(content.splitlines()) if content else 0,
                      "token_estimate": max(1, len(content) // 4) if content else 0, "content": content}
        stored[relative] = {"stat": stamp, "record": record}
        result = dict(record)
        if not include_content:
            result["content"] = None
        records.append(result)
    if persist:
        write_json(cache_file, stored)
    return records


def compute_ast_coupling(python_files: dict[str, str]) -> dict[str, Any]:
    """
    Computes Afferent Coupling (Ca), Efferent Coupling (Ce), Instability (I),
    SPOF identification, and resilience pattern detection across Python source files.
    """
    all_modules: set[str] = set()
    import_graph: dict[str, set[str]] = {}

    for path in python_files.keys():
        norm = path.replace("\\", "/").rstrip(".py")
        mod_name = norm.replace("/", ".")
        all_modules.add(mod_name)
        import_graph[mod_name] = set()

    resilience_patterns: dict[str, int] = {
        "timeout": 0,
        "retry": 0,
        "circuit_breaker": 0,
        "fallback": 0,
    }

    for path, content in python_files.items():
        norm = path.replace("\\", "/").rstrip(".py")
        mod_name = norm.replace("/", ".")
        deps: set[str] = set()

        for line in content.splitlines():
            stripped = line.strip()

            # Scan resilience patterns
            if "timeout" in stripped.lower() or "timeout=" in stripped:
                resilience_patterns["timeout"] += 1
            if "retry" in stripped.lower() or "backoff" in stripped.lower():
                resilience_patterns["retry"] += 1
            if "circuit_breaker" in stripped.lower() or "circuitbreaker" in stripped.lower():
                resilience_patterns["circuit_breaker"] += 1
            if "fallback" in stripped.lower():
                resilience_patterns["fallback"] += 1

            # Imports
            if stripped.startswith("import ") or stripped.startswith("from "):
                for other in all_modules:
                    if other != mod_name and (other in stripped or other.split(".")[-1] in stripped):
                        deps.add(other)

        import_graph[mod_name] = deps

    ca: dict[str, int] = {m: 0 for m in all_modules}
    ce: dict[str, int] = {m: len(deps) for m, deps in import_graph.items()}
    instability: dict[str, float] = {}

    for src, targets in import_graph.items():
        for target in targets:
            if target in ca:
                ca[target] += 1

    spof_nodes: list[str] = []
    for m in sorted(list(all_modules)):
        aff = ca[m]
        eff = ce[m]
        tot = aff + eff
        inst = round(eff / tot, 3) if tot > 0 else 0.0
        instability[m] = inst

        # Single Point of Failure (SPOF): High afferent coupling (>= 3) and low efferent coupling (<= 1)
        if aff >= 3 and eff <= 1:
            spof_nodes.append(m)

    # Coverage ratio of critical modules having resilience patterns
    total_patterns = sum(resilience_patterns.values())
    resilience_coverage_ratio = round(min(1.0, total_patterns / max(1, len(all_modules))), 3)

    return {
        "afferent_coupling_ca": ca,
        "efferent_coupling_ce": ce,
        "instability_i": instability,
        "spof_nodes": spof_nodes,
        "resilience_patterns_count": resilience_patterns,
        "resilience_coverage_ratio": resilience_coverage_ratio,
    }
