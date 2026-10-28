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
import time
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
    resolve_beacon,
    inspect_python_header,
    route_file,
    check_satellite_freshness,
    safe_io_retry,
    safe_rename_casing,
    discover_unbeaconed_directories,
    scaffold_beacon_for_dir,
    generate_sliced_tree,
    format_sliced_tree,
    validate_beacon_data,
    validate_tree_data,
    build_context_pack,
    get_seed_sections,
    extract_seed_section,
    manage_checkpoint,
    reconcile_repository,
    estimate_tokens_v4,
    compute_node_fingerprint,
    reconcile_plans_lifecycle,
    validate_backlog_queue,
    validate_dependency_dag,
    validate_backlog_data,
    SLICE_CHAR_BUDGET,
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

    def test_escaped_quotes_roundtrip(self):
        original = {
            "purpose": 'Motor con "comillas" internas: v3.3',
            "key_files": ['mod.py: fn(a="x") -> bool'],
        }
        dumped = MiniYAML.dump(original)
        loaded = MiniYAML.load(dumped)
        self.assertEqual(loaded["purpose"], original["purpose"])
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
        self.assertEqual(tree_data["version"], "4.0")
        self.assertEqual(len(tree_data["topology_hash"]), 64)
        self.assertTrue(len(tree_data["project"]) > 0)
        self.assertIn("bootloader", tree_data)
        self.assertIn("nodes", tree_data)
        self.assertIn("01_seed", tree_data["nodes"])
        self.assertEqual(validate_tree_data(tree_data), [])

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

    def test_dynamic_seed_name_resolution(self):
        """Verifies that in a repo named SemanticFlow, 01_seed/.context.yaml and tree.json reference seed-semanticflow-master.md."""
        sem_dir = self.test_path / "SemanticFlow"
        sem_dir.mkdir(parents=True, exist_ok=True)
        init_project(str(sem_dir))

        beacon_path = sem_dir / "01_seed" / ".context.yaml"
        self.assertTrue(beacon_path.exists())
        loaded_beacon = MiniYAML.load(beacon_path.read_text(encoding="utf-8"))
        self.assertIn("key_files", loaded_beacon)
        self.assertIn("seed-semanticflow-master.md", loaded_beacon["key_files"])
        self.assertNotIn("seed-idirectory-master.md", loaded_beacon["key_files"])

        tree_path = sem_dir / ".context" / "tree.json"
        tree_data = json.loads(tree_path.read_text(encoding="utf-8"))
        self.assertIn("01_seed/seed-semanticflow-master.md", tree_data["bootloader"]["tier_2"])
        self.assertNotIn("seed-idirectory-master.md", str(tree_data))

    def test_domain_extension_autodiscovery(self):
        """Verifies that non-canonical first-level directories like crates/ are discovered as domain_extension."""
        init_project(str(self.test_path))
        crates_dir = self.test_path / "crates"
        crates_dir.mkdir(parents=True, exist_ok=True)

        tree_path = sync_tree(self.test_path)
        tree_data = json.loads(tree_path.read_text(encoding="utf-8"))
        self.assertIn("crates", tree_data["nodes"])
        self.assertEqual(tree_data["nodes"]["crates"]["role"], "domain_extension")
        self.assertEqual(tree_data["nodes"]["crates"]["prio"], "p1")
        self.assertTrue(tree_data["nodes"]["crates"]["crawl"])

    def test_tree_schema_file_exists(self):
        """Verifies that the $schema pointer in .context/tree.json resolves to an existing file."""
        init_project(str(self.test_path))
        tree_path = sync_tree(self.test_path)
        tree_data = json.loads(tree_path.read_text(encoding="utf-8"))
        schema_rel = tree_data.get("$schema")
        self.assertIsNotNone(schema_rel)
        main_schema = PROJECT_ROOT / "schemas" / "tree.schema.json"
        self.assertTrue(main_schema.exists(), f"El archivo {main_schema} debe existir físicamente.")
        self.assertEqual(tree_data["$schema"], "../schemas/tree.schema.json")


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


