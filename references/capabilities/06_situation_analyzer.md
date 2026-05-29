# 06 Review Concern Analyzer

## Goal

Analyze the neutral review index from `05_review_normalizer.md` into semantic concern cards. This capability explains what each indexed issue is about, what kind of rebuttal evidence it may require, and how common concerns differ across reviewers.

This is the “understand the review content” layer. It should not yet rank priorities, classify the overall rebuttal posture, or decide AC-criticality. Those importance and situation judgments belong to `07_concern_atomizer.md`.

## Why this is separate from 05 and 07

- 05 preserves and indexes raw review material without judgment.
- 06 interprets the indexed material into concern semantics: topic, nature, evidence need, paper/code verification need, and reviewer-specific nuance.
- 07 weighs those analyzed concerns by scores, confidence, reviewer distribution, AC impact, response feasibility, and rebuttal goals.

This separation follows successful rebuttal workflows: preserve coverage first, understand concerns second, prioritize strategy third.

## Inputs

Read:

- `.awesome-rebuttal/memory/review_memory.json` from 05
- `.awesome-rebuttal/memory/paper_memory.json` if available
- `.awesome-rebuttal/memory/code_memory.json` if available
- `.awesome-rebuttal/memory/project_memory.json`

If `review_memory.json` is missing, unanchored, or lacks issue items, route back to 05.

## Boundary

### This capability does

- convert neutral issue items into semantic concern cards
- classify concern category and concern nature
- identify whether the issue is a claim challenge, evidence gap, wording/scope issue, request, praise, or venue-fit issue
- map common issue groups into semantic clusters
- preserve reviewer-specific nuance inside shared concerns
- identify candidate paper/code evidence needs without deciding priority
- mark possible misunderstandings only as hypotheses requiring paper/code verification
- write `.awesome-rebuttal/memory/review_analysis_memory.json`

### This capability does not

- rank concerns by importance
- mark reviewers as pivotal or persuadable
- classify overall posture such as `high_risk_reject` or `rebuttal_sensitive`
- decide response order, word budget, or AC summary need
- promise new experiments
- draft response text

## Semantic concern card

For each indexed issue item or related group, create:

```json
{
  "concern_id": "SC01",
  "source_issue_item_ids": ["RI:R1:001"],
  "reviewer_sources": ["R1"],
  "source_common_issue_ids": ["CI:novelty-loss-engineering"],
  "category": "novelty|method_design|baseline|dataset_subset|statistics|safety_claim|physical_feasibility|generalization|reproducibility|venue_fit|clarity|positive_evidence|other",
  "concern_nature": "claim_challenge|evidence_gap|experiment_request|clarification_request|scope_or_wording|subjective_judgment|possible_misunderstanding|positive_support|metadata",
  "semantic_summary": "Neutral interpretation of what the reviewer is saying.",
  "reviewer_specific_nuance": [],
  "paper_evidence_need": "none|check_existing_claim|find_table_or_figure|verify_wording|missing_paper_source|unknown",
  "code_evidence_need": "none|check_implementation|check_config|check_logs|missing_code|unknown",
  "candidate_response_families": ["clarification", "cite_existing_evidence", "additional_experiment", "narrow_concession", "claim_softening", "scope_boundary"],
  "verification_status": "verified_against_paper|verified_against_code|needs_paper_check|needs_code_check|unverified",
  "raw_anchors": ["REVIEW:R1:Weaknesses:W1"]
}
```

## Concern nature guide

Use these labels carefully:

- `claim_challenge`: reviewer challenges novelty, safety, physical feasibility, generality, or strength of claim.
- `evidence_gap`: reviewer asks for stronger evidence or points to insufficient support.
- `experiment_request`: reviewer explicitly requests sensitivity, baseline, significance, generalization, etc.
- `clarification_request`: reviewer asks for a missing value, threshold, construction criterion, or explanation.
- `scope_or_wording`: reviewer says terms are too strong or claims should be softened.
- `subjective_judgment`: reviewer makes a value judgment without a concrete requested action.
- `possible_misunderstanding`: only use if the statement appears checkable against paper/code; never mark as definite misunderstanding in 06.
- `positive_support`: reviewer praise or supportive evidence that can stabilize framing later.
- `metadata`: score, confidence, fit, or rubric-only item.

## Semantic common concern analysis

