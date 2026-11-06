"""Evidence-backed incremental evaluation; unknown dependencies invalidate conservatively."""
import hashlib
import inspect
import json
import re
from pathlib import Path

from .runtime import digest


def rule_fingerprint(evaluator, function, config, evidence, attribute_cache):
    source = inspect.getsource(function)
    names = set(re.findall(r"\bev\.([a-zA-Z_]\w*)", source))
    # Helpers can use arbitrary evidence; use the entire evidence in this case.
    if re.search(r"self\.[a-zA-Z_]\w*\(", source):
        names = set(vars(evidence))
    inputs = {}
    for name in sorted(names):
        if name not in attribute_cache:
            value = getattr(evidence, name, None)
            attribute_cache[name] = hashlib.sha256(json.dumps(value, default=str, sort_keys=True).encode()).hexdigest()
        inputs[name] = attribute_cache[name]
    return digest([config, evaluator.profile, source, inputs])


def observed_context(evidence):
    """Exact byte duplication is measured; token quantities remain estimates."""
    tokens = evidence.file_tokens
    groups = {}
    duplicate = 0
    for path, fingerprint in sorted(evidence.file_hashes.items()):
        if fingerprint in groups:
            duplicate += tokens.get(path, 0)
        else:
            groups[fingerprint] = path
    dead = sum(tokens.get(p, 0) for p in evidence.rel_files if p.endswith((".tmp", ".bak", ".swp")))
    return {"total": sum(tokens.values()), "dead": dead, "duplicate": duplicate,
            "distortion": 0.0, "distortion_state": "not_measured",
            "method": "exact_content_duplicates; heuristic_tokens; attention_not_measured"}
