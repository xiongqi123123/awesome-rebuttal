# DEVELOPMENT_LOG.md

## Current requirement snapshot

- Project: `awesome-rebuttal`
- Version target: V1 skeleton
- Architecture: project-level layered skill, one atomic capability per reference file, thin `SKILL.md` router.
- Runtime workspace convention: `Code/`, `Paper/`, `Reference/`, `Temp/`.
- Memory model: JSON project/paper/code/review/venue/strategy/snapshot schemas.
- Versioning modes: manual Git, auto Git, markdown snapshot-only.
- Overleaf support: conditional LeafLink sync helper when user uses cloud Overleaf.

## Completed

- Deep interview requirements captured in `.omx/specs/deep-interview-awesome-rebuttal.md`.
- Development roadmap captured in `.omx/plans/awesome-rebuttal-v1-roadmap.md`.
- Skill scaffold initialized with `skill-creator`.
- Thin `SKILL.md` router written.
- Atomic capabilities, templates, strategy library, memory schemas, synthetic examples, and manual checklists created.
- Validation passed with `quick_validate.py` in a local `.venv`; JSON schemas parse successfully.
- Upgraded `00_workspace_bootstrap.md` and `01_intake_gate.md` with high-detail procedures, questionnaires, memory fields, stop/proceed rules, and quality gates.
- Added shared questionnaire protocol at `awesome-rebuttal/references/core/user_questionnaire_protocol.md` and linked it from `SKILL.md`.

## TODO

- Forward-test the upgraded bootstrap/intake flow on empty, canonical, messy, and Overleaf workspaces.
- Add richer synthetic review packets, not just example READMEs.
- Decide whether to add deterministic helper scripts for schema validation or workspace bootstrap.
- Expand README with installation instructions after target distribution path is decided.

## Suggested next commit message

```text
Make rebuttal state workspace-local and add template handling

Constraint: Skill must work as a global install while storing runtime state inside each active rebuttal workspace.
Rejected: Store memory/templates in the installed skill folder | breaks project isolation and portability
Confidence: high
Scope-risk: moderate
Directive: Treat the built-in one-page template as fallback only, never as official venue truth.
Tested: skill validation, JSON schema parsing, local ignored smoke workspace template compile
Not-tested: user-supplied official <venue> one-page PDF rules/template
```

## Architecture update: global install + project-local state

- The skill is now designed to be globally installable while creating `.awesome-rebuttal/` inside each active workspace.
- Runtime memory, snapshots, logs, and active templates should live under `.awesome-rebuttal/`.
- Added LaTeX environment detection to workspace bootstrap.
- Added `17_rebuttal_template_manager.md` for official/fetched/fallback rebuttal templates.
- Imported `OnePage_Rebuttal_Template` into `awesome-rebuttal/assets/one-page-rebuttal-template/` as the built-in fallback one-page template.
- Forward-tested capability 00 state creation and fallback template compilation in a local ignored smoke workspace.
- Upgraded `03_paper_memory_builder.md` from a short claim checklist into a detailed paper-story, experiment, result, terminology, and rebuttal-hook memory builder.
- Upgraded `04_code_memory_builder.md` into a detailed implementation-architecture, innovation insertion point, config/hyperparameter, entrypoint, feasibility, and reproducibility memory builder.
- Refactored review handling into three layers: 05 neutral review index, 06 semantic review concern analysis, and 07 priority/situation analysis.
- Upgraded `08_strategy_planner.md` to select an evidence-first strategy lens from the actual review pattern, then plan top focused problems, reviewer/concern goals, handoffs, and coverage.

## Snapshot capability update

- Upgraded `09_snapshot_maker.md` into a two-reader checkpoint system:
  - canonical `.awesome-rebuttal/snapshots/snapshot_memory.json` for skill reloads
  - generated `.awesome-rebuttal/snapshots/REBUTTAL_SNAPSHOT.md` or `PROJECT_SNAPSHOT.md` for user reading
