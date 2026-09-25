#!/usr/bin/env python3
"""
Unit tests for iDirectory v3.0 Governance & Scaffolding Engine (FWengine.py).
Zero-dependency test suite using Python standard library unittest.
"""

import os
import sys
import json
import shutil
import tempfile
import unittest
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import FWengine
from FWengine import (
    MiniYAML,
    FOLDER_METADATA,
    ROUTING_MAP,
    sync_beacons,
    sync_tree,
    generate_tree_json,
    compute_context_budget,
    audit_repository,
    init_project,
)


class TestMiniYAML(unittest.TestCase):
    """Verifies that the lightweight MiniYAML parser and serializer operate correctly."""

    def test_dump_scalars_and_dict(self):
        data = {
            "version": 1.0,
            "directory": "src/core",
            "crawl": True,
            "read_priority": "p1",
            "items_count": 42,
            "description": "Núcleo del sistema",
        }
        dumped = MiniYAML.dump(data)
        self.assertIn("version: 1.0", dumped)
        self.assertIn("directory: src/core", dumped)
        self.assertIn("crawl: true", dumped)
        self.assertIn("read_priority: p1", dumped)
        self.assertIn("items_count: 42", dumped)

    def test_dump_and_load_list(self):
        data = {
            "key_files": ["engine_readme.md", "FWengine.py"],
            "tags": ["governance", "context-engineering"],
        }
        dumped = MiniYAML.dump(data)
        loaded = MiniYAML.load(dumped)
        self.assertIn("key_files", loaded)
        self.assertEqual(len(loaded["key_files"]), 2)
        self.assertIn("engine_readme.md", loaded["key_files"])
        self.assertEqual(loaded["tags"], ["governance", "context-engineering"])

    def test_load_boolean_and_null(self):
        yaml_content = """
        crawl: false
        active: true
        backup: null
        priority: p0
        """
        loaded = MiniYAML.load(yaml_content)
        self.assertFalse(loaded["crawl"])
        self.assertTrue(loaded["active"])
        self.assertIsNone(loaded["backup"])
        self.assertEqual(loaded["priority"], "p0")

    def test_roundtrip_nested(self):
        original = {
            "version": 1.0,
            "role": "core_engine",
            "crawl": True,
            "key_files": ["a.txt", "b.py"],
        }
        dumped = MiniYAML.dump(original)
        loaded = MiniYAML.load(dumped)
        self.assertEqual(loaded["role"], original["role"])
        self.assertEqual(loaded["crawl"], original["crawl"])
        self.assertEqual(loaded["key_files"], original["key_files"])


class TestTopologicalManifest(unittest.TestCase):
    """Verifies that the canonical topological metadata adheres to architectural invariants."""

    def test_all_folders_are_lowercase(self):
        """All canonical folder keys must be strictly lowercase."""
        for folder in FOLDER_METADATA.keys():
            self.assertEqual(
                folder,
                folder.lower(),
                f"La carpeta '{folder}' en FOLDER_METADATA debe estar estrictamente en minúsculas (all-lowercase).",
            )

    def test_required_metadata_fields(self):
        """Every canonical folder must declare purpose, role, relevance, crawl, and read_priority."""
        required_fields = ["purpose", "role", "relevance", "crawl", "read_priority"]
        for folder, meta in FOLDER_METADATA.items():
            for field in required_fields:
                self.assertIn(
                    field,
                    meta,
                    f"Falta el campo obligatorio '{field}' en la carpeta '{folder}'.",
                )

    def test_pruning_policy_invariants(self):
        """Heavy data folders must have crawl set to False."""
        no_crawl_folders = ["data/raw", "data/processed", "data/sandbox", "logs", "artifacts/plans/archive"]
        for folder in no_crawl_folders:
            if folder in FOLDER_METADATA:
                self.assertFalse(
                    FOLDER_METADATA[folder]["crawl"],
                    f"La carpeta '{folder}' debe tener 'crawl: False' para prevenir degradación de contexto.",
                )


