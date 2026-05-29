# 02 Information Collection

## Goal

Build an evidence-grounded project packet from all available workspace and user-provided materials before any reviewer analysis, strategy planning, experiment triage, or drafting.

This capability is the bridge between `01_intake_gate.md` and the specialized builders (`03_paper_memory_builder.md`, `04_code_memory_builder.md`, `05_review_normalizer.md`, and rule/template capabilities). It does not argue with reviewers, prioritize concerns, or write rebuttal text. Its job is to make every later claim traceable.

## Boundary

### This capability does

- collect and inventory paper/code/review/rule/user materials
- preserve raw evidence locations and reviewer wording
- assign stable source IDs
- detect missing, duplicated, stale, or conflicting inputs
- create a source index and missing-information report
- update `.awesome-rebuttal/memory/project_memory.json`
- route to the next specialized capability

### This capability does not

- summarize away reviewer comments without raw anchors
- decide rebuttal posture or reviewer strategy
- judge whether an experiment should be run
- draft author-response text
- treat AI-found venue rules as confirmed without user confirmation
- invent paper claims, experiment results, code behavior, or venue permissions

## Inputs

Read these first, if present:

- `.awesome-rebuttal/memory/project_memory.json`
- `.awesome-rebuttal/logs/workspace_bootstrap.md`
- `.awesome-rebuttal/logs/latex_environment.json`
- intake report from `01_intake_gate.md`
- user messages in the current session
- workspace folders mapped by 00, usually `Code/`, `Paper/`, `Reference/`, `Temp/`

## Evidence classes

Collect evidence into these classes. Each item should have a path, source type, confidence, and whether it is ready for downstream use.

| Class | Examples | Downstream owner |
|---|---|---|
| `paper` | PDF, LaTeX source, abstract, figures/tables, supplementary text | `03_paper_memory_builder.md` |
| `code` | repository root, README, configs, scripts, logs, result files | `04_code_memory_builder.md` |
| `review` | raw reviewer comments, scores, confidence, discussion messages | `05_review_normalizer.md` |
| `venue_rule` | official instructions, user-confirmed rules, AI-found pending rules | `01_intake_gate.md`, `14_safety_rule_checker.md` |
| `template` | official rebuttal template, screenshot, fallback template state | `17_rebuttal_template_manager.md` |
| `experiment_evidence` | existing results, tables, logs, planned feasible runs | `10_experiment_triage.md` |
| `author_decision` | priorities, tone, risk posture, git/versioning choices | `08_strategy_planner.md`, `16_rebuttal_versioning.md` |
| `inference` | AI-inferred mapping or hypothesis requiring confirmation | downstream capability only with explicit provenance |

## Collection procedure

### 1. Load current memory and workspace map

Read project memory and identify:

- `skill_state` paths
- workspace classification and path map
- venue/year and rule-source status
- response mode and template route
- paper source type
- versioning mode
- current open questions

If `.awesome-rebuttal/` does not exist, stop and route back to `00_workspace_bootstrap.md`.

### 2. Inventory user-material folders

Use the workspace map from 00. Do a shallow inventory first, then inspect deeper only when it matters.

Recommended inventory depth:

- top-level files and folders in each mapped directory
- file extensions and likely roles
- obvious large/private files noted by path only unless needed
- git repositories under `Code/`, with branch/status summary if cheap
- LaTeX roots under `Paper/` (`main.tex`, `paper.tex`, `rebuttal.tex`, `.bib`, figures)
- review/rule files under `Reference/` (`*.md`, `*.txt`, `*.pdf`, screenshots)
- generated scratch artifacts under `Temp/` should be marked lower priority

Do not move, rename, delete, or rewrite user materials during collection.

### 3. Build raw material manifest

For each discovered item, record:

```json
{
  "source_id": "RAW:001",
  "class": "paper|code|review|venue_rule|template|experiment_evidence|author_decision|inference",
  "path": "Paper/main.tex",
  "provided_by": "user|workspace|ai_search|inference",
  "format": "pdf|tex|md|txt|json|py|yaml|log|url|unknown",
  "status": "ready|needs_extraction|needs_user_confirmation|missing|ignored",
  "confidence": "high|medium|low",
  "notes": []
}
```

Use `ignored` for cache/build artifacts, generated PDFs from smoke tests, or unrelated files.

### 4. Create stable source IDs

Assign stable IDs that later files can cite. Prefer deterministic IDs over positional ones when possible.

| Prefix | Use |
|---|---|
| `PAPER:<section-or-file>:<anchor>` | paper claims, abstract, figures, tables, equations, limitations |
| `CODE:<path>#<symbol-or-line-range>` | code functions, configs, scripts, result logs |
| `REVIEW:<reviewer-id>:<field-or-anchor>` | reviewer comments, scores, confidence, questions |
| `RULE:<venue-year>:<topic>` | confirmed or candidate venue rules |
| `TEMPLATE:<source>:<anchor>` | official/fallback template evidence |
| `EXP:<result-or-log>:<anchor>` | existing or feasible experiment evidence |
| `USER:<timestamp-or-decision-id>` | user-provided decisions and constraints |
| `INF:<short-id>` | AI inference, always with rationale and confirmation status |

Rules:

- Raw reviewer text must always keep a `REVIEW:*` anchor.
- Venue rules found by AI search must be `needs_user_confirmation` until confirmed.
- Inferences must never be used as hard evidence without labeling them as inference.
- If a source is later moved, update its path while preserving its ID if identity is clear.

### 5. Detect extraction needs

Mark whether each source is ready for specialized extraction.

