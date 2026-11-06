#!/usr/bin/env python3
"""Run the installed runtime, respecting a project version pin."""
import json
import sys
from pathlib import Path
sys.dont_write_bytecode = True
here = Path(__file__).resolve()
version = "6.0.0"
for root in (Path.cwd(), *Path.cwd().parents):
    pin = root / ".context/toolchain.json"
    if pin.is_file():
        version = str(json.loads(pin.read_text(encoding="utf-8")).get("runtime_version", version))
        break
    if (root / ".git").exists():
        break
if not version or any(c not in "0123456789." for c in version):
    raise SystemExit("Invalid runtime version pin")
candidates = [Path.home() / ".icontext/versions" / version]
for parent in here.parents:
    candidates.extend([parent / "icontext" / version, parent / ".icontext/versions" / version, parent / "tools/icontext_runtime"])
def matches_version(path):
    try:
        return (path / "icontext_cli.py").is_file() and json.loads((path / "release_manifest.json").read_text(encoding="utf-8")).get("version") == version
    except (OSError, ValueError):
        return False
runtime = next((p for p in candidates if matches_version(p)), None)
if runtime is None:
    raise SystemExit("Requested iContext runtime is not installed; run the v6 installer")
sys.path.insert(0, str(runtime))
from icontext_cli import main
raise SystemExit(main())