- Added consistency rules: JSON is the source of truth, Markdown is generated from JSON, timestamps include timezone, and history is newest-first.
- Added `awesome-rebuttal/scripts/render_snapshot.py` to render/check Markdown from the canonical JSON without new dependencies.
- Expanded `snapshots.schema.json`, snapshot template, versioning notes, and manual checklists to match the new contract.

## Suggested next commit message

```text
Make snapshots reloadable and user-readable from one source

Constraint: Snapshot state must be detailed enough for skill reloads but concise enough for users to scan.
Rejected: Hand-maintained Markdown snapshot | would drift from machine-readable state and create conflicting progress facts
Confidence: high
Scope-risk: narrow
Directive: Treat `snapshot_memory.json` as canonical and regenerate Markdown rather than editing it manually.
Tested: skill validation, JSON schema parsing, snapshot renderer write/check smoke test, private-marker grep
Not-tested: long real-world multi-day snapshot history rendering
```

## Experiment/strategy ordering update

- Reordered the standard workflow so review-driven experiment planning runs after 06 and before final strategy planning.
- Upgraded `10_experiment_triage.md` into a numbered `EXP-*` experiment memory builder that writes `.awesome-rebuttal/memory/experiment_memory.json`.
- Updated 07 to consume experiment memory for evidence-gap feasibility and priority links.
- Updated 08 to consume numbered experiment candidates, map experiments to focused problems/reviewer concerns, and ask a strategy decision questionnaire before locking strategy.
- Added `experiment_memory.schema.json` and expanded strategy schema/checklists accordingly.

## Suggested next commit message

```text
Make experiment planning feed strategy decisions

Constraint: Rebuttal strategy should decide from review-derived experiment options before drafting, not invent experiment needs late.
Rejected: Keep experiments after strategy only | prevents 08 from mapping approved EXP IDs to reviewer concerns and user decisions
Confidence: high
Scope-risk: moderate
Directive: Run 10 after 06 and before final 08; treat experiment recommendations as provisional until the user answers the questionnaire.
Tested: skill validation, JSON schema parsing, snapshot renderer py_compile, private-marker grep
Not-tested: real experiment execution or result ingestion
```

## Response writer update

- Upgraded `11_response_writer.md` into an evidence-aligned drafting capability that balances pushback, clarification, and narrow concessions.
- Added pre-draft alignment gates across review, paper, code/results, strategy, and venue rules.
- Added numeric/data correctness policy, response unit cards, limited-space compression rules, and draft-lock questionnaires.
- Added `.awesome-rebuttal/memory/response_memory.json` plus `.awesome-rebuttal/drafts/` as skill-owned drafting outputs.
- Updated unified/per-reviewer response templates, project memory schema, snapshot/safety references, and acceptance checklists.
- Used the provided ECCV rebuttal file only for generic structural calibration; no paper-specific content was copied into tracked skill files.

## Suggested next commit message

```text
Make response drafting evidence-aligned and concise

Constraint: Rebuttal prose must balance professional pushback with narrow concessions while staying aligned with paper, code, reviews, and venue limits.
Rejected: Draft directly from reviewer comments | risks unsupported arguments, over-apology, and paper/code/review inconsistency
Confidence: high
Scope-risk: moderate
Directive: Build response units and verify numeric claims before paste-ready prose; never copy private example content into the skill.
Tested: skill validation, JSON schema parsing, diff check, private/example marker grep
Not-tested: full one-page LaTeX render with a real response draft
```

## AC summary writer update

- Upgraded `13_ac_summary_writer.md` into an AC-facing factual synthesis capability for split reviews and low-score context.
- Added the core structure: thank AC/reviewers, borrow verified shared positive assessments, summarize decision-critical concerns, then contextualize low-score rationale with evidence without attacking or ranking reviewers.
- Added venue-rule gating, AC fact ledger, low-score handling model, user confirmation questionnaire, draft variants, and safety checks.
- Added `.awesome-rebuttal/memory/ac_summary_memory.json` schema and expanded the AC summary template/checklists.
- Used the user's ECCV wording only to abstract structure and tone; no paper-specific content or reviewer IDs were copied into tracked skill files.

