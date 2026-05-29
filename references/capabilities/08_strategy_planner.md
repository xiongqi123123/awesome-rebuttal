# 08 Rebuttal Strategy Planner

## Goal

Convert the priority/situation analysis from `07_concern_atomizer.md` plus the review-driven experiment memory from `10_experiment_triage.md` into an actionable rebuttal strategy derived from the actual review pattern, paper evidence, experiment options, venue constraints, and author goals.

This capability is where the rebuttal becomes a deliberate plan rather than a list of answers. It should identify the top focused problems to solve, decide how to handle each, map each problem to reviewers, evidence, experiments, user-approved choices, and tone, and produce a strategy matrix that later writing capabilities can follow.

## Strategy selection principle

Do not hard-code one rebuttal strategy. Choose a strategy from the actual review situation. The user may provide a preferred strategic lens, but that lens is advisory and should be checked against 05-07 evidence and the experiment options from 10.

Common strategic lenses include:

- `score_aware_reviewer_management`: stabilize supportive/high-score reviewers, lift borderline reviewers, and weaken low-score reject rationales.
- `consensus_concern_resolution`: focus on concerns shared by multiple reviewers, regardless of score.
- `ac_decision_fact_strategy`: foreground facts that an AC/meta-reviewer is likely to use in the decision.
- `evidence_gap_closure`: prioritize missing evidence, statistics, baselines, or sensitivity analyses that can be resolved during rebuttal.
- `claim_scope_repair`: soften overclaims and clarify scope when reviewers agree wording is too strong.
- `venue_fit_reframing`: address fit/audience concerns when venue relevance is disputed.
- `defensive_stabilization`: when acceptance is plausible, avoid risky new claims and reinforce existing positives.
- `damage_control`: when rejection risk is high, concede valid limitations while preserving the strongest supported contribution.

The user-provided “稳高分 / 冲中分 / 挽救低分” view is one useful `score_aware_reviewer_management` heuristic, not the only possible strategy.

The selected strategy must not be passive apology and must not be empty arguing. It should be evidence-first, bounded, professional, and AC-legible.

## Inputs

Read:

- `.awesome-rebuttal/memory/strategy_memory.json` from 07
- `.awesome-rebuttal/memory/experiment_memory.json` from 10
- `.awesome-rebuttal/memory/review_analysis_memory.json` from 06
- `.awesome-rebuttal/memory/review_memory.json` from 05
- `.awesome-rebuttal/memory/paper_memory.json` if available
- `.awesome-rebuttal/memory/code_memory.json` if available
- `.awesome-rebuttal/memory/project_memory.json`
- confirmed venue rules / response format if available
- author priorities from intake

If 07 priority/situation analysis is missing, route back to 07. If 10 experiment memory is missing, route back to 10 or create a blocked/provisional strategy that explicitly says experiment options are untriaged. If 05/06 review memory is missing, do not invent the strategy from raw intuition.

## Boundary

### This capability does

- define rebuttal goals by the selected strategy lens, which may be reviewer-score groups, consensus concerns, AC facts, evidence gaps, claim-scope repairs, venue-fit themes, or a hybrid
- select the top focused problems, usually top 4-6, according to the chosen strategic lens, major remarks, shared concerns, reviewer weights, evidence feasibility, and numbered experiment candidates
- merge overlapping concerns when one response theme can cover multiple reviewers
- produce a response strategy matrix
- decide response family: clarify, evidence, experiment, concession, claim softening, trade-off, or defer
- define battle stance: where to push, where to concede narrowly, where to soften, and where to provide evidence
- identify global response themes vs per-reviewer details
- map existing paper/code evidence and numbered experiments from 10 to each focused problem and reviewer concern
- recommend strategy/experiment choices with pros and cons, then ask the user to approve, reject, or adjust the plan via questionnaire
- create writing guidance for 11/12/13
- update `.awesome-rebuttal/memory/strategy_memory.json`

### This capability does not

- write paste-ready rebuttal text
- fabricate missing evidence or experiment results
- run experiments
- make final venue-format decisions without confirmed rules
- treat recommended experiments as user-approved unless the user chooses them
- ignore minor concerns; lower-priority items remain in the coverage audit

