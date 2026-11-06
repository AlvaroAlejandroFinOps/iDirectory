---
name: seed-master
description: "Actualiza el ADN exhaustivo por secciones con ThinkingSeed v6; acepta seedMaster como alias. Usar /seed-master en Antigravity o $seed-master en Codex."
metadata:
  version: "6.0.0"
---

# seed-master: iContext v6

Resolve this bundle from its SKILL.md location. Execute commands below as `python <bundle>/scripts/run.py <command>` using the available interpreter; resolve scripts and references from the bundle, never the target project.

Respect user scope and read-only constraints. Never traverse an ancestor with crawl:false, expose secrets or preload a full seed for scoped work. Honor .context/toolchain.json. Antigravity uses /seed-master; Codex uses $seed-master.

1. Run `prepare seed --target <project> --json`. Reuse current content-backed contracts; an optional index operation creates them if absent. Include uncommitted, new, removed and renamed files.
2. Read changed evidence and affected existing master sections. For a new master use references/ThinkingSeed Master.md from this bundle. Templates are bundle-relative, never assumed to exist in the target project.
3. The current agent updates `01_seed/seed-<project>-master.md`: sections 0 through 10, version 6, complete module-level public contracts, epistemic labels, actual tensions, relative paths and receiver handoff. Preserve unrelated sections; never embed implementation bodies.
4. Run `complete seed --target <project> --input-hash <returned-hash> --json`. Re-prepare if inputs changed. Structural/symbol checks do not prove narrative or runtime correctness. Finish the master; run the whole federation only when requested. Legacy seedMaster is a natural-language alias.
