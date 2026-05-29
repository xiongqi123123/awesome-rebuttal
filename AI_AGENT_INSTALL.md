# AI Agent Installation Guide for awesome-rebuttal

This file is written for an AI coding agent. The repository root is the publishable skill package. In other words, after cloning the published repository, the current directory should contain `SKILL.md` directly.

## Mission

Install the `awesome-rebuttal` skill so the user's AI assistant can help with academic paper rebuttal work. Keep runtime project state separate from the installed skill.

## Safety rules for the installing agent

1. Do not modify private paper/review files during installation.
2. Do not push, reset, clean, or rewrite git history.
3. Do not overwrite an existing skill installation without making a backup or asking the user.
4. Do not install large optional dependencies such as LaTeX or LeafLink unless the user asks for that capability.
5. Do not add LeafLink, local paths, credentials, or tool instructions to submission-facing rebuttal text.
6. If a platform lacks native skill support, install a small adapter/rule that points to this skill package's `SKILL.md`.

## Package structure to verify

After cloning or unpacking the published package, verify these paths exist relative to the current directory:

```text
SKILL.md
references/capabilities/
references/memory-schemas/
assets/one-page-rebuttal-template/
scripts/render_snapshot.py
```

If `SKILL.md` is missing, stop. You are probably in the wrong directory. The publishable root should be the inner `awesome-rebuttal/` package, not an outer development workspace.

## Core dependencies

The core skill is documentation-first and has no mandatory package dependency.

Recommended local tools:

- `git` — useful for cloning and optional rebuttal checkpoints.
- Python 3.10+ — optional, only needed for `scripts/render_snapshot.py` and simple local checks. The snapshot renderer uses only the Python standard library.
- A LaTeX compiler — optional, only needed for local one-page PDF compilation.
- Conda — optional, preferred environment manager if the user chooses LeafLink/Overleaf sync.
- LeafLink — optional, only if the paper is hosted on Overleaf/cn.overleaf and the user wants cloud/local sync.

Questionnaire-style choices do **not** require any external package. If the host platform has a native multiple-choice UI, use it. Otherwise ask in plain Markdown with choices such as A/B/C, checkboxes, or short-answer prompts.

## Step 1: clone or locate the package

If the user gives a URL:

```bash
git clone <REPO_URL> awesome-rebuttal
cd awesome-rebuttal
```

If the package already exists locally, `cd` into the package root.

Validate:

```bash
test -f SKILL.md
```

## Step 2: choose target platform

Ask the user which target to install:

```markdown
## Install target

Choose one:
- A. Codex skill
- B. Claude Code skill
- C. Cursor project rules
- D. All available targets
- E. Only prepare a project workspace, no global install
```

If the user already specified the target, proceed without asking again.

## Step 3A: install for Codex

Install location:

```text
${CODEX_HOME:-$HOME/.codex}/skills/awesome-rebuttal
```

Commands:

```bash
CODEX_SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
TARGET="$CODEX_SKILLS_DIR/awesome-rebuttal"
mkdir -p "$CODEX_SKILLS_DIR"

if [ -e "$TARGET" ]; then
  mv "$TARGET" "$TARGET.backup.$(date +%Y%m%d-%H%M%S)"
fi

mkdir -p "$TARGET"
if command -v rsync >/dev/null 2>&1; then
  rsync -a --exclude '.git/' --exclude '.awesome-rebuttal/' --exclude '__pycache__/' ./ "$TARGET"/
else
  cp -R SKILL.md agents references assets scripts README.md AI_AGENT_INSTALL.md LICENSE "$TARGET"/
fi

test -f "$TARGET/SKILL.md"
```

After installation, tell the user to restart Codex so it can reload skills.

## Step 3B: install for Claude Code

Install location:

```text
$HOME/.claude/skills/awesome-rebuttal
```

Commands:

```bash
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
TARGET="$CLAUDE_SKILLS_DIR/awesome-rebuttal"
mkdir -p "$CLAUDE_SKILLS_DIR"

if [ -e "$TARGET" ]; then
  mv "$TARGET" "$TARGET.backup.$(date +%Y%m%d-%H%M%S)"
fi

mkdir -p "$TARGET"
if command -v rsync >/dev/null 2>&1; then
  rsync -a --exclude '.git/' --exclude '.awesome-rebuttal/' --exclude '__pycache__/' ./ "$TARGET"/
else
  cp -R SKILL.md agents references assets scripts README.md AI_AGENT_INSTALL.md LICENSE "$TARGET"/
fi

test -f "$TARGET/SKILL.md"
```

After installation, tell the user to restart Claude Code or reload the session.

If the user's Claude Code setup does not support skills, create a project-level instruction file instead:

```text
<rebuttal-workspace>/AGENTS.md
```

with this content:

```markdown
# awesome-rebuttal adapter

For academic rebuttal work, follow the installed or cloned `awesome-rebuttal/SKILL.md`.
Load only the relevant capability files under `references/capabilities/` as needed.
Runtime state must be stored under the current project's `.awesome-rebuttal/` folder, not inside the installed skill.
Venue rules must be user-confirmed before final drafting.
Interactive analysis follows the user's language; submission-facing rebuttal prose defaults to English.
```

## Step 3C: install for Cursor

