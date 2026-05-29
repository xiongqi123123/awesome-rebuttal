# 01 Intake Gate

## Goal

Convert the user's initial rebuttal request plus workspace evidence into a complete, safe intake packet. This capability decides whether the skill may proceed to analysis, or whether it must ask a questionnaire first.

## Core principle

The user speaks first. Parse what the user already provided, inspect available workspace evidence, then ask only for missing or confirmation-needed information.

Read `references/core/user_questionnaire_protocol.md` whenever missing information or a preference decision blocks the next step.

## Success criteria

After this capability runs, the agent should know:

- target venue/year and rule-source status
- response format and limits
- reviewer comments and reviewer metadata availability
- paper context availability
- code context availability
- evidence and experiment resource constraints
- author goals and risk preference
- progress preservation mode
- whether analysis may begin
- whether a template-based response is needed and should route to `17_rebuttal_template_manager.md`
- which missing fields block drafting vs only reduce confidence

## Intake evidence order

Use this order to avoid unnecessary questioning:

1. **User-provided request**
   - Parse pasted venue, rules, reviews, paper summary, code notes, constraints, and goals.
2. **Workspace evidence**
   - Use the workspace map from `00_workspace_bootstrap.md`.
   - Inspect likely files in `Paper/`, `Code/`, and `Reference/` when available.
3. **Questionnaire**
   - Ask only for fields still missing, ambiguous, or requiring user confirmation.

## Intake completeness levels

| Level | Meaning | Allowed next step |
|---|---|---|
| `complete` | all blocking inputs present and confirmed | full review analysis and strategy |
| `analysis_ready` | enough for stance/concern analysis, but some drafting constraints missing | analysis only; no final draft |
| `partial` | paper/reviews exist but major context gaps remain | ask targeted questionnaire before strategy |
| `blocked` | missing reviews, paper context, or venue/rule source decision | stop and ask |

## Required input groups

### A. Venue and rule source

Required:

- venue/journal name
- year/cycle
- official rebuttal/author-response instructions, or rule-source preference
- anonymity, links, supplemental material, revised PDF, and discussion permissions when relevant

Rule-source status:

- `user_confirmed`: user pasted or confirmed official instructions
- `user_will_provide`: user says they will supply official instructions/template later
- `ai_found_pending_confirmation`: AI found candidate rules but user has not confirmed
- `missing`: no rules and no search preference
- `not_applicable`: user explicitly wants non-format analysis only

### B. Response format and limits

Required before drafting:

- canonical response mode: `openreview_per_reviewer`, `unified_limited`, `pdf_one_page`, `global_comment`, `hybrid`, `openreview_markdown_latex`, or `unknown`
- original user wording for the response mode, if it differs from the canonical value
- word/page/character limit
- deadline or time budget if experiments are considered
- whether follow-up discussion is allowed

If format is unknown, strategy analysis may continue only if output is clearly marked non-final.

### B1. Venue rules schema fields

Populate `.awesome-rebuttal/memory/venue_rules.json` according to `references/memory-schemas/venue_rules.schema.json`.

Required rule-memory groups:

- `status` and `source`: user-provided, user-will-provide, AI-found-pending-confirmation, official source path/URL, retrieval time, confidence, and notes.
- `response`: canonical `mode`, platform, limits, per-reviewer/global/interactive/AC-summary permissions.
- `formatting`: template, PDF/LaTeX/Markdown support, figures/tables/appendix, font/margin constraints.
- `content_permissions`: new experiments/results, external links, supplement/code links, references, revision commitments, paper revision, post-rebuttal discussion.
- `anonymity`: anonymous requirement, self-citation policy, acknowledgements, artifact identity risks.
- `confirmation`: user confirmation state, pending confirmation items, conflicts.
- `language_policy`: interaction follows user language; final submission-facing prose defaults to English unless confirmed rules allow another language.

If rules are AI-found, set `status: ai_found_pending_confirmation` and block final drafting until the user confirms the extracted fields.

### B2. Rebuttal template routing

If the response format is template-based (especially one-page PDF), intake should not build the template itself. Instead, route to `17_rebuttal_template_manager.md` after rule-source handling.

Template source priority:

1. user-provided official template or screenshot
2. AI-found official template, pending user confirmation
3. built-in one-page fallback template at `assets/one-page-rebuttal-template/`

Rules:

- If the official venue provides a template, prefer that template.
- If no official template is found and the user still wants one-page PDF, use the built-in CVPR/ECCV-style two-column fallback template, but label it as fallback rather than official.
- Template state and copied files belong in `.awesome-rebuttal/templates/`, not in the installed skill folder.
- A missing or unconfirmed template blocks final PDF drafting, but not strategy analysis.


### C. Reviews

Required for analysis:

- raw reviewer text
- reviewer IDs or stable labels
- score/recommendation when available
- confidence when available
- strengths, weaknesses, questions, and minor comments if present

Missing score/confidence does not block analysis, but must be marked unknown.

### D. Paper context

Required for analysis:

- title or short identifier
- abstract or summary
- core contributions/claims
- method summary
- experiment overview
- key limitations or known weak points

Full PDF/LaTeX is preferred but not strictly required if the user supplies a sufficient summary.

### E. Code context

Required when rebuttal strategy depends on implementation, reproducibility, or new experiments:

- code location or statement that code is unavailable
- main scripts/configs/results if available
- known reproducibility constraints
- feasible compute/data/time budget

If code is absent, mark code evidence unavailable rather than guessing.

### F. Evidence and experiment resources

Required for experiment triage:

- existing results that may be cited
- results that are planned but not done
- experiments that are feasible before deadline
- experiments that are impossible or not worth doing
- whether new results are allowed by venue rules

### G. Author goals and risk posture

Ask the user to choose or describe:

- stabilize positive reviewer(s)
- persuade borderline reviewer(s)
- weaken reject reviewer rationale
- clarify AC-relevant facts
- produce final response draft
- only produce strategy dossier
- conservative, balanced, or assertive tone

### H. Progress preservation

Required before durable outputs:

- `manual_git`
- `auto_git`
- `markdown_snapshot_only`

If unset, ask using `16_rebuttal_versioning.md`.

## Blocking matrix

| Missing item | Blocks analysis? | Blocks drafting? | Action |
|---|---:|---:|---|
| raw reviews | yes | yes | ask user to paste/upload reviews |
| paper context | yes | yes | ask for PDF/LaTeX/summary |
| venue/rule source decision | no for rough analysis | yes | ask user provide rules or authorize search |
| response format/limit | no for analysis | yes | ask format questionnaire; route template formats to `17_rebuttal_template_manager.md` |
| score/confidence | no | no | mark unknown |
| code context | only if code-based claims/experiments matter | yes for code claims | ask or mark unavailable |
| evidence/resources | blocks experiment triage | blocks experiment claims | ask resource questionnaire |
| author goals | no | partially | ask before strategy prioritization |
| versioning mode | no | no | ask before durable memory/snapshot/commit |

## Procedure

1. **Restate provided information**
   - Summarize what the user already told the skill.
2. **Fill intake table from workspace evidence**
   - Use `Paper/`, `Code/`, `Reference/`, and workspace map.
3. **Assign completeness level**
   - `complete`, `analysis_ready`, `partial`, or `blocked`.
4. **Separate blockers from nice-to-have gaps**
   - Blockers prevent analysis or drafting.
   - Nice-to-have gaps become TODOs.
5. **Ask a focused questionnaire if needed**
   - Use single-choice/multi-select/short-text prompts.
   - Ask only for information required for the next safe stage.
6. **Persist intake state**
   - Update `.awesome-rebuttal/memory/project_memory.json` and relevant memory drafts.
   - Add unresolved items to open questions.
7. **Route next capability**
   - `02_information_collection.md` when intake is sufficient.
   - Stay in intake if blockers remain.

## Suggested intake questionnaire

Use this when multiple required inputs are missing.

```markdown
## Need your input: rebuttal intake

I can continue once the blocking items below are resolved.

1. What is the venue/rule source?
   - A. I will paste official author-response instructions
   - B. Search official instructions for venue/year, then ask me to confirm
   - C. Rules unknown for now; only do non-format analysis

2. What response format should we target?
   - A. OpenReview per-reviewer replies (`openreview_per_reviewer`)
   - B. Unified limited/global text response (`unified_limited` or `global_comment`)
   - C. One-page PDF response (`pdf_one_page`)
   - D. Hybrid global + per-reviewer response (`hybrid`)
   - E. Unknown; infer after rules are confirmed

3. If a one-page/PDF response is needed, how should the template be handled?
   - A. I will provide the official template or screenshot
   - B. Search for an official template, then ask me to confirm
   - C. Use the built-in CVPR/ECCV-style fallback if no official template is found
   - D. Skip template setup for now

4. What review material is available now? (multi-select)
   - [ ] Full reviewer comments
   - [ ] Scores/recommendations
   - [ ] Confidence values
   - [ ] Strengths/weaknesses/questions separated by reviewer
   - [ ] Follow-up discussion already started

5. What paper/code context should I use? (multi-select)
   - [ ] Paper PDF or LaTeX in `Paper/`
   - [ ] Pasted title/abstract/summary
   - [ ] Code in `Code/`
   - [ ] Existing experiment logs/results
   - [ ] Code is unavailable or irrelevant

6. What is your strategic priority?
   - A. Stabilize positive reviewer(s)
   - B. Persuade borderline reviewer(s)
   - C. Weaken reject reviewer rationale
   - D. Help AC understand decision-critical facts
   - E. First produce a neutral strategy dossier
```