class TestBeaconInheritance(unittest.TestCase):
    """Verifies hierarchical beacon directive resolution and strict pruning inheritance."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="idir_inherit_test_")
        self.test_path = Path(self.test_dir)
        init_project(str(self.test_path))

    def tearDown(self):
        if self.test_path.exists():
            shutil.rmtree(self.test_path, ignore_errors=True)

    def test_child_inherits_from_parent_beacon(self):
        """A subfolder inside src/cloud_jobs must inherit its parent directives."""
        subfolder = self.test_path / "src" / "cloud_jobs" / "etl_daily"
        subfolder.mkdir(parents=True, exist_ok=True)
        # Verify no local beacon exists
        self.assertFalse((subfolder / ".context.yaml").exists())

        resolved = resolve_beacon(subfolder, self.test_path)
        self.assertEqual(resolved["role"], "production_pipelines")
        self.assertEqual(resolved["read_priority"], "p1")
        self.assertTrue(resolved["crawl"])
        self.assertTrue(resolved["inherited"])
        self.assertEqual(resolved["inherited_from"], "src/cloud_jobs")

    def test_strict_pruning_inheritance(self):
        """If an ancestor declares crawl: false, no child can override it."""
        deep_raw = self.test_path / "data" / "raw" / "incoming" / "batch_01"
        deep_raw.mkdir(parents=True, exist_ok=True)

        resolved = resolve_beacon(deep_raw, self.test_path)
        self.assertFalse(resolved["crawl"], "Subdirectorio dentro de data/raw debe heredar crawl: False.")

        # Even if a child local beacon declares crawl: true, pruning is invariant
        child_beacon = deep_raw / ".context.yaml"
        child_beacon.write_text("crawl: true\nrole: custom_raw\n", encoding="utf-8")
        resolved_override = resolve_beacon(deep_raw, self.test_path)
        self.assertFalse(resolved_override["crawl"], "Poda debe ser absorbente aun si el hijo declara crawl: true.")


class TestHybridRouting(unittest.TestCase):
    """Verifies light header inspection and content-based routing for Python files."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="idir_route_test_")
        self.test_path = Path(self.test_dir)
        init_project(str(self.test_path))

    def tearDown(self):
        if self.test_path.exists():
            shutil.rmtree(self.test_path, ignore_errors=True)

    def test_inspect_pytest_routes_to_tests(self):
        test_file = self.test_path / "sample_service.py"
        test_file.write_text("import pytest\n\ndef test_add():\n    assert 1 + 1 == 2\n", encoding="utf-8")
        dest = route_file(str(test_file), base_path=str(self.test_path), move=False)
        self.assertEqual(dest.parent.name, "tests")

    def test_inspect_cloud_jobs_routes_to_cloud_jobs(self):
        spark_file = self.test_path / "daily_aggregate.py"
        spark_file.write_text("from pyspark.sql import SparkSession\nfrom google.cloud import bigquery\n", encoding="utf-8")
        dest = route_file(str(spark_file), base_path=str(self.test_path), move=False)
        self.assertTrue(str(dest).replace("\\", "/").endswith("src/cloud_jobs/daily_aggregate.py"))

    def test_inspect_dashboards_routes_to_dashboards(self):
        dash_file = self.test_path / "executive_report.py"
        dash_file.write_text("import streamlit as st\nimport plotly.express as px\nst.title('KPIs')\n", encoding="utf-8")
        dest = route_file(str(dash_file), base_path=str(self.test_path), move=False)
        self.assertTrue(str(dest).replace("\\", "/").endswith("src/dashboards/executive_report.py"))

    def test_inspect_fallback_routes_to_core(self):
        core_file = self.test_path / "auth_provider.py"
        core_file.write_text("class AuthProvider:\n    def authenticate(self, token: str) -> bool:\n        return True\n", encoding="utf-8")
        dest = route_file(str(core_file), base_path=str(self.test_path), move=False)
        self.assertTrue(str(dest).replace("\\", "/").endswith("src/core/auth_provider.py"))

    def test_header_inspection_with_long_docstring(self):
        """Verifies that a python file with >2000 chars of docstrings before import pytest routes to tests."""
        test_file = self.test_path / "long_header_service.py"
        long_docstring = '"""\n' + ("A" * 2500) + '\n"""\nimport pytest\n\ndef test_feature():\n    pass\n'
        test_file.write_text(long_docstring, encoding="utf-8")
        dest = route_file(str(test_file), base_path=str(self.test_path), move=False)
        self.assertEqual(dest.parent.name, "tests")


