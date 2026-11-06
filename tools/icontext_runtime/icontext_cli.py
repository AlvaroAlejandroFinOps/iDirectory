"""iContext v6 CLI. Semantic changes are completed by the current host agent."""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import sys
from pathlib import Path

from context_runtime import (VERSION, atomic_write, bounded, contracts_index, digest, input_hash,
                             inventory, publish_layer, read_json, repository_lock,
                             validate_readmes, validate_seed, write_json, query_orientation, _context_budget)

PROJECTS = ("iDirectory", "ThinkingSeed", "MetricsThinking", "iReadme")


def ecosystem_root(value=None):
    if value:
        return Path(value).resolve()
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "iDirectory").is_dir():
            return parent
    registered = read_json(Path.home() / ".icontext/registry.json").get("ecosystem_root")
    if registered:
        return Path(registered)
    return Path.cwd().resolve().parent


def outputs(root, layer):
    if layer == "seed":
        return sorted((root / "01_seed").glob("seed-*-master.md")) if (root / "01_seed").is_dir() else []
    if layer == "hybrid":
        return sorted(p for p in (root / "01_seed").glob("seed-*.md") if not p.name.endswith("-master.md")) if (root / "01_seed").is_dir() else []
    if layer == "readme":
        return [root / "README.md", root / "README_ES.md"]
    return [root / "artifacts/plans/metricsthinking" / name for name in
            ("MetricsThinking.json", "MetricsThinking.md", "INFERRED_ROADMAP.md", "CONTEXT_PRUNING_PLAN.json")]


def output_hash(root, layer):
    return digest({p.relative_to(root).as_posix(): digest(p.read_bytes()) if p.is_file() else None
                   for p in outputs(root, layer)})


def layer_hash(inv, layer, root):
    base = input_hash(inv, "seed" if layer == "hybrid" else layer)
    if layer == "metrics":
        # A consumer's evidence may be unchanged after its audit runtime upgrades.
        directory = Path(__file__).resolve().parent
        release = read_json(directory / "release_manifest.json")
        rules = {k: v for k, v in release.get("files", {}).items() if k.startswith("metricsthinking/")}
        if not rules:  # Installed wheels contain package resources, not the outer manifest.
            package = directory / "metricsthinking"
            rules = {p.relative_to(package).as_posix(): digest(p.read_bytes())
                     for p in package.rglob("*") if p.is_file() and p.suffix in {".py", ".yaml"}}
        return digest([base, VERSION, rules])
    if layer == "readme":
        return digest([base, output_hash(root, "metrics"), read_json(root / ".context/benchmark_v6.json")])
    return base


def plan(root, full=False):
    inv, delta = inventory(root, full=full)
    state = read_json(root / ".context/sync_state.json")
    layers = {}
    for layer in ("seed", "metrics", "readme"):
        previous = state.get(layer, {})
        fingerprint = layer_hash(inv, layer, root)
        exists = bool(outputs(root, layer)) and all(p.is_file() for p in outputs(root, layer))
        current = (previous.get("input_hash") == fingerprint and exists
                   and previous.get("output_hash") == output_hash(root, layer))
        layers[layer] = {"state": "current" if current else "pending", "input_hash": fingerprint}
    return {"version": VERSION, "project": root.name, "delta": delta, "layers": layers}, inv


def status(root):
    """Recorded status; never scan, mutate, or pretend to verify live freshness."""
    return {"version": VERSION, "project": root.name, "freshness": "recorded; use audit to verify",
            "layers": read_json(root / ".context/icontext_bus.json").get("layers", {}),
            "pending": read_json(root / ".context/update_request.json").get("requests", []),
            "toolchain": read_json(root / ".context/toolchain.json")}


