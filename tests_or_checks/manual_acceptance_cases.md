# Manual Acceptance Cases

## Case 1: Empty workspace bootstrap

Input: empty project folder.
Expected: skill recommends or creates `Code/`, `Paper/`, `Reference/`, `Temp/`, then asks versioning mode.

## Case 2: Existing workspace adaptation

Input: folder with `src/`, `paper.tex`, `reviews.md`.
Expected: skill maps existing paths non-destructively and does not force renames.

## Case 3: Overleaf paper

Input: user says paper is on Overleaf.
Expected: skill asks whether to use LeafLink sync into `Paper/`; no LeafLink text appears in final rebuttal.

## Case 4: Missing venue rules

Input: reviews and paper but no author response instructions.
Expected: skill asks user to provide rules or authorize AI search; drafting blocked until confirmed.

## Case 5: Strategy-first rebuttal

Input: paper summary + three reviews.
Expected: stance map, atomic concern ledger, common clusters, strategy matrix, experiment triage before response draft.

## Case 6: Snapshot-only progress

Input: user selects markdown snapshot-only.
Expected: skill maintains `.awesome-rebuttal/snapshots/snapshot_memory.json` as the detailed skill reload entry and renders `.awesome-rebuttal/snapshots/REBUTTAL_SNAPSHOT.md` or `.awesome-rebuttal/snapshots/PROJECT_SNAPSHOT.md` from the JSON. The Markdown latest section and history use exact timestamps and newest-first order.

## Case 7: Messy workspace questionnaire

Input: workspace has `src/`, `main.tex`, `review1.txt`, and no canonical folders.
Expected: skill summarizes detected candidates and asks a workspace mapping questionnaire before creating/moving files.

## Case 8: Intake starts from user-provided context

Input: user pastes venue, partial reviews, and paper summary but omits response format.
Expected: skill restates provided fields, marks response format as blocker for drafting, and asks a focused format/rule questionnaire rather than asking for everything again.

## Case 9: Global skill with project-local state

Input: skill is installed globally and user runs it inside a new rebuttal workspace.
Expected: skill creates `.awesome-rebuttal/memory`, `.awesome-rebuttal/snapshots`, `.awesome-rebuttal/templates`, `.awesome-rebuttal/logs`, and `.awesome-rebuttal/cache`; no runtime state is written to the installed skill folder.

## Case 10: LaTeX environment missing

Input: PDF rebuttal requested but `latexmk`/`pdflatex` are unavailable.
Expected: skill records missing LaTeX status and asks a platform-specific setup questionnaire; it does not install packages without explicit instruction.

## Case 11: One-page template fallback

Input: user wants one-page PDF, no official template is available/confirmed.
Expected: skill routes to `17_rebuttal_template_manager.md`, copies built-in `assets/one-page-rebuttal-template/` into `.awesome-rebuttal/templates/active-rebuttal-template/`, labels it as fallback, and does not claim it is official.

## Case 12: Paper memory without paper source

Input: workspace has reviews/code but no current paper PDF/LaTeX/summary.
Expected: `03_paper_memory_builder.md` creates a blocked paper-memory report, does not fabricate claims or results, and asks for the current submitted paper source.

## Case 13: Paper memory with full paper

Input: workspace has current paper PDF or LaTeX.
Expected: skill extracts narrative spine, contribution ledger, claim-evidence map, method memory, experiment matrix, result ledger, figure/table index, terminology, limitations, and rebuttal relevance hooks with source anchors.

## Case 14: Code memory with implementation repo

Input: workspace has a local implementation repo under `Code/`.
Expected: `04_code_memory_builder.md` maps architecture, innovation insertion points, implementation anchors, configs/hyperparameters, train/eval entrypoints, dataset/evaluation pipeline, experiment feasibility, reproducibility risks, and claim-code links when paper memory is available.

## Case 15: Code memory without paper memory

Input: code exists but current paper source is missing or paper memory is blocked.
Expected: skill builds provisional code-side memory and `code_to_possible_claims` without claiming alignment to paper claims; it asks for paper source before using code as paper-claim evidence.

## Case 16: Neutral review indexing

Input: raw reviews with reviewer IDs, scores, strengths, weaknesses, and body text.
Expected: `05_review_normalizer.md` preserves raw reviews, extracts explicit metadata, creates raw anchors, issue item index, and common issue index; it does not assign strategic severity, pivotal reviewers, or response modes.

## Case 17: Semantic review concern analysis

Input: completed review index from 05.
Expected: `06_situation_analyzer.md` creates semantic concern cards, semantic common clusters, reviewer semantic summaries, evidence availability, and coverage audit without priority ranking or posture labels.

## Case 18: Priority and situation analysis

Input: completed semantic review concern analysis from 06.
Expected: `07_concern_atomizer.md` ranks concern priority, classifies rebuttal posture, builds reviewer priority map, identifies AC-facing decision facts and evidence gap urgency, and traces every priority concern back to semantic concern IDs and raw review anchors.

## Case 19: Strategy planner top focused problems

Input: completed 07 priority analysis, completed `experiment_memory.json`, plus an optional author strategy lens, such as “stabilize high-score, lift borderline, rescue low-score reviewers.”
Expected: `08_strategy_planner.md` treats the author lens as advisory, selects the best strategy lens from the actual review pattern, chooses up to six major focused problems, lists stable reviewer labels and anonymous reviewer IDs for each, maps linked `EXP-*` experiments or no-experiment rationale to each problem, defines evidence-first response stance, paper-edit handoffs, global themes, per-reviewer or per-concern strategy, and a coverage plan for non-top concerns. It presents recommended strategy/experiment trade-offs and asks a questionnaire before locking the plan.


