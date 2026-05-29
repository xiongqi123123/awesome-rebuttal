# 11 Response Writer

## Goal

Draft rebuttal text that is strategy-driven, evidence-grounded, concise under venue limits, and internally consistent across the paper, code, reviewer comments, experiment memory, and confirmed rules.

The writer's job is not to “win by arguing” or “sound humble by apologizing.” It should produce professional, logically clear responses that acknowledge valid concerns briefly, then answer with evidence, precise clarification, bounded concessions, or approved experiment results.

## Required inputs

Read before drafting:

- `.awesome-rebuttal/memory/strategy_memory.json` from 08 — required
- `.awesome-rebuttal/memory/experiment_memory.json` from 10 — required when experiments are mentioned or deferred
- `.awesome-rebuttal/memory/review_analysis_memory.json` from 06 — required for semantic concern cards and common clusters
- `.awesome-rebuttal/memory/review_memory.json` from 05 — required for raw reviewer anchors, stable labels, anonymous IDs, scores/confidence if provided
- `.awesome-rebuttal/memory/paper_memory.json` — required for claims, terminology, figures/tables, existing results, and limitations
- `.awesome-rebuttal/memory/code_memory.json` — required when implementation, hyperparameters, runtime, reproducibility, or new experiment feasibility is discussed
- `.awesome-rebuttal/memory/project_memory.json` — required for response mode, venue/rule status, workspace paths, and user decisions
- `.awesome-rebuttal/memory/template_memory.json` — required when writing into a template/one-page PDF
- confirmed venue rules and response limits

If strategy is not user-approved or critical facts are missing, write a blocked/provisional blueprint and ask a questionnaire instead of producing paste-ready text.

## Outputs

Write skill-owned outputs under the active workspace, not the installed skill folder:

```text
.awesome-rebuttal/
├── memory/response_memory.json
├── drafts/response_blueprint.md
├── drafts/author_response_draft.md
├── drafts/coverage_map.md
└── logs/response_writer_report.md
```

When using a LaTeX/PDF template, also write or update the active project template under `.awesome-rebuttal/templates/` or a user-approved export path.

## Boundary

### This capability does

- create a response blueprint before final prose
- draft `openreview_per_reviewer`, `unified_limited`, `pdf_one_page`, `global_comment`, `hybrid`, or `openreview_markdown_latex` responses
- convert strategy matrix rows into paragraphs/sections
- align every factual claim with paper/code/review/experiment/rule provenance
- compress language for word/page limits while preserving precision
- map every response paragraph to reviewer concerns and focused problems
- verify numeric claims, table references, hyperparameters, and experiment result status before wording
- mark missing or unconfirmed facts as TODOs/placeholders
- prepare text for `14_safety_rule_checker.md`

### This capability does not

- invent experiment results, tables, plots, citations, or reviewer positions
- mention new results unless result provenance exists and rules allow them
- rewrite paper claims beyond the approved strategy without recording the edit handoff
- attack reviewers, imply bad faith, or use manipulative flattery
- over-apologize or concede central claims unnecessarily
- bypass confirmed venue rules, anonymity constraints, or length limits


## Language policy

- Discuss drafting choices with the user in the user's language by default.
- Write submission-facing author-response prose in English by default.
- Record output-language choices in `response_memory.language_policy`.
- Preserve exact technical terms, metric names, dataset names, method names, and reviewer identifiers.
- Convert user-provided Chinese strategy notes into professional English rebuttal prose; do not translate literally if it would sound informal or combative.
- If a venue explicitly permits/requires another language, record that in venue rules before drafting.

## Writing stance: evidence-first, not apology-first or argument-first

Use a balanced rebuttal stance:

| Reviewer situation | Bad response | Preferred response |
|---|---|---|
| Reviewer misunderstood a detail | “The reviewer is wrong.” | “We clarify that ...; this is supported by Sec./Table/Code anchor ...” |
| Reviewer found a real limitation | Long apology or full collapse of claim | “We agree this setting is limited; our claim is scoped to ..., and we will clarify ...” |
| Reviewer asks for missing evidence | Unsupported promise | “We added/ran `<approved result>` with provenance, or mark as TODO/future work if unavailable.” |
| Reviewer challenges novelty | Defensive assertion | Distinguish mechanism, evidence, and scope; concede overlap only where true. |
| Reviewer asks minor clarity | Spend major space | One concise sentence or revision note unless it affects decision. |
| Reviews conflict | Answer one side only | State the decision-relevant fact and show how it resolves the disagreement. |