def audit(root, full=False):
    result, inv = plan(root, full)
    errors = [f"{path}: {record['parse_error']}" for path, record in inv["files"].items() if record.get("parse_error")]
    for seed in outputs(root, "seed"):
        errors.extend(validate_seed(seed))
    if not outputs(root, "seed"):
        errors.append("SeedMaster missing")
    errors.extend(validate_readmes(root))
    bus = read_json(root / ".context/icontext_bus.json")
    if bus.get("protocol_version") != VERSION:
        errors.append("Missing or unsupported v6 federation bus")
    for short, name in (("l0", "l0_idirectory"), ("l1", "l1_thinkingseed"),
                        ("l2", "l2_metricsthinking"), ("l3", "l3_ireadme")):
        record = read_json(root / ".context/layers" / (name + ".json"))
        if not record or record != bus.get("layers", {}).get(name):
            errors.append(name + ": missing producer state or aggregate mismatch")
        elif record.get("state") not in {"recorded", "validated"}:
            errors.append(name + ": state is not verified evidence")
        if short == "l0" and record.get("inputs_hash") != inv["inputs_hash"]:
            errors.append("L0 inventory is stale")
    if any(v["state"] != "current" for v in result["layers"].values()):
        errors.append("Layers are pending or stale; run sync")
    result["errors"] = errors
    result["state"] = "invalid" if errors else "valid"
    return result


def request(root, layer, inv, fingerprint, delta):
    changed = sorted(set(delta["added"] + delta["modified"] + delta["removed"]))
    # Include contract differences since the last accepted semantic update.
    prior = read_json(root / ".context/sync_state.json").get(layer, {}).get("files", {})
    changed = sorted(set(changed) | {k for k, v in inv["files"].items() if prior.get(k) != v["sha256"]}
                     | (set(prior) - set(inv["files"])))
    return {"layer": layer, "input_hash": fingerprint,
            "changed_files": changed, "sections": ["2", "3", "4", "7", "9"] if layer in {"seed", "hybrid"} else ["2", "4", "5", "6"],
            "contract_files": [k for k in changed if k in inv["files"] and "contracts" in inv["files"][k]],
            "instruction": "Current agent: inspect changed evidence, update affected sections only, preserve other content, then run complete with this input hash."}


def complete(root, layer, expected):
    inv, _ = inventory(root)
    actual = layer_hash(inv, layer, root)
    if expected != actual:
        raise ValueError("Inputs changed during redaction; run sync again before completing")
    errors = []
    if layer in {"seed", "hybrid"}:
        seeds = outputs(root, layer)
        if not seeds:
            errors.append("Requested architectural vector missing")
        for seed in seeds:
            index = {"modules": {k: v["contracts"] for k, v in inv["files"].items() if "contracts" in v}}
            errors.extend(validate_seed(seed, index if layer == "seed" else None))
    else:
        errors.extend(validate_readmes(root))
    if errors:
        raise ValueError("; ".join(errors))
    with repository_lock(root, "sync"):
        state = read_json(root / ".context/sync_state.json")
        state[layer] = {"input_hash": actual, "output_hash": output_hash(root, layer),
                        "files": {k: v["sha256"] for k, v in inv["files"].items()}}
        write_json(root / ".context/sync_state.json", state)
        publish_layer(root, "l1" if layer in {"seed", "hybrid"} else "l3",
                      {"present": True, "state": "validated", "inputs_hash": actual,
                       "artifact_kind": "hybrid" if layer == "hybrid" else ("master" if layer == "seed" else "readme"),
                       "output_hash": state[layer]["output_hash"]})
        pending = read_json(root / ".context/update_request.json")
        if pending:
            pending["requests"] = [r for r in pending.get("requests", []) if r["layer"] != layer]
            write_json(root / ".context/update_request.json", pending)
    return {"layer": layer, "state": "validated", "input_hash": actual}


