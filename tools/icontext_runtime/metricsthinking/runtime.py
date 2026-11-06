"""iContext v6 portable runtime. Standard library only; queries never persist state.

Canonical source: iDirectory/src/core/context_runtime.py. Other copies are generated.
"""
from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import re
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

VERSION = "6.0.0"
ANALYZER_VERSION = "6.0.0:3"
EXCLUDED = {".git", ".context", ".venv", "venv", "env", "__pycache__", "node_modules",
            ".pytest_cache", ".mypy_cache", ".ruff_cache", "target", "dist", "build"}
PRUNED = {"data/raw", "data/processed", "data/sandbox", "logs", "artifacts/plans/archive",
          "artifacts/plans/backlog", "artifacts/plans/metricsthinking", "tools/icontext_runtime"}
LAYER_NAMES = {"l0": "l0_idirectory", "l1": "l1_thinkingseed", "l2": "l2_metricsthinking", "l3": "l3_ireadme"}


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {} if default is None else default


def digest(value):
    data = value if isinstance(value, bytes) else json.dumps(value, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def atomic_write(path, content):
    """Replace only changed bytes. Return whether a file was written."""
    import uuid
    path = Path(path)
    data = content.encode("utf-8") if isinstance(content, str) else content
    try:
        if path.read_bytes() == data:
            return False
    except FileNotFoundError:
        pass
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".tmp_{os.getpid()}_{uuid.uuid4().hex}_{path.name}")
    try:
        tmp.write_bytes(data)
        for attempt in range(10):
            try:
                os.replace(tmp, path)
                break
            except PermissionError:
                if attempt == 9:
                    raise
                time.sleep(0.01 * (1.5 ** attempt))
    finally:
        tmp.unlink(missing_ok=True)
    return True


def write_json(path, value):
    return atomic_write(path, json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")


@contextmanager
def repository_lock(root, name="publish", timeout=10):
    """OS lock: automatically released on process death; no stale-lock stealing."""
    path = Path(root) / ".context" / f".{name}.lock"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as handle:
        if path.stat().st_size == 0:
            handle.write(b"0")
            handle.flush()
        deadline = time.monotonic() + timeout
        while True:
            try:
                handle.seek(0)
                if os.name == "nt":
                    import msvcrt
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except (OSError, BlockingIOError):
                if time.monotonic() >= deadline:
                    raise TimeoutError(f"Repository busy: {name}")
                time.sleep(0.02)
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def publish_layer(root, layer, payload):
    """Own one sidecar; aggregate all layers under a common process lock."""
    root = Path(root)
    name = LAYER_NAMES.get(layer, layer)
    with repository_lock(root):
        sidecar = root / ".context" / "layers" / f"{name}.json"
        previous = read_json(sidecar)
        value = {"version": VERSION, **payload}
        if {k: v for k, v in previous.items() if k != "published_at"} == value:
            value = previous
        else:
            value["published_at"] = datetime.now(timezone.utc).isoformat()
        write_json(sidecar, value)
        bus_path = root / ".context" / "icontext_bus.json"
        old_bus = read_json(bus_path)
        layers = dict(old_bus.get("layers", {}))
        for key in LAYER_NAMES.values():
            record = read_json(root / ".context" / "layers" / f"{key}.json")
            if record:
                layers[key] = record
            elif key not in layers:
                layers[key] = {"present": False, "state": "unknown"}
        for record in layers.values():
            record.setdefault("state", "legacy_unverified")
        bus = {"$schema": "../schemas/icontext_bus.schema.json", "protocol_version": VERSION, "project": root.name, "layers": layers}
        if {k: v for k, v in old_bus.items() if k != "updated_at"} == bus:
            return old_bus
        bus["updated_at"] = datetime.now(timezone.utc).isoformat()
        write_json(bus_path, bus)
        return bus


def ignore_patterns(root):
    patterns = []
    for name in (".gitignore", ".agentignore"):
        path = Path(root) / name
        if path.is_file():
            patterns.extend(line.strip() for line in path.read_text(encoding="utf-8").splitlines()
                            if line.strip() and not line.lstrip().startswith("#"))
    return patterns


def ignored(relative, patterns):
    result = False
    for pattern in patterns:
        negate = pattern.startswith("!")
        pattern = pattern.lstrip("!").strip("/")
        parts = relative.split("/")
        if (fnmatch.fnmatchcase(relative, pattern) or relative.startswith(pattern + "/")
                or ("/" not in pattern and any(fnmatch.fnmatchcase(p, pattern) for p in parts))):
            result = not negate
    return result


def crawl_allowed(directory):
    beacon = Path(directory) / ".context.yaml"
    if beacon.is_file():
        return not re.search(r"(?mi)^\s*crawl\s*:\s*false\s*(?:#.*)?$", beacon.read_text(encoding="utf-8"))
    return True


def iter_files(root, patterns=None):
    """Prune before descending, including inherited beacon restrictions."""
    root = Path(root).resolve()
    patterns = ignore_patterns(root) + (patterns or [])
    if not crawl_allowed(root):
        return
    for current, dirs, files in os.walk(root, followlinks=False):
        cur = Path(current)
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED
                         and not (cur / d).is_symlink()
                         and (cur / d).relative_to(root).as_posix() not in PRUNED
                         and not ignored((cur / d).relative_to(root).as_posix(), patterns)
                         and crawl_allowed(cur / d))
        for name in sorted(files):
            path = cur / name
            rel = path.relative_to(root).as_posix()
            if (path.is_symlink() or name.startswith(".tmp_") or name == ".DS_Store"
                    or name == "desktop.ini" or name.endswith((".pyc", ".coverage")) or ignored(rel, patterns)):
                continue
            if name.startswith(".") and name not in {".context.yaml", ".gitignore", ".agentignore", ".cursorrules"}:
                continue
            yield path


