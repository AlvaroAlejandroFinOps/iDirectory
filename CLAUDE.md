# Claude Code Project Guidelines: iDirectory Context Engineering

This repository is governed by the **iDirectory v3.0 Context Engineering Protocol** (by **Gravity HyperScale Thinking**).

## 🚀 MANDATORY BOOTLOADER SEQUENCE (DO NOT BLIND CRAWL)
Before writing or analyzing code, you MUST follow this sequence:
1. Review governance rules in [`AGENTS.md`](file:///d:/0001%20HyperScale%20Thinking/PROYECTOS%20CLOUD/iContext/iDirectory/AGENTS.md).
2. Read the compact satellite map in [`.context/tree.json`](file:///d:/0001%20HyperScale%20Thinking/PROYECTOS%20CLOUD/iContext/iDirectory/.context/tree.json) (~250 tokens). DO NOT run recursive `find` or `ls` calls.
3. Read the project DNA in [`01_seed/seed-idirectory-master.md`](file:///d:/0001%20HyperScale%20Thinking/PROYECTOS%20CLOUD/iContext/iDirectory/01_seed/seed-idirectory-master.md).
4. Read the target directory `.context.yaml` beacon before editing or creating files.

## 🛠️ CLI Operations
- Audit repository governance: `python FWengine.py audit`
- Route any new file: `python FWengine.py route "<file_path>" --move`
- Inspect context budget: `python FWengine.py context --budget`
