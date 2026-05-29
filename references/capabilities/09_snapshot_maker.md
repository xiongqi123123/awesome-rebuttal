# 09 Snapshot Maker

## Goal

Create compact, durable rebuttal checkpoints that can restore the skill's working context without forcing the user to read every memory file. A snapshot must serve two readers from one source of truth:

- **Skill reload entry:** `.awesome-rebuttal/snapshots/snapshot_memory.json` — detailed, structured, machine-readable, and safe to load at the start of a later session.
- **User progress view:** `.awesome-rebuttal/snapshots/REBUTTAL_SNAPSHOT.md` or `PROJECT_SNAPSHOT.md` — concise Markdown generated from the JSON, newest checkpoint first, with exact timestamps.

The JSON is canonical. The Markdown must be rendered from the JSON and must not contain independent facts that could drift.

## When to create or refresh a snapshot

Refresh the snapshot at every durable checkpoint, and whenever the user asks for a progress save:

1. workspace bootstrap completed or changed
2. intake/rule status changed
3. paper memory or code memory changed
4. review index or review analysis changed
5. priority/situation analysis changed
6. strategy matrix changed
7. experiment triage changed
8. response draft, AC summary, or template state changed
9. final safety check completed
10. before ending a long session or switching workspaces

If no meaningful state changed, update only if the user explicitly asks; otherwise report the existing latest snapshot.

## File layout

Use this layout inside the active rebuttal workspace, never inside the installed skill folder:

```text
.awesome-rebuttal/snapshots/
├── snapshot_memory.json          # canonical skill reload entry; detailed latest state + history index
├── REBUTTAL_SNAPSHOT.md          # user-readable progress view, rendered from snapshot_memory.json
└── archive/                      # optional full JSON archives for major milestones
    └── YYYYMMDD-HHMMSS-<stage>.json
```

Use `PROJECT_SNAPSHOT.md` instead of `REBUTTAL_SNAPSHOT.md` only when the workspace is not yet tied to a specific rebuttal packet. Record the selected Markdown path in `snapshot_memory.json.md_export.path`.

## Inputs to summarize

Read only the memory files needed for the checkpoint stage:

- `.awesome-rebuttal/memory/project_memory.json`
- `.awesome-rebuttal/memory/paper_memory.json`, if available
- `.awesome-rebuttal/memory/code_memory.json`, if available
- `.awesome-rebuttal/memory/review_memory.json`, if available
- `.awesome-rebuttal/memory/review_analysis_memory.json`, if available
- `.awesome-rebuttal/memory/experiment_memory.json`, if available
- `.awesome-rebuttal/memory/strategy_memory.json`, if available
- `.awesome-rebuttal/memory/template_memory.json`, if available
- `.awesome-rebuttal/memory/response_memory.json`, if available
- `.awesome-rebuttal/memory/ac_summary_memory.json`, if available
- `.awesome-rebuttal/memory/safety_memory.json`, if available
- `.awesome-rebuttal/memory/versioning_memory.json`, if available
- `.awesome-rebuttal/memory/overleaf_sync_memory.json`, if available
- venue/rule confirmation notes, compile logs, draft paths, and safety checklist outputs when relevant

Do not copy raw full reviews, full paper text, private code dumps, or long draft paragraphs into the snapshot. Store IDs, paths, short summaries, source anchors, and unresolved decisions.

## Canonical JSON structure

`snapshot_memory.json` should be detailed enough to reload the skill, but layered enough to stay manageable. Use this structure:

```json
{
  "version": "0.2",
  "updated_at": "2026-05-29T21:30:00+08:00",
  "timezone": "Asia/Shanghai",
  "snapshot_order": "newest_first",
  "latest_snapshot_id": "snap-20260529-213000-strategy",
  "latest_snapshot": {
    "snapshot_id": "snap-20260529-213000-strategy",
    "created_at": "2026-05-29T21:30:00+08:00",
    "stage": "strategy",
    "stage_label": "Strategy matrix refreshed after priority analysis",
    "status_line": "Review analysis complete; strategy ready; experiment triage pending.",
    "workspace_digest": {},
    "source_freshness": [],
    "memory_status": {},
    "venue_and_format": {},
    "paper_code_digest": {},
    "review_digest": {},
    "situation_digest": {},
    "strategy_digest": {},
    "experiment_digest": {},
    "drafting_digest": {},
    "safety_status": {},
    "open_questions": [],
    "unresolved_todos": [],
    "next_actions": [],
    "changed_since_previous": [],
    "reload_instructions": []
  },
  "snapshot_history": [],
  "archive_files": [],
  "md_export": {
    "path": ".awesome-rebuttal/snapshots/REBUTTAL_SNAPSHOT.md",
    "generated_from": ".awesome-rebuttal/snapshots/snapshot_memory.json",
    "last_rendered_at": "2026-05-29T21:30:00+08:00"
  }
}
```

### Required latest snapshot fields

