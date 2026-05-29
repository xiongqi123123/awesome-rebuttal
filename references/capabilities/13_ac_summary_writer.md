# 13 AC Summary Writer

## Goal

Recommend, plan, and draft an AC-oriented summary when it is allowed by the venue rules and useful for the decision. The core purpose is to help the AC see the decision-relevant facts that may be scattered across reviewer replies, especially when a low-score or reject rationale could dominate the meta-review despite shared positive assessments or newly clarified evidence.

This capability should use a “borrow strength from the review record” strategy: politely cite consensus strengths and shared positive reviewer observations, then connect them to the rebuttal evidence that addresses the low-score concerns. It must not attack any reviewer, rank reviewers against each other, command the AC, or imply that positive reviewers invalidate negative reviewers.

## Language policy

User-facing planning notes may follow the user's language, but generated rebuttal prose/comments/PDF text default to English unless confirmed venue rules require otherwise.

## Required inputs

Read before deciding or drafting:

- `.awesome-rebuttal/memory/strategy_memory.json` from 08 — required
- `.awesome-rebuttal/memory/response_memory.json` from 11, if a response draft exists
- `.awesome-rebuttal/memory/experiment_memory.json` from 10 — required if new evidence or diagnostic results are mentioned
- `.awesome-rebuttal/memory/review_memory.json` from 05 — required for reviewer labels, anonymous IDs, ratings/confidence, and raw anchors
- `.awesome-rebuttal/memory/review_analysis_memory.json` from 06 — required for semantic concerns and shared positive/negative themes
- `.awesome-rebuttal/memory/paper_memory.json` — required for paper story, claims, scope, contributions, and existing evidence
- `.awesome-rebuttal/memory/code_memory.json` — required when implementation, runtime, reproducibility, or experiment feasibility is mentioned
- `.awesome-rebuttal/memory/project_memory.json` and confirmed venue rules — required to know whether AC/global summary text is allowed

If venue rules are unconfirmed or prohibit global/AC-facing text, do not draft a paste-ready AC summary. Instead, record a blocked decision and, if possible, adapt the same facts into the allowed response format.

## Outputs

Write:

```text
.awesome-rebuttal/memory/ac_summary_memory.json
.awesome-rebuttal/drafts/ac_summary_draft.md
.awesome-rebuttal/logs/ac_summary_writer_report.md
```

If the summary is not allowed or not useful, still write `ac_summary_memory.json` with `decision: no|blocked` and the rationale.

## When to include an AC summary

Recommend an AC-oriented summary when one or more conditions holds:

- a low-score/high-confidence reviewer has a central reject rationale that the rebuttal directly addresses;
- reviews are split and the AC needs a concise decision-relevant synthesis;
- positive reviewers share strengths that directly support the paper's core contribution;
- major concerns are common but now answered by verified evidence, approved experiments, or clear scope revisions;
- decision-critical facts are scattered across per-reviewer responses;
- the response format allows a short global opening or AC-directed summary.

Do **not** include one when:

- venue rules disallow global summaries or AC-specific text;
- the summary would consume scarce one-page space better used for direct concern answers;
- there is no meaningful reviewer split or low-score issue to contextualize;
- the summary would rely on unsupported results, speculative claims, or hidden reviewer comparison;
- it would sound like lobbying rather than factual synthesis.

## AC summary posture

The posture is: **grateful + factual + decision-relevant + non-commanding**.

Use:

- “We thank the AC and reviewers...”
- “We appreciate that reviewers recognized...” only when anchored in review strengths.
- “The main concerns focus on...” to neutrally summarize shared issues.
- “In the rebuttal, we address...” to point to evidence or clarifications.
- “Regarding Reviewer `<id>`'s assessment...” to contextualize a low score without attacking it.
- “We understand that the low score is mainly related to...” only if review evidence supports that diagnosis.
- “Our analysis suggests...” only when supported by paper/experiment/code evidence.
- “We hope the AC will consider...” as a polite request, not a command.

Avoid:

- “The AC should ignore Reviewer R...”
- “The low-score reviewer misunderstood everything.”
- “Other reviewers liked the paper, therefore the reject is invalid.”
- “We ask the AC to raise the score...”
- “Clearly / obviously / undoubtedly” unless the claim is directly proven.
- private or deanonymizing details, external links, or unconfirmed results.

## Core rhetorical structure

A strong AC summary usually has two compact paragraphs, or one paragraph if space is very tight.

### Paragraph 1 — shared ground and decision-critical concerns

Purpose: set the decision frame using review-record facts.

Structure:

1. Thank AC and reviewers.
2. Borrow shared positive recognition: motivation, importance, practical value, problem gap, method design, clarity, or empirical promise.
3. State the main concerns neutrally and collectively.
4. State that the rebuttal addresses them with specific evidence, clarifications, approved experiments, or revisions.