## Strategy posture: not apology, not argument

Use a balanced “evidence battle” mode:

| Bad pattern | Better strategy |
|---|---|
| Pure apology | Acknowledge briefly, then provide evidence or concrete correction. |
| Pure arguing | State the reviewer concern fairly, then distinguish with paper/code evidence. |
| Defensive denial | Use structural distinction: what the method does that the criticized baseline/framing does not. |
| Overclaiming | Concede the local limitation while preserving the supported core claim. |
| Promise inflation | Route missing evidence to experiment triage or mark as future work. |
| Scattered point replies | Build 2-4 global themes that cover shared major concerns. |

Recommended response stance labels:

- `push_with_evidence`: reviewer concern can be challenged with existing evidence.
- `clarify_without_defensiveness`: reviewer likely missed or questioned a detail.
- `concede_narrowly_preserve_claim`: reviewer is partly right; limit the concession.
- `soften_overclaim`: wording is too strong; revise scope while keeping contribution.
- `add_or_report_experiment`: evidence gap is important and feasible.
- `explain_tradeoff`: design choice has a measurable benefit/cost trade-off.
- `defer_with_reason`: not feasible or not allowed; give bounded future-work framing.

## Top focused problem selection

The planner should normally produce **up to 6 focused problems**. This is not simply the top six issue items. It should merge concerns when one response can cover multiple reviewers.

Selection criteria:

1. Major remarks over minor issues.
2. Common concerns mentioned by multiple reviewers.
3. High-confidence low-score reviewer concerns that may influence AC.
4. Borderline reviewer concerns that are concrete and addressable.
5. Concerns that threaten the paper's central contribution, evidence sufficiency, or venue fit.
6. Concerns that can be answered with existing paper/code evidence or feasible rebuttal experiments.
7. Positive/supportive reviewer points that can stabilize global framing.
8. Author-stated strategy lens, if any, after checking it against the review evidence.

Do not spend top-6 slots on typos, formatting, or minor presentation unless presentation is a major decision factor.

## Strategy lens and reviewer goal model

First choose a `selected_strategy_lens` and explain why it fits the review pattern. Then, if the selected lens uses reviewer-score management, build reviewer groups from 07:

```json
{
  "reviewer_goal_model": {
    "stabilize_high_score": ["R5"],
    "lift_borderline": ["R3", "R4"],
    "weaken_low_score_rejects": ["R1", "R2"],
    "unknown_or_mixed": []
  }
}
```

Use both stable labels and anonymous IDs when available.

For each group:

### Stabilize high-score/supportive reviewers

Goal:

- reinforce what they liked
- answer their residual concerns so they stay supportive
- avoid introducing risky new claims

Strategy:

- cite broad evaluation, clear ablations, practical value, or other praised evidence
- show that shared concerns are bounded and handled
- keep tone confident and concise

### Lift borderline reviewers

Goal:

- resolve concrete blockers
- provide missing details, sensitivity, statistics, or clarification
- show the contribution is stronger or more bounded than they feared

Strategy:

- prioritize their explicit questions
- give direct evidence or experiment plan/results
- make it easy for them to justify score improvement

### Weaken low-score/reject reviewers

Goal:

- reduce the force of their main reject arguments for the AC
- do not expect full conversion unless concerns are factual and fixable
- separate valid limitations from overbroad rejection rationale

Strategy:

- concede local valid points
- show remaining supported contribution
- use existing evidence, ablation, or additional results if available
- avoid emotional disagreement

## Focused problem card

For each top problem:

