"""
Lifecycle and Active Plans Governance for MetricsThinking™ v5.0.
Inspects artifacts/plans/active/, evicts completed/stale plans to artifacts/plans/archive/,
cleans residual audit artifacts, and synchronizes artifacts/plans/backlog/queue.json.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None


def extract_plan_metadata(plan_path: Path) -> dict[str, Any]:
    """Extracts frontmatter metadata from a Markdown plan file."""
    if not plan_path.is_file():
        return {}

    try:
        content = plan_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}

    if not content.startswith("---"):
        return {}

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}

    raw_yaml = parts[1].strip()
    if yaml is not None:
        try:
            parsed = yaml.safe_load(raw_yaml)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

    # Fallback line-by-line parser for simple key-values
    meta: dict[str, Any] = {}
    for line in raw_yaml.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if v.lower() == "true":
                meta[k] = True
            elif v.lower() == "false":
                meta[k] = False
            else:
                meta[k] = v
    return meta


def update_plan_frontmatter(plan_path: Path, updates: dict[str, Any]) -> None:
    """Updates or injects YAML frontmatter in a Markdown plan file preserving body content."""
    try:
        content = plan_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return

    meta: dict[str, Any] = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            raw_yaml = parts[1].strip()
            if yaml is not None:
                try:
                    parsed = yaml.safe_load(raw_yaml)
                    if isinstance(parsed, dict):
                        meta = parsed
                except Exception:
                    pass
            body = parts[2].lstrip("\r\n")

    meta.update(updates)

    if yaml is not None:
        dumped = yaml.safe_dump(meta, sort_keys=False).strip()
    else:
        lines = [f"{k}: {json.dumps(v) if not isinstance(v, (str, int, float, bool)) else v}" for k, v in meta.items()]
        dumped = "\n".join(lines)

    new_content = f"---\n{dumped}\n---\n\n{body}"
    plan_path.write_text(new_content, encoding="utf-8")


def evaluate_plan_completion(plan_path: Path, checkpoint_data: dict[str, Any] | None = None) -> tuple[bool, str]:
    """
    Evaluates whether a plan in artifacts/plans/active/ should be archived.
    Returns (should_archive, rationale).
    """
    if not plan_path.is_file():
        return False, "File not found"

    meta = extract_plan_metadata(plan_path)
    status = str(meta.get("status", "")).lower().strip()
    plan_id = str(meta.get("id") or meta.get("plan_id") or plan_path.stem)

    # 1. Frontmatter explicit terminal status
    if status in ("completed", "archived", "superseded", "done", "closed"):
        return True, f"Plan metadata declares terminal status: '{status}'"

    # 2. Checkpoint correlation
    if checkpoint_data:
        cp_status = str(checkpoint_data.get("status", "")).lower()
        cp_plan_id = str(checkpoint_data.get("plan_id", ""))
        if cp_status == "completed" and (cp_plan_id in (plan_id, plan_path.name, plan_path.stem)):
            return True, f"Checkpoint marks plan '{cp_plan_id}' as completed"

    # 3. Expiration date check
    expires_at_str = meta.get("expires_at")
    if expires_at_str:
        try:
            # Handle ISO date string
            clean_date = str(expires_at_str).split("T")[0]
            exp_date = datetime.fromisoformat(clean_date).replace(tzinfo=timezone.utc)
            if exp_date < datetime.now(timezone.utc):
                return True, f"Plan expired on {expires_at_str}"
        except Exception:
            pass

    # 4. Ground Truth Task Check (Markdown checkboxes & FEP packets)
    try:
        content = plan_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False, "Could not read plan content"

    # Checkboxes: - [ ] vs - [x]
    pending_boxes = re.findall(r"^[\s]*[-*]\s*\[\s\]", content, flags=re.MULTILINE)
    completed_boxes = re.findall(r"^[\s]*[-*]\s*\[[xX]\]", content, flags=re.MULTILINE)
    total_boxes = len(pending_boxes) + len(completed_boxes)

    if total_boxes > 0:
        if len(pending_boxes) == 0:
            return True, f"All {len(completed_boxes)} checklist tasks completed (100% ground truth)"
        else:
            return False, f"Incomplete: {len(pending_boxes)}/{total_boxes} checklist tasks pending"

    # Check FEP packets (if document uses Flash Execution Packets format)
    fep_total = re.findall(r"###\s+FEP-\d+", content)
    fep_done = re.findall(r"###\s+FEP-\d+.*(?:\[DONE\]|\[COMPLETED\]|status:\s*done)", content, flags=re.IGNORECASE)
    if fep_total and len(fep_total) == len(fep_done):
        return True, f"All {len(fep_total)} FEP packets completed"

    return False, "Plan is active or in progress"


def sync_backlog_queue(repo_root: Path, archived_plan_ids: list[str]) -> int:
    """
    Synchronizes artifacts/plans/backlog/queue.json by transitioning matching items to 'done'.
    Returns number of updated backlog items.
    """
    if not archived_plan_ids:
        return 0

    queue_path = repo_root / "artifacts" / "plans" / "backlog" / "queue.json"
    if not queue_path.is_file():
        return 0

    try:
        data = json.loads(queue_path.read_text(encoding="utf-8"))
    except Exception:
        return 0

    items = data.get("items")
    if not isinstance(items, list):
        return 0

    updated_count = 0
    now_iso = datetime.now(timezone.utc).isoformat()
    clean_ids = {pid.lower().strip() for pid in archived_plan_ids}

    for item in items:
        if not isinstance(item, dict):
            continue
        item_id = str(item.get("id", "")).lower()
        plan_ref = str(item.get("plan_id", "")).lower()
        item_intent = str(item.get("intent", "")).lower()

        matches = (
            item_id in clean_ids or
            plan_ref in clean_ids or
            any(cid in item_intent for cid in clean_ids if len(cid) > 3)
        )

        if matches and item.get("status") != "done":
            item["status"] = "done"
            item["completed_at"] = now_iso
            updated_count += 1

    if updated_count > 0:
        queue_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    return updated_count


def reconcile_active_plans(repo_root: Path | str = ".", check_only: bool = False) -> dict[str, Any]:
    """
    Reconciles active plans in artifacts/plans/active/:
    1. Relocates legacy/stray MetricsThinking artifacts to artifacts/plans/metricsthinking/.
    2. Identifies completed/stale plans and moves them to artifacts/plans/archive/.
    3. Updates artifacts/plans/backlog/queue.json with completed plan items.
    """
    root = Path(repo_root).resolve()
    active_dir = root / "artifacts" / "plans" / "active"
    archive_dir = root / "artifacts" / "plans" / "archive"
    mt_dir = root / "artifacts" / "plans" / "metricsthinking"
    cp_file = root / ".context" / "checkpoint.json"

    result: dict[str, Any] = {
        "archived_plans": [],
        "retained_plans": [],
        "cleaned_artifacts": [],
        "backlog_items_updated": 0,
        "violations": []
    }

    if not active_dir.is_dir():
        return result

    archive_dir.mkdir(parents=True, exist_ok=True)
    mt_dir.mkdir(parents=True, exist_ok=True)

    # 1. Clean residual MetricsThinking artifacts from active/
    stray_artifacts = ["INFERRED_ROADMAP.md", "CONTEXT_PRUNING_PLAN.json"]
    for stray_name in stray_artifacts:
        stray_file = active_dir / stray_name
        if stray_file.is_file():
            dest = mt_dir / stray_name
            if not check_only:
                # If destination does not exist, move; otherwise overwrite dest and remove stray
                dest.write_text(stray_file.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
                try:
                    stray_file.unlink()
                except OSError:
                    pass
            result["cleaned_artifacts"].append(stray_name)

    # 2. Checkpoint data
    checkpoint_data = None
    if cp_file.is_file():
        try:
            checkpoint_data = json.loads(cp_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    # 3. Scan active plan markdown files
    active_plans = sorted(active_dir.glob("*.md"))
    archived_plan_ids: list[str] = []

    for plan_file in active_plans:
        # Skip beacon or hidden files
        if plan_file.name.startswith("."):
            continue

        should_archive, reason = evaluate_plan_completion(plan_file, checkpoint_data)
        meta = extract_plan_metadata(plan_file)
        p_id = str(meta.get("id") or meta.get("plan_id") or plan_file.stem)

        if should_archive:
            if not check_only:
                now_str = datetime.now(timezone.utc).isoformat()
                update_plan_frontmatter(plan_file, {
                    "status": "completed",
                    "executable": False,
                    "archived_at": now_str,
                    "archive_rationale": reason
                })
                dest_file = archive_dir / plan_file.name
                # Atomic replace / move
                try:
                    os.replace(plan_file, dest_file)
                except OSError:
                    dest_file.write_text(plan_file.read_text(encoding="utf-8"), encoding="utf-8")
                    plan_file.unlink()
            result["archived_plans"].append({
                "file": plan_file.name,
                "plan_id": p_id,
                "reason": reason
            })
            archived_plan_ids.append(p_id)
            archived_plan_ids.append(plan_file.stem)
        else:
            result["retained_plans"].append({
                "file": plan_file.name,
                "plan_id": p_id,
                "status": meta.get("status", "executing")
            })

    # 4. Synchronize backlog queue
    if not check_only and archived_plan_ids:
        result["backlog_items_updated"] = sync_backlog_queue(root, archived_plan_ids)

    return result
