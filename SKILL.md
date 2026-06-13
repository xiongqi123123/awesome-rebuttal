---
name: awesome-rebuttal
description: Global-installable, project-level academic rebuttal strategy skill for AI/ML/CV/NLP/Robotics papers. Use when authors need a workspace-local .awesome-rebuttal state folder, paper/code/review/venue-rule intake, JSON memory, snapshots, LaTeX/template handling for one-page rebuttals, reviewer stance analysis, strategy planning, experiment triage, safe author response drafting, or AC summaries under confirmed venue rules.
---

# Awesome Rebuttal

Use this skill as a **global-installable, project-level rebuttal workspace assistant**. The installed skill provides reusable procedures and assets; each actual paper/rebuttal workspace gets its own `.awesome-rebuttal/` state folder for memory, snapshots, template state, and logs. Start by understanding the workspace, then collect evidence, persist memory, analyze strategy, and only then draft response text.

## Operating contract

1. Inspect the current workspace before content analysis.
2. Create or use a project-local `.awesome-rebuttal/` state folder; never store runtime memory in the installed skill folder.
3. If the workspace is empty, organize or recommend `Code/`, `Paper/`, `Reference/`, and `Temp/`.
4. If the workspace already contains files, infer the author's organization and adapt non-destructively.
5. Ask how progress should be preserved: `manual_git`, `auto_git`, or `markdown_snapshot_only`.
6. Run the intake gate before analysis. Missing required inputs block drafting.
7. Treat venue rules as user-provided or AI-searched + user-confirmed; never rely on stale built-in venue rules.
8. Keep every factual claim grounded in `paper`, `code`, `review`, `venue_rules`, `user`, or explicit `inference`.
9. Never invent experiments, numbers, citations, reviewer positions, or venue permissions.


## Language policy

- Interaction language: follow the user's language by default for questions, analysis reports, progress updates, and explanations.
- Submission language: final rebuttal artifacts must be written in English unless the user explicitly requests another submission language and the venue permits it.
- Memory: record this choice in `project_memory.language_policy` and mirror any venue-specific exception in `venue_rules.language_policy`.
- Drafting rule: `11_response_writer.md`, `12_template_designer.md`, and `13_ac_summary_writer.md` may discuss plans in the user's language, but author-response text, reviewer replies, AC summaries, OpenReview comments, and PDF rebuttal prose default to English.
- Terminology: preserve exact technical terms, metric names, method names, dataset names, and reviewer wording from the paper/reviews; translate only surrounding explanatory prose when needed.
- If the user provides Chinese strategy notes, convert them into professional English rebuttal prose rather than literal translation.

## Shared questionnaire protocol

Whenever the skill hits missing, ambiguous, or confirmation-dependent information, first summarize what the user already provided and what the workspace evidence shows. Then ask a focused questionnaire instead of guessing.

Read `references/core/user_questionnaire_protocol.md` for the reusable questionnaire pattern. Use it especially in workspace bootstrap and intake, and reuse it later for venue-rule confirmation, experiment feasibility, versioning mode, or any strategy decision that materially changes the output.

Prefer structured choices when possible:

- single-choice for mutually exclusive paths
- multi-select for available inputs or constraints
- short text for pasted rules, reviews, paths, or URLs
- confirmation for inferred workspace maps or AI-found venue rules

Ask only for the smallest missing decision set needed for the next safe step.


## Canonical response modes

Use these exact `response_mode` values across all memory files and capability handoffs:

- `openreview_per_reviewer` — one reply/comment per reviewer thread.
- `unified_limited` — one limited unified response where concerns are merged.
- `pdf_one_page` — one-page PDF/LaTeX rebuttal.
- `global_comment` — one global platform comment/text box.
- `hybrid` — global summary plus per-reviewer replies.
- `openreview_markdown_latex` — OpenReview-style Markdown comment with lightweight LaTeX math.
- `unknown` — not confirmed yet.

Do not introduce aliases such as `per_reviewer`, `global`, `global_text`, `one_page_pdf`, or `markdown_latex_hybrid` in new memory. If user wording uses those terms, normalize to the canonical value and record the original wording in notes if useful.

## Venue rules schema contract

