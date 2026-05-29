# 15 Overleaf / LeafLink Sync Helper

## Goal

When the paper is hosted on Overleaf or cn.overleaf, use a safe, user-approved sync path to make the paper source available under the local rebuttal workspace, preferably `Paper/`, so the skill can build paper memory, align claims, and coordinate edits.

LeafLink is an optional **tool integration** for this workflow, not an advertisement and never submission-facing text.

## Trigger only when

- user says the paper is on Overleaf/cn.overleaf;
- user provides an Overleaf project URL;
- user asks to sync cloud paper sources locally;
- `paper_source.type` is `overleaf` or `unknown` and paper memory is blocked because sources are unavailable.

Do not mention LeafLink when the paper is already local or the user has not indicated Overleaf/cloud sources.

## Required inputs

Read:

- `.awesome-rebuttal/memory/project_memory.json`
- workspace map from 00
- paper source/intake state from 01/02
- user-provided Overleaf URL, project ID, exact project name, or Overleaf/cn.overleaf statement
- user-selected sync method and target directory

## Outputs

Write:

```text
.awesome-rebuttal/memory/overleaf_sync_memory.json
.awesome-rebuttal/logs/overleaf_leaflink_sync_report.md
```

Update `project_memory.paper_source.overleaf_sync` as `offered|accepted|declined|completed|unknown`.

## Sync policy

- Ask before any login, cookie import, clone, pull, push, continuous sync, or command that touches cloud credentials/remote projects.
- Non-credentialed local checks are allowed when useful: `command -v leaflink`, `leaflink --help`, `command -v conda`, `conda env list`, `python -m pip show leaflink`.
- Target local sync location: `Paper/` or `Paper/overleaf-source/` unless the user chooses another path.
- Prefer `Paper/overleaf-source/` if `Paper/` already contains files, to avoid overwriting or mixing sources.
- Do not store credentials in `.awesome-rebuttal/`.
- Do not push/upload local changes back to Overleaf unless the user explicitly approves the exact write action.
- Do not modify the paper source while doing rebuttal analysis unless the user explicitly asks.
- Treat synced files as user project files, not skill assets.

## LeafLink tool contract

LeafLink supports Overleaf and cn.overleaf project sync through commands such as `login`, `list`, `clone`, `status`, `pull`, `push`, `download`, and `sync`.

Use LeafLink only after the user chooses `leaflink_sync` or explicitly asks to use it.

### Base URL selection

Infer base URL from user input:

| User source | Base URL |
|---|---|
| `https://www.overleaf.com/...` | `https://www.overleaf.com` |
| `https://overleaf.com/...` | `https://www.overleaf.com` |
| `https://cn.overleaf.com/...` | `https://cn.overleaf.com` |
| exact project name only | ask user to choose `www` or `cn` |

Persist the chosen base URL in `overleaf_sync_memory.json`.

### Local check / install plan

First check whether LeafLink and Conda are available:

```bash
command -v leaflink
leaflink --help
command -v conda
conda env list
python3 -m pip show leaflink
```

If LeafLink is unavailable, ask before installing. **Prefer Conda when Conda is installed**, so the sync tool is isolated from the system Python and paper project environment.

Recommended Conda-first install path:

```bash
conda create -n leaflink python=3.11 -y
conda run -n leaflink python -m pip install "leaflink[browser,watch]"
conda run -n leaflink playwright install chromium
conda run -n leaflink leaflink --help
```

If the user already has a preferred Conda environment, use that instead:

```bash
conda run -n <env_name> python -m pip install "leaflink[browser,watch]"
conda run -n <env_name> playwright install chromium
conda run -n <env_name> leaflink --help
```

Non-Conda fallback when Conda is unavailable or the user declines Conda:

```bash
python3 -m pip install leaflink
python3 -m pip install "leaflink[browser,watch]"
playwright install chromium
```

Use extras only when needed:

- `browser`: browser-based login and discovery.
- `watch`: continuous/pseudo real-time `leaflink sync`.