class TestFileSystemHardening(unittest.TestCase):
    """Verifies security controls against path traversal and atomic Windows NTFS casing handling."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="idir_fs_test_")
        self.test_path = Path(self.test_dir)
        init_project(str(self.test_path))

    def tearDown(self):
        if self.test_path.exists():
            shutil.rmtree(self.test_path, ignore_errors=True)

    def test_path_traversal_blocked(self):
        # 1. Archivo ubicado fuera de la raíz del proyecto
        outside_file = self.test_path / "normal.txt"
        outside_file.write_text("hello", encoding="utf-8")
        with self.assertRaises(PermissionError):
            route_file(str(outside_file), base_path=str(self.test_path / "subdir"), move=True)

        # 2. Argumento con '../' intentando escapar
        with self.assertRaises(PermissionError):
            route_file("../escape.py", base_path=str(self.test_path), move=True)

    def test_casing_collision_atomic_rename(self):
        """Moving or normalizing a file with uppercase letters must rename to lowercase without error."""
        file_path = self.test_path / "MyPipelineJob.py"
        file_path.write_text("from pyspark.sql import functions as F\n", encoding="utf-8")

        dest = route_file(str(file_path), base_path=str(self.test_path), move=True)
        self.assertTrue(dest.exists())
        self.assertEqual(dest.name, "mypipelinejob.py")
        self.assertFalse(file_path.exists())

    def test_route_move_collision_protection(self):
        """Moving a file when target exists must raise FileExistsError if overwrite=False, and succeed if overwrite=True."""
        src_file = self.test_path / "incoming_job.py"
        src_file.write_text("print('version 1')\n", encoding="utf-8")
        target_dir = self.test_path / "src" / "core"
        target_dir.mkdir(parents=True, exist_ok=True)
        dest_file = target_dir / "incoming_job.py"
        dest_file.write_text("print('existing version')\n", encoding="utf-8")

        # Without overwrite, must raise FileExistsError
        with self.assertRaises(FileExistsError):
            route_file(str(src_file), base_path=str(self.test_path), move=True, overwrite=False)
        self.assertEqual(dest_file.read_text(encoding="utf-8"), "print('existing version')\n")
        self.assertTrue(src_file.exists())

        # With overwrite=True, must overwrite target
        route_file(str(src_file), base_path=str(self.test_path), move=True, overwrite=True)
        self.assertEqual(dest_file.read_text(encoding="utf-8"), "print('version 1')\n")
        self.assertFalse(src_file.exists())


class TestSatelliteFreshness(unittest.TestCase):
    """Verifies drift detection between .context/tree.json and key project directories."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="idir_fresh_test_")
        self.test_path = Path(self.test_dir)
        init_project(str(self.test_path))

    def tearDown(self):
        if self.test_path.exists():
            shutil.rmtree(self.test_path, ignore_errors=True)

    def test_fresh_satellite_returns_no_drift(self):
        sync_tree(self.test_path)
        status = check_satellite_freshness(self.test_path)
        self.assertTrue(status["fresh"])
        self.assertFalse(status["drift_detected"])

    def test_drift_detected_on_new_file(self):
        sync_tree(self.test_path)
        # Create a new file in src/core and advance its mtime
        new_file = self.test_path / "src" / "core" / "new_module.py"
        new_file.write_text("# new code", encoding="utf-8")
        future_time = time.time() + 10.0
        os.utime(new_file, (future_time, future_time))

        status = check_satellite_freshness(self.test_path)
        self.assertFalse(status["fresh"])
        self.assertTrue(status["drift_detected"])


