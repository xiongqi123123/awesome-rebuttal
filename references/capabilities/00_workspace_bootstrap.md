# 00 Workspace Bootstrap

## Goal

Establish the current project workspace before any paper/review analysis. This capability makes a globally installed `awesome-rebuttal` skill behave safely inside each individual paper workspace by creating a project-local state folder and mapping user materials without destructive reorganization.

## Core model

The installed skill folder is read-only reusable knowledge. Runtime state belongs to the current workspace:

```text
<rebuttal-workspace>/
├── Code/                 # user code, repositories, scripts, configs, reproduced outputs
├── Paper/                # user paper PDF/LaTeX; Overleaf sync target if used
├── Reference/            # user reviews, venue rules, related papers, notes
├── Temp/                 # user-approved scratch/intermediate files
└── .awesome-rebuttal/    # skill-owned state, memory, snapshots, templates, logs, cache
```

All skill-owned memory, snapshots, fetched/adapted templates, rule-search logs, and compile logs must live under `.awesome-rebuttal/`. Do not write runtime state into the globally installed skill folder.

## Success criteria

After this capability runs, the agent should know:

- workspace classification: `empty`, `canonical`, `organized`, `messy`, or `unknown`
- where code/paper/reference/temp roles map in this workspace
- where `.awesome-rebuttal/` state directories live
- whether paper assets are local, Overleaf/cn.overleaf, pasted summary, or unknown
- whether LeafLink should be offered as an optional sync helper
- whether a LaTeX toolchain is available for PDF rebuttal workflows
- which progress preservation mode the user selected
- what, if anything, still requires user confirmation

## Inputs

Use three evidence channels in this order:

1. **User statement** — what the author says about workspace layout, paper location, code, Overleaf, progress preservation, and platform.
2. **Workspace inspection** — directory listing, file types, git status, existing `.awesome-rebuttal/`, LaTeX tools.
3. **User questionnaire** — only for missing or decision-bearing information after inspection.

Read `references/core/user_questionnaire_protocol.md` whenever a questionnaire is needed.

## Workspace classification

| Classification | Evidence | Default action |
|---|---|---|
| `empty` | no meaningful user files, or only hidden/tool state | create/recommend canonical user folders + `.awesome-rebuttal/` |
| `canonical` | has `Code/`, `Paper/`, `Reference/`, and `Temp/` or close variants | use as-is and create/update `.awesome-rebuttal/` |
| `organized` | has clear noncanonical layout, e.g. `src/`, `paper/`, `reviews/` | map existing paths; do not rename |
| `messy` | useful files exist but role mapping is unclear | show candidates and ask mapping questionnaire |
| `unknown` | cannot inspect or names are inconclusive | ask user to describe layout |

Treat `.git`, `.omx`, `.venv`, editor folders, cache folders, and `.awesome-rebuttal/` as tool/runtime state, not user paper content.

## Project-local state folder

Create or use this structure:

```text
.awesome-rebuttal/
├── memory/
│   ├── project_memory.json
│   ├── paper_memory.json
│   ├── code_memory.json
│   ├── review_memory.json
│   └── strategy_memory.json
├── snapshots/
│   ├── PROJECT_SNAPSHOT.md
│   └── *.json
├── templates/
│   ├── active-rebuttal-template/
│   └── template-source-summary.md
├── logs/
│   ├── workspace_bootstrap.md
│   ├── latex_environment.json
│   └── rule_search.log
└── cache/
```

Compatibility rule: if older artifacts exist at workspace root (`project_memory.json`, `PROJECT_SNAPSHOT.md`, etc.), do not delete them. Prefer writing the new canonical copy under `.awesome-rebuttal/` and note the migration in the bootstrap report.

## File and folder role detection

Use these heuristics, but ask for confirmation when confidence is medium/low.

### Code role

Likely code paths:

- `Code/`, `code/`, `src/`, `repo/`, `implementation/`, `experiments/`
- files: `pyproject.toml`, `requirements.txt`, `environment.yml`, `package.json`, `train.py`, `eval.py`, `configs/`

### Paper role

Likely paper paths:

- `Paper/`, `paper/`, `manuscript/`, `latex/`, `overleaf/`
- files: `main.tex`, `paper.tex`, `*.pdf`, `figures/`, `tables/`, `refs.bib`
- Overleaf indicators: Overleaf URL, user statement, folder created by sync workflow, `.latexmkrc` or Overleaf-style project export

### Reference role

Likely reference paths:

