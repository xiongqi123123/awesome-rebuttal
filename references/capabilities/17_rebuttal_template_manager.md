# 17 Rebuttal Template Manager

## Goal

Select, fetch, copy, or adapt the response template after venue rules and response format are known or user-confirmed. This capability prepares template assets; `12_template_designer.md` fills them with response units and generates per-format files.

## Source priority

Use this order:

1. **User-provided official template**
   - PDF/LaTeX/Word/template screenshot or official link supplied by the user.
   - Highest priority. Copy or summarize into project state.
2. **AI-found official template**
   - Search official venue/year sources only when user authorizes search.
   - Summarize source/date and ask user to confirm before use.
3. **Built-in one-page fallback template**
   - Use only for `pdf_one_page` when no official template is available/confirmed.
   - Built-in asset path: `assets/one-page-rebuttal-template/`.
   - Treat as ECCV/CVPR-style two-column fallback, not official venue truth.
4. **Generated Markdown templates**
   - Use for `unified_limited`, `openreview_per_reviewer`, `global_comment`, or `hybrid` responses when no file template is needed.

## Response-format policy

### `pdf_one_page`

- Prefer official/user template.
- If unavailable, use built-in ECCV/CVPR-style two-column fallback.
- Adapt only metadata and placeholders until rules are confirmed.
- Requires LaTeX only for compilation, not for drafting `.tex`.

### `openreview_per_reviewer`

- Generate one Markdown file per reviewer under `.awesome-rebuttal/drafts/openreview-comments/`.
- Use reviewer stable labels and anonymous IDs from `review_memory.json`.
- Do not create a one-page PDF unless the user explicitly wants a local planning artifact.

### `unified_limited`

- Generate one compact Markdown scaffold under `.awesome-rebuttal/drafts/final-response-layout.md`.
- Organize by the highest-priority common concerns rather than reviewer-by-reviewer sections.
- Preserve a coverage checklist so lower-priority reviewer concerns are either answered, compressed, or intentionally deferred.

### `global_comment`

- Generate a single `global-response.md`.
- If platform supports Markdown+LaTeX comments and rules allow, mark `layout_family: openreview_markdown_latex`.

### `hybrid`

- Generate `global-response.md` plus `R*.md` reviewer files.
- Keep shared common concerns in global; reviewer files contain deltas.

### `openreview_markdown_latex`

- Use Markdown plus lightweight LaTeX math when rules/platform allow.
- Avoid custom macros, external image dependencies, or complex LaTeX tables unless previewed/confirmed.

## Project state locations

Do not write template state into the installed skill folder during normal use. In each workspace:

```text
.awesome-rebuttal/
├── templates/
│   ├── active-rebuttal-template/
│   └── template-source-summary.md
├── drafts/
│   ├── openreview-comments/
│   └── latex-mixed-comments/
├── memory/
│   └── template_memory.json
├── snapshots/
└── logs/
```

Generated final submission files may be exported to `Paper/` only when the user asks or finalization begins.

## Template decision fields

Persist in `.awesome-rebuttal/memory/template_memory.json`:

```json
{
  "version": "0.1",
  "status": "missing|user_provided|ai_found_pending_confirmation|confirmed|fallback_builtin|generated_markdown|not_applicable",
  "response_mode": "openreview_per_reviewer|unified_limited|pdf_one_page|global_comment|hybrid|openreview_markdown_latex|unknown",
  "layout_family": "pdf_one_page|unified_limited|openreview_per_reviewer|openreview_global|openreview_markdown_latex|hybrid",
  "source": "user|official_search|builtin|generated|none",
  "source_url": "",
  "workspace_template_dir": ".awesome-rebuttal/templates/active-rebuttal-template/",
  "draft_output_dir": ".awesome-rebuttal/drafts/openreview-comments/",
  "built_in_asset": "assets/one-page-rebuttal-template/",
  "requires_latex": true,
  "confirmed_by_user": false,
  "generated_files": [],
  "compile_status": "not_attempted|passed|failed|blocked_missing_latex|not_applicable",
  "notes": []
}
```

## Procedure

1. Read project memory, venue/rule status, response format, and reviewer index.
2. If response mode is unknown, ask a focused questionnaire.
3. If user provided official template/rules, copy or summarize into `.awesome-rebuttal/templates/` and mark `user_provided`.
4. If AI found official template, ask user to confirm before copying/adapting.
5. If `pdf_one_page` and no official template is available, copy the built-in fallback from `assets/one-page-rebuttal-template/` to `.awesome-rebuttal/templates/active-rebuttal-template/`.
6. If `unified_limited`, create a compact `final-response-layout.md` shell grouped by top common concerns and length budget.
7. If `openreview_per_reviewer`, create empty Markdown shell files per reviewer and a README/paste-order file.
8. If `global_comment`, create `global-response.md` shell.
9. If `hybrid`, create global plus per-reviewer shells.
10. If `openreview_markdown_latex`, create simple Markdown templates with math-safe guidance and preview warning.
11. Run/request LaTeX environment check from 00 before compiling PDF.
12. If LaTeX is available and one-page PDF is used, optionally compile smoke PDF.
13. Persist template memory, update project memory, and write template report.

## Built-in fallback adaptation rules

When using the built-in ECCV/CVPR-style template:

- Do not claim it is official.
- Label it as `fallback two-column one-page rebuttal template`.
- Replace conference/year/paper ID placeholders only with user-confirmed values.
- Remove/rewrite venue-specific instruction text not confirmed for the target venue.
- Preserve anonymity and no-external-link constraints unless confirmed rules say otherwise.
- Keep one-page limit only when user confirms one-page PDF is required or desired.

## Generated Markdown shell examples

### Per-reviewer file

```markdown
# Response to Reviewer R1 (`<anonymous_id_or_unknown>`)

> Paste target: `<confirmed thread/comment target>`
> Status: scaffold

<!-- Response units from 11 will be inserted by 12. -->
```

### Global response file

```markdown
# Global Author Response

> Paste target: `<confirmed global response/comment target>`
> Status: scaffold

<!-- Shared concerns, AC facts if allowed, and response units from 11/13 will be inserted by 12. -->
```

## Output report

```markdown
## Rebuttal Template Report

- Template status:
- Response mode:
- Layout family:
- Source:
- Workspace template directory:
- Draft output directory:
- Generated files:
- Requires LaTeX:
- LaTeX environment:
- User confirmation needed:
- Next action: 12_template_designer.md
```

## Stop / proceed rules

Proceed when:

- response mode is known;
- template/layout family is selected;
- generated scaffolds or active template are written;
- fallback vs official status is explicit.

Stop and ask when:

- user has not confirmed response format;
- AI-found official template needs user confirmation;
- using fallback template for a high-stakes one-page PDF needs user approval;
- creating per-reviewer files requires reviewer/thread mapping that is missing;
- file creation would overwrite user files.

## Safety rules

- Never present fallback template as official.
- Never overwrite user templates without backup or confirmation.
- Never compile/export final rebuttal before venue rules and content are confirmed.
- Never include external links in submission-facing text unless venue rules explicitly allow them.
- Never place LeafLink or local sync instructions in generated response scaffolds.
