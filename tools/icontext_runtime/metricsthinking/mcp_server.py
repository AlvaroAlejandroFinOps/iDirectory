"""
Model Context Protocol (MCP) Server for MetricsThinking™ v5.0.
Exposes 6 canonical tools via stdio JSON-RPC for agentic pair-programming.
"""

import json
from pathlib import Path
import sys
from typing import Any

# Ensure local directory is in sys.path
_PKG_DIR = Path(__file__).resolve().parent
if str(_PKG_DIR) not in sys.path:
    sys.path.insert(0, str(_PKG_DIR))

try:
    from metricsthinking.engine import run_audit
    from metricsthinking.fpai.compensation import apply_pruning_plan
except (ImportError, ValueError):
    try:
        from .engine import run_audit
        from .fpai.compensation import apply_pruning_plan
    except (ImportError, ValueError):
        from engine import run_audit
        from fpai.compensation import apply_pruning_plan


TOOLS = [
    {
        "name": "probe_archetype",
        "description": "Execute a lightweight, sub-second exploratory probe (Fase 0) to detect project archetype, confidence score, detected architectural signatures, and recommended evaluation profile.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target repository path", "default": "."}
            }
        }
    },
    {
        "name": "audit_project",
        "description": "Execute a full MetricsThinking™ v5.0 Ground Truth forensic audit on a repository, calculating maturity score (0-100%), FPAI spectral vector, security vulnerability report, systems resilience, and generating synchronized artifacts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Path to target repository to audit", "default": "."},
                "profile": {"type": "string", "description": "Evaluation profile name or archetype", "default": "default"},
                "prune": {"type": "boolean", "description": "Apply context pruning directly to .agentignore", "default": False},
                "medallion": {"type": "boolean", "description": "Process local Bronze -> Silver -> Gold telemetry pipeline", "default": False}
            }
        }
    },
    {
        "name": "get_project_score",
        "description": "Retrieve project maturity score, maturity band, and active bottleneck.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target repository path", "default": "."},
                "profile": {"type": "string", "description": "Profile name", "default": "default"}
            }
        }
    },
    {
        "name": "get_module_evaluation",
        "description": "Retrieve criteria status and details for a specific canonical module (M01 to M10).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "module_id": {"type": "string", "description": "Canonical module ID (M01 to M10)"},
                "target": {"type": "string", "description": "Target repository path", "default": "."}
            },
            "required": ["module_id"]
        }
    },
    {
        "name": "get_spectral_efficiency",
        "description": "Retrieve FPAI spectral context vector (P, Q_dead, Q_dup, D, S_spectral, S_linear, Power Factor, Divergence).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target repository path", "default": "."}
            }
        }
    },
    {
        "name": "generate_pruning_plan",
        "description": "Generate a prioritized, 100% reversible context pruning plan for dead/redundant/distortive context.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target repository path", "default": "."}
            }
        }
    },
    {
        "name": "apply_pruning_plan",
        "description": "Applies a generated context pruning plan to .agentignore using marker boundaries without deleting physical files.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target repository path", "default": "."}
            }
        }
    },
    # Backward compatibility aliases
    {
        "name": "audit_repository",
        "description": "Alias for audit_project.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "default": "."},
                "profile": {"type": "string", "default": "default"},
                "out_dir": {"type": "string"}
            }
        }
    },
    {
        "name": "list_profiles",
        "description": "List all available MetricsThinking™ evaluation profiles.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "get_audit_report",
        "description": "Retrieve the latest MetricsThinking™ JSON report or Markdown summary for a project.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "default": "."},
                "format": {"type": "string", "enum": ["markdown", "json", "roadmap"], "default": "markdown"}
            }
        }
    }
]


def handle_list_tools() -> list[dict[str, Any]]:
    return TOOLS


