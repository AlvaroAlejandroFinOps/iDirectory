---
name: seed
description: "Actualiza el snapshot arquitectónico ágil por secciones con ThinkingSeed v6. Usar /seed en Antigravity o $seed en Codex."
metadata:
  version: "6.0.0"
---

# seed: iContext v6

Resolve this bundle from its SKILL.md location. Execute commands below as `python <bundle>/scripts/run.py <command>` using the available interpreter; resolve scripts and references from the bundle, never the target project.

Respect user scope and read-only constraints. Never traverse an ancestor with crawl:false, expose secrets or preload a full seed for scoped work. Honor .context/toolchain.json. Antigravity uses /seed; Codex uses $seed.

1. Run `prepare hybrid --target <project> --json`. It includes working-tree additions, changes, deletions and renames; do not rely only on Git commits.
2. Read affected evidence and existing snapshot sections. For a new vector use references/ThinkingSeed_MasterHybrid.md from this bundle. An optional index operation supplies symbolic contracts without reading implementation bodies into context.
3. The current agent authors `01_seed/seed-<project>.md`: sections 0 through 10, version 6, receiver instructions, symbolic interfaces, evidence labels, relative paths and handoff. Keep it concise; disclose selected contract coverage and analysis limits. Never claim exhaustive coverage for a selected subset.
4. Run `complete hybrid --target <project> --input-hash <returned-hash> --json`. A master is not required. If inputs changed, prepare again. Finish this snapshot without updating other products unless requested.
