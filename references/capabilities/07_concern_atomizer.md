# 07 Priority and Situation Analyzer

## Goal

Analyze the priority, importance, and rebuttal situation implied by the semantic concern analysis from `06_situation_analyzer.md`, using the review-driven experiment memory from `10_experiment_triage.md` when available.

This is the strategic weighting layer. It decides which concerns matter most, why they matter, which reviewers or common issues are decision-critical, whether the paper is high-risk/borderline/rebuttal-sensitive, and how experiment feasibility should affect priority before final strategy planning.

## Inputs

Read:

- `.awesome-rebuttal/memory/review_analysis_memory.json` from 06
- `.awesome-rebuttal/memory/review_memory.json` from 05
- `.awesome-rebuttal/memory/experiment_memory.json` from 10 if available; in the standard workflow 10 is run after 06 and before this capability
- `.awesome-rebuttal/memory/paper_memory.json` if available
- `.awesome-rebuttal/memory/code_memory.json` if available
- `.awesome-rebuttal/memory/project_memory.json`
- confirmed venue rules if available
- author priorities from intake if available

If `review_analysis_memory.json` is missing, route back to 06. If `review_memory.json` is missing, route back to 05. If experiment memory is missing, proceed only when no strategy-critical experiment questions exist; otherwise route to 10 to create numbered experiment candidates before final priority weighting.

## Boundary

### This capability does

- classify overall rebuttal posture
- rank analyzed concerns by priority and decision importance
- determine core common concerns that should likely become global response themes
- build reviewer stance / risk / opportunity map
- identify AC-facing decision facts and likely meta-review issues
- use numbered experiment candidates from 10 to refine evidence-gap urgency and response feasibility
- route back to 10 only when a new untriaged experiment need appears
- create coverage and priority audits
- update `.awesome-rebuttal/memory/strategy_memory.json`

### This capability does not

- draft author responses
- invent evidence or experiment results
- decide final wording
- run experiments
- create full experiment candidate cards; that belongs in 10
- ignore low-priority concerns; they must remain in coverage audit

## Priority dimensions

Score each semantic concern qualitatively, with evidence:

| Dimension | Meaning |
|---|---|
| `reviewer_spread` | How many reviewers mention it? |
| `reviewer_weight` | Are high-confidence or negative reviewers involved? |
| `decision_relevance` | Could it change accept/reject decision? |
| `ac_criticality` | Is it likely to appear in AC/meta-review reasoning? |
| `evidence_availability` | Can paper/code/user evidence answer it? |
| `experiment_feasibility` | Do numbered `EXP-*` candidates make the evidence gap realistically answerable? |
| `response_feasibility` | Can it be addressed in rebuttal time/space? |
| `risk_if_unanswered` | What happens if ignored? |
| `positive_leverage` | Can supportive reviewers/strengths help stabilize it? |

Use these to assign:

- `priority_tier`: `P0_blocking|P1_core|P2_supporting|P3_minor|defer`
- `priority_confidence`: `high|medium|low`

## Rebuttal posture labels

Choose one primary label and optionally alternatives:

- `high_risk_reject`
- `borderline`
- `rebuttal_sensitive`
- `weak_accept_unstable`
- `split_review`
- `likely_accept_needs_stabilization`
- `unknown`

Posture should be justified by:

- score distribution
- confidence distribution
- count and nature of P0/P1 concerns
- whether common concerns are answerable
- presence of supportive reviewers and stable strengths
- venue-fit concerns
- whether reviewer disagreement is resolvable with facts

## Priority concern card

```json
{
  "priority_concern_id": "PC01",
  "semantic_concern_ids": ["SC01", "SC02"],
  "label": "novelty / loss-engineering concern",
  "reviewer_sources": ["R1", "R2", "R3", "R5"],
  "priority_tier": "P1_core",
  "priority_rationale": "Shared by multiple reviewers including reject and accept-side reviewers; affects contribution framing.",
  "decision_relevance": "high|medium|low",
  "ac_criticality": "high|medium|low",
  "response_feasibility": "high|medium|low|unknown",
  "evidence_status": "available|partial|missing|needs_experiment|needs_user_input",
  "linked_experiment_ids": ["EXP-001"],
  "recommended_handling": "global_theme|per_reviewer_detail|use_numbered_experiment|claim_softening|defer_with_reason|route_back_to_experiment_triage",
  "next_capability": "08_strategy_planner.md|10_experiment_triage.md|13_ac_summary_writer.md",
  "coverage_note": "..."
}
```

## Reviewer stance and priority map

For each reviewer:

```json
{
  "reviewer_id": "R1",
  "anonymous_id": "<anonymous_reviewer_id_or_unknown>",
  "rating": "2: Weak Reject",
  "confidence": "4: Expert",
  "stance": "negative|borderline|supportive|mixed|unknown",
  "risk_weight": "high|medium|low",
  "persuadability_estimate": "high|medium|low|unknown",
  "main_priority_concerns": ["PC01", "PC02"],
  "positive_leverage_points": [],
  "likely_decision_role": "hard_negative|pivotal|supportive_anchor|stabilize|unknown",
  "notes": []
}
```