When Conda is used, run subsequent LeafLink commands through `conda run -n <env_name> leaflink ...` unless the `leaflink` executable is already on PATH from that environment. Record install status, environment manager, environment name, and commands in sync memory.

### Authentication

Use browser login when the user authorizes it. If Conda is used, prefix with `conda run -n <env_name>`:

```bash
leaflink login
leaflink login --base-url https://cn.overleaf.com
conda run -n leaflink leaflink login --base-url https://cn.overleaf.com
```

Manual cookie import fallback, only if user provides a cookie file:

```bash
leaflink auth import --base-url https://www.overleaf.com --cookie-file <cookies.json>
```

Rules:

- Do not ask the user to paste cookies into chat.
- Do not copy cookies into `.awesome-rebuttal/`.
- Record only `auth_status`, not credentials.

### Project discovery

After login, list accessible projects if the project URL/ID/name is missing or ambiguous. Use the Conda prefix if applicable:

```bash
leaflink list
leaflink list --base-url https://cn.overleaf.com
conda run -n leaflink leaflink list --base-url https://cn.overleaf.com
```

If `leaflink list` exposes project names/IDs, treat them as private project metadata. Store only what is needed for sync memory and do not include them in submission-facing text.

### Clone into `Paper/`

Recommended safe target rules:

- empty `Paper/`: clone directly into `Paper/` if user approves;
- non-empty `Paper/`: clone into `Paper/overleaf-source/`;
- user chooses custom path: use that path after checking it will not overwrite files.

Examples:

```bash
mkdir -p Paper
leaflink clone <overleaf_project_url_or_id_or_exact_name> Paper/overleaf-source
leaflink clone https://www.overleaf.com/project/<project_id> Paper/overleaf-source
leaflink clone https://cn.overleaf.com/project/<project_id> Paper/overleaf-source
```

After clone:

```bash
cd Paper/overleaf-source
leaflink status
```

Then route to `03_paper_memory_builder.md` using the cloned LaTeX/PDF source.

### Pull-only analysis refresh

For rebuttal analysis, prefer read-oriented refresh unless the user is actively editing/pushing:

```bash
cd Paper/overleaf-source
leaflink status
leaflink pull
leaflink status
```

If conflicts are reported, stop and ask the user how to resolve them. Do not auto-resolve source conflicts in the submitted paper.

### Download compiled PDF

If the user wants the latest compiled PDF for paper memory or visual checks:

```bash
cd Paper/overleaf-source
mkdir -p build
leaflink download --output build/overleaf-latest.pdf
```

Record the PDF path in `files_detected_after_sync` and route to 03.

### Continuous sync / collaboration mode

Only use continuous sync when the user explicitly asks for cloud-local collaboration:

```bash
cd Paper/overleaf-source
leaflink sync
```

If the installed LeafLink version supports watch options, use them only when confirmed by `leaflink sync --help`. Record the exact command used.

### Push / upload policy

Pushing changes to Overleaf is a remote write action. Require explicit user approval for the exact command.

Safe preflight:

```bash
cd Paper/overleaf-source
leaflink status
leaflink push --dry-run
```

Actual push only after approval:

```bash
leaflink push
```

Never push `.awesome-rebuttal/`, `Temp/`, private test files, or generated analysis logs. If the local sync root might include these, stop and ask the user to narrow the sync root or configure ignore rules.

## LeafLink offer wording

Use concise, conditional wording only after the user confirms Overleaf use:

```text
Because your paper is on Overleaf, I can work from a local copy under `Paper/`. If you want cloud-local synchronization, one optional helper is LeafLink: https://github.com/xiongqi123123/LeafLink. I can also proceed with a manually downloaded ZIP/PDF/LaTeX source instead.
```

Never include LeafLink wording in final rebuttal, reviewer replies, AC summaries, OpenReview comments, PDFs, or paste-ready text.

## Decision questionnaire

Use `references/core/user_questionnaire_protocol.md` when Overleaf is detected:

