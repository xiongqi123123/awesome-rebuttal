<div align="center">
  <img src="assets/image/awesome-rebuttal.png" alt="Awesome Rebuttal logo" width="260" />

# Awesome Rebuttal

**面向学术论文 rebuttal 的项目级 skill 包：辅助策略分析、证据组织与 author response 写作。**

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

## 这是什么？

`Awesome Rebuttal` 是一个可全局安装、但在具体论文工作区内运行的项目级 skill，面向 AI / ML / CV / NLP / Robotics 等方向的论文 rebuttal。它帮助 AI 编程助手在论文工作区中持久化结构化记忆、分析审稿意见、规划补充实验，并在用户确认会议规则后起草安全、专业的 author response。

本项目与任何会议、出版方、审稿平台或投稿系统均无官方关联。

## 亮点

- **Skill-first 架构**：以 `SKILL.md` 为入口，按原子能力拆分能力文件。
- **项目级状态管理**：每篇论文的 memory、draft、snapshot、template、log 都保存在该工作区的 `.awesome-rebuttal/` 中。
- **审稿意见拆解**：整理 reviewer metadata、原始意见、atomic concerns 与 common concern clusters。
- **策略制定**：分析 rebuttal 局势、优先级问题、不同 reviewer 的目标，以及面向 AC 的决策事实。
- **补充实验规划**：区分必须做、高收益可选、不推荐、不可行的 rebuttal 实验。
- **格式感知写作**：支持一页 PDF、OpenReview 逐 reviewer 回复、global comment、hybrid response、Markdown+LaTeX comment。
- **安全门控**：阻止无证据结论、编造实验、不合规会议权限、攻击性语气和匿名泄露。
- **可选 Overleaf 同步**：仅在用户需要时引导 LeafLink 同步云端/本地论文。

## 安装

发布仓库根目录就是 skill 包根目录。克隆后，当前目录应直接包含 `SKILL.md`。

```bash
git clone https://github.com/xiongqi123123/awesome-rebuttal.git
cd awesome-rebuttal
test -f SKILL.md
```

### 方式 A：手动安装到 Codex

```bash
CODEX_SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
TARGET="$CODEX_SKILLS_DIR/awesome-rebuttal"
mkdir -p "$CODEX_SKILLS_DIR"
rsync -a --exclude '.git/' --exclude '.awesome-rebuttal/' ./ "$TARGET"/
```

安装后重启 Codex。

### 方式 B：手动安装到 Claude Code

```bash
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
TARGET="$CLAUDE_SKILLS_DIR/awesome-rebuttal"
mkdir -p "$CLAUDE_SKILLS_DIR"
rsync -a --exclude '.git/' --exclude '.awesome-rebuttal/' ./ "$TARGET"/
```

安装后重启或 reload Claude Code。

### 方式 C：让大模型辅助安装

把仓库地址和 [`AI_AGENT_INSTALL.md`](AI_AGENT_INSTALL.md) 发给本地 AI 编程助手，让它帮你安装到 Codex、Claude Code 或 Cursor。

推荐提示词：

```text
请从 https://github.com/xiongqi123123/awesome-rebuttal 安装 Awesome Rebuttal。
按照 AI_AGENT_INSTALL.md 操作，不要在没有备份的情况下覆盖已有文件。
```

### 方式 D：Cursor 项目规则

Cursor 可以通过 project rule 指向这个已克隆或已安装的 skill。最小 `.cursor/rules/awesome-rebuttal.mdc` adapter 见 [`AI_AGENT_INSTALL.md`](AI_AGENT_INSTALL.md)。

## 基本使用

在论文 rebuttal 工作区中，对 AI 助手说：

```text
Use Awesome Rebuttal to initialize this rebuttal workspace.
```

推荐工作区结构：

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

如果你的工作区已经有其他结构，skill 应该非破坏式地识别和映射，而不是强制重命名。

## 宿主环境兼容性

| 宿主 | 状态 | 安装方式 |
|---|---|---|
| Codex | 原生 skill 包 | 复制到 `~/.codex/skills/awesome-rebuttal` |
| Claude Code | skill-compatible 包 | 复制到 `~/.claude/skills/awesome-rebuttal` |
| Cursor | 项目规则 adapter | 创建 `.cursor/rules/awesome-rebuttal.mdc` |
| 其他 agent | Prompt/reference 包 | 让 agent 读取 `SKILL.md` |

选择题/问卷不需要额外依赖。宿主有原生选择 UI 就用原生 UI；没有的话，普通 Markdown 的 A/B/C 或 checkbox 就足够。

## Response modes

skill 在 memory 中使用统一的 response mode 命名：

- `openreview_per_reviewer`
- `unified_limited`
- `pdf_one_page`
- `global_comment`
- `hybrid`
- `openreview_markdown_latex`
- `unknown`

交互分析默认跟随用户语言；最终投稿相关 rebuttal 文本默认使用英文，除非用户要求其他语言且会议规则允许。

## 内置资源

- 一页 PDF rebuttal fallback LaTeX 模板：[`assets/one-page-rebuttal-template/`](assets/one-page-rebuttal-template/)
- Snapshot renderer：[`scripts/render_snapshot.py`](scripts/render_snapshot.py)
- Memory schemas：[`references/memory-schemas/`](references/memory-schemas/)
- 原子能力文件：[`references/capabilities/`](references/capabilities/)

## 安全原则

`Awesome Rebuttal` 不应该：

- 编造实验结果、数字、引用、reviewer 立场或会议规则；
- 攻击 reviewer 或暗示 reviewer 恶意；
- 绕过匿名规则或会议规则；
- 过度承诺未来修改；
- 把 LeafLink 或本地工具说明写进最终投稿文本。

## License

MIT License. 见 [`LICENSE`](LICENSE)。

## Star History

<a href="https://www.star-history.com/#xiongqi123123/awesome-rebuttal&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=xiongqi123123/awesome-rebuttal&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=xiongqi123123/awesome-rebuttal&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=xiongqi123123/awesome-rebuttal&type=Date" />
  </picture>
</a>