class TestNTFSIOResilience(unittest.TestCase):
    """Verifies safe_io_retry exponential backoff and atomic casing rename on Windows NTFS."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="idir_resilience_test_")
        self.test_path = Path(self.test_dir)
        init_project(str(self.test_path))

    def tearDown(self):
        if self.test_path.exists():
            shutil.rmtree(self.test_path, ignore_errors=True)

    def test_safe_io_retry_recovers_transient_error(self):
        calls = {"n": 0}

        def flaky():
            calls["n"] += 1
            if calls["n"] < 3:
                raise PermissionError(13, "locked by indexer")
            return "ok"

        result = safe_io_retry(flaky, initial_delay_ms=1.0)
        self.assertEqual(result, "ok")
        self.assertEqual(calls["n"], 3)

    def test_safe_io_retry_does_not_retry_logical_errors(self):
        calls = {"n": 0}

        def missing():
            calls["n"] += 1
            raise FileNotFoundError("missing file")

        with self.assertRaises(FileNotFoundError):
            safe_io_retry(missing, initial_delay_ms=1.0)
        self.assertEqual(calls["n"], 1)

    def test_safe_io_retry_exhausts_and_raises(self):
        calls = {"n": 0}

        def always_locked():
            calls["n"] += 1
            raise PermissionError(13, "persistently locked")

        with self.assertRaises(PermissionError):
            safe_io_retry(always_locked, max_attempts=4, initial_delay_ms=1.0)
        self.assertEqual(calls["n"], 4)

    def test_no_tmp_residue_after_casing_rename(self):
        f = self.test_path / "UpperJob.py"
        f.write_text("from pyspark.sql import functions as F\n", encoding="utf-8")
        route_file(str(f), base_path=str(self.test_path), move=True)
        residues = list((self.test_path / "src" / "cloud_jobs").glob(".tmp_*"))
        self.assertEqual(residues, [])


class TestAutoScaffoldAndRemediation(unittest.TestCase):
    """Verifies beacon auto-discovery, hierarchy scaffolding, and audit --fix auto-remediation."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="idir_scaffold_test_")
        self.test_path = Path(self.test_dir)
        init_project(str(self.test_path))

    def tearDown(self):
        if self.test_path.exists():
            shutil.rmtree(self.test_path, ignore_errors=True)

    def test_init_leaves_no_orphans(self):
        self.assertEqual(discover_unbeaconed_directories(self.test_path), [])
        self.assertTrue((self.test_path / "src" / ".context.yaml").exists())
        loaded = MiniYAML.load((self.test_path / "src" / ".context.yaml").read_text(encoding="utf-8"))
        self.assertEqual(loaded["role"], "namespace")
        self.assertFalse(loaded["tier1_preload"])

    def test_auto_discovery_scaffolds_unbeaconed_folder(self):
        new_dir = self.test_path / "src" / "core" / "temp_domain"
        os.mkdir(new_dir)
        orphans = [p.resolve() for p in discover_unbeaconed_directories(self.test_path)]
        self.assertIn(new_dir.resolve(), orphans)
        sync_beacons(self.test_path)
        beacon = new_dir / ".context.yaml"
        self.assertTrue(beacon.exists())
        loaded = MiniYAML.load(beacon.read_text(encoding="utf-8"))
        self.assertEqual(loaded["role"], "shared_backend")
        self.assertEqual(loaded["directory"], "src/core/temp_domain")
        self.assertFalse(loaded["tier1_preload"])

    def test_discovery_respects_crawl_false_and_hidden(self):
        (self.test_path / "data" / "raw" / "incoming").mkdir(parents=True)
        (self.test_path / ".hidden_tool").mkdir()
        (self.test_path / "src" / "__pycache__").mkdir()
        orphans = [p.resolve() for p in discover_unbeaconed_directories(self.test_path)]
        self.assertNotIn((self.test_path / "data" / "raw" / "incoming").resolve(), orphans)
        self.assertNotIn((self.test_path / ".hidden_tool").resolve(), orphans)
        self.assertNotIn((self.test_path / "src" / "__pycache__").resolve(), orphans)

    def test_scaffold_never_overwrites_existing_beacon(self):
        beacon = self.test_path / "src" / "core" / ".context.yaml"
        beacon.write_text("role: custom\n# USER_NOTE: manual\n", encoding="utf-8")
        self.assertIsNone(scaffold_beacon_for_dir(beacon.parent, self.test_path))
        self.assertIn("USER_NOTE", beacon.read_text(encoding="utf-8"))

    def test_route_file_creates_beacon_on_new_target(self):
        shutil.rmtree(self.test_path / "src" / "dashboards")
        dash = self.test_path / "kpi_board.py"
        dash.write_text("import streamlit as st\n", encoding="utf-8")
        dest = route_file(str(dash), base_path=str(self.test_path), move=True)
        self.assertTrue(dest.exists())
        beacon = self.test_path / "src" / "dashboards" / ".context.yaml"
        self.assertTrue(beacon.exists())
        self.assertEqual(MiniYAML.load(beacon.read_text(encoding="utf-8"))["role"], "bi_viz")

    def test_audit_fix_flag_resolves_missing_beacons(self):
        (self.test_path / "infrastructure").mkdir()
        (self.test_path / "01_seed" / ".context.yaml").unlink()
        self.assertFalse(audit_repository(self.test_path))
        self.assertTrue(audit_repository(self.test_path, fix=True))
        self.assertTrue((self.test_path / "infrastructure" / ".context.yaml").exists())
        self.assertTrue((self.test_path / "01_seed" / ".context.yaml").exists())
        self.assertTrue(audit_repository(self.test_path))

    def test_sync_beacons_preserves_agent_enrichment(self):
        core_beacon = self.test_path / "src" / "core" / ".context.yaml"
        with open(core_beacon, "a", encoding="utf-8") as fh:
            fh.write('key_files:\n  - "auth.py (exports: verify_token)"\nimports_from:\n  - "schemas"\nexported_to:\n  - "src/cloud_jobs"\n')
        sync_beacons(self.test_path)
        reloaded = MiniYAML.load(core_beacon.read_text(encoding="utf-8"))
        self.assertEqual(reloaded.get("key_files"), ["auth.py (exports: verify_token)"])
        self.assertEqual(reloaded.get("imports_from"), ["schemas"])
        self.assertEqual(reloaded.get("exported_to"), ["src/cloud_jobs"])
        # force_defaults=True restores canonical defaults
        sync_beacons(self.test_path, force_defaults=True)
        restored = MiniYAML.load(core_beacon.read_text(encoding="utf-8"))
        self.assertNotIn("imports_from", restored)

    def test_audit_detects_and_fixes_invalid_beacon_schema(self):
        core_beacon = self.test_path / "src" / "core" / ".context.yaml"
        raw = core_beacon.read_text(encoding="utf-8").replace("read_priority: p1", "read_priority: p9")
        core_beacon.write_text(raw + "# USER_NOTE: keep me\n", encoding="utf-8")
        self.assertTrue(len(validate_beacon_data(MiniYAML.load(core_beacon.read_text(encoding="utf-8")))) > 0)
        self.assertFalse(audit_repository(self.test_path, fix=False))
        self.assertTrue(audit_repository(self.test_path, fix=True))
        repaired_text = core_beacon.read_text(encoding="utf-8")
        self.assertIn("# USER_NOTE: keep me", repaired_text)
        self.assertEqual(validate_beacon_data(MiniYAML.load(repaired_text)), [])

    def test_audit_detects_deep_uppercase_directory(self):
        deep_upper = self.test_path / "src" / "core" / "MySubService"
        deep_upper.mkdir(parents=True)
        scaffold_beacon_for_dir(deep_upper, self.test_path)
        self.assertFalse(audit_repository(self.test_path, fix=False))


