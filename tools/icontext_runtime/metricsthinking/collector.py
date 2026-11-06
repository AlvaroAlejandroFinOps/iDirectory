"""
Evidence Collector for MetricsThinking™ v4.0.
Performs comprehensive, strictly READ-ONLY single-pass inspection of the target repository.
"""

import os
from pathlib import Path
import subprocess
import sys
from typing import Any
import yaml

# Ensure local directory is in sys.path
_PKG_DIR = Path(__file__).resolve().parent
if str(_PKG_DIR) not in sys.path:
    sys.path.insert(0, str(_PKG_DIR))

try:
    from metricsthinking.models import EvidencePrimitiveSummary
    from metricsthinking.backends import scan_directory, compute_ast_coupling
    from metricsthinking.detector import ArchetypeDetector, ArchetypeDetectionResult
except (ImportError, ValueError):
    try:
        from .models import EvidencePrimitiveSummary
        from .backends import scan_directory, compute_ast_coupling
        from .detector import ArchetypeDetector, ArchetypeDetectionResult
    except (ImportError, ValueError):
        from models import EvidencePrimitiveSummary
        from backends import scan_directory, compute_ast_coupling
        from detector import ArchetypeDetector, ArchetypeDetectionResult


class ProjectEvidence:
    """Encapsulates all raw physical evidence collected from the repository."""

    def __init__(self, target_path: str):
        self.root_path = Path(target_path).resolve()
        self.project_name = self.root_path.name
        self.exists = self.root_path.exists()

        # Raw findings
        self.files: list[Path] = []
        self.rel_files: list[str] = []
        self.dirs: list[Path] = []
        self.rel_dirs: list[str] = []

        # Metadata
        self.git_commit: str | None = None
        self.git_branch: str | None = None
        self.is_git: bool = False

        # Specific collections (canonical & legacy compatibility)
        self.seeds: list[str] = []
        self.manifests: dict[str, str] = {}
        self.context_files: list[str] = []
        self.schemas: list[str] = []
        self.tests: list[str] = []
        self.ci_workflows: list[str] = []
        self.docs: list[str] = []
        self.source_files: list[str] = []
        self.adrs: list[str] = []
        self.dashboards: list[str] = []
        self.tools_and_scripts: list[str] = []
        self.skills: list[str] = []
        self.agent_instructions: list[str] = []
        self.master_templates: list[str] = []
        self.skill_installers: list[str] = []
        self.coverage_benchmarks: list[str] = []

        # v3.0 Universal Evidence Primitives
        self.evidence_primitives: dict[str, EvidencePrimitiveSummary] = {}
        self.detected_archetype: str | None = None
        self.detected_mode: str | None = None
        self.archetype_detection: Any = None
        self.seed_detected: bool = False
        self.seed_version: str | None = None
        self.seed_data: dict[str, Any] = {}

        # Code stats
        self.total_files: int = 0
        self.total_lines_of_code: int = 0
        self.file_extensions: dict[str, int] = {}
        self.file_cache: dict[str, str] = {}  # RelPath -> Content snippet or full text
        self.file_hashes: dict[str, str] = {}
        self.file_sizes: dict[str, int] = {}
        self.file_lines: dict[str, int] = {}
        self.file_tokens: dict[str, int] = {}

        # v4.0 AST & Resilience & Security primitives
        self.python_files: dict[str, str] = {}
        self.ast_metrics: dict[str, Any] = {}
        self.lockfile_pinned: bool = True


