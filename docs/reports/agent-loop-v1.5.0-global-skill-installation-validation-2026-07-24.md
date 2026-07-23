# Agent Loop v1.5.0 全局 Skill 安装能力验证报告

日期：2026-07-24

验证分支：`alpha/v1.5.0`

基线提交：`699d5a68d35854a31931701d970ed7b0fc439ac9`

结论：通过 Human Review 前的实现与聚焦验证；本报告生成时尚未执行 commit、push、tag、release、publish 或 `main` 同步。

## 验证目标

验证 Agent Loop 源仓库可通过 Vercel `skills` CLI 安装到 Codex、Kimi Code CLI、Claude Code 和 OpenCode，并确认升级、清单、项目 `AGENTS.md` 刷新提醒、安装授权边界和正式发布默认通道形成一致契约。

## RED / GREEN

RED 基线在安装文档落地前执行：

```text
FAIL: README.md missing global installation contract: npx -y skills add Shadow-linux/agent-loop
```

文档、边界和测试完成后执行：

```bash
bash tests/validate-global-skill-installation.sh
```

结果：

```text
PASS: global Agent Loop installation, update, verification, fallback, and project-guidance reminder contract is complete
```

相邻维护契约：

```text
PASS: maintainer full-validation guidance is durable and correctly scoped
PASS: root AGENTS block refresh contract is complete
```

## 隔离本地安装

验证在临时 `HOME`、`XDG_CONFIG_HOME` 和 npm cache 下执行，没有写入维护者真实的全局 Skill 目录：

```bash
npx -y skills add . \
  --global \
  --skill agent-loop \
  --agent codex \
  --agent kimi-code-cli \
  --agent claude-code \
  --agent opencode \
  --copy \
  --yes
```

安装器确认：

```text
Found 1 skill
Selected 1 skill: agent-loop
copy → Codex, Kimi Code CLI, Claude Code, OpenCode
```

实际布局：

```text
~/.agents/skills/agent-loop
~/.claude/skills/agent-loop
```

前者是通用 Skill 安装位置；后者是 Claude Code 兼容位置。使用 `--copy` 时两处均为目录；安装器的其他模式可使用兼容链接，不能把它们错误描述为四份独立的运行时安装。

以下关键文件存在：

```text
SKILL.md
references/runtime.md
references/design.md
templates/root-AGENTS.md
scripts/check-root-agents-blocks.py
```

全局清单命令返回：

```text
agent-loop ~/.agents/skills/agent-loop
```

## GitHub 源、更新与发布通道

通过同一 GitHub 仓库的 SSH 地址执行源发现成功，发现且只发现一个 `agent-loop` Skill；隔离远端安装和：

```bash
npx -y skills update agent-loop -g -y
```

均成功，更新结果为：

```text
All global skills are up to date
```

当前环境访问 GitHub HTTPS 443 失败，因此 `Shadow-linux/agent-loop` HTTPS shorthand 未能在本机完成在线复验；SSH 对同一仓库的发现、安装和更新成功。README 保留标准 shorthand，正式发布检查仍应在可访问 GitHub HTTPS 的 CI 或工作站再执行一次。

远端分支证据：

```text
main          47e3e7c29ee41ec76d1546978557406f01c15cb5
v1.4.0        81adf6422e509ee0b6012522398a3a908323b131
alpha/v1.5.0  699d5a68d35854a31931701d970ed7b0fc439ac9
```

远端 `main` 的 `SKILL.md` 当前仍声明 `Version: 1.3.0`。这不是本次安装实现的失败，但说明正式 v1.5.0 发布必须将已验收发布提交同步到 `main`，否则默认 `npx skills add/update` 用户不会获得最新正式版。

已固化的发布原则：

- `main` 是默认公开安装通道，必须指向最新正式稳定版的同一提交。
- `vX.Y.Z` 是该正式版本的长期维护分支。
- `alpha/*` 只能显式选择，不能成为默认安装来源。
- 同步 `main` 属于独立的 branch/merge/push Human Gate；本次没有执行或授权该动作。

## 权限与边界

- 人类可通过明确命令全局安装或更新 Agent Loop。
- Agent 不得自动或无范围地安装、升级 Skill。
- 全局 Skill 升级不会自动修改任何项目 `AGENTS.md`。
- 项目 guidance 刷新仍需要单独 Human Review，并保留人类原文。
- 安装授权不扩大 Feature、Git、发布、生产、付费、破坏性或外部动作权限。

## 回滚

若 Human Review 不接受，可仅回退本次拥有的 README、Usage、CHANGELOG、维护规则、Proposal、Plan、验证场景、聚焦测试和本报告。无需删除或迁移任何真实全局 Skill，因为验证只使用了隔离临时目录。

## 剩余风险

- 当前环境无法验证 GitHub HTTPS shorthand；需要在 HTTPS 可达环境复验。
- 本次验证覆盖安装结构与 CLI 清单，没有逐个启动四个 Agent CLI 进行交互式加载测试。
- Windows 未做真实主机安装；当前结论依赖跨平台 Node.js CLI 契约和无平台专属安装脚本的实现。
- v1.5.0 尚未正式发布，`main` 同步仍属于后续 Release Gate。
