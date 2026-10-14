# Claude Code Project Guidelines: iDirectory Context Engineering

This repository is governed by the **iDirectory v3.0 Context Engineering Protocol** (by **Gravity HyperScale Thinking**).

## 🚀 TWO-TIER BOOTLOADER SEQUENCE (DO NOT BLIND CRAWL)
Before writing or analyzing code, you MUST follow the two-tier sequence:

### 🔹 Tier 1: Atomic / Surgical Tasks (Default)
1. Review governance rules in [`AGENTS.md`](file:///d:/0001%20HyperScale%20Thinking/PROYECTOS%20CLOUD/iContext/iDirectory/AGENTS.md).
2. Read compact satellite map in [`.context/tree.json`](file:///d:/0001%20HyperScale%20Thinking/PROYECTOS%20CLOUD/iContext/iDirectory/.context/tree.json) (~250 tokens). DO NOT run recursive `find` or `ls` calls.
3. Read the target directory `.context.yaml` beacon (or resolve via upward inheritance).
4. **DO NOT pre-load `01_seed/seed-idirectory-master.md`** to protect the token budget.

### 🔸 Tier 2: Deep Architecture / Full Audit (Explicit Triggers Only)
- Triggered by `/seedMaster`, `/metrics`, `/ultraThinking`, `/plan`, or direct user architectural redesign requests.
- Sequence: `AGENTS.md` -> `.context/tree.json` -> `01_seed/seed-idirectory-master.md` -> Beacons -> Execution.

### 🛡️ Post-Task Synchronization Contract
If you create or restructure directories, run `python FWengine.py beacon --sync` and `python FWengine.py map --sync` before completing the task.

## 🛠️ CLI Operations
- Audit repository governance: `python FWengine.py audit`
- Route any new file: `python FWengine.py route "<file_path>" --move`
- Inspect context budget: `python FWengine.py context --budget`
