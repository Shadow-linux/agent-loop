# Agent Loop v1.5.0 正式版候选全量验证报告

## 1. 审计对象与边界

- 日期：2026-07-24
- 分支：`alpha/v1.5.0`
- Skill 版本：`1.5.0`
- 审计对象：Git `HEAD` `699d5a68d35854a31931701d970ed7b0fc439ac9` 加当前工作区中的 Global Skill Installation 实现
- 验证方法：`docs/maintenance/full-validation-method.md`
- 目标：判断当前候选是否可提交并推送，供人类合并到 `main` 后成为正式 v1.5.0 默认安装基线
- 授权边界：人类已授权当前有效改动的 commit 和 push；未授权 tag、GitHub Release、publish、删除 `alpha/v1.5.0` 或由本 Agent 合并 `main`

## 2. 总结

总分：**99/100**

等级：**STRONG**

当前 Critical / High / Medium：**0 / 0 / 0**

发布判断：当前候选可提交并推送到 `alpha/v1.5.0`，供人类合并 `main`。`main` 合并成功并指向同一提交后，默认 `npx skills add/update` 才会取得正式 v1.5.0。

| 检查 | 结果 |
|---|---|
| 全部 Shell tests | 42/42 PASS |
| 全部 Python tests | 280/280 PASS，89.786s |
| Ruby adversarial tests | 2/2 files PASS |
| Skill / OpenAI metadata YAML | 2/2 PASS |
| Repository JSON | 3/3 PASS |
| Shell syntax | 43/43 PASS |
| Markdown fence balance | 280/280 PASS |
| `git diff --check` / staged diff check | PASS |
| Global Skill isolated install | PASS |
| Global Skill focused contract | PASS |

## 3. 六域评分

| 审计域 | 结果 | 分数 | 当前结论 |
|---|---:|---:|---|
| Logic Correctness | PASS | 100 | Requirement、ADR、Feature、Bug、Lightweight、Memory、Git/Release Gate 路由保持一致；安装能力未改变 canonical stage 或状态 |
| Autonomy | PASS | 99 | Agent 保持事实调查、唯一建议和安全推进责任；安装、项目 guidance 刷新和 Git 动作仍由独立 Human Gate 控制 |
| Project Entry / Evidence Graph + DDD Onboarding | PASS | 99 | Project Entry、可靠 memory、dual-root、stale guidance 和 Onboarding 路径均通过回归；安装包包含完整 runtime/reference/template/script |
| Development / Test Workflow | PASS | 100 | Plan、TDD、Verify、Review、Drift、Memory、Submit、Completion 与 Bug/Feature ownership 闭环完整 |
| Memory | PASS | 100 | `product.md`、ADR、Feature Product Slice、Project Memory 和冲突驱动的 Post-Merge Reconciliation 权威边界未漂移 |
| Recommendation | PASS | 99 | README/Usage 给人类可直接使用的安装、升级、接管与项目 guidance 刷新表达；`main` 稳定通道规则明确 |
| **合计** |  |  | **99/100，STRONG** |

## 4. RED 基线与 GREEN

### Global Skill Installation RED

聚焦测试在 README 尚未提供新安装入口时失败：

```text
FAIL: README.md missing global installation contract: npx -y skills add Shadow-linux/agent-loop
```

这证明旧文档无法满足 GitHub 全局安装、四 Agent 目标、升级与项目 guidance 刷新契约。

### GREEN

实现后：

```text
PASS: global Agent Loop installation, update, verification, fallback, and project-guidance reminder contract is complete
```

随后重新执行全部 Shell、Python、Ruby adversarial 和机械检查，结果全部通过。没有只用聚焦测试替代全量验证。

## 5. 关键不变量

| 不变量 | 结果 |
|---|---|
| `SKILL.md` 是简洁入口，design/runtime/reference 承担发布运行权威 | PASS |
| root Stage Map 只负责 first-hop 导航，不复制完整 stage 实现 | PASS |
| Requirement `product.md` 是新产品语义权威，人类原件保持 byte-stable | PASS |
| Product Human Review 与 Requirement lifecycle、ADR、Feature、Git Gate 相互独立 | PASS |
| ADR 是条件触发的技术落地桥梁，不是所有 Feature 的必需文件 | PASS |
| Feature `spec.md` 通过 Product Slice 消费产品定义，不重定义产品含义 | PASS |
| Delivery Contract 不是默认 artifact，创建、接受和 breaking change 各自受控 | PASS |
| 行为变更必须有 TDD RED，非行为 `N/A` 必须有具体理由 | PASS |
| 同时只有一个 Active Feature；Pause / Resume / Close / Reopen 与 memory 同步 | PASS |
| 部分 Feature/Phase 完成不会误关整个 Requirement | PASS |
| accepted ADR 与当前产品或实现 drift 时回到 Decision Scan / Human Review | PASS |
| Follow-up 先调查 identity、ownership 和证据，再选择修复路径 | PASS |
| Submit 依次要求 fresh verification、drift、diff review、Human confirmation 和 submit note | PASS |
| 普通 Chat 不创建 Requirement 或 Feature artifact | PASS |
| Post-Merge Memory Reconciliation 只处理观察到的冲突，不做机械全量扫描 | PASS |
| install、project `AGENTS.md` refresh、commit、push、merge、tag、release、publish 保持独立 Gate | PASS |
| `main` 是最新正式稳定版的默认公开安装通道；alpha 不是默认来源 | PASS |