- `Reference/`, `references/`, `reviews/`, `review/`, `materials/`, `notes/`
- files: reviewer comments, author response instructions, venue rules, related PDFs, supplementary notes

### Temp role

Likely temp paths:

- `Temp/`, `tmp/`, `scratch/`, `cache/`, `intermediate/`
- extraction outputs, search results, OCR output, draft fragments

## LaTeX environment detection

Run a lightweight environment check during bootstrap, because one-page rebuttal workflows may require local compilation.

Check for:

- `latexmk`
- `pdflatex`
- `xelatex`
- `lualatex`
- `bibtex`
- `biber`
- `kpsewhich`
- `tectonic`

Record:

```json
{
  "latex_environment": {
    "status": "available|partial|missing|unknown",
    "tools": {
      "latexmk": "/path/or/null",
      "pdflatex": "/path/or/null",
      "xelatex": "/path/or/null",
      "lualatex": "/path/or/null",
      "bibtex": "/path/or/null",
      "biber": "/path/or/null",
      "kpsewhich": "/path/or/null",
      "tectonic": "/path/or/null"
    },
    "preferred_compile_command": "latexmk -pdf rebuttal.tex",
    "setup_needed": false,
    "platform_hint": "macos|linux|windows|unknown"
  }
}
```

Status rules:

- `available`: `latexmk` + at least one LaTeX engine + `bibtex` or `biber` are available, or `tectonic` is available for a template that can use it.
- `partial`: some tools exist, but a normal bibliography/LaTeX compile may fail.
- `missing`: no viable compiler found.
- `unknown`: cannot inspect.

If missing or partial and a PDF rebuttal is needed, ask the setup questionnaire.

## LaTeX setup questionnaire

```markdown
## Need your input: LaTeX compilation setup

I did not find a complete local LaTeX toolchain, but this workspace may need one-page PDF rebuttal compilation.

1. How do you want to compile PDF rebuttals?
   - A. Install/configure MacTeX or BasicTeX (macOS)
   - B. Install/configure TeX Live (Linux)
   - C. Install/configure MiKTeX or TeX Live (Windows)
   - D. Use Tectonic if compatible
   - E. Compile only on Overleaf; skip local compile checks
   - F. Skip compilation for now; prepare template only

2. Should I continue without local compilation?
   - A. Yes, prepare templates and mark compile status as blocked
   - B. No, pause until LaTeX is configured
```

Do not install LaTeX automatically unless the user explicitly requests it. Installation may be large and platform-specific.

## Procedure

1. **Summarize the user-provided workspace intent**
   - Include whether the skill is globally installed and this is a project workspace.
2. **Inspect top-level workspace**
   - List top-level folders/files.
   - Detect existing `.awesome-rebuttal/`.
   - Note git status if available.
3. **Classify workspace**
   - Use the classification table.
4. **Create or update `.awesome-rebuttal/`**
   - Create `memory/`, `snapshots/`, `templates/`, `logs/`, and `cache/` when safe.
   - This is a reversible, non-destructive action.
5. **Build user-material workspace map**
   - `code_dir`, `paper_dir`, `reference_dir`, `temp_dir`
   - If empty workspace and user authorized setup, create `Code/`, `Paper/`, `Reference/`, `Temp/`.
   - If existing workspace, prefer mapping over moving.
6. **Detect paper source**
   - local PDF, local LaTeX, Overleaf/cn.overleaf, pasted summary, or unknown.
7. **Handle Overleaf case**
   - Ask whether the user wants optional LeafLink sync into `Paper/`.
   - Do not perform login/sync without explicit user instruction.
8. **Detect LaTeX environment**
   - Write `.awesome-rebuttal/logs/latex_environment.json`.
   - If missing/partial and PDF output is likely, ask setup questionnaire or mark blocker.
9. **Ask progress preservation mode** if not selected
   - `manual_git`, `auto_git`, or `markdown_snapshot_only`.
10. **Persist bootstrap state**
   - Write `.awesome-rebuttal/memory/project_memory.json`.
   - Write `.awesome-rebuttal/snapshots/PROJECT_SNAPSHOT.md`.
   - Write `.awesome-rebuttal/logs/workspace_bootstrap.md`.
11. **Route next capability**
   - Continue to `01_intake_gate.md` when workspace and state folder are ready.

## Workspace questionnaire triggers

Ask a questionnaire when any of these is true:

- classification is `messy` or `unknown`
- multiple plausible code/paper/reference directories exist
- user-material folders would need to be moved/renamed
- Overleaf is detected but sync preference is unknown
- progress mode is unknown and durable outputs are about to be written
- LaTeX is missing/partial and PDF rebuttal output is requested or likely
- existing `.awesome-rebuttal/` conflicts with current workspace evidence