| Field | Purpose |
|---|---|
| `snapshot_id` | Stable ID: `snap-YYYYMMDD-HHMMSS-<stage>` in local timezone. |
| `created_at` | Exact ISO timestamp with timezone. |
| `stage` | One of `workspace`, `intake`, `paper_code`, `review_index`, `review_analysis`, `priority`, `strategy`, `experiment`, `draft`, `safety`, `final`. |
| `stage_label` | Human-readable reason for this checkpoint. |
| `status_line` | One-sentence state summary for quick reload. |
| `workspace_digest` | Workspace map, state dir, versioning mode, git/snapshot mode, LaTeX/template status. |
| `source_freshness` | For each memory/source file: path, exists, updated_at if known, status, and freshness risk. |
| `memory_status` | Which memory files are complete/partial/blocked and which capability produced them. |
| `venue_and_format` | Confirmed rule status, response format, page/word limits, anonymity/link/new-experiment constraints, and confirmation source. |
| `paper_code_digest` | Short paper story, contributions, key evidence, code architecture, experiment feasibility, and missing anchors. |
| `review_digest` | Reviewer labels + anonymous IDs, scores/confidence if provided, common concerns, major/minor counts. |
| `situation_digest` | Current posture, confidence, AC-facing facts, high-risk concerns, evidence gaps. |
| `strategy_digest` | Selected strategy lens, top focused problems, reviewer goals, response stances, coverage plan. |
| `experiment_digest` | Must-do/high-value/not-recommended experiments, status, blockers, result availability. |
| `drafting_digest` | Existing response memory, draft paths, template/AC-summary state, coverage state, and remaining writing constraints. |
| `safety_status` | Provenance, commitment, coverage, venue-rule, tone, anonymity, and fabrication gates. |
| `open_questions` | Questions that require user confirmation before the next risky step. |
| `unresolved_todos` | Concrete TODOs with owner/status/priority. |
| `next_actions` | Ordered next actions with suggested capability route. |
| `changed_since_previous` | What changed in this checkpoint. |
| `reload_instructions` | Which files/capabilities to read first when resuming. |

## Snapshot history

Keep `snapshot_history` in **newest-first order**. Each entry should be compact:

```json
{
  "snapshot_id": "snap-20260529-213000-strategy",
  "created_at": "2026-05-29T21:30:00+08:00",
  "stage": "strategy",
  "status_line": "Review analysis complete; strategy ready; experiment triage pending.",
  "key_changes": ["Selected hybrid strategy lens", "Promoted FP01-FP06"],
  "next_action": "Run 10_experiment_triage.md"
}
```

History is for orientation, not archival storage. If a checkpoint contains many details, write the full checkpoint to `archive/` and reference it from `archive_files`.

## Markdown rendering contract

The Markdown file is a generated user view. It should be readable in one to three screens for normal checkpoints, with expandable detail only when useful.

Required Markdown order:

1. title and “do not edit manually” note
2. exact `Updated:` timestamp and timezone
3. `Latest snapshot` summary
4. current stage/status
5. workspace/rule/versioning digest
6. current review situation and strategy
7. top focused problems or top open blockers
8. experiment/draft/safety status
9. next actions
10. `Snapshot history (newest first)` with newest checkpoint at the top

Example shape:

```markdown
# Rebuttal Snapshot

> Generated from `.awesome-rebuttal/snapshots/snapshot_memory.json`. Do not edit this file manually.

- Updated: 2026-05-29T21:30:00+08:00
- Latest snapshot: snap-20260529-213000-strategy
- Stage: strategy — Strategy matrix refreshed after priority analysis
- Status: Review analysis complete; strategy ready; experiment triage pending.

## Current state

- Workspace: canonical; versioning: markdown_snapshot_only; LaTeX: available
- Rules/format: one-page PDF; user-confirmed; no external links
- Posture: rebuttal_sensitive (medium confidence)

## Strategy focus

1. FP01 — Novelty/contribution framing; reviewers: R1 (<anonymous_id>), R3 (<anonymous_id>)
2. FP02 — Missing baseline evidence; reviewers: R2 (<anonymous_id>)

## Next actions

1. Run `10_experiment_triage.md` for FP02 and FP04.
2. Confirm whether new experiment results may be mentioned under venue rules.

## Snapshot history (newest first)

### 2026-05-29T21:30:00+08:00 — strategy

- ID: snap-20260529-213000-strategy
- Status: Review analysis complete; strategy ready; experiment triage pending.
- Key changes: Selected hybrid strategy lens; promoted FP01-FP06.
- Next: Run `10_experiment_triage.md`.
```

## Consistency rules

- Treat JSON as canonical; render Markdown from JSON.
- Never hand-edit facts in Markdown. If Markdown is wrong, update JSON then regenerate Markdown.
- `latest_snapshot_id` must equal `latest_snapshot.snapshot_id` and the first `snapshot_history` entry.
- `updated_at` must match or be later than `latest_snapshot.created_at`.
- `snapshot_history` must be sorted newest to oldest by `created_at`.
- The Markdown top section must reflect the same latest ID, stage, timestamp, status line, next action, and safety state as the JSON.
- If JSON and Markdown disagree, the snapshot is stale; regenerate Markdown before using it for context recovery.

## Deterministic renderer

When available, use the bundled renderer to keep JSON and Markdown consistent:

```bash
python3 awesome-rebuttal/scripts/render_snapshot.py \
  --json .awesome-rebuttal/snapshots/snapshot_memory.json \
  --md .awesome-rebuttal/snapshots/REBUTTAL_SNAPSHOT.md

python3 awesome-rebuttal/scripts/render_snapshot.py \
  --json .awesome-rebuttal/snapshots/snapshot_memory.json \
  --md .awesome-rebuttal/snapshots/REBUTTAL_SNAPSHOT.md \
  --check
```

If the skill is installed globally, resolve the script path from the installed skill folder and pass paths in the active rebuttal workspace.

## Quality gates

Before calling the checkpoint complete:

- JSON parses successfully.
- Markdown was generated from the current JSON.
- Latest snapshot has exact timestamp with timezone.
- User-facing history is newest-first.
- No raw private review/paper/code dump was copied into the snapshot.
- All next actions are concrete and routed to a capability or user confirmation.
- Safety status clearly says `pass`, `blocked`, or `needs_user_confirmation` for each gate.

## Stop/proceed rules

Proceed to the next capability only after the snapshot can restore the current project state. If required memory files are missing, create a partial snapshot that says what is missing and route to the missing capability instead of pretending the stage is complete.
