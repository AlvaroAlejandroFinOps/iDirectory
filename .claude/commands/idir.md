# /idir - Claude Code Command for iDirectory v4.0 Governance & Context Engineering

Execute iDirectory v4.0 governance commands via `python FWengine.py`:
- `reconcile [--check]`: Unified idempotent closure (sync beacons, update SHA-256 `topology_hash` in `.context/tree.json`, and run strict audit).
- `context --pack <dir> --tier 1a`: Single-call surgical context bundle (< 220 tokens: slice + resolved beacon + verified `key_files` + checkpoint).
- `map --slice <dir> [--radius 1]`: Focused topological subgraph (< 150 tokens).
- `seed --toc` / `seed --section <id>`: Sectional query of `01_seed/` without loading the full seed.
- `checkpoint --show | --set ... | --clear`: Manage multi-phase attentional continuity in `.context/checkpoint.json`.
- `route "<file>" [--move] [--overwrite]`: Classify or atomically relocate a file to its canonical lowercase directory.
- `context --budget` / `context --compact`: Inspect governed token budget or emit compact topology string (~165 tokens).
- `audit [--fix]`: Verify lowercase topology, canonical folders, beacon schemas, portable adapters, and satellite freshness.
