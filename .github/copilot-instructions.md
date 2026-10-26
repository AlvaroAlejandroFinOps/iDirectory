# GitHub Copilot Instructions — iDirectory v4.0 Context Engineering

This repository enforces **iDirectory v4.0** (by **Gravity HyperScale Thinking**). Canonical policy resides in `./config/context_policy.json` and full contract in `./AGENTS.md`.

1. **No Blind Recursive Scans (`[INV-02]` & `[INV-03]`):** Never recursively dump or scan directories with `crawl: false` (`data/raw`, `data/processed`, `data/sandbox`, `logs`, `artifacts/plans/archive`).
2. **Adaptive Bootloader Profiles:**
   - **Tier 1A (Known target path):** Run `python FWengine.py context --pack <dir> --tier 1a` (< 220 tokens) or `python FWengine.py map --slice <dir>`. Do not load `./01_seed/seed-idirectory-master.md`.
   - **Tier 1B (Multi-file or scoped plan):** Run `python FWengine.py context --compact` + `python FWengine.py map --slice <dir>` + `python FWengine.py seed --section <id>`.
   - **Tier 2 (Global architecture / `/seedMaster`):** Read `./.context/tree.json` and `./01_seed/seed-idirectory-master.md`.
3. **All-Lowercase Topology (`[INV-06]`):** All governed directory names must be lowercase. Route files via `python FWengine.py route "<file>" --move`.
4. **Unified Closure (`[INV-04]`):** After creating or modifying directories or beacons, execute `python FWengine.py reconcile`.
