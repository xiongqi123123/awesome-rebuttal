# memory.md

## Confirmed product direction

`awesome-rebuttal` is a project-level, strategy-first rebuttal skill for AI/ML/CV/NLP/Robotics papers.

## Durable decisions

- Published repository/package root is the inner skill directory containing `SKILL.md` directly; the outer workspace is development-only.

- Built-in fallback template lives at `assets/one-page-rebuttal-template/` and must not be presented as official.

- Paper memory must capture the story/narrative spine, logic chain, contributions, claim-evidence map, method components, experiment matrix, exact result ledger, figure/table index, domain terminology, limitations, and rebuttal relevance hooks.

- Code memory must capture overall architecture, innovation implementation/insertion points, files/classes/functions, config and hyperparameter controls, train/eval entrypoints, dataset/evaluation pipeline, experiment feasibility, reproducibility risks, and paper claim-code links when paper memory exists.

- Review handling is split into three layers: 05 preserves raw reviews and builds issue/common-issue indexes without strategic labels; 06 performs semantic concern analysis without priority; 07 handles priority, importance, rebuttal posture, reviewer priority map, AC facts, and evidence gap urgency.

- Experiment planning now runs after 06 and before final 08: 10 creates numbered `EXP-*` candidates in `experiment_memory.json`, 07 can use them for evidence-gap priority, and 08 maps user-approved/deferred/rejected experiments into strategy.

- 08 must present recommended strategy/experiment trade-offs and ask a questionnaire before locking the strategy; the final decision belongs to the user.

- Response writing in 11 must build response units before prose, verify numeric/data claims against paper/code/review/experiment memory, avoid both reviewer attacks and excessive apology, and write concise limited-space responses when required.

- AC summary writing in 13 should be used when allowed and decision-relevant: borrow verified shared positive reviewer assessments, neutrally contextualize low-score concerns with evidence, and avoid reviewer ranking, attacks, or commanding the AC.

- Output layout is format-aware: one-page PDF uses official/user template or built-in ECCV/CVPR-style fallback; per-reviewer threaded responses use one Markdown file per reviewer; global/hybrid OpenReview-style comments use Markdown or Markdown+LaTeX only when confirmed rules/platform allow.

- Finalization requires 14 safety gates before copy/paste or PDF export; 15 Overleaf/LeafLink is conditional and never submission-facing; 16 versioning preserves work via manual Git, auto Git, or snapshot-only mode without destructive Git actions.

- 15 now treats LeafLink as an explicit tool path when the user selects Overleaf sync: check/install plan, login, list, clone, status, pull, PDF download, continuous sync, and push dry-run/push are documented with authorization boundaries.

- LeafLink setup should prefer Conda when available (`conda create -n leaflink`, `conda run -n leaflink ...`) and use pip fallback only when Conda is unavailable or declined.

- Response mode memory uses one canonical vocabulary only: `openreview_per_reviewer`, `unified_limited`, `pdf_one_page`, `global_comment`, `hybrid`, `openreview_markdown_latex`, or `unknown`. User wording such as “one-page PDF” or “global text” should be normalized and optionally preserved as notes.

- Venue rules use a strengthened `venue_rules.json` contract: source/confirmation, canonical response mode, platform/limits, response permissions, formatting, content permissions, anonymity, language policy, unknowns, and raw rule excerpts. AI-found rules stay pending until user confirmation.

- Language policy: interactive reports/questions follow the user's language by default; final submission-facing author response prose, reviewer replies, AC summaries, OpenReview comments, and PDF rebuttal text default to English unless confirmed venue rules allow another language.

- Installation should support an AI-agent-readable guide rather than only manual `git clone`: `AI_AGENT_INSTALL.md` tells another AI assistant how to install for Codex, Claude Code, and Cursor adapters, run safe environment checks, and handle optional LaTeX/LeafLink setup. Questionnaire choices do not require dependencies; use native UI when available or plain Markdown choices otherwise.

- Strategy planning in 08 should select a strategy lens from the actual review pattern and author goals, then choose major top focused problems (usually up to six), list reviewer sources with stable labels and anonymous IDs, and produce evidence-first bounded argument plans. The score-aware stabilize/lift/weaken framing is a useful heuristic, not a fixed strategy.

- One-page PDF rebuttal template handling is a separate atomic capability: `17_rebuttal_template_manager.md`.

- Snapshot generation in 09 uses `.awesome-rebuttal/snapshots/snapshot_memory.json` as the canonical skill reload entry and generates user-facing Markdown from it. Snapshot history must be newest-first with exact timezone timestamps; Markdown must not be manually edited with independent facts.

- Workspace bootstrap must detect local LaTeX tools and ask for platform-specific setup if PDF compilation is needed and missing.

- All skill-owned memory, snapshots, logs, and active templates belong under `.awesome-rebuttal/` in the active workspace.

- Skill can be globally installed but must create `.awesome-rebuttal/` inside each project workspace for runtime state.

- Use a layered architecture: `SKILL.md` routes to atomic capability files.
- Runtime workspaces should prefer `Code/`, `Paper/`, `Reference/`, `Temp/`.
- Existing user workspaces must be adapted non-destructively.
- Venue rules are not built-in truth; use user-provided rules or AI search plus user confirmation.
- Persist state with JSON memory.
- Ask user to choose manual Git, auto Git, or markdown snapshot-only mode.
- LeafLink is an optional Overleaf sync helper, not an advertisement.
- Missing or ambiguous runtime information should be resolved with focused questionnaires before guessing.
- Never place LeafLink wording in conference-submission-facing rebuttal text.

## Current project snapshot

- Stage: V1 skeleton with global-install/project-local state architecture, completed core layers through template layout/safety/sync/versioning/snapshots, canonical response-mode naming, strengthened venue-rule schema, global language policy, and AI-agent-readable installation guidance.
- Source plan/spec are development artifacts outside the published package.
- Main skill path: `SKILL.md`.

## Next action

Continue capability-by-capability smoke testing with anonymized/local-only fixtures; do not store private paper/review content in tracked skill files.
