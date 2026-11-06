---
name: idir
description: "Gobierna topología y contexto focalizado con iDirectory v6. Usar /idir en Antigravity o $idir en Codex."
metadata:
  version: "6.0.0"
---

# idir: iContext v6

Resolve this bundle from its SKILL.md location. Execute commands below as `python <bundle>/scripts/run.py <command>` using the available interpreter; resolve scripts and references from the bundle, never the target project.

Respect user scope and read-only constraints. Never traverse an ancestor with crawl:false, expose secrets or preload a full seed for scoped work. Honor .context/toolchain.json. Antigravity uses /idir; Codex uses $idir.

1. Start with `pack <directory> --json`; use --expand only when more evidence is needed. Recorded generations do not certify live freshness.
2. For AST evidence run `index --target <project> --json`; --full verifies content even if timestamps were restored. This does not require ContextControl or another checkout.
3. After topology or beacon changes run the project's `python FWengine.py reconcile` once. Preserve local enrichment; checks use --check.
4. Keep an identified checkpoint for a long task. Finish the requested iDirectory operation; coordinate other products with sync only when requested.