## Case 20: Snapshot consistency renderer

Input: completed strategy snapshot JSON with two history entries.
Expected: `render_snapshot.py --check` passes after rendering; if the Markdown is manually edited or history is not newest-first, the check fails and the skill regenerates from JSON.


## Case 21: Review-driven experiment memory before strategy

Input: completed 06 semantic review concern analysis with experiment-triggering major concerns.
Expected: `10_experiment_triage.md` runs before final 08 strategy planning, creates `.awesome-rebuttal/memory/experiment_memory.json`, assigns stable `EXP-*` IDs, links each experiment to reviewer labels/anonymous IDs and concern IDs, classifies must-do/high-value/nice-to-have/not-recommended, and marks missing resources/rules as questionnaire items without inventing results.


## Case 22: Evidence-aligned response writing

Input: completed user-approved strategy, experiment memory, paper/code/review memory, and confirmed one-page response limit.
Expected: `11_response_writer.md` creates `response_memory.json`, a blueprint, draft, and coverage map under `.awesome-rebuttal/`; every response unit maps to reviewer concerns and evidence anchors; numeric claims are verified or left as TODO; language is concise, non-attacking, and not over-apologetic.

## Case 23: Draft blocked by inconsistent evidence

Input: strategy requests a result but paper memory, code memory, and experiment memory disagree or the result is unverified.
Expected: `11_response_writer.md` blocks paste-ready text, records the conflicting anchors, asks a focused questionnaire or routes to the missing capability, and does not invent or smooth over the discrepancy.


## Case 24: AC summary for low-score context

Input: confirmed rules allow a `global_comment`/AC opening; reviews include shared positive assessments and one low-score rationale addressed by verified rebuttal evidence.
Expected: `13_ac_summary_writer.md` recommends a short AC-facing summary, builds `ac_summary_memory.json`, anchors shared strengths and low-score rationale to reviewer evidence, drafts grateful factual wording, and avoids reviewer attacks, reviewer ranking, or commands to the AC.

## Case 25: AC summary blocked by rules or unsupported facts

Input: user asks for an AC summary, but venue rules are unconfirmed/disallow global text or the low-score rationale/new evidence is unsupported.
Expected: `13_ac_summary_writer.md` records `decision: blocked`, asks a focused questionnaire or routes to missing evidence, and does not produce paste-ready AC-directed text.


## Case 26: One-page PDF template layout

Input: confirmed `pdf_one_page` response mode, no official template, and user accepts fallback.
Expected: `17_rebuttal_template_manager.md` prepares the built-in ECCV/CVPR-style fallback under `.awesome-rebuttal/templates/active-rebuttal-template/` and labels it as fallback; `12_template_designer.md` maps response units into the one-page LaTeX layout without claiming the template is official.

## Case 27: Per-reviewer OpenReview-style Markdown

Input: confirmed threaded/per-reviewer response mode with three reviewers.
Expected: `17_rebuttal_template_manager.md` and `12_template_designer.md` create `.awesome-rebuttal/drafts/openreview-comments/R1.md`, `R2.md`, `R3.md`, and paste-order notes; each file maps only the corresponding reviewer concerns plus shared global content if allowed.

## Case 28: Markdown+LaTeX OpenReview comment

Input: confirmed `openreview_markdown_latex` mode with Markdown and LaTeX math support.
Expected: `12_template_designer.md` creates Markdown comment files with lightweight inline LaTeX, no fragile macros, no external dependencies, and a platform-preview warning if rendering is uncertain.

## Case 29: Final safety gate blocks unsafe paste-ready text

Input: draft contains an unverified result, a TODO placeholder, or unconfirmed external link.
Expected: `14_safety_rule_checker.md` writes `safety_memory.json` with `overall: blocked`, identifies the claim, and routes back to the responsible capability instead of approving copy/paste.

## Case 30: Versioning mode safety

Input: user selects `manual_git`.
Expected: `16_rebuttal_versioning.md` may inspect status and suggest a Lore commit message but does not stage or commit. In `auto_git`, it creates only local milestone commits and never pushes/resets/cleans/rewrites.

## Case 31: Overleaf sync helper is conditional

Input: user says paper is on Overleaf.
Expected: `15_overleaf_leaflink_sync.md` offers manual ZIP/PDF, LeafLink, or other user-approved local sync options; if LeafLink is chosen, it checks/install-plans the `leaflink` CLI, prefers Conda-based installation/execution when Conda exists, selects base URL, supports login/list/clone/status/pull/download/sync/push-dry-run command plans with explicit authorization, writes sync memory, and never inserts LeafLink text into rebuttal/AC/submission-facing drafts.

## Case 32: Response mode normalization

Input: user says “one page PDF”, “global text”, or “per reviewer reply” in natural language.
Expected: intake records canonical `response_format.mode` / `venue_rules.response.mode` as `pdf_one_page`, `global_comment`, or `openreview_per_reviewer`, preserves the original wording only as notes, and does not write old aliases into memory.

## Case 33: Strengthened venue rules memory

Input: user asks the skill to search venue rules.
Expected: the skill records candidate source URL/path, retrieval time, canonical response mode, limits, formatting, content permissions, anonymity, language policy, and pending confirmation items in `venue_rules.json`; status remains `ai_found_pending_confirmation` and drafting is blocked until the user confirms.

## Case 34: Language policy

Input: user interacts in Chinese and asks for rebuttal drafting.
Expected: questionnaires, analysis, and progress updates may be in Chinese, but submission-facing author response, reviewer replies, AC summaries, OpenReview comments, and one-page PDF prose are drafted in English by default, with technical terms and reviewer wording preserved.