## Suggested next commit message

```text
Make AC summaries factual and low-score-aware

Constraint: AC-facing text must contextualize low-score concerns using verified review evidence without attacking reviewers or lobbying the AC.
Rejected: Generic thank-you summary | misses the decision-critical purpose of resolving split/low-score meta-review risk
Confidence: high
Scope-risk: moderate
Directive: Use shared positive reviewer facts as context, not as reviewer ranking; block paste-ready summaries when rules or evidence are unconfirmed.
Tested: skill validation, JSON schema parsing, diff check, private/example marker grep
Not-tested: live venue-specific AC-summary rule confirmation
```

## Template, safety, sync, versioning completion

- Completed `12_template_designer.md` with format-aware layouts for one-page PDF, per-reviewer Markdown, global Markdown, hybrid, and Markdown+LaTeX comment outputs.
- Completed `14_safety_rule_checker.md` as the final paste/PDF safety gate with provenance, experiment-result, commitment, coverage, rule, tone, privacy, consistency, and TODO checks.
- Completed `15_overleaf_leaflink_sync.md` as a conditional Overleaf source helper; LeafLink is offered only when relevant and is blocked from submission-facing text.
- Completed `16_rebuttal_versioning.md` with manual Git, auto Git, and snapshot-only modes plus safe Git boundaries and Lore commit guidance.
- Completed `17_rebuttal_template_manager.md` with source priority and layout scaffolding for fallback one-page LaTeX, per-reviewer Markdown, global Markdown, and Markdown+LaTeX hybrid comments.
- Added schemas for safety, Overleaf sync, and versioning memory; expanded template/project schemas and safety checklist.

## Suggested next commit message

```text
Finish output layout, safety, sync, and versioning capabilities

Constraint: Rebuttal outputs must match confirmed venue formats without leaking helper/tooling text or bypassing safety checks.
Rejected: Single generic response template | cannot support one-page PDF, threaded reviewer replies, and OpenReview-style Markdown/LaTeX comments safely
Confidence: high
Scope-risk: broad
Directive: Treat venue rules as confirmed runtime input; never present fallback templates as official or paste text before 14 passes.
Tested: skill validation, JSON schema parsing, diff check, private/example marker grep
Not-tested: live OpenReview rendering or real Overleaf sync
```

## LeafLink tool-call integration update

- Expanded `15_overleaf_leaflink_sync.md` from a conditional mention into a concrete LeafLink tool integration.
- Added command flows for availability checks, install planning, browser login, cookie import fallback, project listing, clone, status, pull, PDF download, continuous sync, push dry-run, and push with explicit authorization.
- Added base URL selection for overleaf.com vs cn.overleaf.com, safe target directory rules, credential boundaries, conflict stop rules, and contamination checks.
- Expanded `overleaf_sync_memory.schema.json` and acceptance checks to record tool state, command plans, local dirs, and latest PDF paths.

## Suggested next commit message

```text
Make LeafLink an explicit Overleaf sync tool path

Constraint: Overleaf sync support needs actionable LeafLink commands while keeping credentialed/cloud-write operations user-approved.
Rejected: Mention LeafLink only as a link | does not let the skill operate as a tool-integration workflow
Confidence: high
Scope-risk: narrow
Directive: Run only local checks without approval; login, clone, pull, sync, download, and push require explicit user scope.
Tested: skill validation, JSON schema parsing, diff check, private/example marker grep
Not-tested: live LeafLink login/clone against an Overleaf project
```

## LeafLink Conda preference update