def python_contracts(source, relative):
    import ast
    tree = ast.parse(source)
    symbols, signatures, flags, imports = [], [], [], []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
            symbols.append(node.name)
            signatures.append(f"./{relative}::{node.name}({ast.unparse(node.args)}) -> {ast.unparse(node.returns) if node.returns else 'Any'}")
        elif isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
            symbols.append(node.name)
            signatures.append(f"./{relative}::{node.name}(class)")
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "add_argument":
            flags.extend(a.value for a in node.args if isinstance(a, ast.Constant) and isinstance(a.value, str) and a.value.startswith("-"))
    return {"symbols": symbols, "signatures": signatures, "cli_flags": sorted(set(flags)), "imports": sorted(set(imports))}


def inventory(root, persist=False, full=False):
    root = Path(root).resolve()
    path = root / ".context" / "inventory.json"
    previous = read_json(path)
    patterns = ignore_patterns(root)
    policy_hash = digest([patterns, ANALYZER_VERSION, read_json(root / "config/context_policy.json")])
    old = previous.get("files", {}) if previous.get("policy_hash") == policy_hash else {}
    records, reads, parses = {}, 0, 0
    for file in iter_files(root, patterns):
        rel = file.relative_to(root).as_posix()
        stat = file.stat()
        cached = old.get(rel, {})
        stamp = [stat.st_size, stat.st_mtime_ns]
        if not full and cached.get("stat") == stamp:
            records[rel] = cached
            continue
        raw = file.read_bytes()
        reads += 1
        record = {"stat": stamp, "sha256": digest(raw), "size": len(raw)}
        if rel in {"README.md", "README_ES.md"}:
            text = raw.decode("utf-8", errors="replace")
            text = re.sub(r"<!-- ICONTEXT-V6:TELEMETRY:START -->.*?<!-- ICONTEXT-V6:TELEMETRY:END -->", "", text, flags=re.S)
            text = re.sub(r"\n{3,}", "\n\n", text.strip())
            record["semantic_sha256"] = digest(text.encode("utf-8"))
        if file.suffix == ".py":
            if cached.get("sha256") == record["sha256"] and "contracts" in cached:
                record["contracts"] = cached["contracts"]
            else:
                parses += 1
                try:
                    record["contracts"] = python_contracts(raw.decode("utf-8-sig"), rel)
                except (SyntaxError, UnicodeError) as exc:
                    record["parse_error"] = str(exc)
        records[rel] = record
    before = previous.get("files", {})
    added = sorted(set(records) - set(before))
    removed = sorted(set(before) - set(records))
    modified = sorted(k for k in records.keys() & before.keys() if records[k]["sha256"] != before[k]["sha256"])
    renames = []
    for src in removed:
        for dest in added:
            if before[src]["sha256"] == records[dest]["sha256"]:
                renames.append({"from": src, "to": dest})
                break
    result = {"version": VERSION, "analyzer_version": ANALYZER_VERSION, "policy_hash": policy_hash,
              "files": records, "inputs_hash": digest({k: v.get("semantic_sha256", v["sha256"]) for k, v in records.items()})}
    if persist:
        write_json(path, result)
    return result, {"added": added, "modified": modified, "removed": removed, "renamed": renames,
                    "files_read": reads, "ast_parses": parses}


