"""Versioned iContext bundles for Antigravity and Codex. Never replace user rules."""
import json
import os
import shutil
import sys
import time
from pathlib import Path

from context_runtime import VERSION, atomic_write, digest, read_json, write_json

SKILLS = {"idir": ("iDirectory", "skills/v6/idir"),
          "seed": ("ThinkingSeed", "skills/v6/seed"),
          "seed-master": ("ThinkingSeed", "skills/v6/seed-master"),
          "metrics": ("MetricsThinking", "skills/v6/metrics"),
          "readme": ("iReadme", "skills/v6/readme"),
          "icontext": ("ContextControl", "skills/v6/icontext")}

BOOTSTRAP = '''#!/usr/bin/env python3
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
'''


def source_bundles(eco):
    result = {}
    for name, (repo, relative) in SKILLS.items():
        source = Path(eco) / repo / relative
        result[name] = source if (source / "bundle.json").is_file() else Path(__file__).resolve().parent / "skill_bundles" / name
    return result


def inspect_installation(eco, home):
    errors, installed = [], {}
    for agent, dest in (("antigravity", home / ".gemini/config/skills"), ("codex", home / ".agents/skills")):
        installed[agent] = {}
        for name, src in source_bundles(eco).items():
            target = dest / name / "SKILL.md"
            actual = digest(target.read_bytes()) if target.is_file() else None
            expected = digest((src / "SKILL.md").read_bytes()) if (src / "SKILL.md").is_file() else None
            manifest = read_json(src / "bundle.json")
            matches = bool(manifest) and actual == expected and actual is not None
            for relative, fingerprint in manifest.get("files", {}).items():
                resource = dest / name / relative
                matches = matches and resource.is_file() and digest(resource.read_bytes()) == fingerprint
            matches = matches and read_json(dest / name / "bundle.json") == manifest
            installed[agent][name] = {"matches": matches, "hash": actual}
            if not matches:
                errors.append(f"{agent}:{name}: missing or differs from canonical source")
    release = read_json(Path(__file__).resolve().parent / "release_manifest.json")
    runtime = home / ".icontext/versions" / VERSION
    if release:
        for relative, fingerprint in release.get("files", {}).items():
            resource = runtime / relative
            if not resource.is_file() or digest(resource.read_bytes()) != fingerprint:
                errors.append("runtime: missing or differs: " + relative)
    return {"version": VERSION, "state": "invalid" if errors else "current", "installed": installed, "errors": errors}


