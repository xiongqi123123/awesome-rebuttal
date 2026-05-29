# 16 Rebuttal Versioning Manager

## Goal

Preserve rebuttal progress safely using the user's selected mode: manual Git, auto Git, or markdown/JSON snapshot-only. Versioning must protect context, make rollback possible, and avoid accidental destructive Git operations.

## Required inputs

Read:

- `.awesome-rebuttal/memory/project_memory.json`
- `.awesome-rebuttal/snapshots/snapshot_memory.json`, if present
- current workspace git status, if Git is enabled or detected
- user-selected versioning mode from intake/bootstrap

## Outputs

Write/update:

```text
.awesome-rebuttal/memory/versioning_memory.json
.awesome-rebuttal/logs/versioning_report.md
.awesome-rebuttal/snapshots/snapshot_memory.json      # through 09
.awesome-rebuttal/snapshots/REBUTTAL_SNAPSHOT.md      # through 09 renderer
```

## Modes

### `manual_git`

User manages Git manually.

Allowed:

- inspect `git status`, `git diff --stat`, `git log -1`;
- suggest checkpoint boundaries;
- suggest Lore-protocol commit messages;
- create snapshots via 09.

Not allowed unless explicitly asked:

- `git add`;
- `git commit`;
- `git reset`, `git clean`, branch deletion, history rewrite;
- push/pull/rebase/merge.

### `auto_git`

Skill may create local milestone commits after safe verification.

Allowed:

- initialize Git only if the workspace is not a repo and the user selected auto Git;
- create local commits at checkpoint boundaries;
- use Lore commit protocol;
- include only intended workspace files; never include ignored/private temp dirs.

Never do without explicit instruction:

- push to remote;
- rewrite history;
- reset/clean/delete branches;
- commit credentials, private review packets that user marked local-only, or generated build junk;
- include `Test ` or other ignored smoke-test folders.

### `markdown_snapshot_only`

No Git required. Use 09 as the persistence mechanism:

- maintain canonical `.awesome-rebuttal/snapshots/snapshot_memory.json`;
- render `.awesome-rebuttal/snapshots/REBUTTAL_SNAPSHOT.md` or `PROJECT_SNAPSHOT.md` from JSON;
- newest checkpoint appears first with exact timestamp;
- no manual Markdown fact edits.

## Checkpoint boundaries

Create or suggest a checkpoint after:

- workspace bootstrap;
- intake/rule confirmation;
- paper/code memory update;
- review normalization;
- semantic review analysis;
- review-driven experiment planning;
- priority/situation analysis;
- strategy matrix and user strategy decisions;
- response draft / AC summary draft;
- template layout generation;
- final safety check.

## Versioning memory schema sketch

```json
{
  "version": "0.1",
  "mode": "manual_git|auto_git|markdown_snapshot_only|unset",
  "git": {
    "repo_detected": true,
    "branch": "main",
    "head": "...",
    "dirty": true,
    "ignored_private_paths": ["Test ", "Temp/"],
    "last_skill_commit": "..."
  },
  "snapshots": {
    "latest_snapshot_id": "...",
    "snapshot_doc": ".awesome-rebuttal/snapshots/REBUTTAL_SNAPSHOT.md"
  },
  "checkpoint_history": [],
  "recommended_commit_message": "...",
  "blocked_actions": [],
  "next_checkpoint": "..."
}
```

## Commit message protocol

When committing in `auto_git` mode or suggesting commits in `manual_git`, use Lore protocol:

```text
<why this checkpoint was made>

Constraint: <external constraint>
Rejected: <alternative> | <reason>
Confidence: high|medium|low
Scope-risk: narrow|moderate|broad
Directive: <future warning>
Tested: <verification>
Not-tested: <gaps>
```

## Safe Git procedure for `auto_git`

1. Read `.gitignore` and versioning memory.
2. Run `git status --short --ignored` if useful.
3. Verify no ignored/private paths are staged.
4. Run validation appropriate to the checkpoint.
5. Stage only intended files.
6. Commit with Lore message.
7. Update versioning memory and snapshot.
8. Report commit hash and validation evidence.

## Snapshot document must include

Use `09_snapshot_maker.md` for the full JSON/Markdown contract. At minimum:

- canonical `.awesome-rebuttal/snapshots/snapshot_memory.json`;
- generated user Markdown snapshot, not hand-edited;
- exact timestamp with timezone;
- current stage;
- workspace map;
- source freshness;
- latest posture;
- top concerns;
- current strategy;
- experiment/draft/template/safety status;
- unresolved TODOs;
- next action;
- reverse-chronological snapshot history with newest entry first.

## Stop / proceed rules

Proceed when:

- versioning mode is selected;
- checkpoint boundary is reached;
- validation evidence is available or a gap is recorded;
- no destructive Git action is required.

Stop and ask when:

- user has not selected versioning mode;
- committing would include private/local-only files;
- branch/history operation is requested;
- remote push/pull or credentialed operation is needed;
- there are conflicting user edits that would be overwritten.

## Safety rules

- Versioning preserves work; it must not change rebuttal content facts.
- Never hide unverified state by committing as “final.”
- Never push, rewrite, clean, reset, or delete without explicit instruction.
- Always keep snapshots available even when Git is used.