def contracts_index(root, persist=False, full=False):
    inv, stats = inventory(root, persist=persist, full=full)
    modules = {k: v["contracts"] for k, v in inv["files"].items() if "contracts" in v}
    result = {"version": "6.0", "analyzer_version": ANALYZER_VERSION, "project": Path(root).name,
              "$schema": "../schemas/contracts_ast.schema.json",
              "topology_hash": read_json(Path(root) / ".context/tree.json").get("topology_hash", ""),
              "inputs_hash": inv["inputs_hash"], "modules": modules,
              "public_symbols": sorted({s for m in modules.values() for s in m["symbols"]}),
              "cli_flags": sorted({s for m in modules.values() for s in m["cli_flags"]}),
              "signatures_1line": [s for m in modules.values() for s in m["signatures"]]}
    result["contracts_ast_hash"] = digest(modules)
    if persist:
        write_json(Path(root) / ".context/contracts_ast.json", result)
    return result, stats


def input_hash(inv, layer):
    files = inv["files"]
    if layer == "seed":
        files = {k: v for k, v in files.items() if not k.startswith("01_seed/") and k not in {"README.md", "README_ES.md"}}
    elif layer == "readme":
        files = {k: v for k, v in files.items() if k not in {"README.md", "README_ES.md"}}
    return digest({"analyzer": ANALYZER_VERSION, "policy": inv["policy_hash"], "files": {k: v.get("semantic_sha256", v["sha256"]) for k, v in files.items()}})


def estimated_tokens(value):
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return (len(text) + 2) // 3


def _context_budget(root, tier):
    path = Path(root) / "config/context_policy.json"
    policy = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    if tier == "ecosystem":
        value = policy.get("budgets", {}).get("ecosystem_pack_max_tokens", 650)
    else:
        value = policy.get("profiles", {}).get("tier_" + tier, {}).get("target_token_budget", 220 if tier == "1a" else 800)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError("Context token budget must be a positive integer")
    return value


def bounded(payload, limit, removable=("contracts_ast", "edges", "files", "active_topology", "layers")):
    result = json.loads(json.dumps(payload))
    omitted = 0
    for key in removable:
        while estimated_tokens(result) > limit and result.get(key):
            collection = result[key]
            if isinstance(collection, dict):
                collection.pop(next(reversed(collection)))
            elif isinstance(collection, list):
                collection.pop()
            else:
                result[key] = ""
            omitted += 1
            result["omitted"] = omitted
            result["expand"] = "--expand"
    if estimated_tokens(result) > limit:
        raise ValueError("Required context exceeds budget; use --expand")
    return result


def _orientation_stamp(root):
    result = []
    for name in (".agentignore", ".gitignore", "config/context_policy.json"):
        path = Path(root) / name
        if path.is_file():
            st = path.stat()
            result.append([name, st.st_size, st.st_mtime_ns])
    return result


def _orientation_beacons(root, target):
    parts = Path(target).parts
    if ".." in parts or Path(target).is_absolute():
        raise ValueError("Orientation target must remain relative to its project")
    directory = Path(root)
    content, blocked = [], False
    for component in (None, *parts):
        if component not in (None, "."):
            directory = directory / component
        path = directory / ".context.yaml"
        if path.is_file():
            raw = path.read_bytes()
            content.append(digest(raw))
            blocked = blocked or bool(re.search(r"(?mi)^\s*crawl\s*:\s*false\s*(?:#.*)?$", raw.decode("utf-8", errors="replace")))
    return digest(content), blocked


_ORIENTATION_READ_CACHE = {}


