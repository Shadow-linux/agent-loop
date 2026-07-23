# Human-Guided Branch Management RED 基线报告

日期：2026-07-15
分支：`alpha/v1.4.0`
当前 Skill metadata：`1.3.0`
审计对象：当前工作区，行为基线 HEAD `5c6112c91316dc00160184b321e4ded5826fcb51`
历史 raw all-ref 基线 SHA-256：`98906fe837a75f77b5afdbb944497f3c6570d73cae88ef1214228ad330641044`（包含 Codex 桌面自动维护的 `refs/codex/turn-diffs/*`，仅保留为原始记录，不用于判断业务 Git 引用漂移）

## 工作区边界

建立 RED 前，工作区只有以下批准范围文件：

- `docs/proposal/v1.4.x/branch-management-strategy.md`
- `docs/proposal/v1.4.x/branch-management-strategy-implementation-plan.md`

Proposal 只更新了状态行。尚未创建或修改 `SKILL.md`、`references/`、`templates/`、`README.md`、`Usage.md` 或 `CHANGELOG.md` 的 Branch Management 运行行为。

## 现有回归基线

执行：

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
for test_file in tests/*.sh; do bash "$test_file"; done
```

结果：

- Python：`98/98 PASS`
- 既有 Shell contracts：`34/34 PASS`

这证明新增 RED 之前仓库现有回归是绿色，后续失败不是既有基线故障。

## Focused RED

先创建：

```text
tests/validate-branch-management-strategy.sh
```

然后执行：

```bash
bash tests/validate-branch-management-strategy.sh
```

退出码：`1`

精确失败：

```text
FAIL: missing required file: references/branch-management.md
```

## RED 有效性判断

结果是有效 RED：

- 测试脚本能够运行，不是 Shell 语法或路径拼写错误；
- Proposal 和 Implementation Plan 均存在；
- 失败点正是尚未实现的完整运行规则 `references/branch-management.md`；
- 生产运行规则、模板和人类文档尚未为了测试而预先修改；
- 测试还包含 no-new-stage、root-only-one-sentence、durable/volatile artifact ownership、完整 Mermaid 同步和 no-target-workspace 等后续契约。

因此当前 Agent Loop runtime 尚不能声明具备批准的 Human-Guided Branch Management 能力。

## Human Review Repair RED

首次实现进入 Human Review 后，审计发现四类契约缺口：全局 Branch Stop 可能误伤简单项目、Auto Mode 与 create/switch Gate 表述不完整、`declined` Profile 会把未采用方案误记为现行策略、canonical root guidance 使用了固定中文。人类批准修复，同时明确不增加“每次创建或切换分支前都必须主动推荐策略”的新触发规则。

先扩展 focused contract，再逐层修改运行规则。依次观察到以下真实 RED：

```text
FAIL: SKILL.md missing branch-management contract: when an adopted Branch Strategy or versioned/customer delivery applies
FAIL: SKILL.md missing branch-management contract: branch creation, switching, deletion, push, or tag
FAIL: references/branch-management.md missing branch-management contract: existing-project | human-guided-release | not-applicable
FAIL: root AGENTS must contain the exact branch-management reminder once; found 0
```

四次失败分别锁定适用范围、Auto Mode/Git action 授权、declined memory model 和 canonical root language；测试没有通过弱化旧断言或扩大推荐触发来转绿。修复后同一 focused contract 输出：

```text
PASS: Human-Guided Branch Management optional profile, gates, artifacts, diagram, and scope contract is complete
```

补充契约还明确断言：`references/branch-management.md` 不得包含 `before every branch creation or switch`，因此人类问分支管理办法时会得到推荐，但普通 branch create/switch 不会自动升级成强制策略访谈。

## Independent Review Follow-up RED

修复后的独立只读 Review 发现：source authority 已放行 simple `not-needed`，但 Plan 和 Submit / Integrate 的详细 checklist/stage 仍可能无条件要求 Target Release Context/Target Branch。先增加下游适用范围断言，确认新 RED：

```text
FAIL: references/branch-management.md missing branch-management contract: When an adopted Branch Strategy or versioned/customer delivery applies, if Target Release Context or the unique Target Branch is unclear
FAIL: templates/plan.md missing branch-management contract: For a confirmed simple `not-needed` path, set branch-specific fields to `not-applicable`
```

第一个 RED 锁定下游适用范围；修正后继续扩展相同语义的 template/drift 断言，观察到第二个 RED。最终 `references/branch-management.md`、`references/stage-guides.md`、`references/workflow-checklists.md`、`references/submit-and-integrate.md`、`templates/plan.md` 与 inline document template 使用同一 applicable-context 语义；simple `not-needed` 在 Plan/Drift/Submit 把分支专属检查记为 `not-applicable`，不会因缺 Target Release Context/Target Branch 被阻断。同一 focused contract 重新 GREEN。

Review 同时发现 Implementation Plan 声明 Tasks 0-7 已完成，但历史步骤仍保持未勾选。该问题不是 runtime 行为 RED，已按实际证据回填完成项，只保留真实的最终 Human Review 待办。

## Git 与目标项目副作用

- 未创建、切换、合并或删除真实 `release/*`、`customer/*`、`feature/*`、`bugfix/*`、`hotfix/*` 分支；
- 未创建仓库根 `.agent-loop/`；
- 未执行 commit、push、tag、PR、merge、release 或 publish；
- HEAD 保持 `5c6112c91316dc00160184b321e4ded5826fcb51`；标准 `refs/heads`、`refs/remotes`、`refs/tags` 在本轮没有 reflog 变更。
- 当前标准引用快照 SHA-256 为 `8cd849b94efdd5374409c2832b54d0531e2d3d9526d60bc76c5743879fddeef4`。Codex 桌面自动创建或刷新 `refs/codex/turn-diffs/*`，所以不再使用 raw all-ref hash 判断实现是否产生 Git 副作用。