- Updated `15_overleaf_leaflink_sync.md` to prefer Conda when Conda is available for LeafLink installation/execution.
- Added Conda checks, `conda create -n leaflink`, `conda run -n leaflink ...` command patterns, and non-Conda pip fallback.
- Expanded `overleaf_sync_memory.schema.json` to record environment manager and environment name.

## Suggested next commit message

```text
Prefer Conda for LeafLink tool setup

Constraint: LeafLink should be isolated from system Python when Conda is available.
Rejected: Pip-only install path | can pollute the user/system Python environment and ignores available Conda isolation
Confidence: high
Scope-risk: narrow
Directive: Use Conda-first command patterns for LeafLink when Conda exists, with pip fallback only when Conda is unavailable or declined.
Tested: skill validation, JSON schema parsing, diff check, private/example marker grep
Not-tested: actual Conda environment creation or LeafLink login
```

## Response-mode, venue-rule schema, and language policy update

- Standardized runtime response mode vocabulary across the main skill, intake, response writing, template management, template design, and memory schemas.
- Strengthened `venue_rules.schema.json` into a global venue-rule memory contract covering source/confirmation, canonical response mode, platform/limits, response permissions, formatting, content permissions, anonymity, and language policy.
- Added a global language policy: interactive analysis follows the user's language by default, while submission-facing rebuttal prose/comments/PDF text are drafted in English unless confirmed venue rules allow another choice.
- Expanded project/response memory schemas and acceptance checks so mode normalization, rule confirmation, and output-language behavior are testable.

## Suggested next commit message

```text
Normalize response modes and venue rule memory

Constraint: Runtime memories need one response-mode vocabulary and venue rules must capture enough confirmed constraints to gate drafting safely.
Rejected: Keep mode aliases across schemas | causes handoff mismatch between intake, templates, response writing, and safety checks
Confidence: high
Scope-risk: moderate
Directive: Normalize user wording into canonical response_mode values and default final submission prose to English.
Tested: skill validation, JSON schema parsing, diff check, private/example marker grep
Not-tested: live venue-rule ingestion from official conference pages
```

## AI-agent installation guide

- Added `AI_AGENT_INSTALL.md`, a no-Python-installer guide intended for users to paste into an AI coding assistant with the repository URL.
- Covered Codex skill install, Claude Code skill install/fallback project adapter, Cursor project rule adapter, workspace preparation, environment checks, optional LaTeX guidance, and optional Conda-first LeafLink setup.
- Documented that questionnaire-style choices require no external dependency; native UI forms may be used when available, otherwise plain Markdown choices are sufficient.
- Linked the guide from `README.md`.

## Suggested next commit message

```text
Document AI-agent installation paths

Constraint: Users should be able to hand the repo URL to an AI assistant without relying on a custom installer script.
Rejected: Python installer | user requested a plain model-readable installation guide only
Confidence: high
Scope-risk: narrow
Directive: Keep installation instructions safe, non-destructive, and adapter-based across Codex, Claude Code, and Cursor.
Tested: skill validation, diff check, private/example marker grep
Not-tested: live installation inside fresh Codex/Claude/Cursor environments
```

## Publish-root consolidation

- Moved release-facing docs, license, gitignore, development log, project memory, and checks into the inner `awesome-rebuttal/` package directory.
- Rewrote `AI_AGENT_INSTALL.md` so the published repository root is the skill package root containing `SKILL.md` directly.
- Updated README and memory paths to avoid treating the outer development workspace as the published project.

## Suggested next commit message

```text
Make the inner skill package the publish root

Constraint: The publishable repository is the inner awesome-rebuttal package, not the outer development workspace.
Rejected: Keep install docs at the outer root | causes agents to copy the wrong directory during installation
Confidence: high
Scope-risk: moderate
Directive: Treat the directory containing SKILL.md as the package and git root for releases.
Tested: skill validation, JSON schema parsing, diff check, private/example marker grep
Not-tested: fresh clone from the eventual published repository URL
```