class TestRoutingMapAndHeuristics(unittest.TestCase):
    """Verifies deterministic and heuristic file routing."""

    def test_routing_map_destinations_are_canonical(self):
        """All mapped destinations must exist in FOLDER_METADATA or be valid infrastructure directory."""
        for ext, dest in ROUTING_MAP.items():
            self.assertTrue(
                dest in FOLDER_METADATA or dest == "infrastructure",
                f"La extensión '{ext}' apunta a '{dest}', la cual no está en FOLDER_METADATA.",
            )

    def test_notebooks_route_to_research(self):
        self.assertEqual(ROUTING_MAP.get(".ipynb"), "03_research/notebooks")

    def test_sql_routes_to_cloud_jobs(self):
        self.assertEqual(ROUTING_MAP.get(".sql"), "src/cloud_jobs")

    def test_schemas_route_to_schemas(self):
        self.assertEqual(ROUTING_MAP.get(".json"), "schemas")
        self.assertEqual(ROUTING_MAP.get(".avsc"), "schemas")


class TestLifecycleAndIdempotence(unittest.TestCase):
    """Tests project initialization, beacon synchronization, and satellite generation in isolation."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="idir_test_")
        self.test_path = Path(self.test_dir)

    def tearDown(self):
        if self.test_path.exists():
            shutil.rmtree(self.test_path, ignore_errors=True)

    def test_init_project_creates_structure(self):
        init_project(str(self.test_path))

        # Check key folders
        self.assertTrue((self.test_path / ".context").exists())
        self.assertTrue((self.test_path / "01_seed").exists())
        self.assertTrue((self.test_path / "02_foundation" / "engine").exists())
        self.assertTrue((self.test_path / "src" / "core").exists())

        # Check files
        self.assertTrue((self.test_path / ".context" / "tree.json").exists())
        self.assertTrue((self.test_path / ".agentignore").exists())
        self.assertTrue((self.test_path / ".gitignore").exists())

    def test_sync_beacons_idempotency(self):
        init_project(str(self.test_path))

        # First sync
        count1 = sync_beacons(self.test_path)
        self.assertGreater(count1, 15)

        # Record modification times and contents
        beacon_sample = self.test_path / "01_seed" / ".context.yaml"
        content1 = beacon_sample.read_text(encoding="utf-8")

        # Second sync
        count2 = sync_beacons(self.test_path)
        content2 = beacon_sample.read_text(encoding="utf-8")

        self.assertEqual(count1, count2)
        self.assertEqual(content1, content2)

    def test_sync_tree_generates_valid_schema(self):
        init_project(str(self.test_path))
        tree_path = sync_tree(self.test_path)
        self.assertTrue(tree_path.exists())

        tree_data = json.loads(tree_path.read_text(encoding="utf-8"))
        self.assertEqual(tree_data["version"], "3.0")
        self.assertTrue(len(tree_data["project"]) > 0)
        self.assertIn("bootloader", tree_data)
        self.assertIn("nodes", tree_data)
        self.assertIn("01_seed", tree_data["nodes"])

    def test_audit_repository_pass_and_fail(self):
        init_project(str(self.test_path))
        # Brand new initialized project should pass audit
        self.assertTrue(audit_repository(self.test_path))

        # Introduce an uppercase directory violation
        bad_dir = self.test_path / "BadFolder"
        bad_dir.mkdir()
        self.assertFalse(audit_repository(self.test_path))
        bad_dir.rmdir()

        # Remove a beacon to trigger missing beacon violation
        beacon_file = self.test_path / "01_seed" / ".context.yaml"
        beacon_file.unlink()
        self.assertFalse(audit_repository(self.test_path))


class TestTokenBudgetComputation(unittest.TestCase):
    """Tests the context token budget calculator."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="idir_budget_test_")
        self.test_path = Path(self.test_dir)
        init_project(str(self.test_path))

    def tearDown(self):
        if self.test_path.exists():
            shutil.rmtree(self.test_path, ignore_errors=True)

    def test_compute_budget_returns_records(self):
        budget = compute_context_budget(self.test_path)
        self.assertIsInstance(budget, list)
        self.assertGreater(len(budget), 10)

        first = budget[0]
        self.assertIn("directory", first)
        self.assertIn("role", first)
        self.assertIn("est_tokens", first)
        self.assertIn("crawl", first)


if __name__ == "__main__":
    unittest.main()