def install(eco, agents, home, local=None, dry_run=False, only=None, source_runtime=None):
    eco, home = Path(eco), Path(home)
    if any(agent not in {"antigravity", "codex", "claude"} for agent in agents):
        raise ValueError("Supported agents: antigravity,codex,claude")
    runtime_source = Path(source_runtime) if source_runtime else eco / "ContextControl/tools/icontext_runtime"
    if not (runtime_source / "release_manifest.json").is_file():
        runtime_source = Path(__file__).resolve().parent
    if not (runtime_source / "release_manifest.json").is_file():
        import tempfile
        import zipfile
        import _icontext_assets
        payload = Path(_icontext_assets.__file__).parent / "runtime_payload.zip"
        with tempfile.TemporaryDirectory(prefix="icontext_install_") as temporary:
            with zipfile.ZipFile(payload) as archive:
                for member in archive.infolist():
                    relative = Path(member.filename)
                    if relative.is_absolute() or ".." in relative.parts:
                        raise ValueError("Invalid runtime payload path")
                    atomic_write(Path(temporary) / relative, archive.read(member))
            return install(eco, agents, home, local=local, dry_run=dry_run, only=only, source_runtime=temporary)
    runtime_dest = (Path(local) / ".agents/icontext" if local else home / ".icontext/versions") / VERSION
    locations = {"antigravity": ".gemini/config/skills", "codex": ".agents/skills", "claude": ".claude/skills"}
    destinations = [Path(local) / ".agents/skills"] if local else [home / locations[a] for a in agents]
    selected = {k: (v if (v / "bundle.json").is_file() else runtime_source / "skill_bundles" / k)
                for k, v in source_bundles(eco).items() if only is None or k in only}
    result = {"version": VERSION, "state": "planned" if dry_run else "installed", "skills": list(selected),
              "agents": agents, "writes": 0}
    if dry_run:
        return result
    release = read_json(runtime_source / "release_manifest.json")
    for name, source in selected.items():
        manifest = read_json(source / "bundle.json")
        if manifest.get("version") != VERSION or not manifest.get("files"):
            raise ValueError(f"Missing or unsupported bundle manifest: {name}")
        for relative, fingerprint in manifest["files"].items():
            if digest((source / relative).read_bytes()) != fingerprint:
                raise ValueError(f"Bundle integrity error: {name}/{relative}")
    # Each release is assembled from its manifest, never from an unfiltered scan.
    for relative, fingerprint in release["files"].items():
        source = runtime_source / relative
        if digest(source.read_bytes()) != fingerprint:
            raise ValueError(f"Distribution integrity error: {relative}")
        result["writes"] += atomic_write(runtime_dest / relative, source.read_bytes())
    result["writes"] += atomic_write(runtime_dest / "release_manifest.json", (runtime_source / "release_manifest.json").read_bytes())
    for dest in destinations:
        for name, source in selected.items():
            manifest = read_json(source / "bundle.json")
            if not manifest:
                raise ValueError(f"Missing bundle manifest: {name}")
            for relative in manifest["files"]:
                target = dest / name / relative
                raw = (source / relative).read_bytes()
                if target.is_file() and target.read_bytes() != raw:
                    # Preserve user edits before replacing managed files.
                    backup = home / ".icontext/backups" / digest(str(target))[:12] / digest(target.read_bytes()) / relative
                    atomic_write(backup, target.read_bytes())
                result["writes"] += atomic_write(target, raw)
            result["writes"] += atomic_write(dest / name / "bundle.json", (source / "bundle.json").read_bytes())
    if not local:
        # Quarantine old iContext copies; other personal skills stay untouched.
        for old_root in (home / ".codex/skills", home / ".gemini/config/skills"):
            names = ("dir", "idir", "seed", "seedMaster", "metrics", "readme", "icontext") if old_root.name == "skills" and ".codex" in old_root.parts else ("seedMaster",)
            for name in names:
                if name not in selected and not (name == "seedMaster" and "seed-master" in selected) and not (name == "dir" and "idir" in selected):
                    continue
                target = old_root / name
                skill = target / "SKILL.md"
                if not skill.is_file():
                    continue
                text = skill.read_text(encoding="utf-8")
                if not any(marker in text for marker in ("iDirectory", "ThinkingSeed", "MetricsThinking", "Enterprise Paper-Grade", "iContext")):
                    continue
                resolved = target.resolve()
                resolved.relative_to(old_root.resolve())
                backup = home / ".icontext/backups/legacy" / digest(str(resolved))[:12] / name
                if backup.exists():
                    backup = backup.with_name(name + "_" + str(time.time_ns()))
                backup.parent.mkdir(parents=True, exist_ok=True)
                os.rename(resolved, backup)
        launcher = home / ".local/bin/icontext.py"
        atomic_write(launcher, BOOTSTRAP)
        if os.name == "nt":
            atomic_write(launcher.with_suffix(".cmd"), f'@"{sys.executable}" -B "{launcher}" %*\n')
            if home.resolve() == Path.home().resolve():
                import winreg
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
                    try:
                        user_path, kind = winreg.QueryValueEx(key, "Path")
                    except FileNotFoundError:
                        user_path, kind = "", winreg.REG_EXPAND_SZ
                    directory = str(launcher.parent)
                    if directory.casefold() not in {p.rstrip("\\").casefold() for p in user_path.split(";")}:
                        winreg.SetValueEx(key, "Path", 0, kind, user_path.rstrip(";") + ";" + directory)
                result["path_registered"] = True
                # Notify future Explorer-launched terminals of the user PATH.
                import ctypes
                notify = ctypes.windll.user32.SendMessageTimeoutW
                notify.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_size_t,
                                   ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_uint,
                                   ctypes.POINTER(ctypes.c_size_t)]
                notified = ctypes.c_size_t()
                notify(0xFFFF, 0x001A, 0, "Environment", 2, 1000, ctypes.byref(notified))
        else:
            command = launcher.with_suffix("")
            atomic_write(command, f'#!/bin/sh\nexec "{sys.executable}" -B "{launcher}" "$@"\n')
            command.chmod(0o755)
        write_json(home / ".icontext/registry.json", {"ecosystem_root": str(eco.resolve()), "runtime_version": VERSION})
    result["command"] = "icontext" if not local else "python .agents/skills/icontext/scripts/run.py"
    if not local:
        result["command_path"] = str((home / ".local/bin/icontext.cmd") if os.name == "nt" else (home / ".local/bin/icontext"))
    return result
