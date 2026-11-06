"""
Archetype & Profile Detector for MetricsThinking™ v4.0.
Provides lightweight, multi-signal static probing (Pre-Flight Archetype Sniffing)
to determine the optimal evaluation profile with high confidence and token economy.
"""

from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import re
from typing import Any
import yaml


@dataclass
class ArchetypeScore:
    archetype: str
    score: float
    signals: list[str] = field(default_factory=list)


@dataclass
class ArchetypeDetectionResult:
    primary_archetype: str
    confidence: float  # 0.0 to 1.0
    inspection_mode: str
    recommended_profile: str
    detected_signals: list[str]
    runner_up_archetypes: list[tuple[str, float]]
    is_custom: bool = False
    is_emerging_domain: bool = False
    rationale: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "primary_archetype": self.primary_archetype,
            "confidence": round(self.confidence, 4),
            "confidence_pct": f"{self.confidence * 100:.1f}%",
            "inspection_mode": self.inspection_mode,
            "recommended_profile": self.recommended_profile,
            "detected_signals": self.detected_signals,
            "runner_up_archetypes": [
                {"archetype": a, "confidence_pct": f"{c * 100:.1f}%"}
                for a, c in self.runner_up_archetypes
            ],
            "is_custom": self.is_custom,
            "is_emerging_domain": self.is_emerging_domain,
            "rationale": self.rationale,
        }


BUILTIN_PROFILES: set[str] = {
    "default", "software-engineering", "agent-skill", "data-platform", "web-app",
    "mlops", "llmops", "dataops", "gitops", "platform-eng", "devsecops",
    "chaos-eng", "dual-track", "team-topologies", "sdd"
}


ARCHETYPE_INSPECTION_MODES: dict[str, str] = {
    "agent-skill": "governance_spec",
    "sdd": "governance_spec",
    "devsecops": "governance_spec",
    "team-topologies": "governance_spec",
    "data-platform": "pipeline_orchestration",
    "dataops": "pipeline_orchestration",
    "mlops": "pipeline_orchestration",
    "llmops": "pipeline_orchestration",
    "gitops": "declarative_config",
    "platform-eng": "declarative_config",
    "chaos-eng": "declarative_config",
    "web-app": "source_code",
    "software-engineering": "source_code",
    "default": "source_code",
    "dual-track": "polyglot_hybrid",
    "custom": "source_code",
}


