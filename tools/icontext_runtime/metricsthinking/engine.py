"""
MetricsThinking™ Engine & Orchestrator.
Universal Project Auditor executing Ground Truth forensic inspection.
"""

import sys
from pathlib import Path

# Ensure local directory is in sys.path for standalone script execution
_PKG_DIR = Path(__file__).resolve().parent
if str(_PKG_DIR) not in sys.path:
    sys.path.insert(0, str(_PKG_DIR))

try:
    from metricsthinking.collector import ProjectCollector
    from metricsthinking.detector import ArchetypeDetector, ArchetypeDetectionResult, probe_archetype
    from metricsthinking.evaluator import CriteriaEvaluator
    from metricsthinking.models import ProjectAuditReport
    from metricsthinking.renderer import ReportRenderer
    from metricsthinking.scorer import AuditScorer
except (ImportError, ValueError):
    try:
        from .collector import ProjectCollector
        from .detector import ArchetypeDetector, ArchetypeDetectionResult, probe_archetype
        from .evaluator import CriteriaEvaluator
        from .models import ProjectAuditReport
        from .renderer import ReportRenderer
        from .scorer import AuditScorer
    except (ImportError, ValueError):
        from collector import ProjectCollector
        from detector import ArchetypeDetector, ArchetypeDetectionResult, probe_archetype
        from evaluator import CriteriaEvaluator
        from models import ProjectAuditReport
        from renderer import ReportRenderer
        from scorer import AuditScorer


PROFILE_ALIASES: dict[str, str] = {
    # Agent skills & AI Context Engineering
    "agent-skill": "agent-skill",
    "agent_skill": "agent-skill",
    "agentskill": "agent-skill",
    "skill": "agent-skill",
    "skills": "agent-skill",
    "ai-skill": "agent-skill",
    "ai_skill": "agent-skill",
    "context-skill": "agent-skill",
    "context-engineering": "agent-skill",
    "context_engineering": "agent-skill",
    "prompt-engineering": "agent-skill",
    "prompt_engineering": "agent-skill",
    "agent": "agent-skill",
    "agents": "agent-skill",
    # Data platform & DataOps
    "data-platform": "data-platform",
    "data_platform": "data-platform",
    "data": "data-platform",
    "lakehouse": "data-platform",
    "medallion": "data-platform",
    "dataops": "dataops",
    # Web app
    "web-app": "web-app",
    "web_app": "web-app",
    "webapp": "web-app",
    "web": "web-app",
    "frontend": "web-app",
    # LLMOps & GenAI
    "llmops": "llmops",
    "llm": "llmops",
    "genai": "llmops",
    "rag": "llmops",
    # MLOps
    "mlops": "mlops",
    "ml": "mlops",
    # GitOps
    "gitops": "gitops",
    "k8s": "gitops",
    "kubernetes": "gitops",
    # Platform engineering
    "platform-eng": "platform-eng",
    "platform": "platform-eng",
    "platform_eng": "platform-eng",
    # DevSecOps
    "devsecops": "devsecops",
    "security": "devsecops",
    "sec": "devsecops",
    # Chaos engineering
    "chaos-eng": "chaos-eng",
    "chaos": "chaos-eng",
    # SDD / Spec-driven
    "sdd": "sdd",
    "api": "sdd",
    "spec": "sdd",
    "spec-driven": "sdd",
    # Dual-track & Team topologies
    "dual-track": "dual-track",
    "agile": "dual-track",
    "team-topologies": "team-topologies",
    "team": "team-topologies",
    # Default
    "software-engineering": "default",
    "software": "default",
    "default": "default",
    "auto": "auto"
}


def resolve_profile_name(hint_or_name: str | None) -> str:
    """Resolves profile names, aliases, or natural language prompts into canonical profile name."""
    if not hint_or_name:
        return "default"

    clean = hint_or_name.strip().lower()

    # Direct match in aliases
    if clean in PROFILE_ALIASES:
        return PROFILE_ALIASES[clean]

    # Natural language pattern matching (e.g. "evalua este proyecto como una skill para IA")
    if any(k in clean for k in ["skill", "habilidad", "agente", "agent", "prompt", "context engineering", "thinkingseed"]):
        return "agent-skill"
    if any(k in clean for k in ["lakehouse", "data platform", "plataforma de datos", "dbt", "bigquery", "medallion"]):
        return "data-platform"
    if any(k in clean for k in ["dataops", "calidad de datos", "contratos de datos"]):
        return "dataops"
    if any(k in clean for k in ["web app", "web", "frontend", "react", "nextjs", "vite", "ui"]):
        return "web-app"
    if any(k in clean for k in ["llmops", "genai", "rag", "langchain", "llamaindex", "guardrails"]):
        return "llmops"
    if any(k in clean for k in ["mlops", "machine learning", "modelo ml", "model registry"]):
        return "mlops"
    if any(k in clean for k in ["gitops", "kubernetes", "k8s", "helm", "argo"]):
        return "gitops"
    if any(k in clean for k in ["platform eng", "plataforma", "backstage", "developer portal", "iac"]):
        return "platform-eng"
    if any(k in clean for k in ["devsecops", "seguridad", "security", "sast", "sbom"]):
        return "devsecops"
    if any(k in clean for k in ["chaos eng", "caos", "resiliencia", "fault injection"]):
        return "chaos-eng"
    if any(k in clean for k in ["sdd", "spec-driven", "openapi", "swagger", "api first"]):
        return "sdd"
    if any(k in clean for k in ["dual-track", "discovery", "hipotesis"]):
        return "dual-track"
    if any(k in clean for k in ["team topologies", "topologias de equipo"]):
        return "team-topologies"

    return clean