```json
{
  "focused_problem_id": "FP01",
  "title": "Novelty and contribution framing",
  "priority_rank": 1,
  "source_priority_concern_ids": ["PC:novelty"],
  "source_semantic_concern_ids": ["SC001", "SC007"],
  "mentioned_by": [
    {"stable_label": "R1", "anonymous_id": "..."},
    {"stable_label": "R2", "anonymous_id": "..."}
  ],
  "major_or_minor": "major",
  "why_it_matters": "Attacks the central contribution and appears across reviewers.",
  "target_strategy_goal": ["score_aware_reviewer_management", "consensus_concern_resolution"],
  "strategy_stance": "concede_narrowly_preserve_claim",
  "response_family": ["structural_distinction", "cite_existing_evidence", "claim_softening"],
  "evidence_plan": [],
  "linked_experiment_ids": ["EXP-001"],
  "experiment_usage": [
    {"experiment_id": "EXP-001", "usage": "primary_evidence|backup_evidence|not_needed|deferred", "user_decision_required": true}
  ],
  "paper_edit_handoff": [],
  "risk_if_mishandled": "Over-arguing could reinforce novelty criticism; over-conceding could collapse contribution.",
  "success_criterion": "Reviewer/AC sees the work as a focused, practical planning refinement with validated safety/physical benefits, not merely arbitrary loss tuning."
}
```

## Strategy matrix fields

For every focused problem and remaining coverage item, record:

- problem/concern ID
- reviewer sources, including stable label and anonymous ID
- major/minor status
- response goal
- response stance
- response mode(s)
- evidence to cite
- missing evidence
- linked experiment IDs and user decision state
- paper edit need
- tone guidance
- expected decision impact
- risk
- next capability

## Possible top-focused-problem shapes

The planner should infer the actual top focused problems from 07. The following shapes are examples, not a fixed template. When reviews resemble a mixed rebuttal-sensitive case, candidates often include:

1. **Central novelty / contribution framing**
   - Usually shared across low-score and borderline reviewers.
   - Strategy: structural distinction + narrow concession + evidence of practical value.
2. **Evidence strength for key claimed benefit**
   - Includes small gains, statistics, significance, or effect size concerns.
   - Strategy: cite strongest exact evidence; if needed, use the numbered experiment candidates from 10 or route back to 10 for missing triage.
3. **Dataset/subset or experimental design credibility**
   - Includes selection bias, subset construction, distribution, or reproducibility details.
   - Strategy: clarify construction criteria + statistics + fairness checks.
4. **Missing baseline / comparison coverage**
   - Strategy: explain closest baselines, add feasible comparison if possible, or justify infeasibility.
5. **Mechanism detail / sensitivity / hyperparameter questions**
   - Includes thresholds, margins, weights, class-agnostic simplifications.
   - Strategy: provide values, sensitivity, rationale, or claim boundary.
6. **Claim wording / scope / venue fit / trade-off**
   - Strategy: soften overclaims, explain trade-offs, frame fit using confirmed venue rules and reviewer positives.

The actual top focused problems must come from 07's priority-ranked concerns and reviewer evidence, not from this example list or any single user-provided heuristic alone.

## Evidence planning

For each focused problem, classify evidence state:

- `ready_existing_paper`: cite paper table/figure/section.
- `ready_existing_code`: cite implementation/config/log anchor.
- `needs_user_result`: user must provide result/value.
- `needs_experiment_triage`: route back to 10 for a numbered candidate before final strategy.
- `needs_rule_confirmation`: cannot decide final form yet.
- `not_feasible`: use bounded concession or future work.

If paper memory is blocked, strategy can be provisional but must mark paper evidence as missing.

## Experiment integration from 10

Strategy planning consumes `experiment_memory.json`; it should not rediscover experiment ideas from scratch unless 10 missed an evidence gap.

For each focused problem, decide how each linked experiment affects the response:

- `primary_evidence`: the response should rely on this result if already available or user-approved and successful.
- `backup_evidence`: useful if space allows or if a stronger result is needed.
- `clarification_only`: experiment is unnecessary; answer with existing paper/code evidence or explanation.
- `deferred_alternative`: experiment is not feasible/allowed; use limitation, claim softening, or future-work framing.
- `do_not_use`: risky, distracting, rule-incompatible, or rejected by user.

Strategy matrix rows must include:

```json
{
  "focused_problem_id": "FP02",
  "linked_experiment_ids": ["EXP-001", "EXP-004"],
  "experiment_decision": [
    {
      "experiment_id": "EXP-001",
      "triage_class": "must_do",
      "strategy_usage": "primary_evidence",
      "user_decision": "accepted|rejected|defer|unset",
      "if_result_positive": "Use as concise quantitative support.",
      "if_result_negative_or_missing": "Fall back to bounded concession plus existing evidence."
    }
  ]
}
```

If 08 identifies a new untriaged experiment need, route back to 10 and do not finalize the strategy until the candidate has an ID, feasibility estimate, and user decision state.


## User decision questionnaire

08 must interact with the author before locking final strategy when multiple defensible strategies or experiment choices exist. The skill may recommend a plan, but the user decides the final route. Use `references/core/user_questionnaire_protocol.md`.

Questionnaire principle:

1. Show the recommended strategy lens and why.
2. Show 2-3 viable alternatives only when they materially differ.
3. For each recommended top problem and experiment, list benefit, risk, cost, and consequence if skipped.
4. Ask the user to approve, reject, defer, or adjust the plan.
5. Persist the user decision in `strategy_memory.json` and do not present rejected experiments as active strategy.

Recommended questionnaire shape:

```json
{
  "questionnaire_id": "strategy_decision_v1",
  "summary_before_question": "I recommend a hybrid strategy: address shared major concerns first, then use score-aware reviewer management. EXP-001 is must-do if rules allow; EXP-004 is too risky.",
  "questions": [
    {
      "id": "strategy_lens_choice",
      "type": "single_choice",
      "prompt": "Which strategy lens should we lock for drafting?",
      "options": [
        "recommended_hybrid",
        "score_aware_reviewer_management",
        "consensus_concern_resolution",
        "damage_control",
        "custom"
      ]
    },
    {
      "id": "focused_problem_scope",
      "type": "multi_select",
      "prompt": "Which focused problems must be covered in the top-level response?",
      "options": ["FP01", "FP02", "FP03", "FP04", "FP05", "FP06"]
    },
    {
      "id": "experiment_strategy_choice",
      "type": "multi_select",
      "prompt": "Which experiments should the strategy actively depend on?",
      "options": ["EXP-001", "EXP-002", "defer_experiments_until_results", "do_not_use_new_experiments"]
    }
  ]
}
```

If the response format is very limited, ask the user to choose the priority trade-off: maximize AC-legible common concerns, maximize per-reviewer coverage, maximize experiment evidence, or minimize risk.

## Coverage model

Even when selecting top 6, every indexed concern must be accounted for:

- `covered_by_focused_problem`
- `covered_by_minor_reply`
- `covered_by_global_theme`
- `deferred_with_reason`
- `needs_user_input`

This prevents the final response from silently dropping reviewer concerns.

## Output schema sketch

```json
{
  "version": "0.1",
  "strategy_status": "complete|partial|blocked",
  "selected_strategy_lens": "score_aware_reviewer_management|consensus_concern_resolution|ac_decision_fact_strategy|evidence_gap_closure|claim_scope_repair|venue_fit_reframing|defensive_stabilization|damage_control|hybrid",
  "strategy_rationale": "Why this lens fits the actual review pattern.",
  "reviewer_goal_model": {},
  "top_focused_problems": [],
  "strategy_matrix": [],
  "experiment_strategy_mapping": [],
  "user_strategy_decision": {},
  "strategy_questionnaire": {},
  "global_response_themes": [],
  "per_reviewer_strategy": [],
  "experiment_dependencies": [],
  "paper_edit_handoffs": [],
  "coverage_plan": {},
  "tone_plan": {},
  "next_routes": []
}
```

## Output report