## Suggested workspace questionnaire

```markdown
## Need your input: workspace setup

I found:
- Code candidates: <paths or none>
- Paper candidates: <paths or none>
- Reference candidates: <paths or none>
- Temp candidates: <paths or none>
- Skill state folder: .awesome-rebuttal exists/created/missing
- Git repository: yes/no
- Overleaf signal: yes/no/unknown
- LaTeX environment: available/partial/missing/unknown

1. How should I organize user materials?
   - A. Use canonical layout: `Code/`, `Paper/`, `Reference/`, `Temp/`
   - B. Keep existing layout and record a path map
   - C. Show detected files first; do not create or move anything yet
   - D. Other: <describe>

2. Where should skill state live?
   - A. `.awesome-rebuttal/` in this workspace (recommended)
   - B. Existing state folder: <path>
   - C. Other: <path>

3. Where is the paper source?
   - A. Local PDF/LaTeX already in workspace
   - B. Overleaf/cn.overleaf; ask about LeafLink sync
   - C. I will paste paper summary for now
   - D. Not ready yet

4. How should progress be preserved?
   - A. Manual Git: suggest commits only
   - B. Auto Git: local milestone commits allowed
   - C. Markdown snapshot only: maintain reloadable snapshot file
```

## `project_memory.json` bootstrap fields

```json
{
  "skill_state": {
    "state_dir": ".awesome-rebuttal/",
    "memory_dir": ".awesome-rebuttal/memory/",
    "snapshot_dir": ".awesome-rebuttal/snapshots/",
    "template_dir": ".awesome-rebuttal/templates/",
    "log_dir": ".awesome-rebuttal/logs/",
    "cache_dir": ".awesome-rebuttal/cache/"
  },
  "workspace": {
    "classification": "empty|canonical|organized|messy|unknown",
    "code_dir": "Code/",
    "paper_dir": "Paper/",
    "reference_dir": "Reference/",
    "temp_dir": "Temp/",
    "mapping_confidence": "high|medium|low"
  },
  "paper_source": {
    "type": "local_pdf|local_latex|local_pdf_or_latex_pending_copy|overleaf|pasted_summary|unknown",
    "overleaf_sync": "not_needed|offered|accepted|declined|completed"
  },
  "latex_environment": {
    "status": "available|partial|missing|unknown",
    "setup_needed": false
  },
  "versioning": {
    "mode": "manual_git|auto_git|markdown_snapshot_only|unset",
    "git_repo_detected": false,
    "snapshot_doc": ".awesome-rebuttal/snapshots/PROJECT_SNAPSHOT.md"
  }
}
```

## Output skeleton

```markdown
## Workspace Bootstrap Report

- Classification: empty|canonical|organized|messy|unknown
- Mapping confidence: high|medium|low
- Skill state folder: .awesome-rebuttal/ created|exists|blocked
- Code path: ...
- Paper path: ...
- Reference path: ...
- Temp path: ...
- Paper source type: local_pdf|local_latex|overleaf|pasted_summary|unknown
- Overleaf/LeafLink status: not_needed|offered|accepted|declined|completed
- LaTeX environment: available|partial|missing|unknown
- Progress preservation: manual_git|auto_git|markdown_snapshot_only|unset
- Non-destructive actions taken:
  - ...
- Decisions still needed:
  - ...
- Next capability: 01_intake_gate.md | blocked_for_user_input
```

## Stop / proceed rules

Proceed to intake when:

- `.awesome-rebuttal/` exists or a user-approved alternate state folder is selected,
- workspace map is high or medium confidence,
- no destructive organization action is pending,
- progress preservation mode is selected or explicitly deferred.

Proceed with warning when:

- LaTeX is missing but no PDF output is currently required.

Stop and ask when:

- moving/renaming user files would be required,
- Overleaf sync is requested but not confirmed,
- auto git is desired but user has not explicitly selected it,
- paper/reference locations cannot be inferred,
- PDF rebuttal output is required and LaTeX setup choice is missing.

## Safety rules

- Never destructively move, delete, or overwrite user files during bootstrap.
- Never store runtime memory in the installed/global skill folder.
- Never push, reset, clean, or rewrite git history.
- Never invoke LeafLink login/sync without explicit user instruction.
- Never install LaTeX automatically without explicit instruction.
- Prefer mapping over reorganization for existing workspaces.