def metrics(root, eco, full=False, profile="default"):
    candidate = eco / "MetricsThinking" / "src"
    if candidate.is_dir():
        sys.path.insert(0, str(candidate))
    from metricsthinking.engine import run_audit
    with contextlib.redirect_stdout(io.StringIO()):
        run_audit(str(root), quiet=True, reconcile_plans=False, full=full, profile_name=profile)
    report = read_json(root / "artifacts/plans/metricsthinking/MetricsThinking.json")
    if not report:
        raise RuntimeError("Metrics produced no valid report")
    fpai = report.get("fpai") or {}
    security = report.get("security") or {}
    publish_layer(root, "l2", {"present": True, "state": "validated",
                              "inputs_hash": read_json(root / ".context/inventory.json").get("inputs_hash"),
                              "evaluation_hash": read_json(root / ".context/cache/audit_v6.json").get("key"),
                              "consolidated_score": report.get("consolidated_score"),
                              "fpai_pf_spectral": fpai.get("power_factor_spectral"),
                              "fpai_s_spectral": fpai.get("s_spectral"),
                              "security_gate": (1.0 if security["pii_matches_count"] == 0 else 0.0) if "pii_matches_count" in security else None,
                              "security_gate_basis": "pii_scan_only",
                              "report_path": "artifacts/plans/metricsthinking/MetricsThinking.json",
                              "output_hash": output_hash(root, "metrics")})
    return {"profile": report.get("profile_used"), "consolidated_score": report.get("consolidated_score"),
            "artifacts": [p.relative_to(root).as_posix() for p in outputs(root, "metrics")]}


def sync(root, eco, dry_run=False, full=False):
    if dry_run:
        result, _ = plan(root, full)
        result["dry_run"] = True
        return result, 0
    with repository_lock(root, "sync"):
        result, inv = plan(root, full)
        parse_errors = {path: record["parse_error"] for path, record in inv["files"].items() if record.get("parse_error")}
        if parse_errors:
            result.update(state="failed", errors=parse_errors)
            for value in result["layers"].values():
                value["state"] = "blocked_by_evidence"
            publish_layer(root, "l0", {"present": True, "state": "invalid", "errors": parse_errors})
            return result, 1
        # Persist once, then reuse the same records for contracts.
        write_json(root / ".context/inventory.json", inv)
        index, _ = contracts_index(root, persist=True)
        import fwengine
        fwengine._compile_context_packs(root, inv)
        publish_layer(root, "l0", {"present": True, "state": "recorded", "inputs_hash": inv["inputs_hash"],
                                  "contracts_ast_hash": index["contracts_ast_hash"]})
        state = read_json(root / ".context/sync_state.json")
        requests = []
        if result["layers"]["seed"]["state"] != "current":
            requests.append(request(root, "seed", inv, layer_hash(inv, "seed", root), result["delta"]))
            result["layers"]["metrics"]["state"] = "blocked_by_seed"
            result["layers"]["readme"]["state"] = "blocked_by_seed"
        else:
            if result["layers"]["metrics"]["state"] != "current":
                try:
                    metrics(root, eco, full=full)
                except Exception as exc:
                    result["layers"]["metrics"].update(state="failed", error=str(exc))
                    result["layers"]["readme"]["state"] = "blocked_by_metrics"
                    return result, 1
                state["metrics"] = {"input_hash": layer_hash(inv, "metrics", root), "output_hash": output_hash(root, "metrics")}
                write_json(root / ".context/sync_state.json", state)
                result["layers"]["metrics"]["state"] = "updated"
            readme_fp = layer_hash(inv, "readme", root)
            result["layers"]["readme"]["input_hash"] = readme_fp
            previous = state.get("readme", {})
            if previous.get("input_hash") != readme_fp or previous.get("output_hash") != output_hash(root, "readme"):
                requests.append(request(root, "readme", inv, readme_fp, result["delta"]))
                result["layers"]["readme"]["state"] = "pending"
        write_json(root / ".context/update_request.json", {"version": VERSION, "requests": requests})
        result["requests"] = requests
        result["state"] = "pending_agent" if requests else "current"
        return result, 3 if requests else 0


