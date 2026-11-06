---
name: icontext
description: "Coordina estado, contexto, sincronización incremental y auditoría del ecosistema iContext v6. Usar /icontext en Antigravity o $icontext en Codex."
metadata:
  version: "6.0.0"
---

# icontext: iContext v6

Resolve this bundle from its SKILL.md location. Execute commands below as `python <bundle>/scripts/run.py <command>` using the available interpreter; resolve scripts and references from the bundle, never the target project.

Respect user scope and read-only constraints. Never traverse an ancestor with crawl:false, expose secrets or preload a full seed for scoped work. Honor .context/toolchain.json. Antigravity uses /icontext; Codex uses $icontext.

1. No action specified: use status or help. status, pack, audit, prepare, sync --dry-run and doctor are read-only; doctor --fix explicitly repairs.
2. For a requested update run `sync --target <project> --json`; --all selects the four ecosystem repositories. Exit 3 means the current agent must redact, 1 means a required failure, 0 means complete.
3. Act on the returned seed request: read changed evidence, update affected master sections only, then run `complete seed --target <project> --input-hash <returned-hash> --json`.
4. Run sync again. Metrics executes once its dependencies are valid. Act on the readme request, preserving project-specific bilingual content, then run `complete readme --target <project> --input-hash <returned-hash> --json`.
5. Run sync until current; failures block dependent phases. Never label pending redaction as complete. The terminal never calls an external AI provider; the active host agent performs semantic work. Use --json for structure and --verbose for detail.
