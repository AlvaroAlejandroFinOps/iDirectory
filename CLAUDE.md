# Claude Code Project Guidelines: iDirectory Context Engineering (v4.0)

This repository is governed by the **iDirectory v4.0 Adaptive Context Engineering Protocol** (by **Gravity HyperScale Thinking**). Canonical policy: [`./config/context_policy.json`](./config/context_policy.json).

## 🚀 ADAPTIVE BOOTLOADER SEQUENCE (DO NOT BLIND CRAWL)
Before writing or analyzing code, select the minimal sufficient context profile from [`./AGENTS.md`](./AGENTS.md):

### 🔹 Tier 1A: Atomic / Known-Path Tasks (Default)
1. Run `python FWengine.py context --pack <target_dir> --tier 1a` (< 220 tokens) or `python FWengine.py map --slice <target_dir>` (< 150 tokens).
2. DO NOT run recursive `find` or `ls -R` calls, and never enter `crawl: false` branches (`data/raw`, `data/processed`, `data/sandbox`, `logs`, `artifacts/plans/archive`).
3. **DO NOT pre-load `./01_seed/seed-idirectory-master.md`** in Tier 1A.

### 🔹 Tier 1B: Scoped Multi-File or `/plan` Tasks
1. Run `python FWengine.py context --compact` (~165 tokens) + `python FWengine.py map --slice <dir>` for affected modules.
2. For architectural contract checks, query sections surgically via `python FWengine.py seed --toc` and `python FWengine.py seed --section <id>`.

### 🔸 Tier 2: Global Architecture / Full Forensic Audit (Explicit Triggers Only)
- Triggered only by `/seedMaster`, `/metrics`, `/ultraThinking`, or cross-domain architectural redesign.
- Sequence: `./AGENTS.md` -> `./.context/tree.json` -> `./01_seed/seed-idirectory-master.md` -> Target Beacons -> Execution.

### 🛡️ Unified Post-Task Synchronization Contract
If you create or restructure directories or beacons, run the single idempotent closure command:
```bash
python FWengine.py reconcile
```

## 🛠️ CLI Operations
- Unified reconcile & audit: `python FWengine.py reconcile`
- Focused context pack: `python FWengine.py context --pack <dir> --tier 1a`
- Subgraph slice: `python FWengine.py map --slice <dir>`
- Sectional seed lookup: `python FWengine.py seed --toc` / `python FWengine.py seed --section <id>`
- Session continuity checkpoint: `python FWengine.py checkpoint --show`
- Route any new file: `python FWengine.py route "<file_path>" --move`
- Inspect context budget: `python FWengine.py context --budget`