Template:

```text
We thank the AC and reviewers for their careful and constructive feedback. We appreciate that the reviews recognized <shared strength(s) anchored to reviewer comments>. The main concerns focus on <decision-critical concern cluster(s)>. In the rebuttal, we directly address these concerns with <verified evidence / approved experiments / clarifications / scoped revisions>.
```

### Paragraph 2 — low-score contextualization without attacking

Purpose: reduce the force of a low-score or reject rationale by stating what the concern is, how it is addressed, and why the core contribution remains supported.

Structure:

1. Name the reviewer/assessment neutrally if rules allow.
2. State what the low score appears to be based on, using review evidence.
3. State how the rebuttal addresses it, with result/status/provenance.
4. Explain the bounded diagnosis or corrected scope.
5. Politely ask the AC to consider the new/clarified evidence together with shared positive assessments.

Template:

```text
Regarding Reviewer <stable_or_anonymous_id>'s assessment, we understand that the low score is mainly related to <specific concern>. We address this in the rebuttal with <evidence/analysis/clarification>, and will incorporate the corresponding revision if accepted. The evidence suggests <bounded conclusion> while preserving <supported core contribution>. We hope the AC will consider this evidence together with the reviewers' positive assessment of <shared strengths> when making the final decision.
```

If reviewer-specific discussion is not allowed, replace reviewer naming with:

```text
Regarding the lowest-score assessment, ...
```

or omit the second paragraph and fold the fact into a global concern block.

## Decision model

Create an `ac_summary_decision` before drafting:

```json
{
  "decision": "yes|no|blocked",
  "reason": "split_review|low_score_context|scattered_decision_facts|not_allowed|not_useful|insufficient_evidence",
  "venue_rule_status": "confirmed_allowed|confirmed_disallowed|needs_confirmation",
  "recommended_placement": "opening_global_paragraph|closing_global_paragraph|separate_ac_summary|hybrid_global_intro|do_not_include",
  "target_length": "one_sentence|one_short_paragraph|two_short_paragraphs|bullets",
  "space_budget": {"target_words": 120, "max_words": 180},
  "risk_level": "low|medium|high",
  "required_user_confirmation": true
}
```

## AC fact ledger

Use facts from 07/08, but verify them before drafting:

```json
{
  "fact_id": "ACF-001",
  "fact_type": "shared_strength|common_concern|low_score_rationale|new_evidence|diagnosis|scope_revision|experiment_result|paper_claim",
  "summary": "...",
  "source": "review|paper|code|experiment|strategy|user|venue_rule",
  "source_anchor": "...",
  "reviewer_sources": [
    {"stable_label": "R2", "anonymous_id": "<anonymous_id_or_unknown>", "role": "positive_strength|low_score_concern|shared_concern"}
  ],
  "support_status": "verified|needs_user_confirmation|blocked",
  "allowed_in_ac_summary": true
}
```

Only `verified` facts should appear in paste-ready prose. `needs_user_confirmation` facts may appear as TODO placeholders in a draft, not final text.

## Low-score handling model

For each low-score or reject reviewer that may matter:

```json
{
  "reviewer": {"stable_label": "R1", "anonymous_id": "<anonymous_id_or_unknown>"},
  "rating": "...",
  "confidence": "...",
  "main_low_score_rationale": "...",
  "rationale_source_anchors": [],
  "is_rationale_factual_misunderstanding": "yes|no|partial|unknown",
  "is_rationale_addressed": "yes|partial|no",
  "addressing_evidence": ["paper_anchor", "EXP-001", "response_unit_id"],
  "safe_ac_framing": "...",
  "unsafe_framing_to_avoid": "..."
}
```

This model is for factual context, not reviewer ranking. Do not compare reviewers as “good” and “bad.”

## User confirmation questionnaire

Even when the skill recommends an AC summary, the user decides whether to include it. Use `references/core/user_questionnaire_protocol.md` when:

- venue rules may not allow AC-specific/global text;
- the summary consumes limited one-page space;
- naming the low-score reviewer may be sensitive;
- the user must choose between direct concern coverage and AC framing;
- new evidence/result status needs confirmation.

Recommended questionnaire:

```json
{
  "questionnaire_id": "ac_summary_decision_v1",
  "summary_before_question": "I recommend a short AC-facing opening because the reviews share positive recognition of the work, while one low-score rationale may dominate the decision. The summary would stay factual and non-commanding.",
  "questions": [
    {
      "id": "include_ac_summary",
      "type": "single_choice",
      "prompt": "Should we include an AC-oriented summary if the rules allow it?",
      "options": ["yes_short_opening", "yes_closing_note", "no_save_space_for_concerns", "blocked_until_rules_confirmed"]
    },
    {
      "id": "low_score_reference_style",
      "type": "single_choice",
      "prompt": "How should we refer to the low-score concern?",
      "options": ["name_reviewer_if_allowed", "say_lowest_score_assessment", "avoid_reviewer_specific_reference"]
    },
    {
      "id": "positive_strengths_to_borrow",
      "type": "multi_select",
      "prompt": "Which verified shared strengths should the summary use?",
      "options": ["motivation", "problem_gap", "practical_value", "method_design", "evaluation_strength", "clarity", "none"]
    }
  ]
}
```

## Output schema sketch

```json
{
  "version": "0.1",
  "status": "ready|partial|blocked|not_recommended",
  "decision": {},
  "source_strategy_memory": ".awesome-rebuttal/memory/strategy_memory.json",
  "source_response_memory": ".awesome-rebuttal/memory/response_memory.json",
  "ac_fact_ledger": [],
  "low_score_context": [],
  "shared_positive_assessment": [],
  "decision_critical_concerns": [],
  "evidence_to_highlight": [],
  "draft_variants": [],
  "selected_draft": {},
  "coverage_and_risk_check": {},
  "user_confirmation": {},
  "open_questions": []
}
```

## Draft variants

Generate variants when useful:

1. `ultra_short_opening` — 1-2 sentences for severe space limits.
2. `standard_two_paragraph` — shared positives + low-score contextualization.
3. `no_reviewer_specific` — avoids naming any reviewer or low-score reviewer.
4. `closing_note` — if opening space is better used for direct answers.

Each variant should include:

- word count;
- allowed placement;
- risk level;
- facts used;
- facts omitted;
- whether user/venue confirmation is required.

## Output report

```markdown
## AC Summary Decision

- Decision: yes|no|blocked
- Reason: ...
- Venue/rule status: ...
- Recommended placement: ...
- Target length: ...
- Main risk: ...

### Facts used

| Fact | Source | Status | Use |
|---|---|---|---|
| Shared motivation praise | R2/R3 review anchors | verified | opening |
| Low-score rationale | R1 weakness anchor | verified | paragraph 2 |
| New evidence | EXP-001 result log | verified/needs_confirmation | paragraph 2 |

### Draft

<AC summary draft or TODO placeholders>

### Safety notes

- No reviewer attack:
- No reviewer ranking:
- No unsupported result:
- Rule compliant:
```

## Procedure

1. **Confirm rule allowance**
   - Check whether global/AC-facing summary text is allowed.
   - If unclear, ask or block paste-ready drafting.
2. **Decide whether summary is useful**
   - Use 07/08 posture, reviewer split, low-score rationale, AC facts, and response format.
3. **Build AC fact ledger**
   - Extract shared positive assessments, common concerns, low-score rationale, evidence, and diagnosis.
4. **Verify facts**
   - Check every fact against review/paper/code/experiment/response memory.
5. **Choose placement and length**
   - Opening, closing, separate AC summary, hybrid global intro, or do not include.
6. **Ask user confirmation if needed**
   - Especially for low-score reference style and space trade-off.
7. **Draft variants**
   - Use the two-paragraph structure by default when space allows.
8. **Run safety precheck**
   - No reviewer attack, no reviewer ranking, no unsupported claims, no rule violation.
9. **Persist outputs**
   - Write `ac_summary_memory.json`, draft, and report.
10. **Route next**
   - Route to `11_response_writer.md` if the AC summary must be integrated into the full response.
   - Route to `12_template_designer.md` if it must fit a one-page PDF.
   - Route to `14_safety_rule_checker.md` before final/paste-ready use.

## Stop / proceed rules

Proceed to draft when:

- venue rules allow the summary or global opening;
- facts are verified;
- the summary has a clear decision purpose;
- the user has confirmed inclusion if space or tone trade-offs are material.

Proceed with warning when:

- the summary is useful but space-limited, so only an ultra-short variant is feasible;
- reviewer-specific naming is not confirmed, so a no-reviewer-specific variant is safer.

Stop and ask when:

- rules are unconfirmed;
- the low-score rationale is inferred but not anchored in the review;
- new evidence/result status is missing;
- the summary would reduce direct coverage of P0/P1 concerns too much;
- user preference determines whether to include or omit the summary.

## Safety rules

- The AC summary is a factual synthesis, not lobbying.
- Do not instruct the AC how to decide; politely ask them to consider verified evidence.
- Do not portray low-score reviewers as wrong, careless, or less important.
- Do not pit reviewers against each other; use positive reviewer comments only as part of the review record.
- Do not introduce new claims beyond the strategy and evidence memory.
- Do not mention LeafLink, private links, hidden identities, or unconfirmed artifacts.