Use `references/memory-schemas/venue_rules.schema.json` as the global rule-memory contract. Venue rules are runtime evidence, not built-in knowledge.

Every `venue_rules.json` should separate:

- `status` and `source`: missing/user-provided/AI-found-pending-confirmation plus URL/path/retrieval notes.
- `response`: canonical `mode`, platform, limits, per-reviewer/global/interactive/AC-summary permissions.
- `formatting`: official template, PDF/LaTeX/Markdown support, figures/tables/appendix, and page-layout constraints.
- `content_permissions`: new experiments/results, links, supplements, code links, references, revision commitments.
- `anonymity`: anonymous requirement, self-citation, acknowledgements, and identity-risk notes.
- `confirmation`: user confirmation timestamp, pending questions, and conflicts.
- `language_policy`: interaction language follows user; final submission-facing prose defaults to English.

If rules are AI-searched, keep `status: ai_found_pending_confirmation` until the user confirms them. Unknown fields stay `unknown`; do not infer permissions silently.

## Required workflow

Follow this order unless the user asks for a narrower capability:

1. **Workspace bootstrap** — read `references/capabilities/00_workspace_bootstrap.md`; create/use `.awesome-rebuttal/`, detect LaTeX environment, and if decisions are missing use `references/core/user_questionnaire_protocol.md`.
2. **Intake gate** — read `references/capabilities/01_intake_gate.md`; parse user-provided context first, then ask a questionnaire for blockers.
3. **Template management** — read `17_rebuttal_template_manager.md` after intake when response format requires a `pdf_one_page` template, `openreview_per_reviewer` Markdown scaffolds, `global_comment` Markdown, or `openreview_markdown_latex` comments.
4. **Information collection** — read `references/capabilities/02_information_collection.md`.
5. **Paper/code memory** — read `03_paper_memory_builder.md` and/or `04_code_memory_builder.md` when paper or code context is present.
6. **Review indexing** — read `05_review_normalizer.md`; preserve raw reviews, build raw anchors, issue item index, and common issue index without strategic analysis.
7. **Review concern analysis** — read `06_situation_analyzer.md`; interpret indexed concerns semantically without priority ranking.
8. **Review-driven experiment planning** — read `10_experiment_triage.md`; generate numbered `EXP-*` experiment candidates from reviewer concerns and persist `experiment_memory.json` before final strategy planning.
9. **Priority and situation analysis** — read `07_concern_atomizer.md`; rank concern importance, classify rebuttal posture, build reviewer priority map, link P0/P1 evidence gaps to numbered experiments, and identify AC-facing decision facts.
10. **Strategy planning** — read `08_strategy_planner.md`; combine priority analysis, experiment memory, paper/code evidence, venue constraints, and user decisions. Use a questionnaire for strategy/experiment trade-offs before locking the plan.
11. **Snapshots/versioning** — read `09_snapshot_maker.md` and `16_rebuttal_versioning.md` at each durable checkpoint.
12. **Writing** — read `11_response_writer.md`, `13_ac_summary_writer.md`, and `12_template_designer.md` only after strategy is evidence-backed and user-approved; 12 selects `pdf_one_page`, `openreview_per_reviewer`, `global_comment`, `hybrid`, or `openreview_markdown_latex` layout.
13. **Rehearsal** — read `18_rebuttal_rehearsal.md` once a draft exists; simulate reviewer/AC personas reading paper-vs-rebuttal in isolation, then route hardening back to 11/13. Advisory only; it never approves submission.
14. **Safety gate** — read `14_safety_rule_checker.md` before any final or paste-ready text/PDF/comment.
15. **Discussion rounds** — read `19_discussion_round_handler.md` after the first rebuttal is submitted; ingest reviewer/AC follow-up replies, track score/engagement per round, draft delta-only follow-ups (reusing the 18 answer bank), and route each through 14 before posting.
16. **Overleaf sync** — read `15_overleaf_leaflink_sync.md` only when the paper is on Overleaf/cn.overleaf or the user asks about cloud/local synchronization.

Read only the capability files needed for the current request.

## Core outputs

A complete strategy-first run should produce:

- Intake completeness report
- workspace-local `.awesome-rebuttal/memory/*.json` for project, paper, code, reviews, experiments, strategy, responses, templates, AC summaries, safety, versioning, and optional Overleaf sync
- Reviewer stance map
- Atomic concern ledger
- Common concern clusters
- Response strategy matrix
- Numbered review-driven experiment memory and triage (`EXP-*`)
- Format-aware response blueprint and evidence-aligned response draft
- Coverage map from reviewer concerns to response units
- Rehearsal findings from simulated reviewer/AC personas, with a prioritized hardening list and an anticipated follow-up answer bank
- Multi-round discussion state: reviewer engagement/score tracker, per-thread decisions, and delta-only follow-up drafts gated by safety
- Optional AC summary decision, fact ledger, and draft when rules allow
- Rule/safety checklist and `safety_memory.json` final gate
- Rebuttal template report and active template copy when template-based response is needed
- Canonical `.awesome-rebuttal/snapshots/snapshot_memory.json` plus generated user Markdown snapshot, or git checkpoint according to the selected versioning mode


## Project-local state folder

For each actual rebuttal workspace, create or use:

```text
.awesome-rebuttal/
├── memory/      # project/paper/code/review/experiment/strategy/response/template/rehearsal/discussion/safety/versioning memory
├── drafts/      # response blueprints, drafts, and coverage maps
├── snapshots/   # JSON and markdown reload snapshots
├── templates/   # active rebuttal templates copied/adapted for this project
├── logs/        # rule-search, compile, and validation logs
└── cache/       # disposable skill cache; safe to regenerate
```

The installed/global skill folder contains reusable instructions and assets only. Runtime memory, snapshots, fetched templates, and logs belong in the current workspace's `.awesome-rebuttal/` folder.

## Workspace convention

Recommended runtime workspace:

```text
<rebuttal-workspace>/
├── Code/        # code, scripts, configs, reproduced outputs
├── Paper/       # paper PDF/LaTeX; Overleaf sync target if used
├── Reference/   # reviews, venue rules, reference papers, notes
└── Temp/        # temporary extraction, scratch drafts, search/cache outputs
```

Do not force this layout on an existing organized workspace. Map existing paths and record them in project memory.

## Progress preservation modes

Ask the user to choose one:

- `manual_git`: suggest checkpoint boundaries and commit messages; do not commit unless explicitly asked.
- `auto_git`: create local milestone commits only; no push, history rewrite, or destructive git operations without explicit instruction.
- `markdown_snapshot_only`: maintain `.awesome-rebuttal/snapshots/snapshot_memory.json` as the canonical reload entry and render `.awesome-rebuttal/snapshots/REBUTTAL_SNAPSHOT.md` or `.awesome-rebuttal/snapshots/PROJECT_SNAPSHOT.md` as the user-readable progress summary.


## LaTeX environment policy

During workspace bootstrap, detect whether a local LaTeX toolchain is available (`latexmk`, `pdflatex`, `xelatex`, `lualatex`, `bibtex`/`biber`, `kpsewhich`, or `tectonic`). If no compiler is available and a PDF rebuttal is needed, ask the user to choose a setup path for their platform: MacTeX/BasicTeX on macOS, TeX Live on Linux, MiKTeX/TeX Live on Windows, Tectonic, Overleaf-only compilation, or skip local compilation for now.

## Overleaf / LeafLink policy

LeafLink is not an advertisement. It is a conditional helper for authors whose paper is on cloud Overleaf.

- Ask whether the paper is on Overleaf/cn.overleaf.
- If yes, offer LeafLink as an optional way to sync the project into `Paper/`: https://github.com/xiongqi123123/LeafLink
- If no, stay silent and use local paper files.
- Never include LeafLink text in final rebuttal, reviewer replies, AC summaries, or conference-submission-facing text.

## Safety gates

Block finalization if any of these fail:

1. **Provenance gate** — every factual statement has a source.
2. **Commitment gate** — every promise is already done, explicitly approved, or framed as future work.
3. **Coverage gate** — every reviewer concern is answered, intentionally deferred, or marked `needs_user_input`.
4. **Venue-rule gate** — format/links/supplementary claims are allowed by confirmed rules.
5. **Tone gate** — no reviewer attacks, defensiveness, flattery manipulation, or unprofessional phrasing.