def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[dict[str, Any]]:
    target = arguments.get("target", ".")
    profile = arguments.get("profile", "default")

    if name == "probe_archetype":
        from .detector import probe_archetype
        res = probe_archetype(target)
        return [{"type": "text", "text": json.dumps(res.to_dict(), indent=2, ensure_ascii=False)}]

    if name in ["audit_project", "audit_repository"]:
        prune = arguments.get("prune", False)
        medallion = arguments.get("medallion", False)
        out_dir = arguments.get("out_dir")

        report, artifacts = run_audit(
            target_path=target,
            profile_name=profile,
            out_dir=out_dir,
            prune=prune,
            medallion=medallion,
            quiet=True
        )

        res_dict = {
            "project_name": report.project_name,
            "consolidated_score": round(report.consolidated_score, 2),
            "maturity_band": report.maturity_band.value,
            "active_bottleneck": report.active_bottleneck,
            "fpai_power_factor_spectral": report.fpai.power_factor_spectral if report.fpai else 1.0,
            "attack_surface_index": report.security.attack_surface_index if report.security else 0.0,
            "artifacts": {k: str(v) for k, v in artifacts.items()},
        }
        return [{"type": "text", "text": json.dumps(res_dict, indent=2)}]

    elif name == "get_project_score":
        report, _ = run_audit(target_path=target, profile_name=profile, quiet=True)
        return [{
            "type": "text",
            "text": json.dumps({
                "project_name": report.project_name,
                "consolidated_score": round(report.consolidated_score, 2),
                "maturity_band": report.maturity_band.value,
                "active_bottleneck": report.active_bottleneck,
            }, indent=2)
        }]

    elif name == "get_module_evaluation":
        mod_id = arguments.get("module_id", "M01").upper()
        report, _ = run_audit(target_path=target, quiet=True)
        mod = next((m for m in report.modules if m.module_id.upper() == mod_id), None)
        if not mod:
            return [{"type": "text", "text": json.dumps({"error": f"Module '{mod_id}' not found."})}]
        return [{
            "type": "text",
            "text": json.dumps({
                "module_id": mod.module_id,
                "name": mod.name,
                "phase_completion_pct": round(mod.phase_completion_pct, 2),
                "weight": mod.weight,
                "status": mod.status.value,
                "criteria": [c.model_dump() for c in mod.criteria]
            }, indent=2)
        }]

    elif name == "get_spectral_efficiency":
        report, _ = run_audit(target_path=target, quiet=True)
        if not report.fpai:
            return [{"type": "text", "text": json.dumps({"error": "FPAI vector not available."})}]
        return [{"type": "text", "text": report.fpai.model_dump_json(indent=2)}]

    elif name == "generate_pruning_plan":
        report, _ = run_audit(target_path=target, quiet=True)
        if not report.pruning_plan:
            return [{"type": "text", "text": json.dumps({"error": "Pruning plan not available."})}]
        return [{"type": "text", "text": report.pruning_plan.model_dump_json(indent=2)}]

    elif name == "apply_pruning_plan":
        report, _ = run_audit(target_path=target, quiet=True)
        if not report.pruning_plan:
            return [{"type": "text", "text": json.dumps({"error": "No pruning plan generated."})}]
        res = apply_pruning_plan(report.pruning_plan, repo_root=target, update_agentignore=True)
        return [{"type": "text", "text": json.dumps(res, indent=2)}]

    elif name == "list_profiles":
        pkg_dir = Path(__file__).resolve().parent
        repo_root = pkg_dir.parent.parent
        profiles_dir = repo_root / "config" / "profiles"
        profiles = ["default", "agent-skill", "data-platform", "web-app"]
        if profiles_dir.exists():
            profiles = [p.stem for p in profiles_dir.glob("*.yaml")]
        return [{"type": "text", "text": json.dumps({"profiles": profiles}, indent=2)}]

    elif name == "get_audit_report":
        tgt_path = Path(target).resolve()
        fmt = arguments.get("format", "markdown")
        mt_dir = tgt_path / "artifacts" / "plans" / "metricsthinking"
        if fmt == "json":
            file_path = mt_dir / "MetricsThinking.json"
            if not file_path.exists():
                file_path = tgt_path / "artifacts" / "MetricsThinking.json"
        elif fmt == "roadmap":
            file_path = mt_dir / "INFERRED_ROADMAP.md"
            if not file_path.exists():
                file_path = tgt_path / "artifacts" / "plans" / "active" / "INFERRED_ROADMAP.md"
        else:
            file_path = mt_dir / "MetricsThinking.md"
            if not file_path.exists():
                file_path = tgt_path / "artifacts" / "MetricsThinking.md"

        if not file_path.exists():
            return [{"type": "text", "text": f"Error: Report file '{file_path}' not found. Run audit_project first."}]
        return [{"type": "text", "text": file_path.read_text(encoding="utf-8")}]

    else:
        raise ValueError(f"Unknown tool: {name}")


def run_mcp_server():
    """Runs the stdio JSON-RPC server loop."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            req_id = request.get("id")
            method = request.get("method")
            params = request.get("params", {})

            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {
                            "name": "metricsthinking-mcp",
                            "version": "6.0.0"
                        },
                        "capabilities": {
                            "tools": {}
                        }
                    }
                }
            elif method == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": handle_list_tools()
                    }
                }
            elif method == "tools/call":
                name = params.get("name")
                arguments = params.get("arguments", {})
                content = handle_call_tool(name, arguments)
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": content
                    }
                }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method '{method}' not found"
                    }
                }

            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    run_mcp_server()