def query_orientation(root, target=".", tier="1a", expand=False):
    """Fast recorded view. Return None when a verified cache cannot be used."""
    root = Path(root)
    target = target.replace("\\", "/").removeprefix("./").rstrip("/") or "."
    (root / target).resolve().relative_to(root.resolve())
    cache_file = root / ".context/orientation_cache.json"
    if not cache_file.is_file():
        return None
    stamp = cache_file.stat().st_mtime_ns
    cached_stamp, table = _ORIENTATION_READ_CACHE.get(str(root), (None, {}))
    if cached_stamp != stamp:
        table = read_json(cache_file)
        _ORIENTATION_READ_CACHE[str(root)] = (stamp, table)
    entry = table.get("entries", {}).get(target)
    if not entry or table.get("policy_stamp") != _orientation_stamp(root):
        return None
    chain_hash, blocked = _orientation_beacons(root, target)
    if blocked:
        return {"idir_pack": "6.0", "focus": target, "crawl": False, "state": "pruned", "files": [], "edges": {}}
    if entry.get("beacon_chain_hash") != chain_hash:
        return None
    value = json.loads(json.dumps(entry["pack"]))
    value.update(tier=tier, state="recorded", generation=table.get("generation"))
    from stat import S_ISREG
    verified = []
    for item in value.get("files", []):
        name = item.rsplit("(~", 1)[0]
        path = root / target / name
        try:
            st = path.stat()
            if S_ISREG(st.st_mode):
                ratio = 3.6 if path.suffix.lower() in {".py", ".sql", ".json", ".yaml", ".yml", ".avsc", ".tf", ".sh", ".ps1", ".toml"} else 4
                binary = path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp", ".bmp", ".pbix", ".parquet", ".delta", ".avro", ".orc", ".feather", ".pdf", ".zip", ".tar", ".gz", ".7z", ".whl", ".pyc", ".pyd", ".so", ".dll", ".exe"}
                verified.append(f"{name}(~{0 if binary else max(1, int(st.st_size / ratio))}t)")
        except OSError:
            pass
    value["files"] = verified
    checkpoint = read_json(root / ".context/checkpoint.json")
    if (checkpoint.get("status") in {"executing", "approved", "paused"}
            and (not checkpoint.get("expires_at") or checkpoint["expires_at"] > datetime.now(timezone.utc).isoformat())):
        value["checkpoint"] = {"plan_id": checkpoint.get("plan_id"), "session_id": checkpoint.get("session_id"),
            "objective": checkpoint.get("objective", "")[:80], "constraints": [str(v)[:80] for v in checkpoint.get("constraints", [])[:2]],
            "phase": checkpoint.get("current_phase"), "next": checkpoint.get("next_action", "")[:80]}
    return value if expand else bounded(value, _context_budget(root, tier))


def validate_seed(path, index=None):
    text = Path(path).read_text(encoding="utf-8")
    errors = []
    if not re.search(r'<SEED_ARCHITECTURAL_VECTOR\b[^>]*contains_source_code="false"', text) or "</SEED_ARCHITECTURAL_VECTOR>" not in text:
        errors.append("Missing architectural vector container")
    if "CONTEXT HANDOFF" not in text or "0.1" not in text:
        errors.append("Missing receiver instructions or handoff")
    if not {str(n) for n in range(11)}.issubset(set(re.findall(r"(?m)^##\s+(\d+)\.", text))):
        errors.append("Missing numbered architectural sections 0 through 10")
    if index is not None:
        expected = {symbol for name, module in index.get("modules", {}).items()
                    if not name.startswith("tests/") for symbol in module.get("symbols", [])}
        missing = sorted(symbol for symbol in expected if symbol not in text)
        if missing:
            errors.append("Missing public contracts: " + ", ".join(missing[:20]))
    if re.search(r"(?<![A-Za-z0-9_])[A-Za-z]:[/\\]|file:///|(?<![:/A-Za-z0-9])/(?:home|Users)/", text):
        errors.append("Local absolute path")
    for language, body in re.findall(r"```([^\n]*)\n(.*?)```", text, re.S):
        if language.strip() in {"yaml", "yml"} and body.lstrip().startswith("seed_schema_version:"):
            # Seed identity metadata is a contract, not implementation source.
            continue
        if language.strip() in {"python", "py", "sh", "bash", "ps1", "sql", "json", "yaml", "rust", "go"} and len(body.strip().splitlines()) > 5:
            errors.append("Implementation block exceeds five lines")
    return errors


def validate_readmes(root):
    errors = []
    headings = []
    for name, other in (("README.md", "README_ES.md"), ("README_ES.md", "README.md")):
        path = Path(root) / name
        if not path.is_file():
            errors.append(f"Missing {name}")
            continue
        text = path.read_text(encoding="utf-8")
        sections = re.findall(r"(?m)^##\s+(\d+)\.", text)
        headings.append(sections)
        if sections != [str(i) for i in range(1, 9)]:
            errors.append(f"{name}: expected eight ordered sections")
        # Absolute paths are valid in fenced terminal examples when users request
        # copy-pasteable commands. Keep authored prose free of machine-local paths.
        prose = re.sub(r"```.*?```", "", text, flags=re.S)
        if other not in text or re.search(r"(?<![A-Za-z0-9_])[A-Za-z]:[/\\]|file:///|(?<![:/A-Za-z0-9])/(?:home|Users)/", prose):
            errors.append(f"{name}: invalid language links or local paths")
    if len(headings) == 2 and headings[0] != headings[1]:
        errors.append("Language section mismatch")
    return errors
