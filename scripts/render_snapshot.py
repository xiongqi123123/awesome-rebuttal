#!/usr/bin/env python3
"""Render awesome-rebuttal snapshot Markdown from canonical JSON.

The JSON is the source of truth. This script intentionally renders a compact
user-facing Markdown view from selected JSON fields so the two files cannot
drift through manual editing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise SystemExit(f"Snapshot JSON must be an object: {path}")
    return data


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def text(value: Any, default: str = "not recorded") -> str:
    if value is None:
        return default
    if isinstance(value, str):
        return value if value.strip() else default
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def first_present(mapping: dict[str, Any], *keys: str, default: str = "not recorded") -> str:
    for key in keys:
        if key in mapping and mapping[key] not in (None, "", []):
            return text(mapping[key], default=default)
    return default


def parse_time(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return datetime.min


def bullet_list(values: Any, empty: str = "not recorded", limit: int | None = None) -> list[str]:
    items = as_list(values)
    if limit is not None:
        items = items[:limit]
    if not items:
        return [f"- {empty}"]
    rendered: list[str] = []
    for item in items:
        if isinstance(item, dict):
            label = first_present(item, "title", "summary", "status_line", "description", "question", "action", "id")
            extra = first_present(item, "route", "next_route", "capability", "status", default="")
            rendered.append(f"- {label}" + (f" — {extra}" if extra else ""))
        else:
            rendered.append(f"- {text(item)}")
    return rendered


def render_focus_items(snapshot: dict[str, Any]) -> list[str]:
    strategy = snapshot.get("strategy_digest") or {}
    situation = snapshot.get("situation_digest") or {}
    review = snapshot.get("review_digest") or {}
    candidates = (
        strategy.get("top_focused_problems")
        or strategy.get("focused_problems")
        or situation.get("high_risk_concerns")
        or review.get("common_concerns")
        or snapshot.get("unresolved_todos")
        or []
    )
    items = as_list(candidates)[:8]
    if not items:
        return ["1. not recorded"]
    lines: list[str] = []
    for idx, item in enumerate(items, start=1):
        if isinstance(item, dict):
            title = first_present(item, "title", "concern", "problem", "summary", "id")
            reviewers = item.get("mentioned_by") or item.get("reviewers") or item.get("sources") or []
            if isinstance(reviewers, list) and reviewers:
                reviewer_text = ", ".join(
                    first_present(r, "stable_label", "reviewer_id", "anonymous_id") if isinstance(r, dict) else text(r)
                    for r in reviewers
                )
                lines.append(f"{idx}. {title} — reviewers/sources: {reviewer_text}")
            else:
                route = first_present(item, "next_route", "route", "strategy_stance", "status", default="")
                lines.append(f"{idx}. {title}" + (f" — {route}" if route else ""))
        else:
            lines.append(f"{idx}. {text(item)}")
    return lines


def safety_line(snapshot: dict[str, Any]) -> str:
    safety = snapshot.get("safety_status") or {}
    if not isinstance(safety, dict) or not safety:
        return "not recorded"
    parts = []
    for key in ["provenance", "commitment", "coverage", "venue_rule", "tone", "anonymity", "fabrication", "overall"]:
        if key in safety:
            parts.append(f"{key}={text(safety[key])}")
    return ", ".join(parts) if parts else text(safety)


def render_markdown(data: dict[str, Any], json_path: Path) -> str:
    latest = data.get("latest_snapshot") or {}
    if not isinstance(latest, dict):
        raise SystemExit("latest_snapshot must be an object")

    history = [h for h in as_list(data.get("snapshot_history")) if isinstance(h, dict)]
    history = sorted(history, key=lambda h: parse_time(text(h.get("created_at"), "")), reverse=True)

    updated_at = text(data.get("updated_at") or latest.get("created_at"))
    timezone = text(data.get("timezone"), "timezone not recorded")
    snapshot_id = text(latest.get("snapshot_id") or data.get("latest_snapshot_id"))
    stage = text(latest.get("stage"))
    stage_label = text(latest.get("stage_label"))
    status_line = text(latest.get("status_line"))

    workspace = latest.get("workspace_digest") or {}
    venue = latest.get("venue_and_format") or {}
    situation = latest.get("situation_digest") or {}
    experiments = latest.get("experiment_digest") or {}
    drafting = latest.get("drafting_digest") or {}

    digest = hashlib.sha256(
        json.dumps(latest, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:16]

    lines: list[str] = [
        "# Rebuttal Snapshot",
        "",
        f"> Generated from `{json_path.as_posix()}`. Do not edit this file manually; update the JSON and regenerate Markdown.",
        "",
        f"- Updated: {updated_at} ({timezone})",
        f"- Latest snapshot: {snapshot_id}",
        f"- Latest snapshot hash: `{digest}`",
        f"- Stage: {stage} — {stage_label}",
        f"- Status: {status_line}",
        "",
        "## Current state",
        "",
        f"- Workspace: {first_present(workspace, 'classification', 'workspace_status')}; versioning: {first_present(workspace, 'versioning_mode', 'versioning')}; LaTeX/template: {first_present(workspace, 'latex_status', 'template_status')}",
        f"- Rules/format: {first_present(venue, 'rule_source_status', 'rule_status')}; response mode: {first_present(venue, 'response_mode', 'format')}",
        f"- Posture: {first_present(situation, 'posture')} ({first_present(situation, 'posture_confidence', 'confidence')})",
        f"- Safety: {safety_line(latest)}",
        "",
        "## Strategy focus or blockers",
        "",
        *render_focus_items(latest),
        "",
        "## Experiments and drafting",
        "",
        f"- Experiments: {first_present(experiments, 'summary', 'status', 'experiment_status')}",
        f"- Draft/template: {first_present(drafting, 'summary', 'draft_status', 'template_status')}",
        "- Open questions:",
        *bullet_list(latest.get("open_questions"), empty="none recorded", limit=8),
        "",
        "## Next actions",
        "",
        *bullet_list(latest.get("next_actions"), empty="none recorded", limit=8),
        "",
        "## Snapshot history (newest first)",
        "",
    ]

    if not history:
        lines.append("- No prior snapshots recorded.")
    else:
        for entry in history:
            created = text(entry.get("created_at"))
            entry_stage = text(entry.get("stage"))
            lines.extend([
                f"### {created} — {entry_stage}",
                "",
                f"- ID: {text(entry.get('snapshot_id'))}",
                f"- Status: {text(entry.get('status_line'))}",
            ])
            changes = as_list(entry.get("key_changes"))
            if changes:
                lines.append("- Key changes: " + "; ".join(text(c) for c in changes))
            else:
                lines.append("- Key changes: not recorded")
            lines.extend([
                f"- Next: {text(entry.get('next_action'))}",
                "",
            ])

    return "\n".join(lines).rstrip() + "\n"


def validate_consistency(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    latest = data.get("latest_snapshot") or {}
    latest_id = latest.get("snapshot_id") if isinstance(latest, dict) else None
    if data.get("latest_snapshot_id") != latest_id:
        errors.append("latest_snapshot_id must equal latest_snapshot.snapshot_id")
    history = [h for h in as_list(data.get("snapshot_history")) if isinstance(h, dict)]
    if history:
        if history[0].get("snapshot_id") != latest_id:
            errors.append("first snapshot_history entry must be the latest snapshot")
        times = [parse_time(text(h.get("created_at"), "")) for h in history]
        if times != sorted(times, reverse=True):
            errors.append("snapshot_history must be newest-first by created_at")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Render awesome-rebuttal Markdown snapshot from canonical JSON.")
    parser.add_argument("--json", required=True, type=Path, help="Path to snapshot_memory.json")
    parser.add_argument("--md", required=True, type=Path, help="Path to output Markdown snapshot")
    parser.add_argument("--check", action="store_true", help="Check that Markdown matches rendered output without writing")
    args = parser.parse_args()

    data = load_json(args.json)
    errors = validate_consistency(data)
    if errors:
        raise SystemExit("Snapshot consistency errors:\n- " + "\n- ".join(errors))

    rendered = render_markdown(data, args.json)
    if args.check:
        current = args.md.read_text(encoding="utf-8") if args.md.exists() else ""
        if current != rendered:
            raise SystemExit(f"Markdown snapshot is stale: {args.md}")
        print(f"snapshot markdown is current: {args.md}")
        return

    args.md.parent.mkdir(parents=True, exist_ok=True)
    args.md.write_text(rendered, encoding="utf-8")
    print(f"wrote {args.md}")


if __name__ == "__main__":
    main()
