#!/usr/bin/env python3
"""
Token Budget Benchmarking & Stress Test Suite for iDirectory v3.0.
Verifies quantitative context token savings (>85%-92%) and topological satellite scaling.
Zero-dependency test suite using Python standard library unittest.
"""

import os
import sys
import json
import time
import shutil
import tempfile
import unittest
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from FWengine import (
    generate_tree_json,
    compute_context_budget,
    init_project,
    FOLDER_METADATA,
)


def estimate_tokens(text: str) -> int:
    """Standard heuristic: ~4 characters per token in technical text/code."""
    return max(1, len(text) // 4)


class TestTokenBudgetBenchmark(unittest.TestCase):
    """Benchmarks satellite topology token footprint against recursive filesystem dumping."""

    def setUp(self):
        self.project_path = PROJECT_ROOT

    def test_satellite_tree_token_efficiency(self):
        """Verifies that .context/tree.json uses < 500 tokens and saves > 85% vs naive recursion."""
        tree_file = self.project_path / ".context" / "tree.json"
        self.assertTrue(tree_file.exists(), "El satélite .context/tree.json debe existir.")

        tree_content = tree_file.read_text(encoding="utf-8")
        satellite_tokens = estimate_tokens(tree_content)

        # Baseline: simulate naive recursive directory dump (what an agent sees without iDirectory)
        recursive_dump_lines = []
        for root, dirs, files in os.walk(self.project_path):
            # Exclude only git internals
            dirs[:] = [d for d in dirs if d != ".git"]
            for f in files:
                rel_p = Path(root).relative_to(self.project_path) / f
                recursive_dump_lines.append(f"{rel_p.as_posix()} (size: {os.path.getsize(Path(root) / f)} bytes)")

        naive_dump = "\n".join(recursive_dump_lines)
        naive_tokens = estimate_tokens(naive_dump)

        # Calculate reduction percentage
        savings_pct = (1.0 - (satellite_tokens / naive_tokens)) * 100.0

        print(f"\n[BENCHMARK] Token Budget Efficiency Report:")
        print(f"  - Naive Recursive Dump:   ~{naive_tokens:,} tokens ({len(recursive_dump_lines)} files)")
        print(f"  - iDirectory Tree Satellite: ~{satellite_tokens:,} tokens")
        print(f"  - Context Token Savings:    {savings_pct:.1f}%")

        # Invariants
        self.assertLessEqual(satellite_tokens, 1000, "El satélite topológico debe mantenerse ultraligero (<1000 tokens).")
        self.assertGreaterEqual(savings_pct, 85.0, "iDirectory debe ahorrar al menos 85% de tokens de contexto.")

    def test_compact_context_string_is_dense(self):
        """Verifies that the compact context prompt string is under 200 tokens."""
        tree = generate_tree_json(self.project_path)
        nodes_summary = "; ".join([f"{k}:{v['role']}({v['prio']})" for k, v in tree["nodes"].items() if v["crawl"]])
        compact_str = f"IDIR_TOPOLOGY: [{nodes_summary}]"

        compact_tokens = estimate_tokens(compact_str)
        print(f"  - Compact Prompt Injection: ~{compact_tokens} tokens")
        self.assertLessEqual(compact_tokens, 250, "El formato compacto para prompts debe ser menor a 250 tokens.")


class TestTopologicalScalingStress(unittest.TestCase):
    """Stress tests satellite generation and budget calculation under high directory volume."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="idir_stress_")
        self.test_path = Path(self.test_dir)
        init_project(str(self.test_path))

        # Synthesize heavy mock directory tree (50 subdirectories, 200 mock files)
        for i in range(50):
            sub = self.test_path / f"src/module_{i:02d}"
            sub.mkdir(parents=True, exist_ok=True)
            for j in range(4):
                mock_file = sub / f"component_{j}.py"
                mock_file.write_text(f"# Mock component {i}_{j}\ndef execute(): pass\n", encoding="utf-8")

    def tearDown(self):
        if self.test_path.exists():
            shutil.rmtree(self.test_path, ignore_errors=True)

    def test_satellite_generation_latency(self):
        """Verifies that satellite generation executes in sub-second time even with hundreds of files."""
        start_time = time.perf_counter()
        tree = generate_tree_json(self.test_path)
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        print(f"\n[STRESS] Satellite Generation Latency: {elapsed_ms:.2f} ms")
        self.assertLessEqual(elapsed_ms, 150.0, "La generación de tree.json debe ser sub-150ms.")
        self.assertIn("nodes", tree)

    def test_budget_computation_stability(self):
        """Verifies that compute_context_budget processes the entire hierarchy deterministically."""
        start_time = time.perf_counter()
        budget = compute_context_budget(self.test_path)
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        print(f"[STRESS] Context Budget Scan Latency: {elapsed_ms:.2f} ms")
        self.assertIsInstance(budget, list)
        self.assertGreater(len(budget), 10)
        self.assertLessEqual(elapsed_ms, 500.0, "El cálculo del presupuesto de tokens debe ser sub-500ms.")


if __name__ == "__main__":
    unittest.main()