class TestTreeSlicing(unittest.TestCase):
    """Verifies focused subtree generation (map --slice), dependency traversal, and budget pruning."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="idir_slice_test_")
        self.test_path = Path(self.test_dir)
        init_project(str(self.test_path))

    def tearDown(self):
        if self.test_path.exists():
            shutil.rmtree(self.test_path, ignore_errors=True)

    def test_tree_slicing_structure_and_dependencies(self):
        core_beacon = self.test_path / "src" / "core" / ".context.yaml"
        with open(core_beacon, "a", encoding="utf-8") as fh:
            fh.write('key_files:\n  - "auth.py"\nimports_from:\n  - "schemas"\nexported_to:\n  - "src/cloud_jobs"\n')
        (self.test_path / "src" / "core" / "auth").mkdir()
        sliced = generate_sliced_tree(self.test_path, "src/core")
        nodes = sliced["nodes"]
        self.assertTrue(sliced["sliced"])
        self.assertEqual(sliced["focus_node"], "src/core")
        self.assertEqual(nodes["src/core"]["edge"], "focus")
        self.assertEqual(nodes["src/core"].get("key_files"), ["auth.py"])
        self.assertEqual(nodes["src"]["edge"], "parent")
        self.assertEqual(nodes["src/core/auth"]["edge"], "child")
        self.assertEqual(nodes["schemas"]["edge"], "dep")
        self.assertEqual(nodes["src/cloud_jobs"]["edge"], "consumer")
        for key in nodes:
            self.assertNotIn("\\", key)
        self.assertLessEqual(len(format_sliced_tree(sliced)), SLICE_CHAR_BUDGET)

    def test_slice_pruned_branch_has_no_children(self):
        (self.test_path / "data" / "raw" / "batch").mkdir(parents=True)
        sliced = generate_sliced_tree(self.test_path, "data/raw")
        self.assertTrue(sliced["nodes"]["data/raw"].get("pruned"))
        self.assertFalse(any(n["edge"] == "child" for n in sliced["nodes"].values()))

    def test_slice_blocks_traversal(self):
        with self.assertRaises(PermissionError):
            generate_sliced_tree(self.test_path, "../outside")


class TestV4AdversarialAndContinuity(unittest.TestCase):
    """Adversarial test suite for iDirectory v4.0 fixes (V-01..V-07) and new capabilities (Opt-1..Opt-7)."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="idir_v4_test_")
        self.test_path = Path(self.test_dir)
        init_project(str(self.test_path))

    def tearDown(self):
        if self.test_path.exists():
            shutil.rmtree(self.test_path, ignore_errors=True)

    def test_compute_budget_never_walks_crawl_false(self):
        """[V-01] Placing a heavy file in data/raw must produce 0 tokens in default compute_context_budget."""
        heavy = self.test_path / "data" / "raw" / "dump.txt"
        heavy.write_text("X" * 40000, encoding="utf-8")
        budget = {item["directory"]: item for item in compute_context_budget(self.test_path)}
        self.assertIn("data/raw", budget)
        self.assertEqual(budget["data/raw"]["est_tokens"], 0)
        self.assertEqual(budget["data/raw"]["files"], 0)
        self.assertTrue(budget["data/raw"]["pruned"])

    def test_freshness_detects_beacon_and_artifacts_mutation(self):
        """[V-02] Modifying src/core/.context.yaml or artifacts/plans/active/ must trigger satellite drift."""
        sync_tree(self.test_path)
        self.assertTrue(check_satellite_freshness(self.test_path)["fresh"])

        # 1. Mutate local beacon (without changing mtime into the future, testing SHA-256 topology_hash)
        beacon = self.test_path / "src" / "core" / ".context.yaml"
        beacon.write_text(beacon.read_text(encoding="utf-8") + "# mutated comment\n", encoding="utf-8")
        status_beacon = check_satellite_freshness(self.test_path)
        self.assertFalse(status_beacon["fresh"])
        self.assertFalse(status_beacon["topology_hash_match"])

        # Resync and test artifacts/plans/active mutation
        sync_tree(self.test_path)
        self.assertTrue(check_satellite_freshness(self.test_path)["fresh"])
        new_plan = self.test_path / "artifacts" / "plans" / "active" / "new_sprint.md"
        new_plan.write_text("# Sprint Plan\n", encoding="utf-8")
        self.assertFalse(check_satellite_freshness(self.test_path)["fresh"])

    def test_audit_fails_on_missing_canonical_directory(self):
        """[V-03] Deleting src/core/ must make audit_repository fail, and audit --fix must restore it."""
        shutil.rmtree(self.test_path / "src" / "core")
        self.assertFalse(audit_repository(self.test_path, fix=False))
        self.assertTrue(audit_repository(self.test_path, fix=True))
        self.assertTrue((self.test_path / "src" / "core").is_dir())
        self.assertTrue((self.test_path / "src" / "core" / ".context.yaml").is_file())

    def test_audit_fails_on_stale_satellite(self):
        """[V-03] Mutating governed files without syncing tree.json must fail strict audit."""
        (self.test_path / "src" / "core" / "extra.py").write_text("x = 1\n", encoding="utf-8")
        self.assertFalse(audit_repository(self.test_path, fix=False))
        self.assertTrue(audit_repository(self.test_path, fix=True))
        self.assertTrue(audit_repository(self.test_path, fix=False))

    def test_slice_hard_budget_with_massive_dependencies(self):
        """[V-05] A beacon with excessive imports_from and key_files must stay <= SLICE_CHAR_BUDGET and set budget_exceeded."""
        deps = []
        for i in range(12):
            d = self.test_path / "src" / f"dep_module_long_name_{i:02d}"
            d.mkdir(parents=True, exist_ok=True)
            scaffold_beacon_for_dir(d, self.test_path)
            deps.append(f"src/dep_module_long_name_{i:02d}")
        kfiles = [f"very_long_module_name_{i:02d}.py: execute_complex_pipeline(arg1, arg2) -> Dict" for i in range(10)]
        core_beacon = self.test_path / "src" / "core" / ".context.yaml"
        loaded = MiniYAML.load(core_beacon.read_text(encoding="utf-8"))
        loaded["imports_from"] = deps
        loaded["key_files"] = kfiles
        core_beacon.write_text(MiniYAML.dump(loaded) + "\n", encoding="utf-8")

        sliced = generate_sliced_tree(self.test_path, "src/core")
        serialized = format_sliced_tree(sliced)
        self.assertLessEqual(len(serialized), SLICE_CHAR_BUDGET)
        self.assertTrue(sliced.get("budget_exceeded"))

    def test_validate_beacon_strict_additional_properties_and_lengths(self):
        """[V-06] validate_beacon_data must reject unknown keys, oversized strings, and backslashes in lists."""
        beacon = self.test_path / "src" / "core" / ".context.yaml"
        data = MiniYAML.load(beacon.read_text(encoding="utf-8"))
        data[" rogue_key "] = "not_allowed"
        data["purpose"] = "P" * 250
        data["imports_from"] = ["src\\bad_slash"]
        errors = validate_beacon_data(data)
        self.assertGreaterEqual(len(errors), 3)

    def test_reconcile_command_idempotency(self):
        """[Opt-4] reconcile_repository must heal orphans, sync tree_hash, and leave repo clean."""
        (self.test_path / "src" / "core" / "sub_feature").mkdir(parents=True)
        self.assertTrue(reconcile_repository(self.test_path, check_only=False))
        self.assertTrue(reconcile_repository(self.test_path, check_only=True))

    def test_context_pack_tier1a_budget(self):
        """[Opt-2] build_context_pack must return slice + beacon + verified files under 220 tokens."""
        (self.test_path / "src" / "core" / "service.py").write_text("def run(): return True\n", encoding="utf-8")
        reconcile_repository(self.test_path)
        pack = build_context_pack(self.test_path, "src/core", tier="1a")
        serialized = json.dumps(pack, ensure_ascii=False, separators=(",", ":"))
        self.assertEqual(pack["focus"], "src/core")
        self.assertIn("service.py(~", ",".join(pack["files"]))
        self.assertLessEqual(estimate_tokens_v4(serialized), 220)

    def test_seed_sectional_toc_and_extraction(self):
        """[Opt-3] get_seed_sections and extract_seed_section must extract targeted sections without full dump."""
        sections = get_seed_sections(PROJECT_ROOT)
        self.assertGreater(len(sections), 5)
        sec4 = extract_seed_section(PROJECT_ROOT, "4.1")
        self.assertIn("SEED SECTION", sec4)
        self.assertIn("FWengine.py", sec4)
        self.assertLess(estimate_tokens_v4(sec4), 3500)

    def test_checkpoint_lifecycle(self):
        """[Opt-5] manage_checkpoint must create, update, integrate with context pack, and clear checkpoint.json."""
        cp = manage_checkpoint(
            self.test_path,
            action="set",
            plan_id="plan-v4",
            status="executing",
            phase="P2",
            next_action="Run unit tests",
            completed_step="P0 done",
        )
        self.assertEqual(cp["plan_id"], "plan-v4")
        self.assertIn("P0 done", cp["completed_steps"])
        pack = build_context_pack(self.test_path, "src/core", tier="1a")
        self.assertEqual(pack["checkpoint"]["phase"], "P2")
        cleared = manage_checkpoint(self.test_path, action="clear")
        self.assertTrue(cleared["cleared"])

    def test_adapter_portability_no_local_paths(self):
        """[V-07] None of the repository's agent adapters may contain non-portable 'file:///' URIs."""
        for adapter in ("AGENTS.md", "GEMINI.md", "CLAUDE.md", ".cursorrules", ".github/copilot-instructions.md"):
            ap = PROJECT_ROOT / adapter
            self.assertTrue(ap.is_file(), f"El adaptador {adapter} debe existir.")
            content = ap.read_text(encoding="utf-8")
            self.assertNotIn("file:///", content.lower(), f"Ruta local detectada en {adapter}")

    def test_active_plans_reject_superseded_status(self):
        """[Opt-6] A plan in artifacts/plans/active/ with status: superseded must fail audit and be archived on --fix."""
        bad_plan = self.test_path / "artifacts" / "plans" / "active" / "old_plan.md"
        bad_plan.write_text("---\nstatus: superseded\nexecutable: false\n---\n# Old\n", encoding="utf-8")
        sync_tree(self.test_path)
        self.assertFalse(audit_repository(self.test_path, fix=False))
        self.assertTrue(audit_repository(self.test_path, fix=True))
        self.assertFalse(bad_plan.exists())
        self.assertTrue((self.test_path / "artifacts" / "plans" / "archive" / "old_plan.md").exists())