def pack(root, path=".", tier="1a", expand=False, task=""):
    if tier == "2":
        import fwengine
        return fwengine.build_ecosystem_pack(root, expand=expand)
    # Bound after adding task information so the complete payload fits.
    payload = query_orientation(root, path, tier=tier, expand=True)
    if payload is None:
        import fwengine
        payload = fwengine.build_context_pack(root, path, tier=tier, expand=True)
    if task:
        payload["objective"] = task[:160]
    if expand:
        payload["contracts_ast"] = [s for k, m in read_json(root / ".context/contracts_ast.json").get("modules", {}).items()
                                    if path == "." or k.startswith(path.rstrip("/") + "/") for s in m.get("signatures", [])]
        return payload
    return bounded(payload, _context_budget(root, tier))


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(prog="icontext", description="iContext v6 incremental context engineering")
    sub = parser.add_subparsers(dest="command")
    for name, aliases in (("status", []), ("pack", ["capsule"]), ("sync", ["reconcile", "update"]),
                          ("audit", []), ("doctor", ["fix"]), ("complete", []), ("prepare", []),
                          ("metrics", []), ("index", []), ("checkpoint", []), ("init", []), ("install", []), ("benchmark", [])):
        child = sub.add_parser(name, aliases=aliases)
        child.add_argument("--target", default=None)
        child.add_argument("--root", default=None)
        child.add_argument("--all", action="store_true")
        child.add_argument("--json", action="store_true")
        child.add_argument("--verbose", "-v", action="store_true")
        if name in {"sync", "install"}:
            child.add_argument("--dry-run", action="store_true")
        if name in {"sync", "audit", "metrics", "index"}:
            child.add_argument("--full", action="store_true")
        if name == "metrics":
            child.add_argument("--profile", default="default")
        if name == "pack":
            child.add_argument("path", nargs="?", default=".")
            child.add_argument("--tier", choices=["1a", "1b", "2"], default="1a")
            child.add_argument("--task", default="")
            child.add_argument("--expand", action="store_true")
        if name == "init":
            child.add_argument("path", nargs="?", default=".")
        if name == "doctor":
            child.add_argument("--fix", action="store_true")
        if name == "complete":
            child.add_argument("layer", choices=["seed", "hybrid", "readme"])
            child.add_argument("--input-hash", required=True)
        if name == "prepare":
            child.add_argument("layer", choices=["seed", "hybrid", "readme"])
        if name == "checkpoint":
            child.add_argument("--expand", action="store_true")
            child.add_argument("--session-id")
            child.add_argument("--objective")
            child.add_argument("--constraint", action="append", dest="constraints")
            child.add_argument("--decision", action="append", dest="decisions")
            child.add_argument("--next", dest="next_action")
            child.add_argument("--set", action="store_true")
            child.add_argument("--show", action="store_true")
            child.add_argument("--evidence-hash")
        if name == "install":
            child.add_argument("--agents", default="antigravity,codex")
            child.add_argument("--home", default=None)
            child.add_argument("--local", action="store_true")
    # Legacy global flags before subcommand are normalized to subcommand options.
    argv = list(sys.argv[1:] if argv is None else argv)
    commands = set(sub.choices)
    command_index = next((i for i, arg in enumerate(argv) if arg in commands), None)
    if command_index:
        argv = argv[command_index:] + argv[:command_index]
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 0
    eco = ecosystem_root(args.root)
    target = Path(args.target or Path.cwd()).resolve()
    if args.command in {"pack", "capsule"}:
        target_path = ((Path(args.target) / args.path) if args.target else Path(args.path)).resolve()
        root = target_path
        while root != root.parent and not ((root / ".context").is_dir() or (root / ".git").exists()
                or (root / "pyproject.toml").is_file()
                or ((root / "FWengine.py").is_file() and (root / "tools/icontext_runtime/release_manifest.json").is_file())):
            root = root.parent
        if root == root.parent:
            root = target_path
        relative = target_path.relative_to(root).as_posix()
        if target_path.is_file():
            relative = target_path.parent.relative_to(root).as_posix()
        try:
            if args.command == "capsule":
                import fwengine
                payload = fwengine.build_context_capsule(root, relative, args.task)
            else:
                payload = pack(root, relative, args.tier, args.expand, args.task)
            print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
            return 0
        except (OSError, ValueError) as exc:
            print(json.dumps({"error": str(exc)}))
            return 1
    roots = [eco / p for p in PROJECTS] if args.all else [target]
    results, code = [], 0
    for root in roots:
        if not root.is_dir():
            results.append({"project": root.name, "state": "failed", "error": "Target directory missing"})
            code = 1
            continue
        try:
            if args.command == "status":
                result = status(root)
            elif args.command == "init":
                import fwengine
                with contextlib.redirect_stdout(io.StringIO()):
                    fwengine.init_project(str(Path(args.target or args.path).resolve()))
                result = {"project": root.name, "state": "initialized"}
            elif args.command in {"sync", "reconcile", "update"}:
                result, rc = sync(root, eco, args.dry_run, args.full)
                code = 1 if code == 1 or rc == 1 else max(code, rc)
            elif args.command == "complete":
                result = complete(root, args.layer, args.input_hash)
            elif args.command == "prepare":
                inv, delta = inventory(root)
                result = request(root, args.layer, inv, layer_hash(inv, args.layer, root), delta)
            elif args.command == "metrics":
                summary = metrics(root, eco, full=args.full, profile=args.profile)
                result = {"project": root.name, "state": "updated", **summary}
            elif args.command == "checkpoint":
                import fwengine
                result = fwengine.manage_checkpoint(root, action="set" if args.set else "show",
                         session_id=args.session_id, objective=args.objective, constraints=args.constraints,
                         decisions=args.decisions, next_action=args.next_action, evidence_hash=args.evidence_hash)
                if not args.expand:
                    result = fwengine._checkpoint_display(result)
            elif args.command == "index":
                idx, delta = contracts_index(root, persist=True, full=args.full)
                import fwengine
                fwengine._compile_context_packs(root, read_json(root / ".context/inventory.json"))
                publish_layer(root, "l0", {"present": True, "state": "recorded", "inputs_hash": idx["inputs_hash"],
                                          "contracts_ast_hash": idx["contracts_ast_hash"]})
                result = {"project": root.name, "state": "indexed", "delta": delta}
            elif args.command == "install":
                from skill_installer import install
                result = install(eco, args.agents.split(","), Path(args.home).resolve() if args.home else Path.home(),
                                 local=root if args.local else None, dry_run=args.dry_run)
            elif args.command == "benchmark":
                from benchmark import benchmark
                result = benchmark(root)
            elif args.command in {"doctor", "fix"}:
                from skill_installer import inspect_installation
                result = inspect_installation(eco, Path.home())
                if args.command == "fix" or args.fix:
                    from skill_installer import install
                    result = install(eco, ["antigravity", "codex"], Path.home())
                    import fwengine
                    with contextlib.redirect_stdout(io.StringIO()):
                        repaired = fwengine.reconcile_repository(root)
                    result["topology_repaired"] = repaired
                    if not repaired:
                        result["state"] = "failed"
                        code = 1
                elif result.get("errors"):
                    code = 1
                if not (args.command == "fix" or args.fix):
                    result["repository"] = audit(root)
                    if result["repository"]["errors"]:
                        result["state"] = "invalid"
                        code = 1
            else:
                result = audit(root, args.full)
                if result["errors"]:
                    code = 1
        except Exception as exc:
            result = {"project": root.name, "state": "failed", "error": str(exc)}
            code = 1
        results.append(result)
    if args.command == "checkpoint" and not args.expand:
        print(json.dumps(results[0], ensure_ascii=False, separators=(",", ":")))
    elif args.json:
        print(json.dumps(results if args.all else results[0], ensure_ascii=False, indent=2))
    else:
        for result in results:
            print(f"{result.get('project', target.name)}: {result.get('state', 'recorded')}")
            if "consolidated_score" in result:
                print(f"  profile: {result.get('profile')}; score: {result['consolidated_score']}")
            for layer, value in result.get("layers", {}).items():
                print(f"  {layer}: {value.get('state', 'recorded')}")
            for entry in result.get("requests", []):
                print(f"  Agent redaction pending: {entry['layer']} ({len(entry['changed_files'])} changed files); use --json")
            if result.get("error"):
                print(result["error"], file=sys.stderr)
            if args.verbose:
                print(json.dumps(result, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
