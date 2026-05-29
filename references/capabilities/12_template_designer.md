# 12 Format-Aware Template Designer

## Goal

Turn the approved response plan from `11_response_writer.md` into the correct output structure for the confirmed venue format: one-page PDF/LaTeX, `openreview_per_reviewer` Markdown files, `global_comment` Markdown text, or `openreview_markdown_latex` comments. This capability controls layout and file organization; it does not invent content.

## Language policy

User-facing planning notes may follow the user's language, but generated rebuttal prose/comments/PDF text default to English unless confirmed venue rules require otherwise.

## Required inputs

Read:

- `.awesome-rebuttal/memory/project_memory.json` — response mode, workspace paths, venue/rule status
- `.awesome-rebuttal/memory/template_memory.json` from 17 — active template source/status
- `.awesome-rebuttal/memory/response_memory.json` from 11 — response units, draft outputs, coverage map, length budgets
- `.awesome-rebuttal/memory/ac_summary_memory.json` from 13, if AC summary is included
- confirmed venue rules (`venue_rules.schema.json` fields: response.mode, response.limits, response permissions, content_permissions, formatting, anonymity, confirmation, language_policy) / response limits
- `.awesome-rebuttal/memory/venue_rules.json` if present

If `response_memory.json` is missing, route to 11. If response mode or venue rules are missing, ask through the shared questionnaire protocol.

## Outputs

Write under the active workspace:

```text
.awesome-rebuttal/
├── drafts/
│   ├── final-response-layout.md
│   ├── openreview-comments/
│   │   ├── R1.md
│   │   ├── R2.md
│   │   └── global-response.md
│   └── latex-mixed-comments/
├── templates/
│   └── active-rebuttal-template/
├── memory/
│   └── template_memory.json
└── logs/
    └── template_designer_report.md
```

Export to `Paper/` or another user-visible location only when the user asks or the workflow reaches finalization.

## Template family selection

Use confirmed response mode and venue rules.

| Response mode | Default output family | File organization | Notes |
|---|---|---|---|
| `pdf_one_page` | ECCV/CVPR-style two-column LaTeX template | `.awesome-rebuttal/templates/active-rebuttal-template/rebuttal.tex` | Use official/user template if provided; otherwise built-in fallback from 17. |
| `unified_limited` | Compact unified Markdown blueprint or PDF-ready section plan | `.awesome-rebuttal/drafts/final-response-layout.md` | Use for strict word/page/character limits where common concerns must be merged and prioritized. |
| `openreview_per_reviewer` | Markdown per reviewer | `.awesome-rebuttal/drafts/openreview-comments/R*.md` | Use for OpenReview-style reviewer threads when rules/platform allow reviewer-specific replies. |
| `global_comment` | Markdown or Markdown+LaTeX global comment | `.awesome-rebuttal/drafts/openreview-comments/global-response.md` | Use one global response box/comment. |
| `hybrid` | Global Markdown plus per-reviewer Markdown | `global-response.md` plus `R*.md` files | Keep global AC/common issues short; reviewer files contain deltas. |
| `openreview_markdown_latex` | Markdown with inline LaTeX math/table fragments | `.awesome-rebuttal/drafts/latex-mixed-comments/*.md` | Use when platform supports Markdown-style comments with LaTeX math; confirm rules first. |

For ICML-like or other OpenReview-style threaded rebuttals, do **not** assume the current year's rules. If confirmed rules say each reviewer has an interactive/comment thread, generate one Markdown file per reviewer and optionally a global note. If confirmed rules say only one global comment is allowed, generate only the global file.

## One-page PDF / ECCV-CVPR-style layout

Use `17_rebuttal_template_manager.md` to prepare the active LaTeX template.

Recommended structure:

1. Optional compact opening / AC facts, only if allowed and valuable.
2. 3-6 grouped concern blocks from 11 response units.
3. Compact verified tables/figures only when they save space and are rule-compliant.
4. One-sentence residual clarifications for lower-priority issues.
5. No long closing unless required.

Layout rules:

- Prefer grouped headings such as `Question 1: <topic> (<reviewer labels>)` when rules allow reviewer IDs.
- Use verified reviewer labels/anonymous IDs from `review_memory.json`; do not invent or expose hidden identities.
- Keep headings short to avoid two-column overflow.
- Keep tables compact and only with verified numbers from `response_memory.numeric_claims`.
- Do not include hyperlinks, supplementary references, or external resources unless venue rules confirm they are allowed.
- If LaTeX compilation is unavailable, still generate `.tex` and mark compile status blocked.