class ArchetypeDetector:
    """
    Evaluates physical evidence and architectural signatures to detect project archetype
    without deep file parsing, maximizing token economy and SDD alignment.
    """

    def __init__(self, target_path: str | Path, custom_profiles_dir: Path | None = None):
        self.target = Path(target_path).resolve()
        self.custom_profiles_dir = custom_profiles_dir

    def detect_from_evidence(self, evidence: Any) -> ArchetypeDetectionResult:
        """Runs multi-signal detection using pre-collected ProjectEvidence."""
        rel_files = getattr(evidence, "rel_files", [])
        file_cache = getattr(evidence, "file_cache", {})
        seed_data = getattr(evidence, "seed_data", {})
        return self._evaluate_signals(rel_files, file_cache, seed_data)

    def detect_from_filesystem(self) -> ArchetypeDetectionResult:
        """Performs lightweight directory probe (sub-100ms) without loading full files."""
        if not self.target.exists():
            return ArchetypeDetectionResult(
                primary_archetype="software-engineering",
                confidence=0.5,
                inspection_mode="source_code",
                recommended_profile="default",
                detected_signals=["Target directory does not exist; default applied"],
                runner_up_archetypes=[],
                rationale="Target path not found."
            )

        rel_files: list[str] = []
        file_snippets: dict[str, str] = {}
        seed_data: dict[str, Any] = {}

        # Quick crawl skipping standard build/cache/git dirs
        excluded = {
            ".git", ".venv", "venv", "node_modules", "__pycache__",
            ".pytest_cache", ".ruff_cache", "dist", "build", ".system_generated"
        }

        for root, dirs, files in os.walk(self.target):
            dirs[:] = [d for d in dirs if d not in excluded and not d.startswith(".")]
            rel_root = os.path.relpath(root, self.target)
            if rel_root == ".":
                rel_root = ""

            for f in files:
                rel = os.path.join(rel_root, f).replace("\\", "/")
                rel_files.append(rel)

                # Read only critical small discovery files (first 3000 chars)
                lower = f.lower()
                if (
                    lower in ["package.json", "pyproject.toml", "cargo.toml", "dbt_project.yml", "chart.yaml", "catalog-info.yaml"]
                    or (lower.endswith(".md") and ("seed" in lower or "01_seed" in rel or lower == "skill.md"))
                    or ("openapi" in lower or "swagger" in lower)
                ):
                    try:
                        p = Path(root) / f
                        if p.stat().st_size < 1_000_000:
                            with open(p, "r", encoding="utf-8", errors="ignore") as fh:
                                file_snippets[rel] = fh.read(3000)
                    except Exception:
                        pass

        # Check for seed frontmatter
        for rel, content in file_snippets.items():
            if ("01_seed" in rel or "seed-" in rel) and content.startswith("---"):
                try:
                    parts = content.split("---")
                    if len(parts) >= 3:
                        parsed = yaml.safe_load(parts[1])
                        if isinstance(parsed, dict):
                            seed_data = parsed
                            break
                except Exception:
                    pass

        return self._evaluate_signals(rel_files, file_snippets, seed_data)

    def _discover_custom_profiles(self) -> dict[str, Path]:
        """Discovers custom YAML profiles in target repo and configured directories."""
        profiles: dict[str, Path] = {}
        search_dirs = [
            self.target / ".metricsthinking" / "profiles",
            self.target / "config" / "profiles",
        ]
        if self.custom_profiles_dir and self.custom_profiles_dir.exists():
            search_dirs.append(self.custom_profiles_dir)

        # User global config
        user_global = Path.home() / ".gemini" / "config" / "skills" / "metrics" / "profiles"
        if user_global.exists():
            search_dirs.append(user_global)

        for d in search_dirs:
            if d.exists():
                for p in d.glob("*.yaml"):
                    stem = p.stem.lower()
                    if stem not in profiles:
                        profiles[stem] = p
                for p in d.glob("*.yml"):
                    stem = p.stem.lower()
                    if stem not in profiles:
                        profiles[stem] = p
        return profiles

    def _evaluate_signals(
        self,
        rel_files: list[str],
        file_snippets: dict[str, str],
        seed_data: dict[str, Any]
    ) -> ArchetypeDetectionResult:
        """Core multi-signal scoring engine across all canonical and custom archetypes."""

        # 1. Authoritative Seed Override (Ground Truth First)
        raw_declared = seed_data.get("domain_archetype") or seed_data.get("archetype") or seed_data.get("project_type")
        if raw_declared:
            arch_str = str(raw_declared).strip().lower()
            if arch_str in ["library", "module", "cli", "sdk"]:
                arch_str = "software-engineering"
            if arch_str not in ["generic", "modular-framework", "unknown", "software"]:
                mode = seed_data.get("inspection_mode") or ARCHETYPE_INSPECTION_MODES.get(arch_str, "source_code")
                return ArchetypeDetectionResult(
                    primary_archetype=arch_str,
                    confidence=0.98,
                    inspection_mode=mode,
                    recommended_profile="default" if arch_str == "software-engineering" else arch_str,
                    detected_signals=[f"Declaración explícita en Seed Master ({seed_data.get('project_name', 'Seed')}): {raw_declared} -> {arch_str}"],
                    runner_up_archetypes=[],
                    rationale="Arquetipo establecido formalmente en el ThinkingSeed Master como fuente única de verdad (SSOT)."
                )

        # Scores dictionary
        scores: dict[str, ArchetypeScore] = {
            "sdd": ArchetypeScore("sdd", 0.0),
            "data-platform": ArchetypeScore("data-platform", 0.0),
            "web-app": ArchetypeScore("web-app", 0.0),
            "mlops": ArchetypeScore("mlops", 0.0),
            "llmops": ArchetypeScore("llmops", 0.0),
            "dataops": ArchetypeScore("dataops", 0.0),
            "gitops": ArchetypeScore("gitops", 0.0),
            "platform-eng": ArchetypeScore("platform-eng", 0.0),
            "devsecops": ArchetypeScore("devsecops", 0.0),
            "chaos-eng": ArchetypeScore("chaos-eng", 0.0),
            "dual-track": ArchetypeScore("dual-track", 0.0),
            "team-topologies": ArchetypeScore("team-topologies", 0.0),
            "agent-skill": ArchetypeScore("agent-skill", 0.0),
            "software-engineering": ArchetypeScore("software-engineering", 10.0, ["Estructura base de software"]),
        }

        # Check custom profiles discovered
        custom_profiles = self._discover_custom_profiles()
        for c_name in custom_profiles:
            if c_name not in scores:
                scores[c_name] = ArchetypeScore(c_name, 0.0)

        # Scan files for multi-signal signatures
        total_files = len(rel_files)
        pkg_json_content = ""
        pyproject_content = ""

        has_src = any(f.startswith(("src/", "app/", "lib/", "pkg/")) for f in rel_files)
        has_tests = any("test" in f.lower() for f in rel_files)
        source_code_count = sum(1 for f in rel_files if f.endswith((".py", ".rs", ".go", ".ts", ".js", ".java", ".c", ".cpp")))

        if has_src and source_code_count >= 5:
            scores["software-engineering"].score += 25.0
            scores["software-engineering"].signals.append(f"Código fuente estructurado en paquetes ({source_code_count} módulos)")

        if has_tests:
            scores["software-engineering"].score += 15.0

        for rel in rel_files:
            lower = rel.lower()
            is_test_file = lower.startswith("tests/") or "/tests/" in lower or "test_" in lower or lower.endswith("_test.py") or ".spec." in lower

            # --- SDD (Spec-Driven Development) Signals ---
            if ("openapi" in lower or "swagger" in lower) and not is_test_file:
                scores["sdd"].score += 45.0
                scores["sdd"].signals.append(f"Contrato formal de API ({rel})")
            elif lower.endswith(".proto") and not is_test_file:
                scores["sdd"].score += 35.0
                scores["sdd"].signals.append(f"Especificación Protobuf ({rel})")
            elif (lower.startswith(("specs/", "contracts/")) or "/specs/" in lower or "/contracts/" in lower) and not is_test_file:
                scores["sdd"].score += 30.0
                scores["sdd"].signals.append(f"Directorio de contratos/especificaciones ({rel})")
            elif "spectral" in lower and (lower.endswith(".yaml") or lower.endswith(".json") or lower.endswith(".yml")) and not is_test_file:
                scores["sdd"].score += 25.0
                scores["sdd"].signals.append(f"Linter de contratos Spectral ({rel})")

            # --- Data Platform Signals ---
            if (lower == "dbt_project.yml" or lower.endswith("/dbt_project.yml")) and not is_test_file:
                scores["data-platform"].score += 50.0
                scores["data-platform"].signals.append(f"Proyecto dbt Core / Cloud ({rel})")
            elif any(k in lower for k in ["/bronze/", "/silver/", "/gold/"]) and not is_test_file:
                scores["data-platform"].score += 35.0
                scores["data-platform"].signals.append(f"Arquitectura Medallion Lakehouse ({rel})")
            elif ("workflow_settings.yaml" in lower or "dataform.json" in lower) and not is_test_file:
                scores["data-platform"].score += 40.0
                scores["data-platform"].signals.append(f"Orquestación BigQuery Dataform ({rel})")

            # --- DataOps Signals ---
            if "great_expectations" in lower:
                scores["dataops"].score += 45.0
                scores["dataops"].signals.append(f"Suite de calidad Great Expectations ({rel})")
            elif "soda" in lower and (lower.endswith(".yml") or lower.endswith(".yaml")):
                scores["dataops"].score += 40.0
                scores["dataops"].signals.append(f"Contrato de datos Soda Core ({rel})")
            elif "datacontract" in lower:
                scores["dataops"].score += 40.0
                scores["dataops"].signals.append(f"Especificación de Data Contract ({rel})")

            # --- Web App Signals ---
            if lower.endswith((".tsx", ".jsx", ".vue", ".svelte")):
                scores["web-app"].score += 6.0
            elif "tailwind.config" in lower or "vite.config" in lower or "next.config" in lower:
                scores["web-app"].score += 25.0
                scores["web-app"].signals.append(f"Configuración de frontend moderno ({rel})")
            elif lower.startswith(("src/components/", "app/routes/", "pages/")):
                scores["web-app"].score += 15.0

            # --- MLOps Signals ---
            if lower == "dvc.yaml" or lower.endswith("/dvc.yaml"):
                scores["mlops"].score += 50.0
                scores["mlops"].signals.append(f"Pipeline de datos y modelos DVC ({rel})")
            elif "mlproject" in lower:
                scores["mlops"].score += 40.0
                scores["mlops"].signals.append(f"Manifiesto MLflow Project ({rel})")
            elif "model_cards" in lower or "model_card" in lower:
                scores["mlops"].score += 35.0
                scores["mlops"].signals.append(f"Tarjeta de modelo Model Card ({rel})")

            # --- LLMOps Signals ---
            if lower.startswith("prompts/") or "/prompts/" in lower:
                scores["llmops"].score += 25.0
            elif "ragas" in lower or "deepeval" in lower:
                scores["llmops"].score += 45.0
                scores["llmops"].signals.append(f"Framework de evaluación de LLMs ({rel})")
            elif "guardrails" in lower and (lower.endswith(".py") or lower.endswith(".yaml")):
                scores["llmops"].score += 35.0
                scores["llmops"].signals.append(f"Políticas de Guardrails para LLMs ({rel})")

            # --- GitOps Signals ---
            if lower == "chart.yaml" or lower.endswith("/chart.yaml"):
                scores["gitops"].score += 50.0
                scores["gitops"].signals.append(f"Helm Chart declarativo ({rel})")
            elif lower == "kustomization.yaml" or lower.endswith("/kustomization.yaml"):
                scores["gitops"].score += 45.0
                scores["gitops"].signals.append(f"Manifiesto Kustomize ({rel})")
            elif "/templates/" in lower and lower.endswith(".yaml") and not has_src:
                scores["gitops"].score += 20.0

            # --- Platform Engineering Signals ---
            if lower == "catalog-info.yaml" or lower.endswith("/catalog-info.yaml"):
                scores["platform-eng"].score += 55.0
                scores["platform-eng"].signals.append(f"Catálogo de servicios Backstage ({rel})")

            # --- DevSecOps Signals ---
            if lower.endswith(".rego"):
                scores["devsecops"].score += 40.0
                scores["devsecops"].signals.append(f"Políticas Policy-as-Code OPA/Rego ({rel})")
            elif any(k in lower for k in ["trivy.yaml", "semgrep.yaml", ".snyk"]):
                scores["devsecops"].score += 35.0
                scores["devsecops"].signals.append(f"Configuración de escaneo de seguridad ({rel})")

            # --- Chaos Engineering Signals ---
            if "chaos" in lower and (lower.endswith(".yaml") or lower.endswith(".yml")):
                scores["chaos-eng"].score += 45.0
                scores["chaos-eng"].signals.append(f"Escenario de Chaos Engineering ({rel})")

            # --- AI Agent Skill Signals (Strictly Evaluated) ---
            if (lower.endswith("skill.md") and ("skills/" in lower or ".agents/" in lower)):
                # Only high score if this is a genuine skill definition
                scores["agent-skill"].score += 40.0
                scores["agent-skill"].signals.append(f"Definición formal de habilidad SKILL.md ({rel})")
            elif "install_skill.py" in lower:
                scores["agent-skill"].score += 20.0
                scores["agent-skill"].signals.append(f"Instalador multi-agente ({rel})")

            # Notice: AGENTS.md, GEMINI.md, .cursorrules do NOT give points to agent-skill directly,
            # because they are standard multi-agent governance files used in all types of projects.

        # Snippet-level inspection (package.json, pyproject.toml)
        for rel, content in file_snippets.items():
            lower = rel.lower()
            if "package.json" in lower:
                if any(k in content for k in ['"react"', '"vue"', '"svelte"', '"next"', '"vite"', '"@angular"']):
                    scores["web-app"].score += 45.0
                    scores["web-app"].signals.append("Dependencias frontend UI en package.json (React/Vue/Next/Vite)")
            elif "pyproject.toml" in lower or "requirements.txt" in lower:
                if any(k in content for k in ["dbt-core", "dbt-bigquery", "pyspark", "delta-spark"]):
                    scores["data-platform"].score += 35.0
                    scores["data-platform"].signals.append("Librerías de Lakehouse/dbt en dependencias")
                if any(k in content for k in ["torch", "tensorflow", "scikit-learn", "mlflow"]):
                    scores["mlops"].score += 30.0
                    scores["mlops"].signals.append("Frameworks de ML en dependencias")
                if any(k in content for k in ["langchain", "llama-index", "ragas", "anthropic", "openai"]):
                    scores["llmops"].score += 30.0
                    scores["llmops"].signals.append("SDKs de LLMs/RAG en dependencias")

        # Normalize UI points if there are many frontend files
        if scores["web-app"].score > 0 and source_code_count > 0:
            frontend_files = sum(1 for f in rel_files if f.endswith((".tsx", ".jsx", ".vue", ".svelte", ".css", ".html")))
            if frontend_files / max(1, total_files) > 0.35:
                scores["web-app"].score += 25.0
                scores["web-app"].signals.append(f"Alta densidad de componentes frontend ({frontend_files} archivos)")

        # Penalize agent-skill if the repo is predominantly a software application or library
        if scores["agent-skill"].score > 0:
            if source_code_count >= 10 and scores["software-engineering"].score > 30.0:
                # Skill is just an auxiliary accessory, not the project's core archetype
                scores["agent-skill"].score = min(scores["agent-skill"].score, 25.0)

        # Sort scores descending
        ranked = sorted(scores.values(), key=lambda s: s.score, reverse=True)
        top = ranked[0]
        second = ranked[1] if len(ranked) > 1 else None

        # Calculate confidence
        total_top_score = top.score
        if total_top_score <= 15.0:
            # Low confidence across all specialized profiles -> fallback to software-engineering or custom
            primary = "software-engineering"
            confidence = 0.50
            is_emerging = True
            rationale = "No se detectaron marcadores determinísticos dominantes de perfiles especializados; se aplica el metamodelo universal de software."
        else:
            diff = (top.score - (second.score if second else 0.0))
            confidence = min(0.95, max(0.55, (top.score / (top.score + (second.score if second else 10.0))) * 1.1))
            primary = top.archetype
            is_emerging = False
            rationale = f"Marcadores dominantes físicos confirmados: {', '.join(top.signals[:3])}."

        inspection_mode = ARCHETYPE_INSPECTION_MODES.get(primary, "source_code")
        recommended_profile = "default" if primary == "software-engineering" else primary

        runner_ups: list[tuple[str, float]] = []
        for r in ranked[1:4]:
            if r.score > 10.0:
                c_norm = min(0.90, round(r.score / (top.score + 1.0), 2))
                runner_ups.append((r.archetype, c_norm))

        is_custom = (primary not in BUILTIN_PROFILES) and (primary in custom_profiles)

        return ArchetypeDetectionResult(
            primary_archetype=primary,
            confidence=confidence,
            inspection_mode=inspection_mode,
            recommended_profile=recommended_profile,
            detected_signals=top.signals,
            runner_up_archetypes=runner_ups,
            is_custom=is_custom,
            is_emerging_domain=is_emerging,
            rationale=rationale
        )


def probe_archetype(target_path: str = ".", custom_profiles_dir: Path | None = None) -> ArchetypeDetectionResult:
    """Convenience entry point for fast pre-flight archetype probing."""
    detector = ArchetypeDetector(target_path, custom_profiles_dir=custom_profiles_dir)
    return detector.detect_from_filesystem()