For each common issue index from 05, produce a non-priority semantic cluster:

```json
{
  "semantic_cluster_id": "SCC01",
  "source_common_issue_id": "CI:novelty-loss-engineering",
  "neutral_label": "novelty / loss-function engineering",
  "reviewer_sources": ["R1", "R2", "R3", "R5"],
  "semantic_core": "Reviewers see the method as mostly regularization/loss engineering rather than a new architecture.",
  "variant_readings": [
    {"reviewer_id": "R1", "variant": "says no new architecture/paradigm"},
    {"reviewer_id": "R3", "variant": "calls components straightforward and asks about alternatives"}
  ],
  "evidence_questions": ["What exact contribution wording is in the paper?", "Are ablations sufficient to support each component?"],
  "candidate_response_families": ["structural_distinction", "narrow_concession", "cite_ablation"]
}
```

Do not attach priority or AC-criticality here.

## Reviewer-level semantic summary

For each reviewer, summarize content without strategic labels:

- stable label and anonymous reviewer ID
- main positive topics
- main concern topics
- explicit questions/requests
- wording/scope issues
- metadata extracted from 05
- unknowns

Avoid terms like `pivotal`, `hard negative`, `persuadable`, or `must-win`.

## Evidence cross-check

Use paper/code memories only to set evidence availability, not to argue.

Evidence statuses:

- `paper_available`: source exists and likely contains relevant evidence
- `paper_missing`: paper memory blocked or absent
- `code_available`: code anchor likely relevant
- `code_missing`: code memory absent or no anchor found
- `needs_user_input`: cannot check without user-provided source/rules/results
- `not_applicable`

If paper source is missing, do not infer that a reviewer is wrong.

## Procedure

1. **Validate review index**
   - Confirm reviewer count, raw anchors, issue item index, and common issue index.
2. **Create semantic concern cards**
   - Convert issue items into concern cards while preserving source issue IDs.
3. **Build semantic common clusters**
   - Interpret each common issue neutrally and preserve reviewer-specific variants.
4. **Create reviewer semantic summaries**
   - Summarize positives, concerns, requests, and wording issues per reviewer.
5. **Cross-check evidence availability**
   - Use paper/code memories when present; otherwise mark missing or unknown.
6. **Coverage audit**
   - Ensure every 05 issue item appears in at least one semantic concern card or is explicitly marked metadata/praise.
7. **Persist memory**
   - Write `.awesome-rebuttal/memory/review_analysis_memory.json`.
   - Write `.awesome-rebuttal/logs/review_concern_analysis_report.md`.
8. **Route next**
   - Continue to `07_concern_atomizer.md` for priority, importance, and situation analysis.

## Output schema sketch

```json
{
  "version": "0.1",
  "status": "complete|partial|blocked",
  "source_review_memory": ".awesome-rebuttal/memory/review_memory.json",
  "reviewer_semantic_summaries": [],
  "semantic_concern_cards": [],
  "semantic_common_clusters": [],
  "evidence_availability": {},
  "coverage_audit": {},
  "open_questions": []
}
```

## Output report

```markdown
## Review Concern Analysis Report

- Status: complete|partial|blocked
- Source issue items: <count>
- Semantic concern cards: <count>
- Semantic common clusters: <count>
- Reviewer semantic summaries: <count>
- Evidence availability:
  - paper: available|missing|partial
  - code: available|missing|partial
- Coverage audit:
  - covered issue items: <count>
  - metadata/praise-only items: <count>
  - unresolved items: <count>
- Next route: `07_concern_atomizer.md`
```

## Stop / proceed rules

Proceed to 07 when:

- every issue item from 05 is covered or explicitly classified as metadata/praise,
- common issue semantics are described,
- evidence availability is marked without fabricating missing paper/code facts.

Proceed with warning when:

- paper/code memory is missing,
- some reviewer sections were hard to parse but raw anchors exist,
- semantic grouping is partial.

Stop and ask when:

- 05 review index is missing or unanchored,
- reviewer boundaries are unresolved,
- issue items cannot be traced to raw reviews.

## Safety rules

- Do not prioritize in 06.
- Do not call a concern invalid unless paper/code evidence proves it; usually mark `needs_paper_check`.
- Do not erase reviewer-specific variants inside common concerns.
- Do not invent experiments, values, or paper evidence.
