# awesome-rebuttal

`awesome-rebuttal` is a global-installable but project-level skill for AI / ML / CV / NLP / Robotics paper rebuttals. The installed skill supplies reusable workflows and assets; each actual rebuttal workspace gets its own `.awesome-rebuttal/` folder for JSON memory, snapshots, templates, logs, and cache. It helps authors organize a rebuttal workspace, collect paper/code/review context, analyze reviewer concerns, plan supplementary experiments, and draft safe author responses under confirmed venue rules.

## Philosophy

- Strategy before prose.
- Evidence before claims.
- User-confirmed venue rules before formatting assumptions.
- Author control before automation.


## AI-agent installation

For users who want to paste this repository link into an AI coding assistant and ask it to install the skill, use [`AI_AGENT_INSTALL.md`](AI_AGENT_INSTALL.md). It contains copy/paste-safe instructions for Codex, Claude Code, Cursor, optional LaTeX checks, and optional LeafLink setup.

## Project-local skill state

Each runtime workspace should contain a skill-owned state folder:

```text
.awesome-rebuttal/
├── memory/
├── snapshots/
├── templates/
├── logs/
└── cache/
```

Do not store runtime memory in the global installed skill folder.

## Recommended rebuttal workspace

Create a dedicated workspace for each paper/rebuttal:

```text
<rebuttal-workspace>/
├── Code/        # code repositories, scripts, configs, reproduced outputs
├── Paper/       # paper PDF/LaTeX; Overleaf sync target if used
├── Reference/   # reviews, venue instructions, reference papers, notes
└── Temp/        # scratch extraction, intermediate analysis, cache
```

If the workspace is empty, the skill can organize it this way. If it already contains files, the skill should adapt non-destructively.

## Repository/package root

The published repository root is this directory: it contains `SKILL.md` directly. If you are developing from a larger workspace, publish the inner `awesome-rebuttal/` package directory, not the outer development workspace.

## One-page rebuttal template

The skill includes a built-in fallback one-page two-column rebuttal template at:

```text
assets/one-page-rebuttal-template/
```

If the venue provides an official template, use the official template. If no official template is available and the user still wants one-page PDF output, the skill may copy this built-in CVPR/ECCV-style fallback into `.awesome-rebuttal/templates/active-rebuttal-template/` and adapt conference metadata. Never present the fallback as official.

## Overleaf workflow

If your paper is hosted on Overleaf or cn.overleaf, the skill can ask whether you want a local synced copy in `Paper/`. For that situation, you can optionally use [LeafLink](https://github.com/xiongqi123123/LeafLink), a CLI for syncing local folders with Overleaf projects.

This is not required and is never inserted into submission-facing rebuttal text.

## LaTeX environment

Workspace bootstrap checks for `latexmk`, `pdflatex`, `xelatex`, `lualatex`, `bibtex`/`biber`, `kpsewhich`, or `tectonic`. If a PDF rebuttal is needed and LaTeX is missing, the skill should ask the user whether to install/configure a platform-specific toolchain, compile on Overleaf, or skip local compilation.

## Skill layout

The installable skill/package root is:

```text
.
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── capabilities/
│   ├── templates/
│   ├── strategy-library/
│   ├── memory-schemas/
│   └── examples/
└── assets/
    └── one-page-rebuttal-template/
```

`SKILL.md` is intentionally a thin router. Each atomic capability has its own file.

## Questionnaire-first clarification

When required information is missing, the skill should not guess. It summarizes what it found, then asks a compact questionnaire using single-choice, multi-select, short-text, or confirmation prompts. This applies first to workspace bootstrap and intake, then to later venue-rule, experiment, and drafting decisions.

## Progress preservation

At runtime, choose one:

- `manual_git`: the skill suggests checkpoint boundaries and commit messages.
- `auto_git`: the skill can make local milestone commits; no push or destructive git actions.
- `markdown_snapshot_only`: the skill maintains `.awesome-rebuttal/snapshots/REBUTTAL_SNAPSHOT.md` / `.awesome-rebuttal/snapshots/PROJECT_SNAPSHOT.md` for context reload.


## Language and response modes

The skill follows the user's language for interactive analysis and questionnaires by default. Final submission-facing rebuttal text is written in English unless the user explicitly requests another language and the venue permits it.

Canonical response modes used in memory are: `openreview_per_reviewer`, `unified_limited`, `pdf_one_page`, `global_comment`, `hybrid`, `openreview_markdown_latex`, and `unknown`.

Venue rules are stored in `.awesome-rebuttal/memory/venue_rules.json` using the bundled schema. The schema separates source/confirmation, canonical response mode and limits, formatting rules, content permissions, anonymity, and language policy. AI-found rules remain pending until the user confirms them.

## Safety

The skill blocks finalization if factual claims lack provenance, reviewer concerns disappear, venue rules are unconfirmed, or the tone becomes unprofessional.
