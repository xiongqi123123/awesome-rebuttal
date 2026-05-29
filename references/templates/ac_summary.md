# AC-Oriented Summary Template

Use only if confirmed venue rules allow global or AC-facing text.

## Decision

- Include AC summary: yes|no|blocked
- Reason: split_review|low_score_context|scattered_decision_facts|not_allowed|not_useful|insufficient_evidence
- Rule source:
- Recommended placement: opening_global_paragraph|closing_global_paragraph|separate_ac_summary|hybrid_global_intro|do_not_include
- Target length: one_sentence|one_short_paragraph|two_short_paragraphs|bullets
- User confirmation:

## Fact ledger

| Fact ID | Type | Summary | Source anchor | Status | Use |
|---|---|---|---|---|---|
| ACF-001 | shared_strength | | | verified|needs_confirmation|blocked | opening |
| ACF-002 | low_score_rationale | | | verified|needs_confirmation|blocked | context |
| ACF-003 | evidence_to_highlight | | | verified|needs_confirmation|blocked | context |

## Draft skeleton

```text
We thank the AC and reviewers for their careful and constructive feedback. We appreciate that the reviews recognized <verified shared strengths>. The main concerns focus on <decision-critical concern cluster>. In the rebuttal, we directly address these concerns with <verified evidence / clarifications / approved experiments>.

Regarding <reviewer reference style>, we understand that the low score is mainly related to <anchored concern>. We address this with <evidence/analysis/clarification> and will incorporate the corresponding revision if accepted. The evidence suggests <bounded conclusion> while preserving <supported contribution>. We hope the AC will consider this evidence together with the reviewers' positive assessment of <shared strengths> when making the final decision.
```

## Safety checklist

- [ ] Rule allows this summary.
- [ ] No reviewer attack.
- [ ] No reviewer ranking or “positive reviewers overrule negative reviewer” framing.
- [ ] Every positive strength is anchored in reviews.
- [ ] Every result/evidence claim is verified.
- [ ] Tone is grateful, factual, and non-commanding.