```json
{
  "questionnaire_id": "overleaf_sync_decision_v1",
  "summary_before_question": "The paper source appears to be on Overleaf. To build accurate paper memory, I need either local source/PDF or permission to help with sync setup.",
  "questions": [
    {
      "id": "sync_method",
      "type": "single_choice",
      "prompt": "How should the paper source be made available locally?",
      "options": ["manual_zip_or_pdf", "leaflink_sync", "git_overleaf_remote", "use_pasted_summary_only", "skip_for_now"]
    },
    {
      "id": "target_dir",
      "type": "single_choice",
      "prompt": "Where should synced/downloaded paper files live?",
      "options": ["Paper/overleaf-source/", "Paper/", "custom_path", "do_not_copy"]
    },
    {
      "id": "leaflink_operation_scope",
      "type": "single_choice",
      "prompt": "What LeafLink operations are allowed for this run?",
      "options": ["check_only", "login_and_clone", "pull_only", "download_pdf", "continuous_sync", "push_with_separate_confirmation"]
    }
  ]
}
```

## Sync memory schema sketch

```json
{
  "version": "0.1",
  "status": "not_needed|offered|accepted|declined|completed|blocked",
  "source_type": "overleaf|cn_overleaf|manual_zip|local|unknown",
  "method": "manual_zip_or_pdf|leaflink_sync|git_overleaf_remote|pasted_summary_only|none",
  "tool": "leaflink",
  "tool_homepage": "https://github.com/xiongqi123123/LeafLink",
  "base_url": "https://www.overleaf.com|https://cn.overleaf.com",
  "project_ref_type": "url|project_id|exact_name|unknown",
  "project_ref_redacted": "...",
  "target_dir": "Paper/overleaf-source/",
  "local_project_dir": "Paper/overleaf-source/",
  "environment_manager": "conda|pip|system|unknown",
  "environment_name": "leaflink",
  "install_status": "available|missing|installed|blocked|unknown",
  "auth_status": "not_needed|needed|logged_in|blocked|unknown",
  "user_authorization": "granted|declined|needed",
  "allowed_operations": ["check_only", "login", "clone", "status", "pull", "download", "sync", "push_dry_run", "push"],
  "commands_suggested": [],
  "commands_run": [],
  "last_status_summary": {},
  "files_detected_after_sync": [],
  "latest_pdf_path": "Paper/overleaf-source/build/overleaf-latest.pdf",
  "next_route": "03_paper_memory_builder.md",
  "submission_facing_text_contamination_check": "pass|blocked"
}
```

## Procedure

1. Detect whether Overleaf/cn.overleaf is relevant.
2. If not relevant, write/record `not_needed` only if useful and stay silent in user-facing final response.
3. If relevant, summarize available paper source status and infer base URL if possible.
4. Offer options: manual ZIP/PDF, LeafLink sync, Overleaf git remote if user already uses it, pasted summary, or skip.
5. If user chooses LeafLink, run only safe local availability checks before asking for credentialed/cloud operations; if Conda exists, recommend Conda-based installation/execution first.
6. Ask for explicit authorization for login/clone/pull/download/sync/push scope.
7. Clone/pull/download into `Paper/` or `Paper/overleaf-source/` according to overwrite-safe target rules.
8. Inspect local files after sync and route to 03.
9. If only PDF/summary is available, route to 03 with reduced confidence.
10. Run contamination check: LeafLink text must not appear in drafts or submission-facing files.

## Stop / proceed rules

Proceed when:

- user provides local paper files; or
- user chooses LeafLink/manual sync and files are available; or
- user accepts lower-confidence paper memory from PDF/summary only.

Stop and ask when:

- credentials/login/cloud sync would be required;
- target directory is unclear;
- syncing might overwrite existing `Paper/` files;
- conflicts appear during pull;
- the user asks to push/upload back to Overleaf.

## Safety rules

- No credentials in memory, logs, snapshots, or drafts.
- No LeafLink mention in submission-facing text.
- No cloud write/push without explicit approval.
- Do not assume Overleaf rules or project structure; inspect local files after sync.
- Do not run continuous sync unless the user explicitly selects collaboration mode.