## Per-reviewer Markdown layout

Use when the venue/platform allows reviewer-specific replies or threaded discussion.

Generate:

```text
.awesome-rebuttal/drafts/openreview-comments/
├── README.md                 # paste order and rule notes
├── global-response.md         # optional, only if allowed/useful
├── R1.md
├── R2.md
└── R3.md
```

Each `R*.md` should contain:

```markdown
# Response to Reviewer R1 (`<anonymous_id_or_unknown>`)

> Paste target: `<thread/comment target>`
> Status: draft|ready|blocked
> Safety: run 14 before paste

Thank you for your constructive feedback.

## Major concern: <topic>

<evidence-aligned response from RU-*>

## Minor clarifications

- <short item>
```

Rules:

- Major concerns before minor concerns.
- Do not duplicate long global explanations in every reviewer file; refer to a global response only if rules/platform allow it.
- Preserve reviewer-specific tone and goals from 08.
- Keep Markdown simple: headings, bullets, compact tables only if platform supports them.

## Markdown+LaTeX hybrid layout

Use for OpenReview-style comments when confirmed platform/rules support Markdown plus LaTeX math fragments.

Guidelines:

- Write prose in Markdown.
- Use inline LaTeX for symbols: `$\tau$`, `$\Delta$`, `$O(n)$`.
- Use display math sparingly and only when necessary.
- Prefer Markdown tables for simple numeric comparisons; use LaTeX tabular fragments only if the platform renders them reliably and rules allow.
- Avoid custom macros that may not render in platform comments.
- Avoid image/PDF dependencies unless rules explicitly allow attachments or links.
- Keep a plain-text fallback for every math-heavy statement.

## Hybrid global + per-reviewer layout

Use when a global summary is allowed and per-reviewer replies are also allowed.

- `global-response.md`: shared strengths, common major concerns, AC-legible facts, and shared experiment evidence.
- `R*.md`: reviewer-specific remaining concerns and deltas only.
- Avoid contradictions: global response and reviewer files must use the same values, experiment statuses, and claim scope.

## Template source safety

Template Designer must respect 17's source priority:

1. user-provided official template;
2. AI-found official template, after user confirmation;
3. built-in ECCV/CVPR-style one-page fallback for `pdf_one_page` only.

Never present fallback as official. Never overwrite user templates without backup/confirmation.

## Template memory fields

Update `.awesome-rebuttal/memory/template_memory.json` with:

```json
{
  "layout_family": "pdf_one_page|unified_limited|openreview_per_reviewer|openreview_global|openreview_markdown_latex|hybrid",
  "generated_files": [],
  "paste_targets": [],
  "length_budget": {},
  "compile_or_render_status": "not_applicable|not_attempted|passed|failed|blocked_missing_latex|needs_platform_preview",
  "consistency_checks": {
    "response_units_mapped": "pass|blocked",
    "numeric_claims_verified": "pass|blocked|needs_user_confirmation",
    "rule_constraints_applied": "pass|blocked|needs_user_confirmation"
  }
}
```

## Output report

```markdown
## Template Design Report

- Response mode:
- Layout family:
- Template source:
- Generated files:
- Paste/export targets:
- Length/page constraints:
- Compile/render status:
- User confirmation needed:
- Next route: 14_safety_rule_checker.md
```

## Stop / proceed rules

Proceed when:

- response mode and limits are confirmed;
- response units from 11 are available;
- template source is selected or not needed;
- generated files map every ready response unit.

Proceed with warning when:

- LaTeX compile is unavailable but `.tex` can still be generated;
- platform rendering of Markdown+LaTeX needs manual preview;
- some lower-priority response units are intentionally compressed.

Stop and ask when:

- response mode is unknown;
- venue rules about global vs per-reviewer replies are unclear;
- a one-page PDF is requested but no official/fallback template decision is approved;
- generated output would require omitting P0/P1 concerns.

## Safety rules

- Template/layout decisions must not change factual content.
- Do not add unsupported claims to fit layout.
- Do not include private paths, LeafLink text, or local tool instructions in paste-ready comments.
- Run 14 before final copy/paste or PDF export.
