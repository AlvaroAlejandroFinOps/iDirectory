"""
Seed-to-Code Drift Detection Auditor.

Compares repository implementation against the architectural ground truth in 01_seed/.
"""

from pathlib import Path
import re
from typing import Any


def audit_seed_to_code_drift(
    seed_path: str,
    repo_files: dict[str, str],
) -> dict[str, Any]:
    """
    Audits discrepancies between the architecture declared in the Seed and the physical repository.

    Returns:
        {
            "drift_detected": bool,
            "missing_files": list[str],
            "undocumented_files": list[str],
            "signature_mismatches": list[dict],
            "drift_score": float,  # 0.0 to 1.0
        }
    """
    seed_p = Path(seed_path)
    if not seed_p.exists():
        return {
            "drift_detected": True,
            "missing_files": [],
            "undocumented_files": list(repo_files.keys()),
            "signature_mismatches": [{"error": f"Seed file not found: {seed_path}"}],
            "drift_score": 1.0,
        }

    seed_content = seed_p.read_text(encoding="utf-8", errors="replace")

    # Extract declared paths from seed markdown (e.g. `src/...`, `crates/...`, `config/...`)
    declared_paths: set[str] = set()
    # Matches patterns like `src/metricsthinking/engine.py` or `./src/...`
    matches = re.findall(r"`(?:\./)?([a-zA-Z0-9_\-./]+\.[a-zA-Z0-9]+)`", seed_content)
    for m in matches:
        clean = m.replace("\\", "/").lstrip("./")
        if "/" in clean and not clean.startswith("http"):
            declared_paths.add(clean)

    # Filter repo source files (exclude tests, cache, git, artifacts)
    relevant_repo_files: set[str] = set()
    for f in repo_files.keys():
        norm = f.replace("\\", "/").lstrip("./")
        if (
            norm.startswith("src/")
            or norm.startswith("crates/")
            or norm.startswith("schemas/")
            or norm.startswith("config/")
        ):
            if not any(ign in norm for ign in ["__pycache__", ".pytest_cache", ".git"]):
                relevant_repo_files.add(norm)

    # Missing files: declared in seed as key components but missing from repo
    missing_files = sorted(list(declared_paths - relevant_repo_files))
    # Undocumented files: in src/ but not mentioned in seed
    undocumented_files = sorted(list(relevant_repo_files - declared_paths))

    # AST signature mismatch check (v5.0): verify public symbols in Python files appear in Seed
    import ast
    signature_mismatches: list[dict[str, Any]] = []
    for rel_f, src_text in sorted(repo_files.items()):
        norm = rel_f.replace("\\", "/").lstrip("./")
        if not norm.endswith(".py") or not (norm.startswith("src/") or norm.startswith("scripts/")):
            continue
        if not src_text or len(src_text) < 10:
            continue
        try:
            tree = ast.parse(src_text)
        except Exception:
            continue
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and not node.name.startswith("_"):
                if node.name not in seed_content:
                    signature_mismatches.append({
                        "file": norm,
                        "symbol": node.name,
                        "reason": "Public AST symbol missing from Seed Section 4.1",
                    })

    total = max(1, len(relevant_repo_files) + len(missing_files))
    drift_score = round(min(1.0, (len(missing_files) + len(undocumented_files)) / total), 4)
    drift_detected = drift_score > 0.0 or len(missing_files) > 0 or len(signature_mismatches) > 0

    return {
        "drift_detected": drift_detected,
        "missing_files": missing_files,
        "undocumented_files": undocumented_files,
        "signature_mismatches": signature_mismatches[:20],
        "drift_score": drift_score,
    }