Examples:

- PDF paper present but not parsed → `needs_extraction`, route to 03.
- LaTeX source present with clear root → `ready`, route to 03.
- Code repo present but no README/entrypoint identified → `needs_extraction`, route to 04.
- Review markdown present with stable reviewer labels → `ready`, route to 05.
- Screenshot-only rules → `needs_user_confirmation` or OCR/extraction before safety use.
- One-page PDF format selected but no confirmed template → route to 17.

### 6. Build gap and conflict report

Separate gaps by severity.

#### Blocking gaps

These prevent analysis or drafting:

- no raw reviews for a rebuttal-analysis task
- no paper context: neither PDF/LaTeX nor sufficient summary
- venue rules required for drafting but no user-confirmed rules or rule-source plan
- response format required for drafting but missing
- user asked for PDF output but no template path/route and no fallback decision

#### Analysis-confidence gaps

These allow partial analysis but must be marked:

- missing reviewer score/confidence
- paper available only as summary
- code unavailable for implementation/reproducibility concerns
- experiment logs/results not yet located
- venue rules AI-found but pending confirmation

#### Conflicts

Flag and do not silently resolve:

- multiple paper versions with unclear latest version
- review files disagree on reviewer IDs/scores
- user-stated rule conflicts with official/candidate rule text
- code results conflict with paper tables
- template requirement conflicts with response format

### 7. Persist project packet

Update `.awesome-rebuttal/memory/project_memory.json` with at least:

```json
{
  "source_index": [
    {
      "source_id": "REVIEW:R1:score",
      "class": "review",
      "path": "Reference/reviews.md",
      "status": "ready",
      "confidence": "high"
    }
  ],
  "collection": {
    "status": "complete|analysis_ready|partial|blocked",
    "last_collected_at": "ISO-8601 timestamp",
    "manifest_path": ".awesome-rebuttal/memory/source_manifest.json",
    "missing_report_path": ".awesome-rebuttal/logs/missing_information_report.md",
    "next_routes": []
  },
  "open_questions": []
}
```

Also write:

- `.awesome-rebuttal/memory/source_manifest.json`
- `.awesome-rebuttal/logs/missing_information_report.md`

Do not overwrite specialized memories (`paper_memory.json`, `review_memory.json`, etc.) except to create empty stubs only if another capability expects them.

## Missing-information questionnaire

Use `references/core/user_questionnaire_protocol.md` if collection cannot determine a required source or if conflicts need user judgment.

Prefer a focused questionnaire like:

```markdown
## Need your input: information collection gaps

I found:
- Paper candidates: <paths or none>
- Review candidates: <paths or none>
- Rule/template candidates: <paths or none>
- Code candidates: <paths or none>

To continue safely, please answer:

1. Which paper source should I treat as current?
   - A. `<path>`
   - B. `<path>`
   - C. I will provide/copy the current paper later

2. Which review file is authoritative?
   - A. `<path>`
   - B. I will paste reviews again
   - C. Current reviews are incomplete; continue only with available reviewers

3. How should missing venue/template rules be handled?
   - A. I will provide official rules/template
   - B. Search official sources, then ask me to confirm
   - C. Continue analysis only; block final drafting
```

Ask only the questions that are actually blocking the next route.

## Output report

Produce a concise collection report:

```markdown
## Information Collection Report

- Collection status: complete|analysis_ready|partial|blocked
- Workspace map used: Code=..., Paper=..., Reference=..., Temp=...
- Sources indexed:
  - Paper: <count/status>
  - Code: <count/status>
  - Reviews: <count/status>
  - Rules/templates: <count/status>
  - Experiment evidence: <count/status>
- Blocking gaps:
  - ...
- Confidence gaps:
  - ...
- Conflicts:
  - ...
- Files written:
  - `.awesome-rebuttal/memory/source_manifest.json`
  - `.awesome-rebuttal/logs/missing_information_report.md`
  - `.awesome-rebuttal/memory/project_memory.json`
- Next routes:
  - `03_paper_memory_builder.md`
  - `04_code_memory_builder.md`
  - `05_review_normalizer.md`
```

## Routing rules

Route after collection according to available evidence:

| Evidence state | Next route |
|---|---|
| paper source available | `03_paper_memory_builder.md` |
| code source available and relevant | `04_code_memory_builder.md` |
| raw reviews available | `05_review_normalizer.md` |
| one-page/PDF template needed | `17_rebuttal_template_manager.md` |
| confirmed rules available and drafting later | `14_safety_rule_checker.md` eventually, not immediately |
| major source missing | ask questionnaire before analysis |

If multiple routes are ready, prefer this order unless the user asked otherwise:

1. `03_paper_memory_builder.md`
2. `04_code_memory_builder.md`
3. `05_review_normalizer.md`
4. `17_rebuttal_template_manager.md`
5. analysis capabilities starting at `06_situation_analyzer.md`

## Quality bar

A strong 02 output lets another agent continue without rereading the entire workspace. It should answer:

- What evidence do we have?
- Where is each piece of evidence?
- What can be safely used downstream?
- What still needs user confirmation?
- Which atomic capability should run next?

## Safety rules

- Preserve raw reviewer wording and rule text anchors.
- Do not convert unconfirmed venue rules into confirmed constraints.
- Do not treat generated template smoke-test files as official venue artifacts.
- Do not expose private paper/review contents outside the local workspace.
- Do not run expensive experiments, training, or external sync from this capability.
- Do not fabricate missing source IDs; mark unavailable evidence as `missing` or `needs_user_input`.