Cursor does not need the whole skill copied into every project. Prefer a project rule that points to the cloned or installed skill package.

Inside the user's rebuttal workspace:

```bash
mkdir -p .cursor/rules
cat > .cursor/rules/awesome-rebuttal.mdc <<'RULE'
---
description: Use awesome-rebuttal for academic paper rebuttal strategy, memory, experiments, templates, and safe author-response drafting.
alwaysApply: false
---

# awesome-rebuttal Cursor adapter

When the user asks for AI/ML/CV/NLP/Robotics paper rebuttal help, use the `awesome-rebuttal` workflow.

Core skill entry:
- If the published package is in this workspace, read `SKILL.md` from that package root.
- If installed elsewhere, ask the user for the local path to `awesome-rebuttal/SKILL.md`.

Rules:
- Store runtime state under the current workspace's `.awesome-rebuttal/` folder.
- Use `Code/`, `Paper/`, `Reference/`, and `Temp/` when creating a new rebuttal workspace; adapt existing layouts non-destructively.
- Venue rules are runtime evidence. Use user-provided rules or AI search plus user confirmation; never rely on stale built-in venue assumptions.
- Ask focused questionnaires for missing decisions. Plain Markdown choices are enough.
- Interactive analysis follows the user's language. Submission-facing author response, reviewer replies, AC summaries, OpenReview comments, and PDF rebuttal prose default to English.
- Do not fabricate experiments, numbers, citations, reviewer positions, or venue permissions.
- Do not include LeafLink/local tool text in submission-facing rebuttal text.
RULE
```

Tell the user to ensure Cursor project rules are enabled for the workspace.

## Step 4: optional project workspace preparation

For a new rebuttal project, create or recommend this structure:

```text
<rebuttal-workspace>/
├── Code/
├── Paper/
├── Reference/
├── Temp/
└── .awesome-rebuttal/
    ├── memory/
    ├── drafts/
    ├── snapshots/
    ├── templates/
    ├── logs/
    └── cache/
```

Commands, if the user wants the directories created:

```bash
mkdir -p Code Paper Reference Temp \
  .awesome-rebuttal/memory \
  .awesome-rebuttal/drafts \
  .awesome-rebuttal/snapshots \
  .awesome-rebuttal/templates \
  .awesome-rebuttal/logs \
  .awesome-rebuttal/cache
```

Do not move user files automatically. If files already exist, map them and ask before reorganizing.

## Step 5: environment checks

Run non-invasive checks:

```bash
git --version || true
python3 --version || true
latexmk -version || true
pdflatex --version || true
xelatex --version || true
lualatex --version || true
tectonic --version || true
conda --version || true
leaflink --help || true
```

Record results for the user. Missing tools do not block the core skill.

## Optional: LaTeX setup guidance

Only needed for local PDF compilation. If no LaTeX tool is installed and the user needs one-page PDF output, ask which path they prefer:

```markdown
## LaTeX setup

Choose one:
- A. Use Overleaf only; skip local LaTeX.
- B. Install a lightweight compiler such as Tectonic.
- C. Install MacTeX/BasicTeX on macOS.
- D. Install TeX Live on Linux.
- E. Install MiKTeX/TeX Live on Windows.
- F. Skip PDF compilation for now; generate `.tex` only.
```

Do not install LaTeX without explicit user approval.

## Optional: LeafLink / Overleaf setup guidance

Only needed when the paper is on Overleaf/cn.overleaf and the user wants local sync into `Paper/`.

Ask first:

```markdown
## Overleaf sync

Is your paper on Overleaf/cn.overleaf, and do you want local sync?
- A. Yes, use LeafLink.
- B. Yes, but I will manually download/upload files.
- C. No, use local files only.
```

If the user chooses LeafLink, prefer Conda when available:

```bash
conda create -n leaflink python=3.11 -y
conda run -n leaflink pip install "leaflink[browser,watch]"
conda run -n leaflink python -m playwright install chromium
conda run -n leaflink leaflink --help
```

If Conda is unavailable or declined:

```bash
python3 -m pip install --user "leaflink[browser,watch]"
python3 -m playwright install chromium
leaflink --help
```

Login/clone/pull/push operations touch cloud state or credentials. Ask for explicit user approval before running them.

## Step 6: smoke test after install

Ask the host AI assistant to run a dry skill invocation, without private paper data:

```text
Use awesome-rebuttal. Start a new rebuttal workspace intake and ask me what venue rules, reviewer comments, paper context, response mode, experiment resources, and versioning mode I want to provide.
```

Expected behavior:

- The assistant recognizes the skill.
- It does not draft rebuttal text immediately.
- It asks a focused questionnaire for missing information.
- It says final submission-facing text defaults to English.
- It stores runtime state under `.awesome-rebuttal/` only when the user asks it to proceed.

## Final report to user

After installation, report:

```markdown
## awesome-rebuttal install report

- Package path:
- Installed targets:
- Skill entry path(s):
- Cursor rule path, if created:
- Optional tools found:
  - git:
  - python3:
  - LaTeX:
  - conda:
  - leaflink:
- Optional tools not installed:
- Restart/reload needed:
- Next suggested prompt:
  "Use awesome-rebuttal to initialize this rebuttal workspace."
```
