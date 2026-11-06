"""
CLI Interface for MetricsThinking™.
Command-line auditor, forensic reporter, MCP server, and AI skill installer.
"""

import argparse
import sys
from pathlib import Path

import yaml

# Ensure local directory is in sys.path for standalone script execution
_PKG_DIR = Path(__file__).resolve().parent
if str(_PKG_DIR) not in sys.path:
    sys.path.insert(0, str(_PKG_DIR))

try:
    from metricsthinking.engine import run_audit
except (ImportError, ValueError):
    try:
        from .engine import run_audit
    except (ImportError, ValueError):
        from engine import run_audit


def list_available_profiles() -> None:
    """Lists all available evaluation profiles with descriptions."""
    pkg_dir = Path(__file__).resolve().parent
    repo_root = pkg_dir.parent.parent
    profiles_dir = None
    for cand in [repo_root / "config" / "profiles", Path.cwd() / "config" / "profiles", pkg_dir / "profiles"]:
        if cand.exists():
            profiles_dir = cand
            break

    print("\n" + "=" * 75)
    print("  METRICSTHINKING™ v4.0 UNIVERSAL PROFILES & ARCHETYPES")
    print("=" * 75)

    if not profiles_dir or not profiles_dir.exists():
        print("  No profiles directory found.")
        return

    for p_file in sorted(profiles_dir.glob("*.yaml")):
        try:
            with open(p_file, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            p_name = data.get("name", p_file.stem)
            p_desc = data.get("description", "No description provided.")
            p_arch = data.get("domain_archetype", "generic")
            p_mode = data.get("inspection_mode", "source_code")
            print(f"  • {p_name:<18} [{p_arch}] ({p_mode})")
            print(f"    {p_desc}")
            print()
        except Exception:
            pass
    print("=" * 75)


def main():
    parser = argparse.ArgumentParser(
        prog="metricsthinking",
        description="MetricsThinking™ v4.0: Universal Project Evaluation Engine & Multi-Provider AI Skill"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # 1. audit subcommand
    audit_parser = subparsers.add_parser("audit", help="Run forensic audit on a repository")
    audit_parser.add_argument("--target", "-t", default=".", help="Path to project repository to audit")
    audit_parser.add_argument("--profile", "-p", default="default", help="Profile name (e.g. default, agent-skill, data-platform, web-app, mlops, llmops, dataops, gitops, platform-eng, devsecops, dual-track, team-topologies, chaos-eng, sdd)")
    audit_parser.add_argument("--archetype", "-a", default=None, help="Engineering archetype override (e.g. agent-skill, data-platform, etc.)")
    audit_parser.add_argument("--hint", default=None, help="Natural language hint or context for evaluation (e.g. 'evalua como una skill para IA')")
    audit_parser.add_argument("--out-dir", "-o", default=None, help="Output directory for generated artifacts")
    audit_parser.add_argument("--prefix", default="MetricsThinking", help="Filename prefix for generated artifacts")
    audit_parser.add_argument("--quiet", "-q", action="store_true", help="Suppress console summary table")
    audit_parser.add_argument("--list-profiles", action="store_true", help="List all available profiles and exit")
    audit_parser.add_argument("--prune", action="store_true", help="Apply reversible context pruning via .agentignore")
    audit_parser.add_argument("--medallion", action="store_true", help="Run local Bronze -> Silver -> Gold telemetry pipeline")
    audit_parser.add_argument("--no-reconcile-plans", action="store_true", help="Disable automatic reconciliation and archiving of active plans")

    # 2. install-skill subcommand
    install_parser = subparsers.add_parser("install-skill", help="Install MetricsThinking™ skill for AI assistants")
    install_parser.add_argument(
        "--target", "-t",
        choices=["all", "antigravity", "codex", "claude", "cursor", "copilot", "mcp"],
        default="all",
        help="Target AI assistant / platform (default: all)"
    )
    install_parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Install skill for all supported AI providers (alias for --target all)"
    )
    install_parser.add_argument(
        "--dest", "-d",
        default=".",
        help="Destination directory (default: current directory)"
    )
    install_parser.add_argument(
        "--global", "-g",
        dest="is_global",
        action="store_true",
        help="Install globally into user profile (Google Antigravity global config)"
    )
    install_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing files"
    )

    # 3. mcp subcommand
    mcp_parser = subparsers.add_parser("mcp", help="Start Model Context Protocol (MCP) JSON-RPC stdio server")

    audit_parser.add_argument("--full", action="store_true", help="Recompute evidence and all criteria")

    # 4. prune subcommand
    prune_parser = subparsers.add_parser("prune", help="Generate or apply reversible context pruning plan")
    prune_parser.add_argument("--target", "-t", default=".", help="Path to project repository")
    prune_parser.add_argument("--apply", action="store_true", help="Apply pruning plan to .agentignore")

    # 5. medallion subcommand
    medallion_parser = subparsers.add_parser("medallion", help="Process local Bronze -> Silver -> Gold telemetry")
    medallion_parser.add_argument("--raw-dir", default="data/raw/telemetry", help="Bronze telemetry directory")
    medallion_parser.add_argument("--processed-dir", default="data/processed/telemetry", help="Silver/Gold directory")

    # 6. list-profiles subcommand
    subparsers.add_parser("list-profiles", help="List all available evaluation profiles and archetypes")

    # 7. probe subcommand (Pre-Flight Exploratory Analysis)
    probe_parser = subparsers.add_parser("probe", help="Run lightweight exploratory probe to detect project archetype and optimal profile")
    probe_parser.add_argument("--target", "-t", default=".", help="Path to project repository")
    probe_parser.add_argument("--json", action="store_true", help="Output result as JSON for agent/tool consumption")

    # Default fallback options on root parser for backwards compatibility
    parser.add_argument("--target", "-t", default=".", help="Path to project repository to audit")
    parser.add_argument("--profile", "-p", default="default", help="Profile name")
    parser.add_argument("--archetype", "-a", default=None, help="Engineering archetype override")
    parser.add_argument("--out-dir", "-o", default=None, help="Output directory for generated artifacts")
    parser.add_argument("--prefix", default="MetricsThinking", help="Filename prefix for generated artifacts")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress console summary table")
    parser.add_argument("--list-profiles", action="store_true", help="List all available profiles and exit")
    parser.add_argument("--probe", action="store_true", help="Run exploratory probe and exit")

    args = parser.parse_args()

    try:
        if getattr(args, "list_profiles", False) or args.command == "list-profiles":
            list_available_profiles()
            return

        if args.command == "install-skill":
            target_provider = "all" if getattr(args, "all", False) else args.target
            script_installer = Path(__file__).resolve().parent.parent.parent / "scripts" / "install_skill.py"
            if not script_installer.exists():
                script_installer = Path.cwd() / "scripts" / "install_skill.py"
            if script_installer.exists():
                import importlib.util
                spec = importlib.util.spec_from_file_location("installer", script_installer)
                installer_mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(installer_mod)
                installer_mod.run_installer(
                    target=target_provider,
                    dest=args.dest,
                    is_global=args.is_global,
                    dry_run=args.dry_run
                )
            else:
                try:
                    import scripts.install_skill as installer_mod
                    installer_mod.run_installer(
                        target=target_provider,
                        dest=args.dest,
                        is_global=args.is_global,
                        dry_run=args.dry_run
                    )
                except ImportError:
                    print("[ERROR] Installer script not found.", file=sys.stderr)
                    sys.exit(1)

        elif args.command == "mcp":
            from .mcp_server import run_mcp_server
            run_mcp_server()

        elif args.command == "prune":
            from .fpai.compensation import apply_pruning_plan
            report, _ = run_audit(target_path=args.target, quiet=True)
            if report.pruning_plan:
                if args.apply:
                    res = apply_pruning_plan(report.pruning_plan, repo_root=args.target, update_agentignore=True)
                    print(f"[+] Pruning applied: {res['files_pruned_count']} files updated in .agentignore ({res['tokens_recovered']} tokens recovered).")
                else:
                    print(f"[*] Pruning plan generated for {args.target}:")
                    print(f"    - Items to prune: {len(report.pruning_plan.items)}")
                    print(f"    - Estimated tokens to recover: {report.pruning_plan.total_tokens_recovered}")
                    print("    - Use --apply to update .agentignore safely.")

        elif args.command == "medallion":
            from .fpai.medallion import run_local_medallion_pipeline
            res = run_local_medallion_pipeline(args.raw_dir, args.processed_dir)
            print(f"[+] Medallion pipeline completed:")
            print(f"    - Raw events read: {res['raw_read']}")
            print(f"    - Silver records total: {res['silver_records_total']}")
            print(f"    - Duplicates dropped: {res['duplicates_dropped']}")
            print(f"    - Average FPAI Spectral: {res['gold_kpis'].get('average_fpai_spectral', 1.0):.4f}")

        elif args.command == "probe" or getattr(args, "probe", False):
            from .detector import probe_archetype
            res = probe_archetype(args.target)
            if getattr(args, "json", False):
                import json
                print(json.dumps(res.to_dict(), indent=2, ensure_ascii=False))
            else:
                print("\n" + "=" * 75)
                print("  METRICSTHINKING™ PRE-FLIGHT ARCHETYPE PROBE (FASE 0)")
                print("=" * 75)
                print(f"  • Primary Archetype:     {res.primary_archetype.upper()}")
                print(f"  • Confidence:            {res.confidence * 100:.1f}%")
                print(f"  • Recommended Profile:   {res.recommended_profile}")
                print(f"  • Inspection Mode:       {res.inspection_mode}")
                if res.is_custom:
                    print("  • Profile Source:        Custom (.metricsthinking / local)")
                if res.is_emerging_domain:
                    print("  • Domain Classification: Emerging / Uncataloged (Adaptive Metamodel applied)")
                print(f"  • Rationale:             {res.rationale}")
                print("-" * 75)
                print("  Physical Signals Detected:")
                for sig in res.detected_signals:
                    print(f"    - {sig}")
                if res.runner_up_archetypes:
                    print("-" * 75)
                    print("  Alternative Candidates:")
                    for arch, conf in res.runner_up_archetypes:
                        print(f"    - {arch:<22} ({conf * 100:.1f}%)")
                print("=" * 75)
                print(f"  Recommended Command: python -m metricsthinking.cli audit --target \"{args.target}\" --profile {res.recommended_profile}")
                print("=" * 75 + "\n")

        else:
            # Default to audit
            selected_profile = getattr(args, "hint", None) or args.profile
            run_audit(
                target_path=args.target,
                profile_name=selected_profile,
                archetype=getattr(args, "archetype", None),
                out_dir=args.out_dir,
                prefix=args.prefix,
                quiet=args.quiet,
                prune=getattr(args, "prune", False),
                medallion=getattr(args, "medallion", False),
                reconcile_plans=not getattr(args, "no_reconcile_plans", False),
                full=getattr(args, "full", False),
            )
    except Exception as e:
        print(f"[ERROR] MetricsThinking command failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
