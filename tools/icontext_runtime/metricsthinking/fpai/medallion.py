"""
Client-Side Local Medallion Pipeline (Bronze -> Silver -> Gold).

Processes raw telemetry JSONL logs locally with zero cloud dependencies.
"""

from collections import defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


def run_local_medallion_pipeline(
    raw_telemetry_dir: str = "data/raw/telemetry",
    processed_dir: str = "data/processed/telemetry",
) -> dict[str, Any]:
    """
    Executes local Medallion data engineering pipeline:
    - Bronze: Scans raw JSONL files.
    - Silver: Deduplicates events idempotently, normalizes schema fields.
    - Gold: Aggregates KPIs by repository and execution policy.
    """
    raw_path = Path(raw_telemetry_dir)
    processed_path = Path(processed_dir)
    raw_path.mkdir(parents=True, exist_ok=True)
    processed_path.mkdir(parents=True, exist_ok=True)

    silver_file = processed_path / "silver_events.jsonl"
    gold_file = processed_path / "gold_metrics.json"

    # Step 1: Read existing silver event IDs
    seen_event_ids: set[str] = set()
    existing_records: list[dict[str, Any]] = []

    if silver_file.exists():
        with open(silver_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        rec = json.loads(line)
                        eid = rec.get("event_id")
                        if eid:
                            seen_event_ids.add(eid)
                        existing_records.append(rec)
                    except json.JSONDecodeError:
                        continue

    raw_read = 0
    valid_written = 0
    duplicates_dropped = 0
    new_records: list[dict[str, Any]] = []

    raw_files = sorted(list(raw_path.glob("*.jsonl")))
    for rf in raw_files:
        with open(rf, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                raw_read += 1
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                event_id = data.get("event_id")
                if not event_id:
                    continue

                if event_id in seen_event_ids:
                    duplicates_dropped += 1
                    continue

                # Normalize to Silver
                tokens = data.get("tokens_by_phase") or {}
                attr = data.get("attribution_summary") or {}
                silver_rec = {
                    "event_id": str(event_id),
                    "timestamp": data.get("timestamp", datetime.now(timezone.utc).isoformat()),
                    "repo_id": data.get("repo_id", "unknown"),
                    "task_id": data.get("task_id", "default"),
                    "execution_id": data.get("execution_id", "default"),
                    "stored_tokens": int(tokens.get("stored_tokens", 0)),
                    "scanned_tokens": int(tokens.get("scanned_tokens", 0)),
                    "active_tokens": int(attr.get("active_tokens", 0)),
                    "reactive_tokens": int(attr.get("reactive_tokens", 0)),
                    "fpai_spectral": float(attr.get("fpai_spectral", 0.0)),
                    "fpai_linear": float(attr.get("fpai_linear", 0.0)),
                    "processed_at": datetime.now(timezone.utc).isoformat(),
                }
                new_records.append(silver_rec)
                seen_event_ids.add(event_id)
                valid_written += 1

    # Save Silver
    all_silver = existing_records + new_records
    with open(silver_file, "w", encoding="utf-8") as f:
        for rec in all_silver:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # Step 2: Aggregate to Gold
    gold_kpis: dict[str, Any] = {
        "total_events": len(all_silver),
        "total_active_tokens": sum(r["active_tokens"] for r in all_silver),
        "total_reactive_tokens": sum(r["reactive_tokens"] for r in all_silver),
        "average_fpai_spectral": (
            round(sum(r["fpai_spectral"] for r in all_silver) / len(all_silver), 4)
            if all_silver else 1.0
        ),
        "average_fpai_linear": (
            round(sum(r["fpai_linear"] for r in all_silver) / len(all_silver), 4)
            if all_silver else 1.0
        ),
        "repositories": list(set(r["repo_id"] for r in all_silver)),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    with open(gold_file, "w", encoding="utf-8") as f:
        json.dump(gold_kpis, f, indent=2)

    return {
        "raw_read": raw_read,
        "silver_records_total": len(all_silver),
        "new_silver_written": valid_written,
        "duplicates_dropped": duplicates_dropped,
        "gold_kpis": gold_kpis,
    }