```markdown
## Rebuttal Strategy Plan

- Strategy status: complete|partial|blocked
- Selected strategy lens: ...
- Strategy rationale: ...
- Response posture: evidence-first, bounded, professional battle; no empty apology, no unsupported arguing

### Top focused problems, by priority

1. <problem title>
   - Mentioned by: R1 (<anonymous_id>), R3 (<anonymous_id>)
   - Major/minor: major
   - Why it matters: ...
   - Strategy stance: ...
   - Evidence plan: ...
   - Linked experiments: EXP-* IDs, strategy usage, and user decision state
   - Success criterion: ...

...

### Reviewer goal model, if score-aware lens is used
- Stabilize/support:
- Lift/persuade:
- Weaken/recover:

If another lens is selected, explain the equivalent grouping, e.g. consensus themes, AC facts, evidence gaps, or claim-scope repairs.

### Global response themes
- ...

### Coverage plan
- Covered by top focused problems: <count>
- Minor/per-reviewer coverage: <count>
- Deferred/needs input: <count>

### Strategy decision questionnaire
- Recommended option: ...
- Alternatives and trade-offs: ...
- User decision state: accepted|pending|needs_revision

### Next routes
- `10_experiment_triage.md` only if new untriaged experiment needs appear
- `11_response_writer.md` after user-approved strategy and evidence state are ready
```

## Procedure

1. **Load priority and experiment analysis**
   - Read 07 output from `strategy_memory.json`.
   - Read 10 output from `experiment_memory.json`.
   - Confirm priority-ranked concerns, reviewer priority map, and numbered experiment candidates exist.
2. **Select strategy lens**
   - Choose the strategy lens from actual review evidence and author goals.
   - If using the user's score-aware lens, justify why it fits; otherwise explain the better lens.
3. **Build reviewer or concern goal model**
   - For score-aware strategy, group reviewers into stabilize / lift / weaken based on score, confidence, stance, and author priority.
   - For other strategies, group by consensus concerns, AC facts, evidence gaps, claim-scope repairs, or venue-fit themes.
4. **Select top focused problems**
   - Prefer major remarks, common concerns, high-confidence negative concerns, and addressable borderline concerns.
   - Merge overlapping concerns when a single response theme can cover them.
   - Limit to six unless user asks otherwise.
5. **Choose stance per problem**
   - Push, clarify, concede narrowly, soften, add experiment, explain trade-off, or defer.
6. **Map evidence, experiments, and gaps**
   - Link paper/code/review evidence and numbered `EXP-*` candidates; mark missing evidence honestly.
   - For each problem, decide whether an experiment is primary evidence, backup evidence, deferred, rejected, or unnecessary.
7. **Create paper-edit and writing handoffs**
   - Feed 11/12 for writing/template constraints and route back to 10 only for new untriaged experiment needs.
8. **Ask strategy decision questionnaire**
   - Present recommendation, alternatives, pros/cons, experiment dependencies, and risk.
   - Persist user approvals/rejections/deferrals.
9. **Build global themes and per-reviewer strategy**
   - Global themes cover shared top problems.
   - Per-reviewer strategy preserves reviewer-specific asks.
10. **Coverage audit**
   - Ensure every concern from 07 is covered, deferred, or needs input.
11. **Persist**
   - Update `.awesome-rebuttal/memory/strategy_memory.json`.
   - Write `.awesome-rebuttal/logs/rebuttal_strategy_plan.md`.

## Stop / proceed rules

Proceed to writing when:

- top focused problems are selected and reviewer sources are listed,
- each focused problem has stance, evidence plan, linked experiment IDs or explicit no-experiment rationale, and risk,
- the user has accepted/deferred/rejected strategy-critical experiment choices,
- coverage plan accounts for non-top concerns,
- missing evidence is explicit.

Proceed with warning when:

- paper/code memory is missing, so strategy is provisional,
- venue rules are unconfirmed, so final formatting/writing is blocked,
- evidence plan depends on user-provided results,
- user has not yet answered the strategy questionnaire, so the plan remains provisional.

Stop and ask when:

- 07 priority analysis is missing,
- 10 experiment memory is missing and strategy depends on new evidence,
- top priorities cannot be chosen because review source is conflicting,
- user asks for final text but required evidence or venue rules are unavailable.

## Safety rules

- Never fabricate results, numbers, reviewer positions, or paper evidence.
- Never over-apologize for valid contributions; concede narrowly and preserve supported claims.
- Never over-argue without evidence; route gaps to experiments or claim softening.
- Never drop lower-priority concerns; keep them in coverage.
- Keep AC-facing facts professional and rule-compliant.