class TestV41EnterpriseAndIncremental(unittest.TestCase):
    """
    Test suite for iDirectory v4.1 Enterprise Context Governance and Incremental Merkle Engine.
    Verifies automatic plan garbage collection, backlog queue schema & orphan detection,
    AST dependency firewall, and node_hash incremental caching.
    """

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="idir_v41_test_")
        self.test_path = Path(self.test_dir)
        init_project(str(self.test_path))

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_plan_lifecycle_eviction_on_checkpoint_completion(self):
        """[1] Automatic plan eviction from active/ to archive/ upon checkpoint completion."""
        active_plan = self.test_path / "artifacts" / "plans" / "active" / "plan_release.md"
        active_plan.write_text(
            "---\nid: plan_release\nstatus: executing\nexecutable: true\n---\n# Release Plan v4.1\n",
            encoding="utf-8"
        )
        manage_checkpoint(self.test_path, action="set", plan_id="plan_release", status="completed")

        self.assertTrue(reconcile_repository(self.test_path, check_only=False))

        self.assertFalse(active_plan.exists(), "Plan completado no debe residir en active/")
        archive_plan = self.test_path / "artifacts" / "plans" / "archive" / "plan_release.md"
        self.assertTrue(archive_plan.exists(), "Plan completado debe haber sido movido a archive/")

        archived_text = archive_plan.read_text(encoding="utf-8")
        self.assertIn("status: completed", archived_text)
        self.assertIn("executable: false", archived_text)

        cp_after = manage_checkpoint(self.test_path, action="show")
        self.assertNotEqual(cp_after.get("status"), "completed")

    def test_reconcile_check_blocks_on_multiple_executing_plans(self):
        """[2] Reconcile --check blocks when more than 1 plan has status: executing (strict cardinality)."""
        reconcile_repository(self.test_path, check_only=False)

        plan_a = self.test_path / "artifacts" / "plans" / "active" / "plan_a.md"
        plan_b = self.test_path / "artifacts" / "plans" / "active" / "plan_b.md"
        plan_a.write_text("---\nid: A\nstatus: executing\nexecutable: true\n---\n# Plan A\n", encoding="utf-8")
        plan_b.write_text("---\nid: B\nstatus: executing\nexecutable: true\n---\n# Plan B\n", encoding="utf-8")

        violations = reconcile_plans_lifecycle(self.test_path, check_only=True)
        self.assertTrue(any("cardinalidad estricta" in v.lower() for v in violations))
        self.assertFalse(reconcile_repository(self.test_path, check_only=True))

    def test_backlog_queue_detects_orphan_target_nodes(self):
        """[3] Detects non-existent target nodes in artifacts/plans/backlog/queue.json."""
        reconcile_repository(self.test_path, check_only=False)
        queue_file = self.test_path / "artifacts" / "plans" / "backlog" / "queue.json"
        orphan_payload = {
            "version": "1.0",
            "items": [
                {
                    "id": "BKL-001",
                    "target_nodes": ["src/module_inexistente_xyz"],
                    "tier_estimate": "1a",
                    "intent": "Implementar módulo huérfano",
                    "status": "queued",
                    "acceptance_test": "test_orphan"
                }
            ]
        }
        queue_file.write_text(json.dumps(orphan_payload, indent=2), encoding="utf-8")

        errs = validate_backlog_queue(self.test_path, check_only=True)
        self.assertTrue(any("src/module_inexistente_xyz" in e for e in errs))
        self.assertFalse(reconcile_repository(self.test_path, check_only=True))

    def test_dependency_dag_firewall_blocks_unauthorized_imports(self):
        """[4] Dependency DAG firewall detects unauthorized cross-module imports via AST analysis."""
        reconcile_repository(self.test_path, check_only=False)
        cloud_jobs_beacon = self.test_path / "src" / "cloud_jobs" / ".context.yaml"
        b_data = MiniYAML.load(cloud_jobs_beacon.read_text(encoding="utf-8"))
        b_data["imports_from"] = ["src/core"]
        cloud_jobs_beacon.write_text(MiniYAML.dump(b_data) + "\n", encoding="utf-8")

        unauth_file = self.test_path / "src" / "cloud_jobs" / "rogue_job.py"
        unauth_file.write_text("from src.dashboards import app\n\ndef run(): app.start()\n", encoding="utf-8")

        dag_errs = validate_dependency_dag(self.test_path)
        self.assertTrue(len(dag_errs) > 0)
        self.assertTrue(any("src/dashboards" in e for e in dag_errs))
        self.assertFalse(reconcile_repository(self.test_path, check_only=True))

    def test_incremental_cache_hit_preserves_node_hash(self):
        """[5] Unchanged nodes retain identical node_hash without re-indexing."""
        reconcile_repository(self.test_path, check_only=False)
        seed_dir = self.test_path / "01_seed"
        h1 = compute_node_fingerprint(seed_dir)
        self.assertEqual(len(h1), 16)

        # Mutate src/core only
        core_file = self.test_path / "src" / "core" / "new_service.py"
        core_file.write_text("x = 42\n", encoding="utf-8")

        h2 = compute_node_fingerprint(seed_dir)
        self.assertEqual(h1, h2, "El hash de 01_seed no debe cambiar al mutar src/core")

        h_core = compute_node_fingerprint(self.test_path / "src" / "core")
        self.assertEqual(len(h_core), 16)

    def test_backlog_queue_initialization_and_schema_validation(self):
        """[6] Backlog queue is automatically initialized and validates against schema."""
        fresh_dir = tempfile.mkdtemp(prefix="idir_fresh_bkl_")
        fresh_path = Path(fresh_dir)
        try:
            init_project(str(fresh_path))
            queue_file = fresh_path / "artifacts" / "plans" / "backlog" / "queue.json"
            self.assertTrue(queue_file.is_file())
            content = json.loads(queue_file.read_text(encoding="utf-8"))
            self.assertEqual(content["version"], "1.0")
            self.assertEqual(content["items"], [])

            # Insert valid item
            valid_item = {
                "id": "BKL-100",
                "target_nodes": ["src/core"],
                "tier_estimate": "1b",
                "intent": "Refactorizar cliente",
                "status": "queued",
                "acceptance_test": "test_core_client"
            }
            content["items"].append(valid_item)
            queue_file.write_text(json.dumps(content, indent=2), encoding="utf-8")

            errs = validate_backlog_queue(fresh_path)
            self.assertEqual(errs, [])
        finally:
            shutil.rmtree(fresh_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()