This is where reviewer importance belongs, not in 05.

## Core common concern priority

For each common concern from 06, decide whether it should be:

- global response theme
- per-reviewer response detail
- experiment triage item
- AC summary fact
- claim-softening/concession point
- lower-priority coverage item

Common concerns are the center of this capability. Shared concerns often deserve a global framing response because ACs look for consensus patterns.

## Evidence gap urgency

Classify evidence gaps using existing `EXP-*` candidates when available:

- `numbered_experiment_available`: 10 already created an experiment candidate that can answer this gap
- `urgent_untriaged_experiment_candidate`: likely worth routing back to 10 immediately
- `paper_evidence_lookup`: answer likely exists in paper memory
- `code_evidence_lookup`: answer likely exists in code memory/logs
- `user_value_needed`: missing thresholds/results/rules from user
- `not_feasible_for_rebuttal`: should concede or scope
- `drafting_only`: can be handled by clearer wording

## AC-facing facts

Identify facts likely useful for AC, but do not draft the AC summary yet:

- reviewer split and score distribution
- strongest shared concerns
- strongest shared strengths
- evidence-addressable misunderstandings or gaps
- venue-fit disagreements
- limited but positive empirical gains
- reviewer requests that need experiments or user data

## Procedure

1. **Validate 06 output**
   - Ensure semantic concern cards and common clusters exist.
2. **Compute score/confidence summary**
   - Count rating classes and confidence levels.
3. **Rank concerns**
   - Apply priority dimensions to semantic concerns and common clusters.
4. **Build reviewer stance map**
   - Use metadata + concern priorities + positive support.
5. **Classify rebuttal posture**
   - Pick posture label with evidence and uncertainty.
6. **Build AC-facing decision facts**
   - Identify facts, not polished text.
7. **Build evidence gap urgency ledger**
   - Link priority concerns to `EXP-*` candidates from 10 where possible.
   - Feed `08_strategy_planner.md`; route back to `10_experiment_triage.md` only for new untriaged gaps.
8. **Coverage audit**
   - Ensure every semantic concern has priority status or explicit deferral.
9. **Persist strategy memory**
   - Write/update `.awesome-rebuttal/memory/strategy_memory.json`.
   - Write `.awesome-rebuttal/logs/priority_and_situation_report.md`.

## Output schema sketch

```json
{
  "version": "0.1",
  "analysis_status": "complete|partial|blocked",
  "posture": "rebuttal_sensitive",
  "posture_confidence": "medium",
  "posture_evidence": [],
  "score_confidence_summary": {},
  "priority_ranked_concerns": [],
  "core_common_concern_priority": [],
  "reviewer_priority_map": [],
  "ac_decision_facts": [],
  "evidence_gap_urgency": [],
  "experiment_priority_links": [],
  "coverage_audit": {},
  "next_routes": ["08_strategy_planner.md"]
}
```

## Output report

```markdown
## Priority and Situation Report

- Analysis status: complete|partial|blocked
- Rebuttal posture: ...
- Posture confidence: high|medium|low
- Reviewer distribution: ...
- P0/P1 concerns:
  - ...
- Core common concerns:
  - ...
- Reviewer priority map:
  - ...
- AC-facing decision facts:
  - ...
- Evidence gap urgency:
  - ...
- Experiment priority links:
  - PC01 -> EXP-001 (must_do, user_decision=unset)
- Coverage audit:
  - semantic concerns: <count>
  - priority-ranked: <count>
  - deferred/minor: <count>
  - needs input: <count>
- Next route: `08_strategy_planner.md` / `10_experiment_triage.md`
```

## Stop / proceed rules

Proceed to 08 when:

- posture is classified with evidence,
- P0/P1 concerns are identified,
- core common concerns are prioritized,
- reviewer priority map exists,
- numbered experiment candidates are linked or explicitly unnecessary for P0/P1 evidence gaps,
- coverage audit accounts for all semantic concerns.

Proceed with warning when:

- paper/code memory is missing, so evidence availability is uncertain,
- venue rules are missing, so final drafting constraints are unknown,
- experiment memory is partial, so strategy must ask the user before relying on new experiments,
- some ratings/confidence values are missing.

Stop and ask when:

- 06 semantic concern analysis is missing,
- priority would depend on choosing between conflicting review sources,
- user asks for drafting before core evidence gaps are acknowledged.

## Safety rules

- Every priority concern must trace to semantic concern IDs and raw review anchors.
- Do not mark a concern low priority just because it is hard.
- Do not overpromise experiments; use numbered candidates from 10 and keep user decisions explicit.
- Do not treat priority ranking as final response text.
- Keep all lower-priority concerns in coverage audit.
