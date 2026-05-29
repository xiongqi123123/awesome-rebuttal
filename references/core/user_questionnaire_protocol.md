# User Questionnaire Protocol

Use this protocol whenever the skill cannot safely continue because information is missing, ambiguous, preference-dependent, or needs user confirmation.

## Core principle

First extract what the user already provided. Then ask only for the smallest missing decision set needed for the next safe step.

Do not ask for facts that can be discovered from the workspace. Inspect first, then ask the user to confirm decisions or supply unavailable context.

## When to use

Use a questionnaire for:

- workspace bootstrap choices: create canonical folders, map existing folders, Overleaf sync, versioning mode
- intake gaps: missing venue rules, response format, reviews, paper context, code context, evidence/resources, author goals
- confirmation gates: AI-found venue rules, destructive file moves, auto git, final submission-facing text
- any later capability where an unresolved choice would change strategy or safety

## Question style

Prefer structured input if the runtime provides it. Otherwise use a compact markdown questionnaire.

Allowed question types:

- **single-choice**: exactly one path should be selected
- **multi-select**: multiple constraints or available inputs may apply
- **short text**: user must paste a rule, path, URL, review, or preference
- **confirmation**: user validates an inferred mapping or AI-found rule summary

## Questionnaire shape

Use this shape:

```markdown
## Need your input: <topic>

I found / inferred:
- ...

To continue safely, please answer:

1. <single-choice question>
   - A. <option> — <effect>
   - B. <option> — <effect>
   - C. Other: <free text>

2. <multi-select question, if needed>
   - [ ] <option>
   - [ ] <option>

3. <short text request, if needed>
   <paste here>
```

Keep one questionnaire focused on one stage. Do not mix workspace organization, venue rules, and drafting preferences unless they are all required for the immediate next step.

## Recommended option sets

### Workspace layout action

- Use canonical layout — create/use `Code/`, `Paper/`, `Reference/`, `Temp/`.
- Map existing layout — keep current folders and record a workspace map.
- Review first — show detected files/folders before any organization action.

### Paper source

- Local PDF or LaTeX in `Paper/`.
- Overleaf/cn.overleaf project; consider optional LeafLink sync.
- Paper not available yet; use pasted summary temporarily.

### Venue rule source

- I will provide official rules/instructions.
- Search official rules for venue/year, then ask me to confirm.
- Rules unknown for now; block drafting and continue only with non-format analysis.

### Progress preservation

- Manual Git — suggest commits only.
- Auto Git — local milestone commits allowed.
- Markdown snapshot only — maintain `.awesome-rebuttal/snapshots/REBUTTAL_SNAPSHOT.md` / `.awesome-rebuttal/snapshots/PROJECT_SNAPSHOT.md`.

## Output after questionnaire

After receiving answers:

1. Restate the selected decisions in 3-7 bullets.
2. Update the relevant memory fields.
3. Mark unresolved items as `needs_user_input`.
4. Continue to the next capability only if blockers are cleared.
