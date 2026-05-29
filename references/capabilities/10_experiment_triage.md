# 10 Review-Driven Experiment Planner

## Goal

Generate, number, and triage supplementary experiment candidates directly from reviewer concerns **before final strategy planning**. This capability turns semantic review concerns from `06_situation_analyzer.md` into an experiment memory that later priority analysis and `08_strategy_planner.md` can use.

Although this file is numbered `10`, run it immediately after `06_situation_analyzer.md` and before final `08_strategy_planner.md`. The goal is not to decide the whole rebuttal strategy; the goal is to build a structured experiment option set such as `EXP-001`, `EXP-002`, ... with feasibility, risk, reviewer linkage, and expected rebuttal value.

## Inputs

Read:

- `.awesome-rebuttal/memory/review_analysis_memory.json` from 06 — required
- `.awesome-rebuttal/memory/review_memory.json` from 05 — required for reviewer labels, anonymous IDs, scores, confidence, and raw anchors
- `.awesome-rebuttal/memory/paper_memory.json` if available — for existing evidence, tables, metrics, claims, terminology
- `.awesome-rebuttal/memory/code_memory.json` if available — for runnable code, configs, hyperparameters, datasets, logs, feasibility
- `.awesome-rebuttal/memory/project_memory.json` — for workspace map, response format, venue/rule status, author resources
- confirmed venue rules if available — for whether new results may be reported, links/supplement restrictions, anonymity constraints
- `.awesome-rebuttal/memory/strategy_memory.json` from 07 if already available — optional, for priority weights only

If 06 is missing, route back to 06. If paper/code memory is missing, still create a provisional experiment memory, but mark feasibility and evidence as `unknown` rather than guessing.

## Output

Write:

- `.awesome-rebuttal/memory/experiment_memory.json`
- `.awesome-rebuttal/logs/review_driven_experiment_plan.md`

Do not store results that the author has not provided or that have not been run. Results fields must be empty/TODO unless evidence exists.

## Boundary

### This capability does

- derive experiment candidates from reviewer concerns and common clusters
- assign stable IDs: `EXP-001`, `EXP-002`, ...
- link each experiment to reviewer stable labels, anonymous IDs, raw anchors, semantic concern IDs, and issue IDs
- classify each experiment as `must_do`, `high_value_optional`, `nice_to_have`, or `not_recommended`
- estimate feasibility, cost, risk, venue-rule compatibility, and expected rebuttal value
- define minimum viable experiment (MVE) and stronger variant
- specify what result format would be needed for rebuttal writing
- ask targeted questionnaires when feasibility/resource/rule choices are missing
- persist experiment memory for 07/08

### This capability does not

- run experiments unless the user separately asks and authorizes execution
- invent numbers, plots, tables, or “we ran” claims
- decide final rebuttal strategy by itself
- promise that an experiment will improve acceptance odds
- recommend huge experiments that cannot realistically finish in rebuttal time
- include private code/paper dumps in memory; store paths, anchors, summaries, and commands only

## Experiment candidate ID policy

Use deterministic IDs within the workspace:

- `EXP-001`, `EXP-002`, ... for active candidate experiments
- preserve existing IDs when refreshing memory
- if a candidate is split, keep the original as a parent and create `EXP-003a` only if needed; otherwise prefer new numeric IDs
- never reuse an ID for a different experiment question
- if an experiment is rejected, keep it with `user_decision: rejected` so future strategy does not rediscover it repeatedly

## Experiment candidate card

Each candidate should follow this shape:

```json
{
  "experiment_id": "EXP-001",
  "title": "Baseline comparison with the closest reviewer-requested method",
  "trigger_summary": "Reviewer questions whether the claimed gain is meaningful without baseline X.",
  "linked_semantic_concern_ids": ["SC003"],
  "linked_common_cluster_ids": ["CC002"],
  "linked_issue_item_ids": ["ISS-R2-04"],
  "reviewer_sources": [
    {"stable_label": "R2", "anonymous_id": "<anonymous_id_or_unknown>", "major_or_minor": "major"}
  ],
  "reviewer_request_type": "missing_baseline|ablation|statistical_significance|robustness|dataset_bias|sensitivity|hyperparameter|efficiency|qualitative|reproducibility|failure_case|human_eval|other",
  "hypothesis": "A concise, testable statement of what the experiment would check.",
  "minimum_viable_experiment": "Smallest credible experiment that directly addresses the concern.",
  "stronger_variant": "More complete variant if time/compute allow.",
  "required_assets": {
    "code": "available|partial|missing|unknown",
    "data": "available|partial|missing|unknown",
    "compute": "low|medium|high|unknown",
    "time_estimate": "hours|1_day|multi_day|unknown",
    "owner": "user|agent|unknown"
  },
  "feasibility": "high|medium|low|unknown",
  "venue_rule_compatibility": "allowed|probably_allowed|blocked|needs_user_confirmation|unknown",
  "risk_if_negative": "low|medium|high|unknown",
  "risk_if_not_done": "low|medium|high|unknown",
  "expected_rebuttal_value": "decision_critical|high|medium|low",
  "triage_class": "must_do|high_value_optional|nice_to_have|not_recommended|needs_user_decision",
  "recommended_decision": "do_now|do_if_time|do_not_do|ask_user|wait_for_rules",
  "result_status": "already_done|running|planned|not_started|impossible|needs_user_input",
  "result_record": {
    "numbers": [],
    "tables_or_figures": [],
    "logs_or_paths": [],
    "provenance": []
  },
  "response_usage_plan": {
    "can_support_response_modes": ["cite_new_result", "cite_existing_result", "clarify_feasibility", "bounded_future_work", "do_not_mention"],
    "likely_strategy_stance": "add_or_report_experiment|push_with_evidence|explain_tradeoff|defer_with_reason",
    "space_cost": "short|medium|long",
    "drafting_note": "How this would be used later, without writing final text."
  },
  "user_decision": "accepted|rejected|defer|needs_questionnaire|unset",
  "open_questions": []
}
```

## Triage classes

Use these classes carefully:

| Class | Meaning | Typical action |
|---|---|---|
| `must_do` | Decision-critical, directly answers a major concern, feasible, and likely safe to report. | Recommend doing or using existing result. |
| `high_value_optional` | Helpful for a P1/P2 concern but not essential for core strategy. | Do if time/compute allow. |
| `nice_to_have` | May improve polish but weak decision impact or too space-expensive. | Usually skip in limited rebuttal. |
| `not_recommended` | Too costly, too risky, rule-incompatible, weakly relevant, or likely to distract. | Do not do; plan alternative response. |
| `needs_user_decision` | Depends on missing resources, rules, or author risk tolerance. | Ask questionnaire. |

## Evaluation dimensions

For every candidate, judge:

1. **Reviewer linkage** — which reviewer(s), stable labels, anonymous IDs, and raw anchors triggered it?
2. **Major vs minor** — is it tied to a major concern or a minor polish point?
3. **Decision value** — can it affect a reviewer or AC's decision logic?
4. **Specificity** — does the experiment answer the exact concern, or only vaguely help?
5. **Feasibility** — can it run with available code/data/compute/time?
6. **Result risk** — would a negative/null result harm the rebuttal more than help?
7. **Venue compatibility** — are new experiments/results allowed or do they need confirmation?
8. **Space cost** — can it be reported within the response format?
9. **Alternative response** — if not done, can clarification/existing evidence/claim softening handle the concern?

## Common experiment patterns

Generate only when triggered by actual reviews:

- missing baseline or closest prior method comparison
- ablation of a claimed component, loss, module, prompt, reward, planner, or data filter
- sensitivity/hyperparameter analysis
- statistical significance, variance, confidence interval, or repeated-seed check
- robustness/generalization on additional split, corruption, dataset, scenario, or domain
- dataset bias or subset selection sanity check
- efficiency/runtime/memory/parameter count comparison
- failure case or qualitative analysis
- reproducibility check: config, seed, data preprocessing, release plan
- user study/human eval only when already available or realistically feasible
- paper-only table/figure lookup when the “experiment” is already in the paper but reviewers missed it

## Questionnaire protocol

Use `references/core/user_questionnaire_protocol.md` when experiment decisions depend on author resources or preferences. The skill should provide recommendations first, then ask the smallest useful decision set.

Recommended questionnaire shape:

```json
{
  "questionnaire_id": "experiment_triage_decision_v1",
  "summary_before_question": "I found 2 must-do, 3 high-value optional, and 2 not-recommended experiment candidates. The main blockers are compute time and whether new results may be reported.",
  "questions": [
    {
      "id": "experiment_resource_budget",
      "type": "single_choice",
      "prompt": "How much experiment budget is realistically available before rebuttal?",
      "options": ["none", "few_hours", "one_day", "multi_day", "already_have_results"]
    },
    {
      "id": "accept_must_do_experiments",
      "type": "multi_select",
      "prompt": "Which recommended must-do experiments should be included in the strategy plan?",
      "options": ["EXP-001", "EXP-002", "defer_all"]
    },
    {
      "id": "risk_tolerance",
      "type": "single_choice",
      "prompt": "If an experiment may produce a weak/negative result, should we run it anyway?",
      "options": ["only_low_risk", "run_if_decision_critical", "run_even_if_risky", "ask_case_by_case"]
    }
  ]
}
```

