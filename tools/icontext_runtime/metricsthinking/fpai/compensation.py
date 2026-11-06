"""
Compensation and Context Pruning Engine.

Materializes prioritized, 100% reversible context pruning plans
and synchronizes `.agentignore` without destructive file deletion.
"""

from datetime import datetime, timezone
import hashlib
from pathlib import Path
from typing import Any

from metricsthinking.models import ContextPruningPlan, PruningActionItem

PRUNE_START_MARKER = "# >>> FPAI-PRUNE-START"
PRUNE_END_MARKER = "# <<< FPAI-PRUNE-END"


def generate_pruning_plan(
    target_path: str,
    dead_files: list[str],
    redundant_files: list[str],
    structural_files: list[str],
    file_sizes: dict[str, int],
) -> ContextPruningPlan:
    """
    Generates a prioritized context pruning plan for dead, duplicate, and distortive files.
    """
    items: list[PruningActionItem] = []
    total_recovered = 0

    # 1. Dead files (Q_DEAD)
    for f in dead_files:
        chars = file_sizes.get(f, 400)
        tokens = max(1, chars // 4)
        lines = max(1, chars // 40)
        h = hashlib.sha256(f.encode("utf-8")).hexdigest()[:16]
        items.append(
            PruningActionItem(
                file_path=f.replace("\\", "/"),
                line_count=lines,
                token_estimate=tokens,
                pruning_type="Q_DEAD",
                sha256_before=h,
                justification="Zero afferent coupling and dormant context ballast",
                reversible=True,
            )
        )
        total_recovered += tokens

    # 2. Redundant files (Q_DUP)
    for f in redundant_files:
        chars = file_sizes.get(f, 400)
        tokens = max(1, chars // 4)
        lines = max(1, chars // 40)
        h = hashlib.sha256(f.encode("utf-8")).hexdigest()[:16]
        items.append(
            PruningActionItem(
                file_path=f.replace("\\", "/"),
                line_count=lines,
                token_estimate=tokens,
                pruning_type="Q_DUP",
                sha256_before=h,
                justification="Semantic duplicate / shingling Jaccard overlap > 0.85",
                reversible=True,
            )
        )
        total_recovered += tokens

    # 3. Structural distortion files (D_STRUCTURAL)
    for f in structural_files:
        chars = file_sizes.get(f, 400)
        tokens = max(1, chars // 4)
        lines = max(1, chars // 40)
        h = hashlib.sha256(f.encode("utf-8")).hexdigest()[:16]
        items.append(
            PruningActionItem(
                file_path=f.replace("\\", "/"),
                line_count=lines,
                token_estimate=tokens,
                pruning_type="D_STRUCTURAL",
                sha256_before=h,
                justification="Conflicting rules or syntax/schema distortion",
                reversible=True,
            )
        )
        total_recovered += tokens

    now = datetime.now(timezone.utc).isoformat()

    return ContextPruningPlan(
        target_path=target_path.replace("\\", "/"),
        items=items,
        total_tokens_recovered=total_recovered,
        active_tokens_remaining=1000,
        power_factor_target=0.85,
        generated_at=now,
    )


def apply_pruning_plan(
    plan: ContextPruningPlan,
    repo_root: str,
    update_agentignore: bool = True,
) -> dict[str, Any]:
    """
    Applies the pruning plan safely by updating .agentignore within boundary markers.
    No physical files are deleted; context exclusion is strictly reversible.
    """
    root_path = Path(repo_root)
    agentignore_path = root_path / ".agentignore"

    paths_to_prune = [item.file_path for item in plan.items]

    if update_agentignore:
        existing_lines: list[str] = []
        if agentignore_path.exists():
            content = agentignore_path.read_text(encoding="utf-8")
            existing_lines = content.splitlines()

        # Extract lines before and after existing markers if present
        new_lines: list[str] = []
        in_marker_block = False

        for line in existing_lines:
            if line.strip() == PRUNE_START_MARKER:
                in_marker_block = True
                continue
            if line.strip() == PRUNE_END_MARKER:
                in_marker_block = False
                continue
            if not in_marker_block:
                new_lines.append(line)

        # Build clean pruned block
        prune_block = [PRUNE_START_MARKER]
        for p in sorted(paths_to_prune):
            clean_p = p.lstrip("./")
            prune_block.append(clean_p)
        prune_block.append(PRUNE_END_MARKER)

        # Combine
        combined_content = "\n".join(new_lines).rstrip()
        if combined_content:
            combined_content += "\n\n" + "\n".join(prune_block) + "\n"
        else:
            combined_content = "\n".join(prune_block) + "\n"

        agentignore_path.write_text(combined_content, encoding="utf-8")

    return {
        "status": "APPLIED",
        "files_pruned_count": len(paths_to_prune),
        "tokens_recovered": plan.total_tokens_recovered,
        "agentignore_updated": update_agentignore,
        "reversible": True,
    }
