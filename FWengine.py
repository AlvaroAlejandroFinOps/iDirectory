#!/usr/bin/env python3
"""Compatibility launcher; generated from iDirectory/tools/build_runtime.py."""
from pathlib import Path
import sys
sys.dont_write_bytecode = True
_runtime_dir = Path(__file__).resolve().parent / "tools/icontext_runtime"
sys.path.insert(0, str(_runtime_dir))
if __name__ == "__main__" and sys.argv[1:2] == ["context"] and "--pack" in sys.argv[2:]:
    import argparse
    query = argparse.ArgumentParser(add_help=False)
    query.add_argument("--pack", required=True)
    query.add_argument("--tier", default="1a", choices=["1a", "1b", "2"])
    query.add_argument("--expand", action="store_true")
    options, unknown = query.parse_known_args(sys.argv[2:])
    if not unknown:
        from icontext_cli import main
        argv = ["pack", options.pack, "--tier", options.tier, "--json"]
        if options.expand:
            argv.append("--expand")
        raise SystemExit(main(argv))
exec(compile((_runtime_dir / "fwengine.py").read_text(encoding="utf-8"), str(_runtime_dir / "fwengine.py"), "exec"), globals())
