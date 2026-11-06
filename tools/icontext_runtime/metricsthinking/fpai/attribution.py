"""
Multi-Layer Attribution and Context Power Attribution Resolver.

Calculates 4-layer multi-signal attribution without external LLM API calls.
"""

import re
from typing import Any


def _get_shingles(text: str, k: int = 3) -> set[str]:
    words = re.findall(r"\w+", text.lower())
    if len(words) < k:
        return set(words)
    return {" ".join(words[i:i+k]) for i in range(len(words) - k + 1)}


def resolve_context_attribution(
    query: str,
    chunks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Resolves multi-signal contextual attribution across 4 deterministic layers:
    1. Lexical word overlap
    2. Code entity / identifier matching
    3. Import and structural dependency links
    4. Shingling Jaccard similarity proxy

    Returns list of annotated chunks with composite scores and power types.
    """
    if not chunks:
        return []

    q_lower = query.lower()
    q_words = set(re.findall(r"\w+", q_lower))
    q_entities = set(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]{2,}\b", query))
    q_shingles = _get_shingles(query, k=3)

    attributed_chunks: list[dict[str, Any]] = []

    for chunk in chunks:
        chunk_id = chunk.get("chunk_id", "unknown")
        content = chunk.get("content", "")
        tokens = max(1, chunk.get("tokens", len(content) // 4 or 1))

        c_lower = content.lower()
        c_words = set(re.findall(r"\w+", c_lower))
        c_entities = set(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]{2,}\b", content))
        c_shingles = _get_shingles(content, k=3)

        # Layer 1: Lexical Overlap
        lexical_score = (
            len(q_words.intersection(c_words)) / max(1, len(q_words))
            if q_words else 0.0
        )

        # Layer 2: Entity Matching
        entity_score = (
            len(q_entities.intersection(c_entities)) / max(1, len(q_entities))
            if q_entities else 0.0
        )

        # Layer 3: Dependency / Reference Check
        dep_score = 0.0
        for ent in q_entities:
            if f"import {ent}" in content or f"from " in content and ent in content:
                dep_score = 1.0
                break
            elif f"{ent}(" in content or f".{ent}" in content:
                dep_score = max(dep_score, 0.7)

        # Layer 4: Shingle Jaccard
        shingle_union = len(q_shingles.union(c_shingles))
        shingle_score = (
            len(q_shingles.intersection(c_shingles)) / shingle_union
            if shingle_union > 0 else 0.0
        )

        # Composite score
        composite = round(
            (0.35 * lexical_score)
            + (0.35 * entity_score)
            + (0.20 * dep_score)
            + (0.10 * shingle_score),
            4
        )

        is_useful = composite >= 0.25
        power_type = "ACTIVE" if is_useful else "REACTIVE"

        attributed_chunks.append({
            "chunk_id": chunk_id,
            "tokens": tokens,
            "composite_score": composite,
            "is_useful": is_useful,
            "power_type": power_type,
            "signals": {
                "lexical": round(lexical_score, 4),
                "entity": round(entity_score, 4),
                "dependency": round(dep_score, 4),
                "shingle": round(shingle_score, 4),
            },
        })

    return attributed_chunks
