---
name: readme
description: "Actualiza README bilingüe preservando el contenido del proyecto y métricas con evidencia, iReadme v6. Usar /readme en Antigravity o $readme en Codex."
metadata:
  version: "6.0.0"
---

# readme: iContext v6

Resolve this bundle from its SKILL.md location. Execute commands below as `python <bundle>/scripts/run.py <command>` using the available interpreter; resolve scripts and references from the bundle, never the target project.

Respect user scope and read-only constraints. Never traverse an ancestor with crawl:false, expose secrets or preload a full seed for scoped work. Honor .context/toolchain.json. Antigravity uses /readme; Codex uses $readme.

1. Run `prepare readme --target <project> --json`. Read changed evidence and affected existing sections; there is no mandatory dependency on another product or bus.
2. The current agent writes project-specific English README.md and Spanish README_ES.md, preserving unaffected sections. Keep eight ordered sections, relative language links, ASCII topology, justified mathematical notation and actual engineering references.
3. Use only supported measurements. Missing or stale evidence is unknown. Never invent latency, memory, ROI or verification claims. Automatic rendering may change only its explicitly managed telemetry block.
4. Run `complete readme --target <project> --input-hash <returned-hash> --json`; prepare again if inputs changed. Golden references require an explicit acceptance operation; preserve authored content. Finish documentation without invoking other products unless requested.