If the user has not confirmed venue rules for new results, ask whether to treat experiments as:

- `reportable_if_successful`
- `internal_strategy_only_until_rules_confirmed`
- `do_not_plan_new_results`

## Output schema sketch

```json
{
  "version": "0.1",
  "status": "complete|partial|blocked",
  "created_at": "...",
  "updated_at": "...",
  "source_review_analysis": ".awesome-rebuttal/memory/review_analysis_memory.json",
  "source_review_memory": ".awesome-rebuttal/memory/review_memory.json",
  "rule_status": "user_confirmed|needs_user_confirmation|missing|not_applicable",
  "resource_assumptions": {},
  "experiment_candidates": [],
  "experiment_clusters": [],
  "triage_summary": {
    "must_do": [],
    "high_value_optional": [],
    "nice_to_have": [],
    "not_recommended": [],
    "needs_user_decision": []
  },
  "reviewer_experiment_map": [],
  "concern_experiment_map": [],
  "strategy_inputs": [],
  "user_decision_state": {
    "questionnaire_needed": true,
    "recommended_questions": [],
    "accepted_experiment_ids": [],
    "rejected_experiment_ids": [],
    "deferred_experiment_ids": []
  },
  "open_questions": []
}
```

## Output report

```markdown
## Review-Driven Experiment Plan

- Status: complete|partial|blocked
- Source: 06 semantic concern analysis
- Rule status for new results: ...
- Resource assumptions: ...

### Recommended experiments

| ID | Class | Reviewer(s) | Concern | Minimum viable experiment | Feasibility | Risk | Recommendation |
|---|---|---|---|---|---|---|---|
| EXP-001 | must_do | R2 (<anonymous_id>) | Missing baseline | ... | medium | low | do_now |

### Not recommended / risky experiments

- EXP-004 — too costly for rebuttal; answer with limitation + future work instead.

### Questions for the author

- Confirm available compute/time.
- Confirm whether new experiment results may be reported under venue rules.
- Choose accepted/deferred/rejected experiments.
```

## Procedure

1. **Load 06 and 05**
   - Use semantic concern cards/common clusters plus raw reviewer metadata.
2. **Extract experiment-triggering concerns**
   - Identify concerns that ask for or imply evidence beyond text clarification.
3. **Create numbered candidates**
   - Assign `EXP-001` IDs and link each to reviewer labels, anonymous IDs, concern IDs, and anchors.
4. **Check existing evidence**
   - If paper/code memory already contains the needed result, mark `result_status: already_done` and use provenance anchors.
5. **Estimate feasibility and risk**
   - Use code memory for runnable commands/configs and project memory for resource constraints.
6. **Classify triage class**
   - Use decision value, feasibility, risk, venue rules, and response space cost.
7. **Build maps**
   - `reviewer_experiment_map`: which reviewers each experiment can answer.
   - `concern_experiment_map`: which semantic/priority concerns each experiment can support.
   - `strategy_inputs`: compact facts for 07/08.
8. **Ask only necessary questions**
   - If resources/rules/risk tolerance decide whether to do an experiment, present recommendations plus a focused questionnaire.
9. **Persist memory**
   - Write `experiment_memory.json` and the Markdown report.
10. **Route forward**
   - Route to 07 for priority/situation weighting if not done.
   - Route to 08 when priority analysis and experiment memory both exist.

## Stop / proceed rules

Proceed to 07/08 when:

- experiment candidates are numbered and linked to reviewer/concern sources,
- triage classes are assigned or explicitly marked `needs_user_decision`,
- missing resources/rules are represented as open questions,
- no results are fabricated.

Proceed with warning when:

- code memory is missing and feasibility is uncertain,
- venue rules are not confirmed,
- user has not yet chosen which recommended experiments to run.

Stop and ask when:

- the next step would require running code, spending compute, changing files, or reporting new results without user approval,
- venue rules may prohibit the proposed result reporting,
- author risk tolerance determines whether to attempt a high-risk experiment.

## Safety rules

- Never say an experiment was run unless result provenance exists.
- Never invent numbers, trends, significance, plots, or qualitative examples.
- Do not recommend experiments just because they sound impressive; tie them to reviewer concerns.
- Do not let experiments distract from direct clarifications or claim-scope repairs.
- If an experiment is not feasible, create a response alternative for 08: existing evidence, clarification, narrow concession, or future-work framing.