class ProjectCollector:
    """Reads repository metadata and builds ProjectEvidence with anti-fraud filtering."""

    EXCLUDED_DIRS = [
        ".git", ".venv", "venv", "node_modules", "__pycache__",
        ".pytest_cache", ".ruff_cache", ".mypy_cache", "dist", "build",
        ".egg-info", "data/raw", "data/processed", "data/sandbox", ".system_generated"
    ]

    def __init__(self, target_path: str, evidence_hints: dict[str, Any] | None = None, persist_cache: bool = False, full: bool = False):
        self.evidence = ProjectEvidence(target_path)
        self.evidence_hints = evidence_hints or {}
        self.persist_cache = persist_cache
        self.full = full

    def collect(self) -> ProjectEvidence:
        """Executes full single-pass read-only scan of the project."""
        if not self.evidence.exists:
            return self.evidence

        self._collect_git_metadata()
        self._single_pass_scan()
        self._classify_files()
        self._parse_seed_metadata()
        self._classify_universal_primitives()
        self._compute_ast_and_resilience()
        return self.evidence

    def _collect_git_metadata(self):
        """Reads git commit and branch if repo has .git directory."""
        git_dir = self.evidence.root_path / ".git"
        if git_dir.exists():
            self.evidence.is_git = True
            try:
                commit = subprocess.check_output(
                    ["git", "rev-parse", "--short", "HEAD"],
                    cwd=str(self.evidence.root_path),
                    stderr=subprocess.DEVNULL,
                    text=True
                ).strip()
                self.evidence.git_commit = commit
            except Exception:
                self.evidence.git_commit = "untracked"

            try:
                branch = subprocess.check_output(
                    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                    cwd=str(self.evidence.root_path),
                    stderr=subprocess.DEVNULL,
                    text=True
                ).strip()
                self.evidence.git_branch = branch
            except Exception:
                self.evidence.git_branch = "unknown"

    def _single_pass_scan(self):
        """Performs single-pass directory crawl via active backend with SHA-256 caching."""
        records = scan_directory(
            str(self.evidence.root_path),
            ignore_patterns=self.EXCLUDED_DIRS,
            include_content=True,
            persist=self.persist_cache, full=self.full,
        )

        seen_dirs: set[str] = set()

        for rec in records:
            rel = rec["path"]
            file_path = self.evidence.root_path / rel
            self.evidence.files.append(file_path)
            self.evidence.rel_files.append(rel)

            ext = file_path.suffix.lower() or "no_ext"
            self.evidence.file_extensions[ext] = self.evidence.file_extensions.get(ext, 0) + 1

            self.evidence.file_hashes[rel] = rec["sha256"]
            self.evidence.file_sizes[rel] = rec["size_bytes"]
            self.evidence.file_lines[rel] = rec["line_count"]
            self.evidence.file_tokens[rel] = rec["token_estimate"]

            if rec.get("content"):
                self.evidence.file_cache[rel] = rec["content"]
                if rel.endswith(".py"):
                    self.evidence.python_files[rel] = rec["content"]

            self.evidence.total_lines_of_code += rec["line_count"]

            # Track parent dirs
            parent = str(Path(rel).parent).replace("\\", "/")
            if parent and parent != ".":
                parts = parent.split("/")
                acc = ""
                for p in parts:
                    acc = f"{acc}/{p}" if acc else p
                    seen_dirs.add(acc)

        for d in sorted(seen_dirs):
            dir_p = self.evidence.root_path / d
            self.evidence.dirs.append(dir_p)
            self.evidence.rel_dirs.append(d)

        self.evidence.total_files = len(self.evidence.files)

        # Check lockfile pinning
        lockfiles = ["requirements.txt", "poetry.lock", "Pipfile.lock", "package-lock.json", "pnpm-lock.yaml", "Cargo.lock"]
        self.evidence.lockfile_pinned = any(lf in self.evidence.rel_files for lf in lockfiles)

    def _classify_files(self):
        """Categorizes files into evidence buckets with strict anti-fraud filtering."""
        custom_source_prefixes = self.evidence_hints.get("source_patterns", [])
        custom_test_prefixes = self.evidence_hints.get("test_patterns", [])

        for rel in self.evidence.rel_files:
            lower = rel.lower()

            # Seeds & Core DNA (Only authoritative markdown seeds, excluding test fixtures or previous reports)
            if (("01_seed" in lower or lower.startswith("seed-") or lower.startswith("seed_") or lower.endswith("seed.md")) and lower.endswith(".md")) and not lower.startswith("tests/") and "artifacts/plans/metricsthinking" not in lower:
                self.evidence.seeds.append(rel)

            # Packaging & Manifests
            if lower in ["pyproject.toml", "package.json", "cargo.toml", "requirements.txt", "setup.py", "go.mod", "kustomization.yaml", "chart.yaml", "terraform.tf", "dbt_project.yml"] and not lower.startswith("tests/"):
                self.evidence.manifests[rel] = lower

            # Governance / iDirectory context
            if lower.endswith(".context.yaml") or lower == ".context/tree.json":
                self.evidence.context_files.append(rel)

            # Schemas & Contracts
            if (("schemas/" in lower and not lower.endswith(".context.yaml")) or lower.endswith(".schema.json") or lower.endswith(".proto") or lower.endswith(".graphql") or lower.endswith(".gql") or "openapi" in lower) and not lower.startswith("tests/"):
                self.evidence.schemas.append(rel)

            # Tests
            is_test = False
            if (("tests/" in lower or "test_" in lower or lower.endswith("_test.py") or ".spec." in lower) and any(lower.endswith(ext) for ext in [".py", ".ts", ".js", ".rs", ".go"])) and not lower.endswith(".context.yaml") and "tests/other" not in lower:
                is_test = True
            elif custom_test_prefixes and any(lower.startswith(p.lower()) or p.lower() in lower for p in custom_test_prefixes):
                is_test = True

            if is_test:
                self.evidence.tests.append(rel)

            # CI/CD
            if (".github/workflows" in lower or lower in [".gitlab-ci.yml", "jenkinsfile", "dockerfile", "docker-compose.yml", ".pre-commit-config.yaml", "skaffold.yaml"]) and not lower.startswith("tests/"):
                self.evidence.ci_workflows.append(rel)

            # Documentation & ADRs
            if (lower.endswith(".md") or "docs/" in lower) and not lower.startswith("tests/") and "artifacts/plans/metricsthinking" not in lower and not lower.endswith(".context.yaml"):
                self.evidence.docs.append(rel)
                if ("adr-" in lower or "docs/notes" in lower or "adr" in lower or "/decisions/" in lower) and lower.endswith(".md"):
                    self.evidence.adrs.append(rel)

            # Dashboards & BI
            if ("dashboards" in lower or "streamlit" in lower or "grafana" in lower) and any(lower.endswith(ext) for ext in [".py", ".ts", ".js", ".tsx", ".json"]) and not lower.endswith(".context.yaml"):
                self.evidence.dashboards.append(rel)

            # Tools & scripts
            if ("tools/" in lower or "scripts/" in lower) and any(lower.endswith(ext) for ext in [".py", ".sh", ".ps1", ".bash", ".ts", ".js"]) and not lower.endswith(".context.yaml"):
                self.evidence.tools_and_scripts.append(rel)

            # Skills & Agent Customizations
            if (lower.endswith("skill.md") or "/skills/" in lower or lower.startswith(".agents/skills/") or lower.startswith("skills/")) and not lower.startswith("tests/"):
                self.evidence.skills.append(rel)

            # Agent Instructions & Multi-assistant configs
            if lower in ["agents.md", "gemini.md", "claude.md", ".cursorrules", ".windsurfrules", ".agentignore"] or "prompts/" in lower or "agent_rules" in lower:
                self.evidence.agent_instructions.append(rel)

            # Master Prompt/Seed Templates
            if ("master" in lower or "hybrid" in lower or "prompt" in lower or "template" in lower) and any(lower.endswith(ext) for ext in [".md", ".txt", ".yaml", ".yml", ".json"]) and not lower.startswith("tests/") and "metrics" not in lower:
                self.evidence.master_templates.append(rel)

            # Skill Installers
            if "install_skill" in lower and any(lower.endswith(ext) for ext in [".py", ".sh", ".ps1"]):
                self.evidence.skill_installers.append(rel)

            # Coverage & Benchmarks
            if ("coverage" in lower or "benchmark" in lower or "eval" in lower) and any(lower.endswith(ext) for ext in [".py", ".md", ".json", ".yaml"]) and not lower.endswith(".context.yaml"):
                self.evidence.coverage_benchmarks.append(rel)

            # Source files
            is_source = False
            if (lower.startswith("src/") or lower.startswith("app/") or lower.startswith("lib/") or lower.startswith("pkg/")) and any(lower.endswith(ext) for ext in [".py", ".ts", ".js", ".rs", ".go", ".sql", ".tf", ".rego"]) and not lower.endswith(".context.yaml"):
                is_source = True
            elif custom_source_prefixes and any(lower.startswith(p.lower()) or p.lower() in lower for p in custom_source_prefixes):
                is_source = True

            if is_source:
                self.evidence.source_files.append(rel)

    def _parse_seed_metadata(self):
        """Parses ThinkingSeed metadata if present in repo, or applies automatic archetype detection."""
        for seed_rel in self.evidence.seeds:
            content = self.evidence.file_cache.get(seed_rel, "")
            if content:
                self.evidence.seed_detected = True
                # Check for YAML frontmatter with ---
                if "---" in content:
                    parts = content.split("---")
                    for p in parts[1:]:
                        try:
                            data = yaml.safe_load(p)
                            if isinstance(data, dict) and any(k in data for k in ["project_name", "domain_archetype", "archetype", "project_type", "seed_version", "seed_schema_version"]):
                                self.evidence.seed_data = data
                                self.evidence.detected_archetype = data.get("domain_archetype") or data.get("archetype") or data.get("project_type")
                                self.evidence.detected_mode = data.get("inspection_mode")
                                self.evidence.seed_version = str(data.get("seed_version", data.get("seed_schema_version", "3.0")))
                                break
                        except Exception:
                            pass
                # Also check for ```yaml code block in seed
                if not self.evidence.detected_archetype and "```yaml" in content:
                    code_blocks = content.split("```yaml")
                    for block in code_blocks[1:]:
                        code_content = block.split("```")[0]
                        try:
                            data = yaml.safe_load(code_content)
                            if isinstance(data, dict) and any(k in data for k in ["project_name", "domain_archetype", "archetype", "project_type", "seed_version", "seed_schema_version"]):
                                self.evidence.seed_data = data
                                self.evidence.detected_archetype = data.get("domain_archetype") or data.get("archetype") or data.get("project_type")
                                self.evidence.detected_mode = data.get("inspection_mode")
                                self.evidence.seed_version = str(data.get("seed_version", data.get("seed_schema_version", "5.0")))
                                break
                        except Exception:
                            pass
                if not self.evidence.seed_version and '<SEED_ARCHITECTURAL_VECTOR' in content:
                    import re
                    m_ver = re.search(r'<SEED_ARCHITECTURAL_VECTOR[^>]*version=["\']([^"\']+)["\']', content)
                    if m_ver:
                        self.evidence.seed_version = m_ver.group(1)
                break

        # Multi-Signal Archetype Detection (SDD-aligned & Extensible)
        curr_arch = (self.evidence.detected_archetype or "").lower()
        if not curr_arch or curr_arch in ["modular-framework", "generic", "software", "library", "unknown"]:
            detector = ArchetypeDetector(self.evidence.root_path)
            res = detector.detect_from_evidence(self.evidence)
            self.evidence.archetype_detection = res
            self.evidence.detected_archetype = res.primary_archetype
            self.evidence.detected_mode = res.inspection_mode

    def _classify_universal_primitives(self):
        """Builds universal evidence primitives for polymorphic evaluation."""
        primitives: dict[str, list[str]] = {
            "config": [],
            "spec": [],
            "pipeline": [],
            "verification": [],
            "implementation": []
        }

        for rel in self.evidence.rel_files:
            lower = rel.lower()

            # Config
            if any(lower.endswith(ext) for ext in [".yaml", ".yml", ".toml", ".ini", ".env", ".tfvars"]) or "config/" in lower or lower in ["dockerfile", "docker-compose.yml", "kustomization.yaml", ".cursorrules", ".windsurfrules", ".agentignore"]:
                primitives["config"].append(rel)

            # Spec
            if lower.endswith(".schema.json") or lower.endswith(".proto") or lower.endswith(".graphql") or "openapi" in lower or "swagger" in lower or lower.startswith("specs/") or lower.startswith("contracts/") or rel in self.evidence.adrs or rel in self.evidence.seeds or rel in self.evidence.skills or rel in self.evidence.agent_instructions:
                primitives["spec"].append(rel)

            # Pipeline
            if ".github/workflows" in lower or "pipelines/" in lower or "dags/" in lower or "flows/" in lower or lower.startswith(".gitlab") or "jenkins" in lower or "argo/" in lower or rel in self.evidence.skill_installers:
                primitives["pipeline"].append(rel)

            # Verification
            if rel in self.evidence.tests or rel in self.evidence.coverage_benchmarks or "evals/" in lower or "benchmarks/" in lower or "experiments/" in lower or "chaos/" in lower or "policies/" in lower or "rego/" in lower:
                primitives["verification"].append(rel)

            # Implementation
            if rel in self.evidence.source_files or rel in self.evidence.skills or rel in self.evidence.master_templates or "models/" in lower or "dbt/" in lower or "prompts/" in lower or "modules/" in lower or "charts/" in lower or "foundation/" in lower:
                primitives["implementation"].append(rel)

        for p_type, p_files in primitives.items():
            tot_lines = sum(self.evidence.file_lines.get(f, 0) for f in p_files)
            self.evidence.evidence_primitives[p_type] = EvidencePrimitiveSummary(
                primitive_type=p_type,
                file_count=len(p_files),
                total_lines=tot_lines,
                sample_paths=p_files[:5],
                verified_valid=len(p_files) > 0
            )

    def _compute_ast_and_resilience(self):
        """Computes AST coupling, instability, SPOFs and resilience pattern counts."""
        if self.evidence.python_files:
            self.evidence.ast_metrics = compute_ast_coupling(self.evidence.python_files)
