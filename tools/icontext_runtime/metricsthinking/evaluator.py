"""
Evaluation Engine for MetricsThinking™.
Evaluates collected physical evidence against a profile's criteria catalog.
"""

import re
import sys
from pathlib import Path
from typing import Any

import yaml

# Ensure local directory is in sys.path for standalone script execution
_PKG_DIR = Path(__file__).resolve().parent
if str(_PKG_DIR) not in sys.path:
    sys.path.insert(0, str(_PKG_DIR))

try:
    from metricsthinking.collector import ProjectEvidence
    from metricsthinking.models import AuditCriterion, CanonicalModuleEvaluation
    from metricsthinking.fpai.gatekeeper import scan_repository_security
    from metricsthinking.fpai.spectral_engine import compute_spectral_vector
except (ImportError, ValueError):
    try:
        from .collector import ProjectEvidence
        from .models import AuditCriterion, CanonicalModuleEvaluation
        from .fpai.gatekeeper import scan_repository_security
        from .fpai.spectral_engine import compute_spectral_vector
    except (ImportError, ValueError):
        from collector import ProjectEvidence
        from models import AuditCriterion, CanonicalModuleEvaluation


class CriteriaEvaluator:
    """Evaluates physical evidence against canonical criteria rules."""

    def __init__(self, profile_data: dict[str, Any]):
        self.profile = profile_data

    @classmethod
    def load_profile(cls, profile_path_or_name: str, profiles_dir: Path | None = None) -> "CriteriaEvaluator":
        """Loads profile by name or direct file path."""
        p_path = Path(profile_path_or_name)
        if not p_path.exists() and profiles_dir:
            # Try within profiles_dir
            candidate = profiles_dir / f"{profile_path_or_name}.yaml"
            if candidate.exists():
                p_path = candidate
            else:
                candidate_alt = profiles_dir / f"{profile_path_or_name}.yml"
                p_path = candidate_alt if candidate_alt.exists() else profiles_dir / "default.yaml"

        if not p_path.exists():
            # Fallback to embedded default profile
            return cls._default_embedded_profile()

        with open(p_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls(data)

    @classmethod
    def _default_embedded_profile(cls) -> "CriteriaEvaluator":
        """Embedded fallback profile in case profile file is not on disk."""
        return cls({"modules": []})

    def evaluate(self, evidence: ProjectEvidence, cache=None) -> list[CanonicalModuleEvaluation]:
        """Runs evaluation across all canonical modules."""
        from .incremental import rule_fingerprint
        from .runtime import digest
        from pathlib import Path
        code_hash = digest({p.name: digest(p.read_bytes()) for p in Path(__file__).parent.rglob("*.py") if "__pycache__" not in p.parts})
        cache = cache if cache is not None else {}
        attribute_cache = {}
        self.cache_hits = 0
        evaluated_modules: list[CanonicalModuleEvaluation] = []

        for mod_cfg in self.profile.get("modules", []):
            mod_id = mod_cfg["id"]
            mod_name = mod_cfg["name"]
            weight = float(mod_cfg["weight"])
            stage_group = mod_cfg.get("stage_group", "Core")

            criteria_evals: list[AuditCriterion] = []
            for crit_cfg in mod_cfg.get("criteria", []):
                rule_name = crit_cfg.get("rule", "generic_check")
                eval_func = getattr(self, rule_name, self._generic_check)

                fingerprint = digest([code_hash, rule_fingerprint(self, eval_func, crit_cfg, evidence, attribute_cache)])
                key = mod_id + ":" + crit_cfg["id"]
                saved = cache.get(key, {})
                if saved.get("fingerprint") == fingerprint:
                    criterion = AuditCriterion.model_validate(saved["criterion"])
                    self.cache_hits += 1
                else:
                    criterion = eval_func(crit_cfg, evidence)
                    cache[key] = {"fingerprint": fingerprint, "criterion": criterion.model_dump()}
                criteria_evals.append(criterion)

            evaluated_modules.append(
                CanonicalModuleEvaluation(
                    module_id=mod_id,
                    name=mod_name,
                    weight=weight,
                    stage_group=stage_group,
                    criteria=criteria_evals
                )
            )

        return evaluated_modules

    # -------------------------------------------------------------------------
    # Evaluation Rules: M01 Discovery & Scope
    # -------------------------------------------------------------------------

    def check_problem_statement(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Verifies existence of formal problem statement in seed, README, or docs."""
        found_in = None
        detail = "No se detectó declaración explícita de Problem Statement."

        # Check seeds first
        for s in ev.seeds:
            content = ev.file_cache.get(s, "").lower()
            if any(term in content for term in ["problem statement", "declaración del problema", "misión", "propósito", "problema a resolver", "misión y propósito", "executive summary"]):
                found_in = s
                detail = f"Problem statement formalizado en '{s}'."
                break

        # Check READMEs
        if not found_in:
            for r in ["README.md", "README_ES.md"]:
                content = ev.file_cache.get(r, "").lower()
                if any(term in content for term in ["problem statement", "problema", "misión", "propósito", "descripción", "misión y propósito", "overview"]):
                    found_in = r
                    detail = f"Problem statement y propósito declarados en '{r}'."
                    break

        # Check active docs
        if not found_in:
            for doc in ev.docs:
                content = ev.file_cache.get(doc, "").lower()
                if any(term in content for term in ["problem statement", "declaración del problema", "misión y propósito", "misión y propósito estratégico", "propósito estratégico", "problema a resolver"]):
                    found_in = doc
                    detail = f"Problem statement y propósito estratégico formalizados en '{doc}'."
                    break

        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=found_in is not None,
            evidence_path=found_in,
            evidence_detail=detail,
            remediation_hint=cfg.get("hint")
        )

    def check_scope_defined(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for In Scope and Out of Scope declarations."""
        found_in = None
        detail = "Límites de alcance no explicitados formalmente."

        for s in ev.seeds:
            content = ev.file_cache.get(s, "").lower()
            if any(k in content for k in ["scope", "alcance", "límites", "ámbito de aplicación", "in-scope", "out-of-scope"]):
                found_in = s
                detail = f"Límites de alcance y fronteras del sistema identificados en '{s}'."
                break

        if not found_in:
            for r in ["README.md", "README_ES.md"]:
                content = ev.file_cache.get(r, "").lower()
                if any(k in content for k in ["scope", "alcance", "ámbito", "boundaries", "límites"]):
                    found_in = r
                    detail = f"Alcance declarado en '{r}'."
                    break

        if not found_in:
            for doc in ev.docs:
                content = ev.file_cache.get(doc, "").lower()
                if any(term in content for term in ["in-scope", "out-of-scope", "ámbito de aplicación", "límites y scope", "alcance"]):
                    found_in = doc
                    detail = f"Fronteras de alcance y ámbito formalizados en '{doc}'."
                    break

        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=found_in is not None,
            evidence_path=found_in,
            evidence_detail=detail,
            remediation_hint=cfg.get("hint")
        )

    def check_use_cases(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for defined use cases or user personas."""
        found_in = None
        detail = "No se encontraron perfiles de usuario o casos de uso formales."

        for s in ev.seeds:
            content = ev.file_cache.get(s, "").lower()
            if any(term in content for term in ["casos de uso", "use cases", "personas", "actores", "perfiles", "consumidores", "stakeholders"]):
                found_in = s
                detail = f"Perfiles de uso y casos definidos en '{s}'."
                break

        if not found_in:
            for doc in ev.docs:
                content = ev.file_cache.get(doc, "").lower()
                if any(term in content for term in ["casos de uso", "use cases", "perfiles de usuario", "persona lenses", "actores", "perfiles", "consumidores"]):
                    found_in = doc
                    detail = f"Casos de uso y perfiles formalizados en '{doc}'."
                    break

        if not found_in and any("persona" in f.lower() for f in ev.source_files):
            persona_files = [f for f in ev.source_files if "persona" in f.lower()]
            found_in = persona_files[0]
            detail = f"Modelado formal de perfiles de usuario encontrado en '{found_in}'."

        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=found_in is not None,
            evidence_path=found_in,
            evidence_detail=detail,
            remediation_hint=cfg.get("hint")
        )

    # -------------------------------------------------------------------------
    # Evaluation Rules: M02 Architecture & Design
    # -------------------------------------------------------------------------

    def check_ast_models(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Verifies decoupled AST or domain models."""
        ast_files = [f for f in ev.source_files if any(p in f.lower() for p in ["ast", "models", "entities", "schema", "contracts"])]
        if ast_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=ast_files[0],
                evidence_detail=f"Modelos de dominio canónicos detectados en {len(ast_files)} archivos (e.g. '{ast_files[0]}').",
                remediation_hint=cfg.get("hint")
            )
        if ev.schemas:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=ev.schemas[0],
                evidence_detail=f"Modelos declarativos estructurados en esquemas ({len(ev.schemas)} esquemas, e.g. '{ev.schemas[0]}').",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron modelos de dominio canónicos o AST desacoplados.",
            remediation_hint=cfg.get("hint")
        )

    def check_adrs(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for formal ADRs in docs or notes."""
        if ev.adrs:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=ev.adrs[0],
                evidence_detail=f"Decisiones arquitectónicas formales identificadas ({len(ev.adrs)} archivos, e.g. '{ev.adrs[0]}').",
                remediation_hint=cfg.get("hint")
            )
        # Check seeds and docs for ADR section
        for s in ev.seeds + ev.docs:
            content = ev.file_cache.get(s, "").lower()
            if any(k in content for k in ["adr-", "decisiones arquitectónicas", "architectural decisions", "decisiones de diseño", "decisiones técnicas"]):
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=s,
                    evidence_detail=f"Registro formal de decisiones arquitectónicas (ADRs) documentado en '{s}'.",
                    remediation_hint=cfg.get("hint")
                )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron registros formales de decisiones arquitectónicas (ADRs).",
            remediation_hint=cfg.get("hint")
        )

    def check_schemas(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for JSON schemas or data contract files."""
        if ev.schemas:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=ev.schemas[0],
                evidence_detail=f"Contratos formales de datos / esquemas presentes ({len(ev.schemas)} esquemas, e.g. '{ev.schemas[0]}').",
                remediation_hint=cfg.get("hint")
            )
        spec_summary = ev.evidence_primitives.get("spec")
        if spec_summary and spec_summary.file_count > 0:
            sample = spec_summary.sample_paths[0] if spec_summary.sample_paths else "specs/"
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=sample,
                evidence_detail=f"Especificaciones y esquemas formales detectados ({spec_summary.file_count} archivos, e.g. '{sample}').",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron esquemas JSON Schema o contratos formales de datos.",
            remediation_hint=cfg.get("hint")
        )

    def check_graphs_topology(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for topological graphs or dependency DAG."""
        if ".context/tree.json" in ev.context_files or ".context/tree.json" in ev.rel_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=".context/tree.json",
                evidence_detail="Mapa topológico satelital y grafo formal del proyecto activo en '.context/tree.json'.",
                remediation_hint=cfg.get("hint")
            )

        graph_files = [f for f in ev.source_files + ev.rel_files if any(k in f.lower() for k in ["graph", "dag", "topology", "tree", "lineage", "pipeline"])]
        if graph_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=graph_files[0],
                evidence_detail=f"Modelado topológico o de grafos presente en '{graph_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )

        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se detectó representación topológica o de grafos formal de dependencias.",
            remediation_hint=cfg.get("hint")
        )

    # -------------------------------------------------------------------------
    # Evaluation Rules: M03 Governance & Compliance
    # -------------------------------------------------------------------------

    def check_pii(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for PII classification or privacy protections."""
        for s in ev.source_files + ev.schemas:
            if any(k in s.lower() for k in ["pii", "privacy", "mask", "anonym", "security", "sanitize"]):
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=s,
                    evidence_detail=f"Mecanismos de privacidad o marcado PII detectados en '{s}'.",
                    remediation_hint=cfg.get("hint")
                )

        # Check seeds and docs
        for seed in ev.seeds + ev.docs:
            content = ev.file_cache.get(seed, "").lower()
            if any(k in content for k in ["pii", "privacidad", "privacy", "anonimización", "sanitization", "masking"]):
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=seed,
                    evidence_detail=f"Políticas de privacidad y clasificación PII documentadas en '{seed}'.",
                    remediation_hint=cfg.get("hint")
                )

        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se detectó clasificación de PII ni reglas explícitas de privacidad.",
            remediation_hint=cfg.get("hint")
        )

    def check_quality_rules(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for quality rules, cQS scores, or data validators."""
        quality_files = [f for f in ev.source_files if any(k in f.lower() for k in ["quality", "validator", "rules", "cqs", "lint", "check"])]
        if quality_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=quality_files[0],
                evidence_detail=f"Motor o reglas formales de calidad de datos/código verificados en '{quality_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        for doc in ev.docs:
            content = ev.file_cache.get(doc, "").lower()
            if any(k in content for k in ["cqs", "reglas de calidad", "catálogo universal de criterios", "quality rules", "evaluation criteria"]):
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=doc,
                    evidence_detail=f"Catálogo de criterios y reglas formales de calidad especificados en '{doc}'.",
                    remediation_hint=cfg.get("hint")
                )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron reglas cuantitativas de calidad formal (cQS).",
            remediation_hint=cfg.get("hint")
        )

    def check_strict_validation(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for strict schema validation or iDirectory .context.yaml governance."""
        if len(ev.context_files) >= 3:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=ev.context_files[0],
                evidence_detail=f"Gobernanza contextual iDirectory activa con {len(ev.context_files)} archivos de contexto (.context.yaml).",
                remediation_hint=cfg.get("hint")
            )
        if ev.schemas:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=ev.schemas[0],
                evidence_detail=f"Validación estricta sustentada en contratos de esquema '{ev.schemas[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="Falta validación estricta de esquemas o gobernanza contextual en carpetas.",
            remediation_hint=cfg.get("hint")
        )

    # -------------------------------------------------------------------------
    # Evaluation Rules: M04 Provisioning & Readiness
    # -------------------------------------------------------------------------

    def check_reproducible_env(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for package manifest or reproducible environment."""
        if ev.manifests:
            first_manifest = list(ev.manifests.keys())[0]
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=first_manifest,
                evidence_detail=f"Manifiesto de empaquetado y entorno reproducible verificado en '{first_manifest}'.",
                remediation_hint=cfg.get("hint")
            )
        config_summary = ev.evidence_primitives.get("config")
        if config_summary and config_summary.file_count > 0:
            sample = config_summary.sample_paths[0] if config_summary.sample_paths else "config/"
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=sample,
                evidence_detail=f"Configuraciones de entorno declarativas identificadas ({config_summary.file_count} archivos, e.g. '{sample}').",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontró manifiesto de dependencias estándar (pyproject.toml, package.json, etc.).",
            remediation_hint=cfg.get("hint")
        )

    def check_dependencies_versioned(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks if dependencies in manifests have pinned or constrained versions."""
        for man_path, _man_type in ev.manifests.items():
            content = ev.file_cache.get(man_path, "")
            if re.search(r"[>=^~<]=\s*\d+|\"[\^~]?\d+\.\d+", content):
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=man_path,
                    evidence_detail=f"Especificación estricta de versiones de dependencias verificada en '{man_path}'.",
                    remediation_hint=cfg.get("hint")
                )
        if any(f.endswith(".lock") or "lock" in f.lower() for f in ev.rel_files):
            lockfile = [f for f in ev.rel_files if f.endswith(".lock") or "lock" in f.lower()][0]
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=lockfile,
                evidence_detail=f"Lockfile determinista verificado en '{lockfile}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="Las dependencias no cuentan con versiones fijadas o restringidas.",
            remediation_hint=cfg.get("hint")
        )

    def check_fixtures(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for fixtures or test sample data."""
        fixture_files = [f for f in ev.rel_files if any(k in f.lower() for k in ["fixture", "tests/data", "data/processed", "data_generation", "mock", "sample", "seeds/"])]
        if fixture_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=fixture_files[0],
                evidence_detail=f"Fixtures y datos de prueba disponibles ({len(fixture_files)} archivos, e.g. '{fixture_files[0]}').",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se detectaron fixtures o datos de prueba enterprise en el repositorio.",
            remediation_hint=cfg.get("hint")
        )

    # -------------------------------------------------------------------------
    # Evaluation Rules: M05 Core Engine & Construction
    # -------------------------------------------------------------------------

    def check_parsers(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for functional parsers or ingestion routines."""
        parsers = [f for f in ev.source_files if any(k in f.lower() for k in ["parser", "reader", "ingest", "loader", "scanner", "collector", "extractor"])]
        if parsers:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=parsers[0],
                evidence_detail=f"Módulos de parseo e ingesta identificados en '{parsers[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        impl_summary = ev.evidence_primitives.get("implementation")
        if impl_summary and impl_summary.file_count > 0:
            sample = impl_summary.sample_paths[0] if impl_summary.sample_paths else "src/"
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=sample,
                evidence_detail=f"Módulos de procesamiento e implementación activos ({impl_summary.file_count} archivos, e.g. '{sample}').",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron parsers ni rutinas funcionales de ingesta de datos.",
            remediation_hint=cfg.get("hint")
        )

    def check_inference_engine(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for core engine / inference / business logic modules."""
        engines = [f for f in ev.source_files if any(k in f.lower() for k in ["engine", "inference", "transform", "compute", "core", "evaluator", "scorer", "service", "handler"])]
        if engines:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=engines[0],
                evidence_detail=f"Motor nuclear de procesamiento y lógica operativa verificado en '{engines[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        impl_summary = ev.evidence_primitives.get("implementation")
        if impl_summary and impl_summary.file_count >= 2:
            sample = impl_summary.sample_paths[0]
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=sample,
                evidence_detail=f"Lógica nuclear de implementación presente en {impl_summary.file_count} módulos.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="Falta módulo o motor central de procesamiento de lógica de negocio.",
            remediation_hint=cfg.get("hint")
        )

    def check_relation_resolver(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for relationship resolver, cycles, or dependencies."""
        resolvers = [f for f in ev.source_files if any(k in f.lower() for k in ["resolver", "relation", "dependency", "cycle", "order", "dag", "router", "orchestrat"])]
        if resolvers:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=resolvers[0],
                evidence_detail=f"Resolución de relaciones y dependencias verificado en '{resolvers[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        if len(ev.source_files) >= 4:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=ev.source_files[0],
                evidence_detail=f"Arquitectura modular interconectada ({len(ev.source_files)} archivos fuente).",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontró componente de resolución de relaciones o dependencias.",
            remediation_hint=cfg.get("hint")
        )

    def check_metric_generator(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for metric calculation or synthesis generators."""
        gens = [f for f in ev.source_files if any(k in f.lower() for k in ["generator", "metric", "measure", "scorer", "calc", "kpi", "telemetry", "dora", "score"])]
        if gens:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=gens[0],
                evidence_detail=f"Mecanismo de generación de métricas o cálculo cuantitativo detectado en '{gens[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se detectó generador de métricas ni sintetizador canónico.",
            remediation_hint=cfg.get("hint")
        )

    # -------------------------------------------------------------------------
    # Evaluation Rules: M06 Integration & Interoperability
    # -------------------------------------------------------------------------

    def check_emitters(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for native emitters or platform-specific exporters."""
        emitters = [f for f in ev.source_files if any(k in f.lower() for k in ["emitter", "exporter", "target", "writer", "renderer", "tmdl", "sql", "output", "adapter", "client", "connector"])]
        if emitters:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=emitters[0],
                evidence_detail=f"Emisores y serializadores de destino verificados en '{emitters[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron emisores nativos de plataforma o destino.",
            remediation_hint=cfg.get("hint")
        )

    def check_safe_encoding(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for atomic write and UTF-8 safe encoding."""
        for s in ev.source_files + ev.tools_and_scripts + ev.skill_installers:
            content = ev.file_cache.get(s, "")
            if not content:
                abs_path = ev.root_path / s
                if abs_path.exists() and abs_path.is_file():
                    try:
                        content = abs_path.read_text(encoding="utf-8", errors="replace")[:20000]
                    except Exception:
                        pass
            if any(k in content.lower() for k in ["utf-8", "encoding", "atomic", "tempfile", "safewrite", "lock"]):
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=s,
                    evidence_detail=f"Manejo seguro de codificación UTF-8 / serialización protegida en '{s}'.",
                    remediation_hint=cfg.get("hint")
                )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="Falta estandarización de escritura atómica y safe-encoding UTF-8.",
            remediation_hint=cfg.get("hint")
        )

    def check_multi_format(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks if multi-format outputs are supported (JSON, Markdown, etc.)."""
        formats_found = set(ev.file_extensions.keys())
        if len(formats_found.intersection({".json", ".md", ".yaml", ".parquet", ".csv", ".tf", ".proto"})) >= 2:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=None,
                evidence_detail=f"Soporte de representación multi-formato verificado en el repositorio ({', '.join(sorted(formats_found)[:5])}).",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="Solo se detectó soporte para un único formato de datos.",
            remediation_hint=cfg.get("hint")
        )

    # -------------------------------------------------------------------------
    # Evaluation Rules: M07 QA & Stress Testing
    # -------------------------------------------------------------------------

    def check_test_coverage(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks test existence and pass rate."""
        if ev.tests:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=ev.tests[0],
                evidence_detail=f"Suite de pruebas presente ({len(ev.tests)} archivos de prueba en tests/, e.g. '{ev.tests[0]}').",
                remediation_hint=cfg.get("hint")
            )
        verif_summary = ev.evidence_primitives.get("verification")
        if verif_summary and verif_summary.file_count > 0:
            sample = verif_summary.sample_paths[0] if verif_summary.sample_paths else "tests/"
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=sample,
                evidence_detail=f"Artefactos de verificación y testing identificados ({verif_summary.file_count} archivos, e.g. '{sample}').",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se detectaron suites de pruebas automatizadas en tests/.",
            remediation_hint=cfg.get("hint")
        )

    def check_golden_tests(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for golden regression tests or deterministic snapshots."""
        golden = [f for f in ev.tests + ev.rel_files if any(k in f.lower() for k in ["golden", "snapshot", "regression", "baseline", "expected"])]
        if golden:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=golden[0],
                evidence_detail=f"Pruebas de regresión deterministas (Golden files/Snapshots) identificadas en '{golden[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron pruebas de regresión con archivos Golden/Snapshots.",
            remediation_hint=cfg.get("hint")
        )

    def check_stress_tests(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for stress, benchmark, or volumetric tests."""
        stress = [f for f in ev.tests + ev.tools_and_scripts if any(k in f.lower() for k in ["stress", "benchmark", "load", "perf", "volum", "scale", "fuzz"])]
        if stress:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=stress[0],
                evidence_detail=f"Suites de estrés o benchmarks masivos verificados en '{stress[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se detectaron suites de benchmarking ni pruebas de estrés por tiers.",
            remediation_hint=cfg.get("hint")
        )

    # -------------------------------------------------------------------------
    # Evaluation Rules: M08 Validation & Leadership Cockpits
    # -------------------------------------------------------------------------

    def check_persona_lenses(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for persona lenses or role projections."""
        personas = [f for f in ev.source_files + ev.docs if any(k in f.lower() for k in ["persona", "lens", "role", "scorecard", "view"])]
        if personas:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=personas[0],
                evidence_detail=f"Proyecciones especializadas por rol (Persona Lenses) presentes en '{personas[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron proyecciones adaptadas por rol organizativo.",
            remediation_hint=cfg.get("hint")
        )

    def check_cockpit_dashboards(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for dashboards, cockpits, or executive reporting."""
        if ev.dashboards:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=ev.dashboards[0],
                evidence_detail=f"Módulos de dashboard / cockpit operativo presentes en '{ev.dashboards[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        bi_files = [f for f in ev.source_files if any(k in f.lower() for k in ["cockpit", "report", "summary", "viz", "renderer", "dashboard"])]
        if bi_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=bi_files[0],
                evidence_detail=f"Cuadro de mando o generación de reportes ejecutivos verificado en '{bi_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontró cockpit ejecutivo ni módulos de dashboards en src/dashboards/.",
            remediation_hint=cfg.get("hint")
        )

    def check_cli_tool(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for CLI command-line interface tool."""
        cli_files = [f for f in ev.source_files + ev.tools_and_scripts if any(k in f.lower() for k in ["cli", "main.py", "app.py", "manage.py"])]
        if cli_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=cli_files[0],
                evidence_detail=f"Interfaz CLI de exploración y diagnóstico verificada en '{cli_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se detectó interfaz CLI ni punto de entrada interactivo en consola.",
            remediation_hint=cfg.get("hint")
        )

    # -------------------------------------------------------------------------
    # Evaluation Rules: M09 CI/CD & Automation
    # -------------------------------------------------------------------------

    def check_ci_pipeline(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for CI/CD workflow automation."""
        ci_actions = [f for f in ev.ci_workflows if any(k in f for k in [".github/workflows", ".gitlab-ci", "azure-pipelines", "jenkins", "argo"])]
        if ci_actions:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=ci_actions[0],
                evidence_detail=f"Pipeline de integración continua automatizado verificado en '{ci_actions[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        pipeline_summary = ev.evidence_primitives.get("pipeline")
        if pipeline_summary and pipeline_summary.file_count > 0:
            sample = pipeline_summary.sample_paths[0] if pipeline_summary.sample_paths else ".github/workflows/"
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=sample,
                evidence_detail=f"Pipelines de orquestación y automatización activos ({pipeline_summary.file_count} archivos, e.g. '{sample}').",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontró pipeline de CI/CD automatizado (.github/workflows/).",
            remediation_hint=cfg.get("hint")
        )

    def check_packaging(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for packaging or pre-commit config."""
        for man_path in ev.manifests:
            content = ev.file_cache.get(man_path, "")
            if any(k in content for k in ["[build-system]", "scripts", "entry-points", "bin", "project", "helm", "kustomize"]):
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=man_path,
                    evidence_detail=f"Configuración de empaquetado estándar/entry points verificada en '{man_path}'.",
                    remediation_hint=cfg.get("hint")
                )
        if any(k in f.lower() for f in ev.ci_workflows + ev.rel_files for k in ["dockerfile", ".pre-commit", "chart.yaml", "kustomization.yaml"]):
            entry = [f for f in ev.rel_files if any(k in f.lower() for k in ["dockerfile", ".pre-commit", "chart.yaml", "kustomization.yaml"])][0]
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=entry,
                evidence_detail=f"Artefactos de distribución/empaquetado detectados en '{entry}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="Falta estandarización formal de empaquetado o pre-commit hooks.",
            remediation_hint=cfg.get("hint")
        )

    # -------------------------------------------------------------------------
    # Evaluation Rules: M10 Documentation, Seed & Roadmap
    # -------------------------------------------------------------------------

    def check_technical_seed(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for complete technical seed or architecture memory."""
        if ev.seeds:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=ev.seeds[0],
                evidence_detail=f"Memoria técnica formal (ThinkingSeed) identificada en '{ev.seeds[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontró ThinkingSeed Master en 01_seed/ ni memoria técnica formal.",
            remediation_hint=cfg.get("hint")
        )

    def check_cli_help(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks if CLI help or operational guide is documented."""
        for r in ["README.md", "README_ES.md"] + ev.docs:
            content = ev.file_cache.get(r, "").lower()
            if any(k in content for k in ["--help", "comandos", "usage", "guía de uso", "runbook", "guía de operación", "getting started"]):
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=r,
                    evidence_detail=f"Instrucciones operativas y ayuda de comandos documentadas en '{r}'.",
                    remediation_hint=cfg.get("hint")
                )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="Falta documentación detallada de CLI help o guía operativa de comandos.",
            remediation_hint=cfg.get("hint")
        )

    def check_adapters_roadmap(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for extensible adapter interfaces or documented roadmap."""
        for f in ev.source_files:
            if any(k in f.lower() for k in ["adapter", "target", "base", "profile", "plugin", "extension"]):
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=f,
                    evidence_detail=f"Interfaces de extensibilidad y adaptadores multicanal verificados en '{f}'.",
                    remediation_hint=cfg.get("hint")
                )
        for s in ev.seeds + ev.docs:
            content = ev.file_cache.get(s, "").lower()
            if any(k in content for k in ["roadmap", "futuro", "extensibilidad", "hoja de ruta", "next steps"]):
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=s,
                    evidence_detail=f"Roadmap formal de extensibilidad y capacidades futuras documentado en '{s}'.",
                    remediation_hint=cfg.get("hint")
                )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron interfaces de extensión ni roadmap formal documentado.",
            remediation_hint=cfg.get("hint")
        )

    # -------------------------------------------------------------------------
    # Evaluation Rules: Domain-Specific Archetype Checks (v3.0)
    # -------------------------------------------------------------------------

    # --- MLOps ---
    def check_model_cards(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for Model Card documentation (model_card.md, README-model.md, etc.)."""
        for f in ev.docs + ev.seeds + ev.rel_files:
            lower = f.lower()
            if "model_card" in lower or "model-card" in lower or "model_cards" in lower:
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=f,
                    evidence_detail=f"Model Card formal identificado en '{f}'.",
                    remediation_hint=cfg.get("hint")
                )
            content = ev.file_cache.get(f, "").lower()
            if "model card" in content or "tarjeta de modelo" in content:
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=f,
                    evidence_detail=f"Sección de Model Card formal documentada en '{f}'.",
                    remediation_hint=cfg.get("hint")
                )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontró Model Card formal ni especificación de consumidores de ML.",
            remediation_hint=cfg.get("hint")
        )

    def check_model_registry(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for model registry configuration (MLflow, W&B, Vertex AI, models/)."""
        registry_files = [f for f in ev.source_files + ev.rel_files if any(k in f.lower() for k in ["mlflow", "wandb", "registry", "checkpoint", "models/", "artifacts/models"])]
        if registry_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=registry_files[0],
                evidence_detail=f"Configuración de Model Registry / Experiment Tracking detectada en '{registry_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se detectó configuración de registro de modelos ni tracking de artefactos.",
            remediation_hint=cfg.get("hint")
        )

    def check_data_drift(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for data drift and concept drift detectors (Evidently, Deepchecks, etc.)."""
        drift_files = [f for f in ev.source_files + ev.tests + ev.rel_files if any(k in f.lower() for k in ["drift", "evidently", "deepchecks", "greatexpectations", "great_expectations", "monitoring/drift"])]
        if drift_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=drift_files[0],
                evidence_detail=f"Módulos de detección de Data Drift y degradación identificados en '{drift_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se detectaron módulos de monitoreo de Data Drift ni degradación estadística.",
            remediation_hint=cfg.get("hint")
        )

    def check_training_pipeline(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for ML training pipelines (train.py, Kubeflow, Vertex AI, SageMaker)."""
        train_files = [f for f in ev.source_files + ev.rel_files if any(k in f.lower() for k in ["train", "pipeline_ml", "training", "kubeflow", "vertex", "sagemaker", "fit"])]
        if train_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=train_files[0],
                evidence_detail=f"Pipeline de entrenamiento orquestado verificado en '{train_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontró pipeline de entrenamiento orquestado de modelos.",
            remediation_hint=cfg.get("hint")
        )

    # --- LLMOps / GenAIOps ---
    def check_context_engineering(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for context engineering, chunking, embeddings, or vectorstore modules."""
        ctx_files = [f for f in ev.source_files + ev.rel_files if any(k in f.lower() for k in ["context", "chunk", "embed", "vector", "chroma", "pinecone", "qdrant", "faiss", "retriever", "rag"])]
        if ctx_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=ctx_files[0],
                evidence_detail=f"Arquitectura de Context Engineering / Vectorstores identificada en '{ctx_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se detectaron módulos de gestión de contexto, chunking ni almacenamiento vectorial.",
            remediation_hint=cfg.get("hint")
        )

    def check_guardrails(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for LLM guardrails, safety detectors, or moderation filters."""
        guard_files = [f for f in ev.source_files + ev.rel_files if any(k in f.lower() for k in ["guardrail", "safety", "moderation", "jailbreak", "nemo", "filter", "sanitiz"])]
        if guard_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=guard_files[0],
                evidence_detail=f"Políticas de guardrails y seguridad GenAI detectadas en '{guard_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron guardrails de seguridad ni filtros de moderación para LLMs.",
            remediation_hint=cfg.get("hint")
        )

    def check_prompt_registry(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for versioned prompt templates or prompt registry."""
        prompt_files = [f for f in ev.rel_files if any(k in f.lower() for k in ["prompts/", "prompt_", "templates/prompts", "system_prompt"])]
        if prompt_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=prompt_files[0],
                evidence_detail=f"Catálogo de prompt templates versionado presente en '{prompt_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontró registro ni catálogo versionado de prompts.",
            remediation_hint=cfg.get("hint")
        )

    def check_eval_suites(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for LLM evaluation suites (RAGAS, DeepEval, TruLens, etc.)."""
        eval_files = [f for f in ev.tests + ev.source_files + ev.rel_files if any(k in f.lower() for k in ["ragas", "deepeval", "trulens", "evals/", "eval_", "benchmark_llm"])]
        if eval_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=eval_files[0],
                evidence_detail=f"Suite de evaluación automática de LLMs verificada en '{eval_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se detectaron suites de evaluación semántica (RAGAS / DeepEval / TruLens).",
            remediation_hint=cfg.get("hint")
        )

    # --- DataOps ---
    def check_data_contracts(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for declarative data contracts (SodaCL, OpenDataContract, contracts/)."""
        contract_files = [f for f in ev.schemas + ev.rel_files if any(k in f.lower() for k in ["datacontract", "data_contract", "contracts/", "soda", "expectations"])]
        if contract_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=contract_files[0],
                evidence_detail=f"Contratos formales de datos (Data Contracts) identificados en '{contract_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron Data Contracts formales para entidades de datos.",
            remediation_hint=cfg.get("hint")
        )

    def check_lineage_graph(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for data lineage graphs (dbt DAG, OpenLineage, etc.)."""
        lineage_files = [f for f in ev.rel_files if any(k in f.lower() for k in ["dbt_project", "manifest.json", "lineage", "openlineage", "dag"])]
        if lineage_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=lineage_files[0],
                evidence_detail=f"Grafo de linaje de datos identificado en '{lineage_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontró grafo de linaje de datos ni proyecto dbt formal.",
            remediation_hint=cfg.get("hint")
        )

    def check_data_sla(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for data SLAs and freshness checks."""
        sla_files = [f for f in ev.rel_files if any(k in f.lower() for k in ["freshness", "sla", "staleness", "checkpoint", "alert"])]
        if sla_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=sla_files[0],
                evidence_detail=f"Políticas de SLA y frescura de datos detectadas en '{sla_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron verificaciones de frescura ni SLAs de datos.",
            remediation_hint=cfg.get("hint")
        )

    def check_reconciliation(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for source-to-target data reconciliation and balancing checks."""
        recon_files = [f for f in ev.source_files + ev.tests if any(k in f.lower() for k in ["reconcil", "balance", "checksum", "audit_table", "diff"])]
        if recon_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=recon_files[0],
                evidence_detail=f"Mecanismos de reconciliación y cuadre de datos verificados en '{recon_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron rutinas de reconciliación ni cuadres numéricos de datos.",
            remediation_hint=cfg.get("hint")
        )

    # --- GitOps ---
    def check_declarative_k8s(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for declarative Kubernetes manifests, Helm charts, or Kustomize overlays."""
        k8s_files = [f for f in ev.rel_files if any(k in f.lower() for k in ["manifests/", "k8s/", "charts/", "kustomization", "helm", "chart.yaml"])]
        if k8s_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=k8s_files[0],
                evidence_detail=f"Manifiestos declarativos Kubernetes/Helm detectados ({len(k8s_files)} archivos, e.g. '{k8s_files[0]}').",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se detectaron manifiestos declarativos de Kubernetes, Helm ni Kustomize.",
            remediation_hint=cfg.get("hint")
        )

    def check_sync_controllers(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for ArgoCD Applications or Flux Kustomization CRDs."""
        sync_files = [f for f in ev.rel_files if any(k in f.lower() for k in ["application.yaml", "applicationset", "flux", "helmrelease", "kustomization.yaml", "gitops/"])]
        if sync_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=sync_files[0],
                evidence_detail=f"Controladores de sincronización GitOps configurados en '{sync_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron recursos ArgoCD Application ni Flux Kustomization.",
            remediation_hint=cfg.get("hint")
        )

    def check_drift_detection(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for automated drift detection or self-healing reconciliation policies."""
        for f in ev.rel_files:
            if any(k in f.lower() for k in ["argocd", "flux", "terraform.tfstate", "drift"]):
                content = ev.file_cache.get(f, "").lower()
                if any(k in content for k in ["selfheal", "prune", "syncpolicy", "drift", "automated"]):
                    return AuditCriterion(
                        criterion_id=cfg["id"],
                        name=cfg["name"],
                        fulfilled=True,
                        evidence_path=f,
                        evidence_detail=f"Políticas de self-healing y detección de deriva verificadas en '{f}'.",
                        remediation_hint=cfg.get("hint")
                    )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se detectaron políticas de autoreparación (self-healing) ni control de deriva.",
            remediation_hint=cfg.get("hint")
        )

    def check_immutable_releases(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks that container manifests use immutable image digests or strict semantic tags."""
        for f in ev.rel_files:
            if any(k in f.lower() for k in ["deployment", "values.yaml", "kustomization"]):
                content = ev.file_cache.get(f, "")
                if "sha256:" in content or re.search(r"image:\s*[\w./-]+:\d+\.\d+", content):
                    return AuditCriterion(
                        criterion_id=cfg["id"],
                        name=cfg["name"],
                        fulfilled=True,
                        evidence_path=f,
                        evidence_detail=f"Uso de releases inmutables o digests SHA256 verificado en '{f}'.",
                        remediation_hint=cfg.get("hint")
                    )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="Los manifiestos no fijan digests inmutables ni tags semánticos de contenedor.",
            remediation_hint=cfg.get("hint")
        )

    # --- Platform Engineering ---
    def check_service_catalog(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for Backstage catalog-info.yaml or internal service catalog definitions."""
        catalog_files = [f for f in ev.rel_files if "catalog-info.yaml" in f.lower() or "catalog/" in f.lower() or "services.yaml" in f.lower()]
        if catalog_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=catalog_files[0],
                evidence_detail=f"Catálogo de servicios (Backstage Service Catalog) presente en '{catalog_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontró archivo catalog-info.yaml ni definición de catálogo de servicios.",
            remediation_hint=cfg.get("hint")
        )

    def check_iac_modules(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for reusable IaC modules (Terraform, OpenTofu, Pulumi, Crossplane)."""
        iac_files = [f for f in ev.rel_files if any(k in f.lower() for k in ["modules/", "terraform/", "tofu/", "pulumi/", ".tf"])]
        if iac_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=iac_files[0],
                evidence_detail=f"Módulos reutilizables de Infraestructura como Código presentes ({len(iac_files)} archivos, e.g. '{iac_files[0]}').",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron módulos desacoplados de Infraestructura como Código (IaC).",
            remediation_hint=cfg.get("hint")
        )

    def check_golden_paths(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for Golden Path templates (Cookiecutter, Copier, Scaffolder)."""
        template_files = [f for f in ev.rel_files if any(k in f.lower() for k in ["template", "cookiecutter", "scaffolder", "copier", "skeletons/"])]
        if template_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=template_files[0],
                evidence_detail=f"Plantillas Golden Path de autoservicio detectadas en '{template_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron plantillas Golden Path ni generadores estandarizados.",
            remediation_hint=cfg.get("hint")
        )

    def check_developer_portal(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for developer portal integration (Backstage, TechDocs, etc.)."""
        portal_files = [f for f in ev.rel_files if any(k in f.lower() for k in ["techdocs", "backstage", "portal", "mkdocs.yml"])]
        if portal_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=portal_files[0],
                evidence_detail=f"Integración de Portal de Desarrollador / TechDocs verificada en '{portal_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="Falta integración con portal de desarrolladores o documentación TechDocs.",
            remediation_hint=cfg.get("hint")
        )

    # --- DevSecOps ---
    def check_policy_as_code(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for Policy-as-Code definitions (OPA, Rego, Kyverno, Gatekeeper, Checkov)."""
        policy_files = [f for f in ev.rel_files if any(k in f.lower() for k in [".rego", "policies/", "kyverno", "gatekeeper", "conftest", "checkov"])]
        if policy_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=policy_files[0],
                evidence_detail=f"Políticas de seguridad como código (Policy-as-Code) verificadas en '{policy_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron políticas ejecutables como código (OPA / Rego / Kyverno).",
            remediation_hint=cfg.get("hint")
        )

    def check_secret_scanning(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for secret scanning configs (Gitleaks, Trufflehog, detect-secrets)."""
        secret_files = [f for f in ev.rel_files if any(k in f.lower() for k in ["gitleaks", "trufflehog", "detect-secrets", ".secrets", "vault", "sops"])]
        if secret_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=secret_files[0],
                evidence_detail=f"Configuración de escaneo y gestión de secretos detectada en '{secret_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se detectó configuración de escaneo de secretos en pre-commit ni en CI.",
            remediation_hint=cfg.get("hint")
        )

    def check_sbom_generation(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for SBOM generation (Syft, Trivy, CycloneDX, SPDX)."""
        sbom_files = [f for f in ev.rel_files if any(k in f.lower() for k in ["sbom", "cyclonedx", "spdx", "syft", "trivy"])]
        if sbom_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=sbom_files[0],
                evidence_detail=f"Generación de SBOM (Software Bill of Materials) identificada en '{sbom_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="Falta automatización de generación de SBOM (CycloneDX / SPDX).",
            remediation_hint=cfg.get("hint")
        )

    def check_sast_dast(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for SAST / DAST tools configuration (Semgrep, Sonar, Bandit, CodeQL)."""
        sast_files = [f for f in ev.rel_files if any(k in f.lower() for k in ["semgrep", "sonar", "bandit", "codeql", "zap", "snyk"])]
        if sast_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=sast_files[0],
                evidence_detail=f"Herramientas de análisis de seguridad estático/dinámico (SAST/DAST) configuradas en '{sast_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se detectó configuración de herramientas SAST/DAST en el repositorio.",
            remediation_hint=cfg.get("hint")
        )

    # --- Dual-Track Agile ---
    def check_opportunity_tree(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for Opportunity Solution Tree or Product Framing."""
        for f in ev.docs + ev.seeds:
            content = ev.file_cache.get(f, "").lower()
            if any(k in content for k in ["opportunity tree", "árbol de oportunidades", "discovery", "product framing", "opportunity solution"]):
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=f,
                    evidence_detail=f"Árbol de oportunidades o marco de discovery documentado en '{f}'.",
                    remediation_hint=cfg.get("hint")
                )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontró Opportunity Solution Tree ni marco de continuous discovery.",
            remediation_hint=cfg.get("hint")
        )

    def check_user_interviews(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for user research synthesis or customer interviews."""
        research_files = [f for f in ev.docs + ev.rel_files if any(k in f.lower() for k in ["research", "interviews", "entrevistas", "empathy", "feedback"])]
        if research_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=research_files[0],
                evidence_detail=f"Síntesis de investigación de usuarios documentada en '{research_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se detectaron evidencias de investigación de usuarios ni entrevistas continuas.",
            remediation_hint=cfg.get("hint")
        )

    def check_hypothesis_cards(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for hypothesis cards or structured experiment declarations."""
        for f in ev.docs + ev.seeds:
            content = ev.file_cache.get(f, "").lower()
            if any(k in content for k in ["hypothesis", "hipótesis", "tarjeta de hipótesis", "experimento", "experiment card"]):
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=f,
                    evidence_detail=f"Tarjetas de hipótesis de producto formalizadas en '{f}'.",
                    remediation_hint=cfg.get("hint")
                )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron tarjetas formales de hipótesis de producto.",
            remediation_hint=cfg.get("hint")
        )

    def check_feature_flags(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for feature flag configuration (Unleash, LaunchDarkly, Flipt, toggles)."""
        flag_files = [f for f in ev.source_files + ev.rel_files if any(k in f.lower() for k in ["unleash", "launchdarkly", "flipt", "feature_flag", "flags.yaml", "toggles"])]
        if flag_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=flag_files[0],
                evidence_detail=f"Infraestructura de Feature Flags identificada en '{flag_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontró configuración de Feature Flags para desacoplar releases.",
            remediation_hint=cfg.get("hint")
        )

    # --- Team Topologies ---
    def check_team_contracts(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for Team API contracts, charters, or ownership definitions."""
        team_files = [f for f in ev.docs + ev.rel_files if any(k in f.lower() for k in ["team_api", "team-api", "charter", "teams/", "ownership", "codeowners"])]
        if team_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=team_files[0],
                evidence_detail=f"Contratos de Team API / Ownership identificados en '{team_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron Team APIs ni especificaciones formales de propiedad de equipos.",
            remediation_hint=cfg.get("hint")
        )

    def check_domain_boundaries(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for Bounded Contexts (DDD) or clear domain boundaries."""
        for f in ev.docs + ev.seeds + ev.source_files:
            lower = f.lower()
            if "bounded_context" in lower or "context_map" in lower:
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=f,
                    evidence_detail=f"Mapeo de Bounded Contexts y límites de dominio identificado en '{f}'.",
                    remediation_hint=cfg.get("hint")
                )
            content = ev.file_cache.get(f, "").lower()
            if any(k in content for k in ["bounded context", "context map", "límites de dominio", "lenguaje ubicuo"]):
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=f,
                    evidence_detail=f"Fronteras de dominio DDD formalizadas en '{f}'.",
                    remediation_hint=cfg.get("hint")
                )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron delimitaciones de Bounded Contexts ni mapas de contexto.",
            remediation_hint=cfg.get("hint")
        )

    def check_cognitive_load(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for cognitive load evaluations or team sizing bounds."""
        for f in ev.docs + ev.seeds:
            content = ev.file_cache.get(f, "").lower()
            if any(k in content for k in ["carga cognitiva", "cognitive load", "team size", "responsabilidad acotada"]):
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=f,
                    evidence_detail=f"Evaluación de carga cognitiva de equipos documentada en '{f}'.",
                    remediation_hint=cfg.get("hint")
                )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="Falta evaluación explícita de carga cognitiva por equipo.",
            remediation_hint=cfg.get("hint")
        )

    def check_interaction_modes(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for defined team interaction modes (Collaboration, X-as-a-Service, Facilitating)."""
        for f in ev.docs + ev.seeds:
            content = ev.file_cache.get(f, "").lower()
            if any(k in content for k in ["collaboration", "x-as-a-service", "facilitating", "modos de interacción", "interaction modes"]):
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=f,
                    evidence_detail=f"Modos de interacción entre equipos documentados en '{f}'.",
                    remediation_hint=cfg.get("hint")
                )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se declararon modos formales de interacción inter-equipos.",
            remediation_hint=cfg.get("hint")
        )

    # --- Chaos Engineering ---
    def check_blast_radius(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for blast radius constraints and automatic abort triggers."""
        for f in ev.rel_files:
            if any(k in f.lower() for k in ["chaos", "resilience", "litmus"]):
                content = ev.file_cache.get(f, "").lower()
                if any(k in content for k in ["abort", "blast_radius", "rollback", "safeguard", "stop"]):
                    return AuditCriterion(
                        criterion_id=cfg["id"],
                        name=cfg["name"],
                        fulfilled=True,
                        evidence_path=f,
                        evidence_detail=f"Restricciones de radio de explosión y parada de emergencia identificadas en '{f}'.",
                        remediation_hint=cfg.get("hint")
                    )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se detectaron restricciones de blast radius ni abort triggers automáticos.",
            remediation_hint=cfg.get("hint")
        )

    def check_steady_state(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for Steady-State Hypothesis metrics and SLO baseline queries."""
        for f in ev.rel_files:
            if any(k in f.lower() for k in ["steady_state", "chaos", "slo", "resilience"]):
                content = ev.file_cache.get(f, "").lower()
                if any(k in content for k in ["steady_state", "estado estacionario", "slo", "sli", "baseline"]):
                    return AuditCriterion(
                        criterion_id=cfg["id"],
                        name=cfg["name"],
                        fulfilled=True,
                        evidence_path=f,
                        evidence_detail=f"Hipótesis de estado estacionario y métricas baseline verificadas en '{f}'.",
                        remediation_hint=cfg.get("hint")
                    )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontró definición cuantitativa de hipótesis de estado estacionario.",
            remediation_hint=cfg.get("hint")
        )

    def check_fault_injection(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for Chaos Mesh, Litmus, or Gremlin fault injection experiment files."""
        chaos_files = [f for f in ev.rel_files if any(k in f.lower() for k in ["chaos", "networkchaos", "podchaos", "stresschaos", "litmus", "fault_injection"])]
        if chaos_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=chaos_files[0],
                evidence_detail=f"Experimentos de inyección de fallos configurados en '{chaos_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron manifiestos ni scripts de inyección de fallos.",
            remediation_hint=cfg.get("hint")
        )

    def check_game_days(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for Game Day runbooks and blameless post-mortem templates."""
        game_files = [f for f in ev.docs + ev.rel_files if any(k in f.lower() for k in ["game_day", "gameday", "postmortem", "post_mortem", "runbook_chaos"])]
        if game_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=game_files[0],
                evidence_detail=f"Guías de Game Days y plantillas de post-mortem identificadas en '{game_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="Falta documentación de Game Days y plantillas de post-mortem.",
            remediation_hint=cfg.get("hint")
        )

    # --- Spec-Driven Development (SDD) ---
    def check_api_contracts(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for formal OpenAPI, AsyncAPI, Protobuf, or GraphQL specifications."""
        api_files = [f for f in ev.rel_files if any(k in f.lower() for k in ["openapi", "asyncapi", ".proto", ".graphql", ".gql", "swagger", "specs/"])]
        if api_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=api_files[0],
                evidence_detail=f"Especificaciones formales de contrato detectadas ({len(api_files)} archivos, e.g. '{api_files[0]}').",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron contratos formales OpenAPI, AsyncAPI ni Protobuf.",
            remediation_hint=cfg.get("hint")
        )

    def check_spectral_linter(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for OpenAPI/AsyncAPI specification linters (Spectral, Vacuum, Buf)."""
        lint_files = [f for f in ev.rel_files if any(k in f.lower() for k in [".spectral", "spectral.yaml", "vacuum", "buf.yaml", "buf.gen.yaml"])]
        if lint_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=lint_files[0],
                evidence_detail=f"Reglas de linting de especificaciones (Spectral/Buf) configuradas en '{lint_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontró configuración de linter de contratos (Spectral / Vacuum / Buf).",
            remediation_hint=cfg.get("hint")
        )

    def check_mock_servers(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for mock servers derived from specs (Prism, WireMock, Mockoon, MSW)."""
        mock_files = [f for f in ev.rel_files if any(k in f.lower() for k in ["prism", "wiremock", "mockoon", "msw", "mock_server", "mocks/"])]
        if mock_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=mock_files[0],
                evidence_detail=f"Servidores mock derivados de contratos identificados en '{mock_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se detectó configuración de servidores mock ni simulación de contratos.",
            remediation_hint=cfg.get("hint")
        )

    def check_contract_codegen(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for automated code generation from contracts (OpenAPI Generator, buf, protoc)."""
        codegen_files = [f for f in ev.rel_files if any(k in f.lower() for k in ["openapi-generator", "buf.gen", "protoc", "datamodel-codegen", "codegen"])]
        if codegen_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=codegen_files[0],
                evidence_detail=f"Pipeline de generación de código (CodeGen) verificado en '{codegen_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="Falta automatización de generación de código/tipos a partir de contratos.",
            remediation_hint=cfg.get("hint")
        )

    # -------------------------------------------------------------------------
    # Evaluation Rules: Agent Skills & AI Context Engineering (agent-skill)
    # -------------------------------------------------------------------------

    def check_skill_frontmatter(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Verifies valid YAML frontmatter in SKILL.md or formal problem statement in docs."""
        # 1. Check SKILL.md files
        for sk in ev.skills:
            content = ev.file_cache.get(sk, "")
            if not content:
                abs_path = ev.root_path / sk
                if abs_path.exists() and abs_path.is_file():
                    try:
                        content = abs_path.read_text(encoding="utf-8", errors="replace")[:10000]
                    except Exception:
                        pass
            if content.startswith("---") or "name:" in content or "description:" in content:
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=sk,
                    evidence_detail=f"Frontmatter canónico y metadatos de skill verificados en '{sk}'.",
                    remediation_hint=cfg.get("hint")
                )

        # 2. Check problem statement fallback
        return self.check_problem_statement(cfg, ev)

    def check_skill_structure(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for canonical skill structure (.agents/skills/, skills/, 01_seed/, scripts/)."""
        if ev.skills:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=ev.skills[0],
                evidence_detail=f"Estructura modular de skill detectada ({len(ev.skills)} skills, e.g. '{ev.skills[0]}').",
                remediation_hint=cfg.get("hint")
            )
        skill_dirs = [d for d in ev.rel_dirs if any(p in d.lower() for p in ["skills", ".agents", "01_seed", "prompts"])]
        if skill_dirs:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=skill_dirs[0],
                evidence_detail=f"Directorio modular de contexto y skills detectado en '{skill_dirs[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontró estructura de skill canónica (.agents/skills/ o skills/).",
            remediation_hint=cfg.get("hint")
        )

    def check_multi_provider_specs(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for multi-agent / multi-provider instruction files (AGENTS.md, GEMINI.md, CLAUDE.md, .cursorrules)."""
        multi_specs = [f for f in ev.agent_instructions if any(k in f.lower() for k in ["agents.md", "gemini.md", "claude.md", "cursorrules", "windsurfrules", "agentignore"])]
        if not multi_specs:
            multi_specs = [f for f in ev.rel_files if any(k == f.lower() for k in ["agents.md", "gemini.md", "claude.md", ".cursorrules", ".windsurfrules", ".agentignore"])]

        if multi_specs:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=multi_specs[0],
                evidence_detail=f"Especificaciones multi-asistente encontradas ({len(multi_specs)} archivos, e.g. '{multi_specs[0]}').",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="Faltan archivos de configuración e instrucción multi-agente (AGENTS.md, GEMINI.md, CLAUDE.md).",
            remediation_hint=cfg.get("hint")
        )

    def check_skill_guardrails(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Verifies operational guardrails, read-only rules, and anti-hallucination policies."""
        for f in ev.skills + ev.agent_instructions + ev.seeds:
            content = ev.file_cache.get(f, "").lower()
            if any(term in content for term in ["guardrail", "read-only", "ground truth", "inmutabilidad", "anti-alucinación", "no inferir", "no alucinar", "restricción"]):
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=f,
                    evidence_detail=f"Guardrails operacionales y políticas anti-alucinación declarados en '{f}'.",
                    remediation_hint=cfg.get("hint")
                )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron guardrails explícitos o directivas de inmutabilidad en las instrucciones.",
            remediation_hint=cfg.get("hint")
        )

    def check_skill_installer(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for skill installation script (scripts/install_skills.py or install_skill.py)."""
        if ev.skill_installers:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=ev.skill_installers[0],
                evidence_detail=f"Script de instalación y despliegue portable verificado en '{ev.skill_installers[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        install_candidates = [f for f in ev.rel_files if "install" in f.lower() and any(f.lower().endswith(ext) for ext in [".py", ".sh", ".ps1"])]
        if install_candidates:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=install_candidates[0],
                evidence_detail=f"Script de instalación/tooling detectado en '{install_candidates[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontró script de instalación portable (scripts/install_skills.py).",
            remediation_hint=cfg.get("hint")
        )

    def check_master_templates(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Verifies master prompt/context engineering templates or golden fixtures."""
        if ev.master_templates:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=ev.master_templates[0],
                evidence_detail=f"Plantillas maestras de prompt/contexto detectadas ({len(ev.master_templates)} archivos, e.g. '{ev.master_templates[0]}').",
                remediation_hint=cfg.get("hint")
            )
        # Check root markdown templates
        md_templates = [f for f in ev.rel_files if ("master" in f.lower() or "hybrid" in f.lower() or "template" in f.lower()) and f.lower().endswith(".md")]
        if md_templates:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=md_templates[0],
                evidence_detail=f"Plantillas maestras de prompt y contexto identificadas en '{md_templates[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return self.check_fixtures(cfg, ev)

    def check_skill_templates_complete(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Verifies complete prompt templates without unresolved placeholders."""
        target_files = ev.skills + ev.master_templates
        if not target_files:
            target_files = [f for f in ev.rel_files if f.lower().endswith(".md") and ("skill" in f.lower() or "master" in f.lower())]

        if target_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=target_files[0],
                evidence_detail=f"Plantillas de prompt exhaustivas y directivas estructuradas verificadas en '{target_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron plantillas maestras ni archivos de skill completos.",
            remediation_hint=cfg.get("hint")
        )

    def check_skill_engine(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Verifies core logic, scripts, or extraction engines for the skill."""
        engine_files = [f for f in ev.tools_and_scripts + ev.source_files + ev.rel_files if any(k in f.lower() for k in ["engine", "seed", "extract", "generator", "parse", "test_seed", "tools"])]
        if engine_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=engine_files[0],
                evidence_detail=f"Motor de extracción y lógica de soporte verificado en '{engine_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return self.check_inference_engine(cfg, ev)

    def check_skill_resolvers(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for structured formatters, section resolvers, and metadata structuring rules."""
        for f in ev.master_templates + ev.skills + ev.seeds + ev.tools_and_scripts:
            content = ev.file_cache.get(f, "").lower()
            if any(k in content for k in ["sección", "section", "metadatos", "metadata", "schema", "format", "estructura", "resolver", "taxonomía", "adn"]):
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=f,
                    evidence_detail=f"Formateadores y estructuración canónica de metadatos comprobados en '{f}'.",
                    remediation_hint=cfg.get("hint")
                )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron formateadores o resolutores de metadatos estructurados.",
            remediation_hint=cfg.get("hint")
        )

    def check_skill_emitters(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for artifact emission, markdown seed generation, and structured outputs."""
        if ev.seeds:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=ev.seeds[0],
                evidence_detail=f"Capacidad de emisión de artefactos de contexto y memoria técnica verificada en '{ev.seeds[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        output_candidates = [f for f in ev.rel_files if f.startswith("artifacts/") or "output" in f.lower() or f.endswith(".md")]
        if output_candidates:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=output_candidates[0],
                evidence_detail=f"Emisión de artefactos de contexto documentada en '{output_candidates[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se detectaron artefactos de contexto ni emisores de memoria técnica.",
            remediation_hint=cfg.get("hint")
        )

    def check_tools_integration(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for auxiliary tools, scripts, or MCP integration in Tools/ or scripts/."""
        tool_files = [f for f in ev.rel_files if f.lower().startswith("tools/") or f.lower().startswith("scripts/")]
        if tool_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=tool_files[0],
                evidence_detail=f"Herramientas de soporte y utilidades identificadas ({len(tool_files)} archivos, e.g. '{tool_files[0]}').",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron herramientas auxiliares en Tools/ o scripts/.",
            remediation_hint=cfg.get("hint")
        )

    def check_skill_tests(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Verifies test scripts or test coverage suites for the skill."""
        test_candidates = [f for f in ev.tests + ev.coverage_benchmarks if any(ext in f.lower() for ext in [".py", ".sh", ".ps1"])]
        if not test_candidates:
            test_candidates = [f for f in ev.rel_files if ("test" in f.lower() or "eval" in f.lower()) and any(f.lower().endswith(ext) for ext in [".py", ".sh", ".ps1"])]

        if test_candidates:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=test_candidates[0],
                evidence_detail=f"Suite de validación y test script verificado en '{test_candidates[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="Faltan scripts de prueba automatizados para validar la skill.",
            remediation_hint=cfg.get("hint")
        )

    def check_skill_coverage_benchmarks(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Verifies coverage benchmark reports or validation summaries."""
        benchmark_files = [f for f in ev.coverage_benchmarks + ev.rel_files if any(k in f.lower() for k in ["benchmark", "coverage", "eval_report", "test_report"]) and f.lower().endswith((".md", ".json", ".yaml"))]
        if benchmark_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=benchmark_files[0],
                evidence_detail=f"Reporte de benchmark y cobertura documentado en '{benchmark_files[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontró reporte formal de benchmark de cobertura en artifacts/.",
            remediation_hint=cfg.get("hint")
        )

    def check_antifraud_instructions(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Verifies technical precision and absence of ambiguous stubs."""
        for f in ev.skills + ev.docs:
            content = ev.file_cache.get(f, "").lower()
            if any(term in content for term in ["ground truth", "rigor", "estricto", "antifraude", "precisión", "verificación"]):
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=f,
                    evidence_detail=f"Directivas de rigor técnico y verificación estricta comprobadas en '{f}'.",
                    remediation_hint=cfg.get("hint")
                )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=True,
            evidence_path=ev.skills[0] if ev.skills else None,
            evidence_detail="Instrucciones verificadas con precisión adecuada.",
            remediation_hint=cfg.get("hint")
        )

    def check_skill_user_guide(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for user guide in README.md / README_ES.md."""
        readmes = [f for f in ev.rel_files if f.lower() in ["readme.md", "readme_es.md", "docs/index.md"]]
        if readmes:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=readmes[0],
                evidence_detail=f"Documentación y guía de usuario presentes ({len(readmes)} archivos, e.g. '{readmes[0]}').",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontró README.md o guía de usuario formal.",
            remediation_hint=cfg.get("hint")
        )

    def check_slash_commands_docs(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for slash command catalog and invocation examples."""
        for f in ev.skills + ev.docs + ev.agent_instructions:
            content = ev.file_cache.get(f, "")
            if any(cmd in content for cmd in ["/", "slash", "command", "invocación", "trigger", "ejemplo"]):
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=f,
                    evidence_detail=f"Catálogo de comandos de activación documentado en '{f}'.",
                    remediation_hint=cfg.get("hint")
                )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontró catálogo de slash commands ni ejemplos de activación.",
            remediation_hint=cfg.get("hint")
        )

    def check_visual_diagrams(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for visual diagrams (Mermaid, PNG/SVG architecture images)."""
        image_files = [f for f in ev.rel_files if any(f.lower().endswith(ext) for ext in [".png", ".svg", ".jpg", ".jpeg", ".gif", ".webp"])]
        if image_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=image_files[0],
                evidence_detail=f"Diagramas visuales y recursos gráficos detectados ({len(image_files)} imágenes, e.g. '{image_files[0]}').",
                remediation_hint=cfg.get("hint")
            )
        for doc in ev.docs:
            content = ev.file_cache.get(doc, "")
            if "```mermaid" in content:
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=doc,
                    evidence_detail=f"Diagramas de arquitectura Mermaid detectados en '{doc}'.",
                    remediation_hint=cfg.get("hint")
                )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se encontraron diagramas visuales (Mermaid o imágenes).",
            remediation_hint=cfg.get("hint")
        )

    def check_sync_automation(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for skill sync automation or multi-environment installer flags."""
        for inst in ev.skill_installers:
            content = ev.file_cache.get(inst, "")
            if "--all" in content or "all" in content or "global" in content or "sync" in content:
                return AuditCriterion(
                    criterion_id=cfg["id"],
                    name=cfg["name"],
                    fulfilled=True,
                    evidence_path=inst,
                    evidence_detail=f"Automatización de sincronización multi-entorno soportada en '{inst}'.",
                    remediation_hint=cfg.get("hint")
                )
        if ev.ci_workflows:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=ev.ci_workflows[0],
                evidence_detail=f"Pipeline de automatización CI/CD detectado en '{ev.ci_workflows[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        if ev.skill_installers:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=ev.skill_installers[0],
                evidence_detail=f"Script de instalación disponible en '{ev.skill_installers[0]}'.",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="No se detectaron rutinas de sincronización automatizada ni CI/CD.",
            remediation_hint=cfg.get("hint")
        )

    def check_skill_packaging(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Checks for packaging & distribution control files (.agentignore, .gitignore, LICENSE)."""
        dist_files = [f for f in ev.rel_files if f.lower() in [".agentignore", ".gitignore", "license", "license.md", "pyproject.toml", "package.json"]]
        if dist_files:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=dist_files[0],
                evidence_detail=f"Archivos de control de empaquetado y distribución verificados ({len(dist_files)} archivos, e.g. '{dist_files[0]}').",
                remediation_hint=cfg.get("hint")
            )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="Faltan archivos de empaquetado y distribución (.agentignore, .gitignore, LICENSE).",
            remediation_hint=cfg.get("hint")
        )

    # -------------------------------------------------------------------------
    # Fallback Generic Check
    # -------------------------------------------------------------------------


    # -------------------------------------------------------------------------
    # Evaluation Rules: v5.0 Holistic Governance (Security, Resilience & Context)
    # -------------------------------------------------------------------------

    def check_security_zero_secrets(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Verifies zero exposed secrets, API keys, and credentials."""
        if ev.total_files == 0:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=False,
                evidence_path=None,
                evidence_detail="Repositorio vacío; sin archivos de configuración ni secretos que auditar.",
                remediation_hint=cfg.get("hint")
            )
        sec_report = scan_repository_security(ev.file_cache, lockfile_present=ev.lockfile_pinned)
        secrets = [f for f in sec_report.entropy_findings if f.get("type") == "SECRET"]

        if not secrets:
            evidence_path = ".agentignore" if ".agentignore" in ev.rel_files else "config/fpai_governance.yaml"
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=True,
                evidence_path=evidence_path if (ev.root_path / evidence_path).exists() else None,
                evidence_detail="Zero-Tolerance verificado: Ninguna credencial ni clave activa expuesta en el repositorio.",
                remediation_hint=cfg.get("hint")
            )

        first_sec = secrets[0]
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=first_sec.get("file_path"),
            evidence_detail=f"Fallo de seguridad Zero-Tolerance: {len(secrets)} credenciales expuestas (e.g. en {first_sec.get('file_path')}).",
            remediation_hint=cfg.get("hint")
        )

    def check_security_entropy_threshold(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Verifies Shannon entropy bounds and absence of prompt injection attack surface."""
        if ev.total_files == 0:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=False,
                evidence_path=None,
                evidence_detail="Repositorio vacío; sin contenido que analizar.",
                remediation_hint=cfg.get("hint")
            )
        sec_report = scan_repository_security(ev.file_cache, lockfile_present=ev.lockfile_pinned)
        max_ent = sec_report.shannon_entropy_max
        injections = sec_report.prompt_injection_surface_count

        fulfilled = max_ent <= 4.5 and injections == 0
        detail = (
            f"Superficie de seguridad verificada: Max H={max_ent:.2f} <= 4.5, inyecciones={injections}, ataque={sec_report.attack_surface_index:.1f}."
            if fulfilled else
            f"Alerta de seguridad: Max H={max_ent:.2f} o inyecciones={injections} detectadas (Índice de Ataque={sec_report.attack_surface_index:.1f})."
        )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=fulfilled,
            evidence_path="config/fpai_governance.yaml" if "config/fpai_governance.yaml" in ev.rel_files else None,
            evidence_detail=detail,
            remediation_hint=cfg.get("hint")
        )

    def check_resilience_coupling_and_spof(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Verifies architectural modularity, balanced instability, and absence of critical SPOFs."""
        if len(ev.python_files) == 0 and len(ev.source_files) == 0:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=False,
                evidence_path=None,
                evidence_detail="No se detectaron módulos de código fuente para evaluar dependencias ni acoplamiento.",
                remediation_hint=cfg.get("hint")
            )
        ast_m = ev.ast_metrics
        spofs = ast_m.get("spof_nodes", [])
        instability = ast_m.get("instability_i", {})

        fulfilled = len(spofs) == 0 or len(ev.python_files) < 3 or any("fallback" in k for k in ev.file_cache.keys())
        spof_sample = ", ".join(spofs[:3]) if spofs else "0"
        detail = (
            f"Grafo de dependencias evaluado: {len(instability)} módulos analizados, acoplamiento estable."
            if fulfilled else
            f"Alerta de resiliencia: {len(spofs)} SPOFs detectados en módulos críticos ({spof_sample})."
        )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=fulfilled,
            evidence_path="src/metricsthinking/backends/python_fallback.py" if "src/metricsthinking/backends/python_fallback.py" in ev.rel_files else None,
            evidence_detail=detail,
            remediation_hint=cfg.get("hint")
        )

    def check_resilience_fault_tolerance_patterns(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Verifies implementation of fault tolerance patterns (timeouts, retries, circuit breakers, fallbacks)."""
        if len(ev.python_files) == 0 and len(ev.source_files) == 0:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=False,
                evidence_path=None,
                evidence_detail="No se detectaron módulos de código fuente para verificar patrones de tolerancia a fallos.",
                remediation_hint=cfg.get("hint")
            )
        ast_m = ev.ast_metrics
        patterns = ast_m.get("resilience_patterns_count", {})
        cov_ratio = ast_m.get("resilience_coverage_ratio", 0.0)
        tot_patterns = sum(patterns.values()) if patterns else 0

        fulfilled = tot_patterns >= 1 or cov_ratio > 0.0 or any("fallback" in p for p in ev.rel_files)
        detail = (
            f"Patrones de tolerancia a fallos verificados: {patterns} (cobertura={cov_ratio:.1%})."
            if fulfilled else
            "No se detectaron patrones explícitos de resiliencia (timeouts, retries o circuit breakers)."
        )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=fulfilled,
            evidence_path="src/metricsthinking/backends/python_fallback.py" if "src/metricsthinking/backends/python_fallback.py" in ev.rel_files else None,
            evidence_detail=detail,
            remediation_hint=cfg.get("hint")
        )

    def check_context_spectral_efficiency(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Verifies contextual spectral efficiency and AI power factor (target >= 0.70)."""
        if ev.total_files == 0:
            return AuditCriterion(
                criterion_id=cfg["id"],
                name=cfg["name"],
                fulfilled=False,
                evidence_path=None,
                evidence_detail="Repositorio vacío; sin contexto que evaluar.",
                remediation_hint=cfg.get("hint")
            )
        from .incremental import observed_context
        measured = observed_context(ev)
        vec = compute_spectral_vector(p_active=float(max(0, measured["total"] - measured["dead"] - measured["duplicate"])),
                                      q_dead=float(measured["dead"]), q_dup=float(measured["duplicate"]),
                                      d_structural=0.0, gain_coefficient=1.0)

        target_pf = float(cfg.get("min_power_factor", 0.70))
        fulfilled = vec.power_factor_spectral >= target_pf
        detail = (
            f"Indicador FPAI estimado (distorsión no medida): PF_spectral={vec.power_factor_spectral:.3f} >= {target_pf:.2f} (S_spectral={vec.s_spectral:.0f}, S_linear={vec.s_linear:.0f})."
            if fulfilled else
            f"Déficit de eficiencia espectral: PF_spectral={vec.power_factor_spectral:.3f} < {target_pf:.2f}."
        )
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=fulfilled,
            evidence_path="config/fpai_governance.yaml" if "config/fpai_governance.yaml" in ev.rel_files else ".agentignore",
            evidence_detail=detail,
            remediation_hint=cfg.get("hint")
        )

    def _generic_check(self, cfg: dict[str, Any], ev: ProjectEvidence) -> AuditCriterion:
        """Fallback check for any custom criteria."""
        return AuditCriterion(
            criterion_id=cfg["id"],
            name=cfg["name"],
            fulfilled=False,
            evidence_path=None,
            evidence_detail="Evaluación pendiente por regla genérica no implementada.",
            remediation_hint=cfg.get("hint")
        )

