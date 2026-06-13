<div align="center">
  <img src="assets/image/awesome-rebuttal.png" alt="Awesome Rebuttal logo" width="260" />

# Awesome Rebuttal

**A project-level skill package for evidence-grounded academic rebuttal strategy and author-response drafting.**

[English](README.md) · [简体中文](README_ZH.md)

[![GitHub Repo](https://img.shields.io/badge/GitHub-xiongqi123123%2Fawesome--rebuttal-181717?logo=github)](https://github.com/xiongqi123123/awesome-rebuttal)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/xiongqi123123/awesome-rebuttal?style=social)](https://github.com/xiongqi123123/awesome-rebuttal/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/xiongqi123123/awesome-rebuttal?style=social)](https://github.com/xiongqi123123/awesome-rebuttal/forks)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-blue)](SKILL.md)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-orange)](AI_AGENT_INSTALL.md)
[![Cursor](https://img.shields.io/badge/Cursor-Rules%20Adapter-purple)](AI_AGENT_INSTALL.md)

</div>

---

## What is this?

`Awesome Rebuttal` is a global-installable, project-level skill for AI / ML / CV / NLP / Robotics paper rebuttals. It helps an AI coding assistant work inside a paper workspace, persist structured rebuttal memory, analyze reviewer concerns, plan supplementary experiments, and draft safe author responses under user-confirmed venue rules.

## Disclaimer

Awesome Rebuttal is **not affiliated with, endorsed by, or officially connected to** any conference, publisher, review platform, or submission system. It is an assistant workflow for organizing evidence and drafting rebuttal text; it does not guarantee acceptance and does not replace the author's responsibility. Before submitting, authors must independently verify the venue rules, anonymity requirements, factual claims, experimental numbers, formatting, and final uploaded files.

## Highlights

- **Skill-first architecture** — one `SKILL.md` entry with layered atomic capability files.
- **Project-local state** — runtime memory, drafts, snapshots, templates, and logs stay under `.awesome-rebuttal/` in each paper workspace.
- **Review understanding** — normalize reviewer metadata, raw comments, atomic concerns, and common concern clusters.
- **Strategy planning** — reason about rebuttal posture, priority concerns, reviewer-specific goals, and AC-facing decision facts.
- **Experiment triage** — separate must-do, high-value optional, not-recommended, and infeasible rebuttal experiments.
- **Format-aware drafting** — supports one-page PDF, OpenReview-style per-reviewer replies, global comments, hybrid responses, and Markdown+LaTeX comments.
- **Safety gates** — block unsupported claims, fabricated results, unconfirmed venue permissions, hostile tone, and anonymity leaks.
- **Optional Overleaf sync** — can guide LeafLink setup only when the user wants cloud/local synchronization.

## Installation

The published repository root is the skill package root. After cloning, the directory should contain `SKILL.md` directly.

```bash
git clone https://github.com/xiongqi123123/awesome-rebuttal.git
cd awesome-rebuttal
test -f SKILL.md
```

### Option A: install manually for Codex

```bash
CODEX_SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
TARGET="$CODEX_SKILLS_DIR/awesome-rebuttal"
mkdir -p "$CODEX_SKILLS_DIR"
rsync -a --exclude '.git/' --exclude '.awesome-rebuttal/' ./ "$TARGET"/
```

Restart Codex after installation.

### Option B: install manually for Claude Code

```bash
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
TARGET="$CLAUDE_SKILLS_DIR/awesome-rebuttal"
mkdir -p "$CLAUDE_SKILLS_DIR"
rsync -a --exclude '.git/' --exclude '.awesome-rebuttal/' ./ "$TARGET"/
```

Restart or reload Claude Code after installation.

### Option C: AI-assisted installation

Send this installation guide link directly to a local AI coding assistant and ask it to follow the instructions:

- GitHub view: https://github.com/xiongqi123123/awesome-rebuttal/blob/main/AI_AGENT_INSTALL.md
- Raw Markdown: https://raw.githubusercontent.com/xiongqi123123/awesome-rebuttal/main/AI_AGENT_INSTALL.md

Suggested prompt:

```text
Please install Awesome Rebuttal by following this guide:
https://github.com/xiongqi123123/awesome-rebuttal/blob/main/AI_AGENT_INSTALL.md
Do not overwrite existing files without backup.
```

### Option D: Cursor project rule

Cursor can use a project rule that points to this cloned or installed skill. See [`AI_AGENT_INSTALL.md`](AI_AGENT_INSTALL.md) for the minimal `.cursor/rules/awesome-rebuttal.mdc` adapter.

## Basic usage

In a paper rebuttal workspace, point your AI assistant at the skill. Common entry points:

```text
# Set up the workspace and memory
Use Awesome Rebuttal to initialize this rebuttal workspace.

# Understand the reviews and plan strategy
Use Awesome Rebuttal: the reviews are in Reference/. Build the concern analysis and a strategy plan.

# Draft a format-aware response
Use Awesome Rebuttal to draft a one-page PDF rebuttal from the approved strategy.

# Stress-test before submitting
Use Awesome Rebuttal to rehearse the rebuttal: simulate the reviewers and AC, and tell me what to harden.

# Handle the discussion period
Use Awesome Rebuttal: here is Reviewer 2's follow-up reply — help me decide whether and how to respond.
```

Recommended workspace layout:

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

If your workspace already has a different structure, the skill will map it non-destructively instead of forcing renames.

## Host compatibility

| Host | Status | Install style |
|---|---|---|
| Codex | Native skill package | copy to `~/.codex/skills/awesome-rebuttal` |
| Claude Code | Skill-compatible package | copy to `~/.claude/skills/awesome-rebuttal` |
| Cursor | Project rule adapter | create `.cursor/rules/awesome-rebuttal.mdc` |
| Other agents | Prompt/reference package | point the agent to `SKILL.md` |


## Included assets

- Built-in fallback one-page LaTeX rebuttal template: [`assets/one-page-rebuttal-template/`](assets/one-page-rebuttal-template/)
- Snapshot renderer: [`scripts/render_snapshot.py`](scripts/render_snapshot.py)
- Memory schemas: [`references/memory-schemas/`](references/memory-schemas/)
- Capability files: [`references/capabilities/`](references/capabilities/)
- Worked examples: [`references/examples/`](references/examples/)

## Capability map

The atomic capability files in [`references/capabilities/`](references/capabilities/), grouped by lifecycle phase:

| Phase | Capabilities |
|---|---|
| 1 · Setup | `00` workspace bootstrap · `01` intake gate · `17` template manager |
| 2 · Evidence & memory | `02` information collection · `03` paper memory · `04` code memory |
| 3 · Review understanding | `05` review normalizer · `06` situation analyzer |
| 4 · Strategy | `10` experiment triage · `07` concern atomizer (priority) · `08` strategy planner |
| 5 · Drafting | `11` response writer · `12` template designer · `13` AC summary writer |
| 6 · Pre-submission gates | `18` rebuttal rehearsal · `14` safety rule checker |
| 7 · Discussion rounds | `19` discussion round handler |
| Cross-cutting | `09` snapshot maker · `16` versioning · `15` Overleaf/LeafLink sync |

Each phase produces structured artifacts — reviewer stance map, atomic concern ledger, strategy matrix, numbered `EXP-*` experiment plan, format-aware draft, coverage map, rehearsal findings, and a reviewer engagement/score tracker — persisted as JSON memory under the workspace's `.awesome-rebuttal/`.

## Safety policy

`Awesome Rebuttal` should not:

- invent experiment results, numbers, citations, reviewer positions, or venue permissions;
- attack reviewers or imply bad faith;
- bypass anonymity or venue rules;
- over-promise future revisions;
- insert LeafLink, local tooling instructions, or any other paper-irrelevant content into final submission-facing text.

## Changelog

### 2026-06-13

- **New — `18` rebuttal rehearsal:** isolated reviewer/AC persona simulation that stress-tests the draft against the paper *before* the safety gate, producing a prioritized hardening list and an anticipated follow-up answer bank. Ships with paste-ready persona prompts (reconstructed reviewer, independent reviewer, AC) and a portable subagent/in-context execution model.
- **New — `19` discussion round handler:** multi-round follow-up handling with a reviewer engagement/score tracker, delta-only follow-up drafting (reusing the rehearsal answer bank), new-concern routing back to analysis, and discussion-etiquette safety gates.
- **Workflow:** extended from one-shot drafting to a full lifecycle (setup → … → multi-round discussion period).

## License

MIT License. See [`LICENSE`](LICENSE).

## Star History

<a href="https://www.star-history.com/#xiongqi123123/awesome-rebuttal&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=xiongqi123123/awesome-rebuttal&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=xiongqi123123/awesome-rebuttal&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=xiongqi123123/awesome-rebuttal&type=Date" />
  </picture>
</a>