Good rebuttal sentences usually do four things in order:

1. **Name the concern fairly.**
2. **State the answer/position clearly.**
3. **Give evidence or approved correction.**
4. **Explain the revision/impact concisely.**

## Alignment gates before drafting

Before writing a paragraph, check the alignment triangle:

1. **Review alignment** — Does the paragraph answer an actual reviewer concern, using the correct stable label and anonymous ID when needed?
2. **Paper alignment** — Does the statement match the submitted paper's claims, terminology, tables, figures, and limitations?
3. **Code/result alignment** — If implementation or results are mentioned, do code memory, logs, or user-provided evidence support the exact wording?
4. **Strategy alignment** — Does the paragraph follow the user-approved strategy, selected lens, top focused problem, stance, and experiment decision?
5. **Rule alignment** — Is this allowed under confirmed venue format, anonymity, link, supplement, and new-result rules?

If any gate fails, do not silently draft around it. Mark `needs_user_input`, route to the missing memory/capability, or ask a questionnaire.

## Numeric and data correctness policy

Every number must have a provenance entry before paste-ready drafting:

```json
{
  "numeric_claim": "<metric/result/hyperparameter>",
  "value": "<exact value>",
  "unit_or_metric": "<metric>",
  "source": "paper_table|experiment_log|code_config|user_provided|venue_rule",
  "source_anchor": "<path/table/line/log>",
  "checked_against": ["paper_memory", "code_memory", "experiment_memory"],
  "status": "verified|needs_user_confirmation|blocked"
}
```

Rules:

- Use exact values only when verified.
- Use qualitative wording only when quantitative evidence is not available, and avoid overstating.
- Do not write “improves,” “outperforms,” “significant,” “robust,” or “SOTA” unless supported by the relevant metric/comparison.
- If a new experiment is only planned or running, do not phrase it as completed.
- If an experiment result is negative/mixed, use the fallback strategy from 08 rather than hiding it.

## Response unit anatomy

For every paragraph or section, create a response unit before prose:

```json
{
  "response_unit_id": "RU-001",
  "mode": "unified_section|per_reviewer_reply|global_comment|hybrid_global|hybrid_reviewer_detail",
  "heading": "<short heading>",
  "linked_focused_problem_ids": ["FP01"],
  "linked_concern_ids": ["SC003", "PC02"],
  "reviewer_sources": [
    {"stable_label": "R2", "anonymous_id": "<anonymous_id_or_unknown>", "major_or_minor": "major"}
  ],
  "strategy_stance": "push_with_evidence|clarify_without_defensiveness|concede_narrowly_preserve_claim|soften_overclaim|add_or_report_experiment|explain_tradeoff|defer_with_reason",
  "evidence": [
    {"type": "paper|code|experiment|venue_rule|user", "anchor": "...", "claim_supported": "..."}
  ],
  "experiment_usage": [
    {"experiment_id": "EXP-001", "usage": "primary_evidence", "result_status": "already_done", "user_decision": "accepted"}
  ],
  "length_budget": {"target_words": 90, "max_words": 120},
  "must_include": [],
  "must_avoid": [],
  "draft_status": "ready|needs_user_input|blocked"
}
```

Only then draft the text.

## Modes

### 1. Per-reviewer reply

Use when the venue expects reviewer-specific replies or OpenReview discussion threads.

Structure:

1. Optional one-sentence gratitude/acknowledgment for the specific reviewer.
2. Major concerns first, in the reviewer's terms.
3. Use short headings or bullets if allowed.
4. Preserve reviewer-specific detail; avoid duplicating long global explanations across reviewers.
5. Cross-reference a global/common answer only if the platform/thread format allows it.

Per reviewer, set a goal from 08:

- stabilize supportive reviewer
- persuade borderline reviewer
- weaken/recover reject rationale
- answer factual misunderstanding
- close coverage for minor issues

### 2. Unified one-page / limited-space response

Use when space is tight, such as a one-page PDF or strict word limit.

Structure:

1. **Compact opening** — thank reviewers and identify 2-4 major themes; avoid a long generic preface.
2. **Grouped major concerns** — each heading should combine common concerns and list reviewer labels/anonymous IDs when allowed.
3. **Evidence-dense body** — short sentences, verified numbers, compact tables only when they save space.
4. **Targeted clarification/revision notes** — one sentence each for lower-priority issues.
5. **Closing only if useful** — avoid ceremonial closings when space is scarce.

Compression rules:

- Merge repeated concerns into one heading.
- Prefer “Concern: answer + evidence + revision” over long narrative.
- Replace apology chains with one precise acknowledgment.
- Use tables for multiple numeric comparisons only when they are more compact than prose.
- Avoid repeating method background already in the paper unless the reviewer confusion requires it.
- Keep low-priority presentation fixes to short “we will clarify/revise” notes.
- If using LaTeX, keep headings short and robust to two-column/page constraints.

### 3. Global text response

Use when the platform provides one global response box.

Structure:

- opening summary of decision-critical facts
- ordered concern blocks from strategy matrix
- concise coverage of reviewer-specific residuals
- unresolved items/TODOs removed before finalization

### 4. Hybrid response

Use when a short global summary plus per-reviewer details is allowed.

Structure:

- global: shared major concerns and AC-legible facts
- per-reviewer: only reviewer-specific deltas, clarifications, and minor concerns
- avoid copying the same paragraph in every reply

## Style calibration from the user's example

The provided one-page rebuttal example suggests the desired granularity should be compact, sectioned, and evidence-heavy:

- a very short opening that thanks reviewers and names recognized strengths only if space allows;
- grouped “Question/Concern” headings with reviewer identifiers in the heading when rules allow;
- common concerns merged across reviewers instead of handled repeatedly;
- quantitative evidence placed in compact tables when it saves space;
- each section answering one concern with a direct result, controlled comparison, sensitivity check, or clarification;
- hyperparameter/implementation clarifications handled in short targeted paragraphs;
- no long philosophical argument, no excessive apology, and no unsupported acceptance-seeking language.

Do not copy content, numbers, reviewer IDs, paper-specific terms, or tables from the example into the skill or another user's rebuttal.

## Wording patterns

Use these as patterns, not fixed phrases:

### Clarification without defensiveness

```text
We clarify that <precise point>. In the submitted paper, <source anchor> shows <evidence>. We will revise <section/figure/table> to make this explicit.
```

### Evidence-backed pushback

```text
The concern is important. However, <specific evidence> indicates that <bounded conclusion>, so the issue does not undermine <supported claim>. We will add <concise revision> to avoid ambiguity.
```

### Narrow concession while preserving claim

```text
We agree that <limited setting> is not fully covered. Our claim is limited to <scope>, where <evidence> supports <claim>. We will soften the wording from <overbroad claim> to <bounded claim>.
```

### New approved experiment result

```text
Following this concern, we ran <EXP-ID: experiment description> under <setting>. The result <verified value/trend> supports <bounded conclusion>. We will include this result in the revision if allowed by the venue rules.
```

Use this only when `experiment_memory.result_status` is `already_done` or the user provides verified results and venue rules allow reporting.

### Missing or infeasible experiment

```text
This experiment would require <resource/time/data> beyond the rebuttal period. Instead, we will clarify <existing evidence/scope> and add <limitation/future work>.
```

Only use if 08 chose `deferred_alternative` or `defer_with_reason`.

## Prohibited wording

Block or rewrite:

- “The reviewer is wrong / failed to understand / ignored ...”
- “We guarantee / will definitely / prove ...” without evidence
- “We have run ...” when result provenance is missing
- “This will surely change the score/decision”
- “We sincerely apologize” repeated as a substitute for evidence
- hidden deanonymizing details, private links, unconfirmed GitHub/Overleaf links
- claims that conflict with paper/code memory, e.g. different dataset split, metric direction, hyperparameter, or baseline definition

## Questionnaire protocol

Use `references/core/user_questionnaire_protocol.md` when drafting depends on user choices.

Ask a focused questionnaire when:

- the strategy questionnaire from 08 is not answered;
- a numeric result is missing or needs confirmation;
- a new experiment result may or may not be reported;
- one-page/word-limit compression requires dropping or merging concerns;
- user must choose between stronger pushback and safer concession;
- venue rules about links, supplements, anonymity, or new results are unclear.

Recommended draft-lock questionnaire:

```json
{
  "questionnaire_id": "response_writer_lock_v1",
  "summary_before_question": "I can draft the one-page response with 4 grouped sections. Two numeric results need confirmation, and one lower-priority concern may need to be compressed into a single sentence.",
  "questions": [
    {
      "id": "compression_priority",
      "type": "single_choice",
      "prompt": "Under the page/word limit, what should the draft prioritize?",
      "options": ["major_common_concerns", "per_reviewer_coverage", "new_experiment_evidence", "safest_low_risk_language"]
    },
    {
      "id": "missing_numbers_policy",
      "type": "single_choice",
      "prompt": "How should unverified numbers be handled?",
      "options": ["leave_TODO_placeholders", "omit_until_confirmed", "ask_case_by_case"]
    },
    {
      "id": "tone_preference",
      "type": "single_choice",
      "prompt": "Which tone should be used for contested concerns?",
      "options": ["evidence_forward", "more_conciliatory", "more_direct_pushback", "balanced_default"]
    }
  ]
}
```

## Response memory schema sketch

```json
{
  "version": "0.1",
  "draft_status": "ready|partial|blocked",
  "response_mode": "openreview_per_reviewer|unified_limited|pdf_one_page|global_comment|hybrid|openreview_markdown_latex|unknown",
  "source_strategy_memory": ".awesome-rebuttal/memory/strategy_memory.json",
  "source_experiment_memory": ".awesome-rebuttal/memory/experiment_memory.json",
  "venue_limits": {},
  "language_policy": {
    "interaction_language": "follow_user",
    "final_writing_language": "English",
    "submission_facing_text_is_english": true
  },
  "style_profile": {},
  "response_units": [],
  "numeric_claims": [],
  "paper_code_review_alignment": [],
  "coverage_map": [],
  "compression_decisions": [],
  "draft_outputs": [],
  "safety_precheck": {},
  "open_questions": []
}
```

## Procedure

1. **Validate prerequisites**
   - Confirm 08 strategy is complete or explicitly provisional.
   - Confirm venue rules and response mode are known.
   - Confirm paper memory exists; code memory exists if implementation/results are mentioned.
2. **Select response mode**
   - openreview_per_reviewer, unified_limited, pdf_one_page, global_comment, hybrid, or openreview_markdown_latex.
3. **Build response blueprint**
   - Convert top focused problems and coverage plan into response units.
   - Assign length budgets and evidence anchors.
4. **Check alignment and numbers**
   - Verify every factual/numeric claim against memory and provenance.
   - Mark TODOs; do not hide uncertainty.
5. **Draft section by section**
   - Use balanced stance, concise logic, and strategy-approved experiment usage.
6. **Compress if needed**
   - Apply limited-space compression rules and record what was merged/dropped/deferred.
7. **Build coverage map**
   - Map each reviewer concern to response unit, sentence, paragraph, or intentional deferral.
8. **Run safety precheck**
   - Check provenance, commitment, coverage, venue, tone, anonymity, and fabrication gates.
9. **Persist outputs**
   - Write `response_memory.json`, blueprint, draft, coverage map, and report.
10. **Route next**
   - Route to `12_template_designer.md` for PDF/template layout if needed.
   - Route to `13_ac_summary_writer.md` if AC summary is allowed and useful.
   - Route to `14_safety_rule_checker.md` before final/paste-ready text.

## Stop / proceed rules

Proceed to draft when:

- strategy is user-approved or clearly marked provisional;
- response mode and limits are known;
- major concerns have response units;
- facts and numbers have provenance or TODO placeholders;
- experiment result status is known for any mentioned `EXP-*`.

Proceed with warning when:

- lower-priority concerns are covered only by compressed notes;
- venue rules are confirmed except minor formatting details;
- some non-critical numbers are left as TODO placeholders.

Stop and ask when:

- venue rules or response limits are missing;
- required paper/code/review evidence conflicts;
- a paragraph would rely on unverified numeric results;
- the draft would need to choose between conflicting user strategy preferences;
- anonymity, links, supplements, or new experiment reporting are uncertain.

## Safety rules

- Every paragraph must map to at least one concern, strategy goal, or allowed AC/global summary fact.
- Every factual claim must have provenance.
- Every experiment mention must include `EXP-*`, result status, user decision, and rule compatibility in memory.
- Every concession must be narrow and not undermine unrelated supported claims.
- Every pushback must be evidence-backed and professional.
- Final text must pass `14_safety_rule_checker.md` before submission or copy-paste.