## 6. 代表性压力场景

| 场景 | 结果 |
|---|---|
| Complex Requirement → Standard Product Definition → Product Review → Decision Scan / ADR → Feature Product Slice | PASS |
| Brief Requirement → `design-not-needed` → Feature Product Slice | PASS |
| Product Review 尚未确认却尝试创建 ADR 或 Feature | STOP |
| ADR Requirement Model coverage 不完整或 compatibility 为 `review-required` | STOP |
| Delivery Contract 未经确认即创建、接受或 breaking change | STOP |
| 行为变更无 RED，或非行为 `N/A` 无理由 | STOP |
| Active Feature 存在时尝试启动另一 Feature | STOP / Human Choice |
| 多 Phase 只完成一部分 | Requirement 保持 `partially-implemented` |
| accepted ADR 与实现不一致 | Drift → Decision Scan / superseding ADR |
| Follow-up 证据不足 | `investigate-first`，不伪造 Feature repair |
| Submit 包含旧验证或无关 dirty work | BLOCK |
| stale memory 或双 memory root | Recovery，禁止静默选择 |
| 普通 Chat | 只回答，不创建工作流 artifact |
| 无冲突的代码 merge 后 | 不启动 memory scan，不创建报告 |
| 小型 memory 冲突 | Agent 基于最新事实在会话内修正；真正歧义才交人类 |
| 人类授权全局安装但未授权 project guidance 写入 | 只安装 Skill，不修改项目 `AGENTS.md` |
| 人类升级全局 Skill | 显示“Agent Loop 版本已更新，请更新项目的 AGENTS.md。”提醒 |
| alpha 分支存在但使用无版本 GitHub shorthand 安装 | 读取 `main`，不会隐式读取 alpha |

## 7. Global Skill Installation 验证

隔离临时 `HOME` 中执行：

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

安装器发现且只选择一个 `agent-loop` Skill，并确认目标为 Codex、Kimi Code CLI、Claude Code 和 OpenCode。安装内容包含：

```text
SKILL.md
references/runtime.md
references/design.md
templates/root-AGENTS.md
scripts/check-root-agents-blocks.py
```

实际通用路径为 `~/.agents/skills/agent-loop`，Claude 兼容路径为 `~/.claude/skills/agent-loop`。这不是四份必须独立维护的仓库。

GitHub SSH 源发现、隔离安装和 `npx skills update agent-loop -g -y` 成功。当前工作站无法访问 GitHub HTTPS 443，因此标准 shorthand 仍需在 HTTPS 可达的 CI 或工作站复验；这属于环境验证缺口，不是当前 Skill 结构失败。

## 8. 当前问题与残余风险

当前没有未解决 Critical、High 或 Medium。

Low / 观察项：

- 当前环境无法在线复验 GitHub HTTPS shorthand；同一仓库的 SSH 源已验证。
- 尚未逐个启动四个 CLI 做真实会话加载测试；安装器目标识别、文件布局和清单已验证。
- Windows 未做真实主机安装；当前实现使用跨平台 Node.js CLI，没有新增平台专属安装脚本。
- `skills list -g --json` 对共享通用路径的 Agent 归属展示不等同于安装器的四目标摘要，不能把该展示字段当成四个 CLI 的独立安装目录清单。
- Optional Visual legacy reader 与跨轮重复推荐仍属于既有 Low 观察边界；本轮没有扩大它们。

## 9. 工作区、提交与发布判断

- 应提交：`AGENTS.md`、`README.md`、`Usage.md`、`CHANGELOG.md`、安装边界、Proposal、Implementation Plan、focused test 和 2026-07-24 两份验证报告。
- 应排除：`.tmp/`、`scripts/__pycache__/`、`tests/__pycache__/`。
- Skill version、`plugin.json`、`templates/root-AGENTS.md`、`references/runtime.md` 和 `references/design.md` 已是 1.5.0 对应状态，本轮未产生意外改动。
- 当前候选满足 commit 和 push 条件。
- 人类已授权 commit 和 push 当前 `alpha/v1.5.0`；本 Agent不会合并 `main`。
- 人类后续将 `alpha/v1.5.0` 的最终提交合并到 `main`；正式默认安装通道只有在 `main` 指向该同一提交后才完成。
- tag、GitHub Release、publish、删除 alpha 分支与 installed Skill sync 仍未授权。