def probe_project(
    target_path: str = ".",
    custom_profiles_dir: Path | None = None
) -> ArchetypeDetectionResult:
    """
    Executes fast, token-economical exploratory probe of target repository.
    Returns detected archetype, confidence score, detected physical signals, and recommended profile.
    """
    return probe_archetype(target_path, custom_profiles_dir=custom_profiles_dir)


def _with_audit_lock(function):
    from functools import wraps
    @wraps(function)
    def wrapped(target_path=".", *args, **kwargs):
        from metricsthinking.runtime import repository_lock
        target = Path(target_path).resolve()
        if not target.is_dir():
            raise FileNotFoundError(f"Target path '{target}' does not exist or is not a directory.")
        with repository_lock(target, "metrics"):
            return function(target_path, *args, **kwargs)
    return wrapped


@_with_audit_lock
def run_audit(
    target_path: str = ".",
    profile_name: str = "default",
    archetype: str | None = None,
    out_dir: str | None = None,
    prefix: str = "MetricsThinking",
    quiet: bool = False,
    prune: bool = False,
    medallion: bool = False,
    reconcile_plans: bool = True,
    full: bool = False,
) -> tuple[ProjectAuditReport, dict[str, Path]]:
    """Executes full 4-phase MetricsThinking™ audit with active plans lifecycle reconciliation."""
    target = Path(target_path).resolve()
    if not target.exists():
        raise FileNotFoundError(f"Target path '{target}' does not exist.")

    # Find profiles directory: check custom profiles in target, config/profiles in target or package root, and global skills
    pkg_dir = Path(__file__).resolve().parent
    repo_root = pkg_dir.parent.parent
    user_global_profiles = Path.home() / ".gemini" / "config" / "skills" / "metrics" / "profiles"
    profiles_candidates = [
        target / ".metricsthinking" / "profiles",
        target / "config" / "profiles",
        repo_root / "config" / "profiles",
        pkg_dir / "profiles",
        user_global_profiles,
    ]
    profiles_dir = None
    for cand in profiles_candidates:
        if cand.exists():
            profiles_dir = cand
            break

    # If archetype is explicitly passed, use it as profile name, resolving aliases and natural language hints
    raw_profile = archetype if archetype else profile_name
    effective_profile = resolve_profile_name(raw_profile)

    out_path = target / "artifacts" / "plans" / "metricsthinking" if not out_dir else Path(out_dir).resolve()

    if not quiet:
        print("[*] Starting MetricsThinking™ Audit v6.0...")
        print(f"    - Target:    {target}")
        print(f"    - Profile:   {effective_profile}")
        print(f"    - Output:    {out_path}")
        print(f"    - Prefix:    {prefix}")

    from metricsthinking.runtime import inventory, digest, read_json, write_json
    if reconcile_plans:
        from metricsthinking.lifecycle import reconcile_active_plans
        reconcile_active_plans(target)
    inv, scan_stats = inventory(target, persist=True, full=full)
    package_root = Path(__file__).parent
    rules_hash = digest({p.relative_to(package_root).as_posix(): digest(p.read_bytes())
                         for p in package_root.rglob("*.py") if "__pycache__" not in p.parts})
    profile_hash = digest({p.name: digest(p.read_bytes()) for p in profiles_dir.glob("*.yaml")}) if profiles_dir else "embedded"
    cache_file = target / ".context/cache/audit_v6.json"
    cache = read_json(cache_file)
    audit_key = digest([inv["inputs_hash"], inv["policy_hash"], rules_hash, profile_hash, effective_profile, prefix])
    if not full and not prune and not medallion and out_dir is None and cache.get("key") == audit_key:
        artifacts = {k: Path(v) for k, v in cache.get("artifacts", {}).items()}
        if artifacts and all(p.is_file() and digest(p.read_bytes()) == cache.get("outputs", {}).get(k) for k, p in artifacts.items()):
            return ProjectAuditReport.model_validate(cache["report"]), artifacts

    # Phase 1: Collect
    collector = ProjectCollector(str(target), persist_cache=True, full=full)
    evidence = collector.collect()
    if not quiet:
        print(f"    - Scanned:   {evidence.total_files} files in repository")

    # Auto-detect archetype from seed/evidence if profile is default/auto
    if (effective_profile in ["default", "auto"]):
        if evidence.detected_archetype:
            detected = resolve_profile_name(evidence.detected_archetype)
            profile_found = False
            for cand in profiles_candidates:
                if cand.exists() and ((cand / f"{detected}.yaml").exists() or (cand / f"{detected}.yml").exists()):
                    effective_profile = detected
                    profiles_dir = cand
                    profile_found = True
                    break
            if not profile_found and detected == "custom":
                effective_profile = "default"

            if not quiet:
                print(f"    - Auto-detected Profile from Repository/Seed: {effective_profile}")

    # Phase 2: Evaluate
    evaluator = CriteriaEvaluator.load_profile(effective_profile, profiles_dir)
    criteria_path = target / ".context/cache/criteria_v6.json"
    criteria_cache = {} if full else read_json(criteria_path)
    modules = evaluator.evaluate(evidence, cache=criteria_cache)
    write_json(criteria_path, criteria_cache)

    # Phase 3: Score
    scorer = AuditScorer(
        modules,
        evidence,
        profile_name=effective_profile,
        profile_data=evaluator.profile
    )
    report = scorer.score()

    # Phase 4: Render & Write
    renderer = ReportRenderer(report)
    artifacts = renderer.write_artifacts(out_path, filename_prefix=prefix)

    if prune and report.pruning_plan:
        from metricsthinking.fpai.compensation import apply_pruning_plan
        prune_res = apply_pruning_plan(report.pruning_plan, repo_root=str(target), update_agentignore=True)
        if not quiet:
            print(f"[+] Reversible context pruning applied: {prune_res['files_pruned_count']} files updated in .agentignore.")

    if medallion:
        from metricsthinking.fpai.medallion import run_local_medallion_pipeline
        raw_t = target / "data" / "raw" / "telemetry"
        proc_t = target / "data" / "processed" / "telemetry"
        med_res = run_local_medallion_pipeline(str(raw_t), str(proc_t))
        if not quiet:
            print(f"[+] Local Medallion pipeline completed: {med_res['silver_records_total']} Silver records, {med_res['duplicates_dropped']} duplicates dropped.")

    if not quiet:
        print("\n" + "=" * 75)
        print(f"  METRICSTHINKING™ AUDIT RESULTS: {report.project_name.upper()}")
        print(f"  Archetype: {report.domain_archetype.value} | Mode: {report.inspection_mode.value}")
        print("=" * 75)
        print(f"  Consolidated Score: {report.consolidated_score:.2f}% / 100.0%")
        print(f"  Maturity Band:      {report.maturity_band.value}")
        print(f"  Active Bottleneck:  {report.active_bottleneck}")
        print("-" * 75)
        print(f"  {'ID':<5} {'Módulo':<40} {'Peso':<8} {'% Fase':<10} {'Estado':<10}")
        print("-" * 75)
        for m in report.modules:
            pct_str = f"{m.phase_completion_pct:.1f}%"
            weight_str = f"{m.weight*100:.0f}%"
            print(f"  {m.module_id:<5} {m.name[:38]:<40} {weight_str:<8} {pct_str:<10} {m.status.value:<10}")
        print("=" * 75)
        print("[+] Artifacts written successfully (artifacts/plans/metricsthinking/):")
        print(f"    - Executive Report: {artifacts['markdown']}")
        print(f"    - Audit Telemetry:  {artifacts['json']}")
        print(f"    - Inferred Roadmap: {artifacts['roadmap']}")
        if "pruning" in artifacts:
            print(f"    - Pruning Plan:     {artifacts['pruning']}")

    # Phase 5: Reconcile Active Plans Lifecycle & Clean residual artifacts (v5.0)
    if reconcile_plans:
        from metricsthinking.lifecycle import reconcile_active_plans
        lifecycle_res = reconcile_active_plans(target)
        if not quiet and (lifecycle_res["archived_plans"] or lifecycle_res["cleaned_artifacts"] or lifecycle_res["backlog_items_updated"]):
            print("-" * 75)
            print("[+] Active Plans Lifecycle Reconciled (iDirectory v5.0):")
            if lifecycle_res["archived_plans"]:
                print(f"    - Plans archived to archive/: {len(lifecycle_res['archived_plans'])}")
                for ap in lifecycle_res["archived_plans"]:
                    print(f"      • {ap['file']} ({ap['reason']})")
            if lifecycle_res["cleaned_artifacts"]:
                print(f"    - Cleaned from active/:        {', '.join(lifecycle_res['cleaned_artifacts'])}")
            if lifecycle_res["backlog_items_updated"]:
                print(f"    - Backlog items marked 'done': {lifecycle_res['backlog_items_updated']}")

    write_json(cache_file, {"key": audit_key, "report": report.model_dump(mode="json"),
                           "artifacts": {k: str(v) for k, v in artifacts.items()},
                           "outputs": {k: digest(v.read_bytes()) for k, v in artifacts.items()}})
    return report, artifacts

