---
name: metrics
description: "Audita con evidencia física, poda heredada y caché incremental en MetricsThinking v6. Usar /metrics en Antigravity o $metrics en Codex."
metadata:
  version: "6.0.0"
---

# metrics: iContext v6

Resolve this bundle from its SKILL.md location. Execute commands below as `python <bundle>/scripts/run.py <command>` using the available interpreter; resolve scripts and references from the bundle, never the target project.

Respect user scope and read-only constraints. Never traverse an ancestor with crawl:false, expose secrets or preload a full seed for scoped work. Honor .context/toolchain.json. Antigravity uses /metrics; Codex uses $metrics.

1. Run `metrics --target <project> --json`. Use --full for an explicitly requested complete recomputation. It works without a seed, README, iDirectory checkout or existing bus.
2. The runtime publishes the four artifacts under artifacts/plans/metricsthinking. Read only their summary and affected modules when reporting results.
3. Distinguish evidence presence, estimated token indicators, exact content duplication, unmeasured distortion and actual executed tests. Never infer functional correctness or model attention from a maturity score or FPAI.
4. Preserve source and user plans. Do not author SeedMaster or README as part of a standalone metrics request. Whole-federation orchestration is a separate explicit request.
