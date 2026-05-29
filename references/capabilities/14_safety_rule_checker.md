# 14 Safety Rule Checker

## Goal

Gate every final or paste-ready output, using response memory, AC summary memory, generated template files, strategy/experiment memories, and confirmed venue rules (`venue_rules.schema.json` fields: response.mode, response.limits, response permissions, content_permissions, formatting, anonymity, confirmation, language_policy). This capability decides whether text can be copied into the conference system or exported as a final PDF/comment.

## Inputs

Read:

- `.awesome-rebuttal/memory/response_memory.json` from 11
- `.awesome-rebuttal/memory/ac_summary_memory.json`, if present
- `.awesome-rebuttal/memory/template_memory.json` from 12/17
- `.awesome-rebuttal/memory/strategy_memory.json`
- `.awesome-rebuttal/memory/experiment_memory.json`
- `.awesome-rebuttal/memory/review_memory.json`
- `.awesome-rebuttal/memory/review_analysis_memory.json`
- `.awesome-rebuttal/memory/paper_memory.json`
- `.awesome-rebuttal/memory/code_memory.json`, when implementation/results are mentioned
- `.awesome-rebuttal/memory/project_memory.json`
- confirmed venue rules (`venue_rules.schema.json` fields: response.mode, response.limits, response permissions, content_permissions, formatting, anonymity, confirmation, language_policy) / `venue_rules.json` if present
- generated draft files under `.awesome-rebuttal/drafts/` and/or active LaTeX template

If response memory is missing, run 11 before paste-ready safety checking.

## Outputs

Write:

```text
.awesome-rebuttal/memory/safety_memory.json
.awesome-rebuttal/logs/final_safety_check.md
```

Optionally write annotated blocking fixes into `.awesome-rebuttal/drafts/safety_fixes.md`.

## Safety gates

Each gate is `pass`, `blocked`, or `needs_user_confirmation`.

1. **Provenance gate**
   - Every factual claim maps to paper, code, review, experiment, venue rule, or user-provided evidence.
   - Every numeric claim has a verified source anchor.
2. **Experiment/result gate**
   - New results are mentioned only if `experiment_memory` says result is available/verified and user-approved.
   - Planned/running experiments are not phrased as completed.
3. **Commitment gate**
   - Every promise is already done, explicitly approved, or clearly framed as future revision/future work.
4. **Coverage gate**
   - Every reviewer concern is answered, intentionally deferred, or marked `needs_user_input`.
   - P0/P1 concerns are not silently compressed away.
5. **Venue-rule gate**
   - Format, length/page limits, anonymity, links, supplements, attachments, new results, and discussion behavior are confirmed and obeyed.
   - Response mode uses the canonical `response.mode` vocabulary and matches the generated layout.
   - Submission-facing text language matches `language_policy.final_writing_language` (English by default).
6. **Tone gate**
   - Professional, concise, and evidence-first.
   - No reviewer attacks, no “reviewer failed to understand,” no manipulative flattery, no score lobbying.
7. **Anonymity/privacy gate**
   - No hidden author identity, local paths, private repository paths, Overleaf/LeafLink mention, or private links in submission-facing text.
8. **Consistency gate**
   - Paper, code, experiment, and draft wording agree on dataset names, metrics, table numbers, hyperparameters, claims, and limitations.
9. **Unknown/TODO gate**
   - No TODO placeholders, unresolved questions, or unconfirmed values remain in paste-ready output.

## Claim audit record

Use compact records for any flagged or high-risk claim:

```json
{
  "claim_id": "CL-001",
  "text_excerpt": "...",
  "claim_type": "numeric|experiment_result|paper_claim|code_detail|venue_rule|reviewer_position|promise|tone|privacy",
  "source_required": true,
  "source_found": "paper_memory:table_2|experiment_memory:EXP-001|review_memory:R2.anchor_4",
  "status": "pass|blocked|needs_user_confirmation",
  "fix": "Replace with verified value or remove claim."
}
```

## Format-specific checks

### One-page PDF / LaTeX

- Compile status recorded if local LaTeX is available.
- Page count within limit if compilation is possible.
- No overflow-prone huge tables unless intentionally accepted.
- Conference/year/paper ID fields match confirmed rules.
- No unconfirmed hyperlinks or external attachments.

### Per-reviewer Markdown

- Each reviewer file maps to the correct reviewer/thread target.
- No reviewer-specific response references another reviewer in a hostile or comparative way.
- Shared content is not contradictory across files.
- Paste targets and reviewer anonymous IDs are recorded but safe.

### Markdown+LaTeX hybrid comments

- No fragile custom macros.
- Math notation has plain-text context.
- Tables are platform-safe or marked for manual preview.
- Render/paste preview is recommended when platform behavior is uncertain.

### AC summary

- Rule allows AC/global summary.
- No reviewer ranking or “positive reviewers overrule negative reviewer” framing.
- Low-score context is anchored and non-attacking.

## Output report

```markdown
## Safety Check

- Overall: pass|blocked|needs_user_confirmation
- Checked files:
  - ...

| Gate | Status | Evidence | Blocking fixes |
|---|---|---|---|
| Provenance | | | |
| Experiment/result | | | |
| Commitment | | | |
| Coverage | | | |
| Venue rules | | | |
| Tone | | | |
| Anonymity/privacy | | | |
| Consistency | | | |
| Unknowns/TODOs | | | |

## Blocking fixes

1. ...

## Approval note

Do not copy/paste or export final PDF until all blocking gates pass.
```

## Stop / proceed rules

Return `pass` only when all gates pass. Return `needs_user_confirmation` when the remaining issue is a user/rule decision. Return `blocked` when the draft contains unsupported claims, safety violations, or unresolved TODOs.

Do not “fix” facts by inventing replacements. Route back to the responsible capability:

- missing evidence -> 03/04/10/11
- strategy conflict -> 08
- format/layout issue -> 12/17
- AC summary issue -> 13
- venue/rule issue -> 01/17 or user confirmation
- snapshot/versioning issue -> 09/16
