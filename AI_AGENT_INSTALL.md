# AI Agent Installation Guide

Repository: https://github.com/xiongqi123123/awesome-rebuttal

This file is for an AI coding agent installing this repository as an agent skill. Keep installation safe and non-destructive.

## 1. Clone and verify package root

If the repository has not been cloned yet:

```bash
git clone https://github.com/xiongqi123123/awesome-rebuttal.git
cd awesome-rebuttal
```

Run from the cloned repository root. This directory must contain `SKILL.md` directly:

```bash
test -f SKILL.md
test -d references
test -d assets
```

If `SKILL.md` is missing, stop and ask the user for the correct package directory.

## 2. Dependencies

No dependency is required for the core skill.

Optional checks:

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

Notes:

- Python 3.10+ is optional and only needed for `scripts/render_snapshot.py`.
- LaTeX is optional and only needed for local PDF compilation.
- Conda and LeafLink are optional and only needed if the user wants Overleaf sync.
- Questionnaire/choice prompts need no package. Use native UI choices if available, otherwise use Markdown A/B/C or checkbox lists.

## 3. Choose install target

If the user has not specified a target, ask:

```markdown
Install target:
- A. Codex
- B. Claude Code
- C. Cursor project rule
- D. All available
- E. No global install; only prepare a project workspace
```

## 4. Install for Codex

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
  cp -R SKILL.md agents references assets scripts README.md README_ZH.md AI_AGENT_INSTALL.md LICENSE "$TARGET"/
fi

test -f "$TARGET/SKILL.md"
```

Tell the user to restart Codex after installation.

## 5. Install for Claude Code

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
  cp -R SKILL.md agents references assets scripts README.md README_ZH.md AI_AGENT_INSTALL.md LICENSE "$TARGET"/
fi

test -f "$TARGET/SKILL.md"
```

Tell the user to restart or reload Claude Code after installation.

## 6. Install for Cursor project rule

Run inside the user's target project/workspace, not necessarily inside this skill repository:

```bash
mkdir -p .cursor/rules
cat > .cursor/rules/awesome-rebuttal.mdc <<'RULE'
---
description: Use the installed awesome-rebuttal skill for academic rebuttal workflows.
alwaysApply: false
---

When the user asks for academic paper rebuttal help, use the installed or cloned awesome-rebuttal skill.

Find the skill entry at one of:
- a local cloned package containing `SKILL.md`
- `~/.codex/skills/awesome-rebuttal/SKILL.md`
- `~/.claude/skills/awesome-rebuttal/SKILL.md`

Load `SKILL.md` first, then only the referenced capability files needed for the task.
Store runtime state in the current project under `.awesome-rebuttal/`.
RULE
```

## 7. Optional project workspace directories

Only create these when the user wants a new rebuttal workspace prepared:

```bash
mkdir -p Code Paper Reference Temp \
  .awesome-rebuttal/memory \
  .awesome-rebuttal/drafts \
  .awesome-rebuttal/snapshots \
  .awesome-rebuttal/templates \
  .awesome-rebuttal/logs \
  .awesome-rebuttal/cache
```

Do not move existing user files unless the user explicitly approves.

## 8. Optional LaTeX setup

If PDF compilation is needed and no LaTeX tool is available, ask the user which route to use:

```markdown
LaTeX setup:
- A. Use Overleaf only
- B. Install Tectonic
- C. Install MacTeX/BasicTeX on macOS
- D. Install TeX Live on Linux
- E. Install MiKTeX/TeX Live on Windows
- F. Skip local compilation
```

Do not install LaTeX without explicit approval.

## 9. Optional LeafLink setup

Only if the user wants Overleaf sync.

Prefer Conda when available:

```bash
conda create -n leaflink python=3.11 -y
conda run -n leaflink pip install "leaflink[browser,watch]"
conda run -n leaflink python -m playwright install chromium
conda run -n leaflink leaflink --help
```

Fallback without Conda:

```bash
python3 -m pip install --user "leaflink[browser,watch]"
python3 -m playwright install chromium
leaflink --help
```

Ask before running login, clone, pull, sync, download, or push commands.

## 10. Final install report

Report:

```markdown
- Package path:
- Installed target(s):
- Skill entry path(s):
- Cursor rule path, if created:
- Optional tools detected:
- Optional tools missing:
- Restart/reload needed:
```