## Minimal questionnaire for one missing field

When only one blocker remains, ask one focused question instead of the full questionnaire.

Examples:

- “Do you want to provide venue rules yourself, or should I search official rules for `<venue> <year>` and ask you to confirm?”
- “Which canonical response mode should I record: `openreview_per_reviewer`, `unified_limited`, `pdf_one_page`, `global_comment`, `hybrid`, `openreview_markdown_latex`, or should I leave it `unknown` until rules are confirmed?”
- “Should progress be preserved with manual Git, auto Git, or markdown snapshot-only?”

## Intake report template

```markdown
## Intake Gate Report

- Completeness: complete|analysis_ready|partial|blocked
- Ready for analysis: yes/no
- Ready for drafting: yes/no

### Provided
- Venue/year:
- Rule source status:
- Response format:
- Reviews:
- Paper context:
- Code context:
- Evidence/resources:
- Author goals:
- Versioning mode:

### Blocking gaps
- ...

### Non-blocking TODOs
- ...

### Assumptions / unknowns
- ...

### Next action
- Continue to `02_information_collection.md`, or
- Ask questionnaire, or
- Wait for user-provided rules/reviews/paper context.
```

## Memory fields to update

```json
{
  "venue": {
    "name": "",
    "year": "",
    "rule_source_status": "missing|user_confirmed|user_will_provide|ai_found_pending_confirmation|not_applicable"
  },
  "response_format": {
    "mode": "openreview_per_reviewer|unified_limited|pdf_one_page|global_comment|hybrid|openreview_markdown_latex|unknown",
    "original_user_label": "",
    "platform": "openreview|cmt|softconf|hotcrp|email_or_pdf|other|unknown",
    "limits": {"page_limit": null, "word_limit": null, "character_limit": null, "deadline": "", "timezone": ""},
    "response_permissions": {"per_reviewer_replies_allowed": "unknown", "global_response_allowed": "unknown", "interactive_discussion_allowed": "unknown", "ac_summary_allowed": "unknown"},
    "content_permissions": {"new_experiments_allowed": "unknown", "new_results_allowed": "unknown", "external_links_allowed": "unknown", "supplement_allowed": "unknown", "code_links_allowed": "unknown", "revision_commitments_allowed": "unknown"}
  },
  "language_policy": {
    "interaction_language": "follow_user",
    "submission_language": "English",
    "final_writing_language": "English",
    "follow_user_language_for_interaction": true
  },
  "template": {
    "status": "missing|user_provided|ai_found_pending_confirmation|confirmed|fallback_builtin|not_applicable",
    "source": "user|official_search|builtin|none",
    "route": "17_rebuttal_template_manager.md"
  },
  "intake": {
    "completeness": "complete|analysis_ready|partial|blocked",
    "ready_for_analysis": false,
    "ready_for_drafting": false,
    "blocking_gaps": [],
    "non_blocking_todos": []
  }
}
```

## Stop / proceed rules

Proceed to information collection when:

- template-based output is either not required yet or routed to `17_rebuttal_template_manager.md`,
- reviews are present or explicitly deferred for a non-review task,
- paper context is present,
- workspace map exists,
- versioning mode is selected or explicitly deferred,
- rule-source status is sufficient for the requested output.

Proceed to analysis-only mode when:

- reviews and paper context exist,
- venue rules/format are missing,
- user agrees to non-format strategy analysis only.

Block drafting when:

- venue rules are missing or unconfirmed,
- response format/limits are missing,
- factual claims lack paper/code/user evidence,
- new experiment results are missing but drafted as completed.

## Quality bar

A good intake gate should make the next step obvious. It should not bury the user in questions, but it must not continue with hidden assumptions that could cause unsafe rebuttal advice.
