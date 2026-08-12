# Agent Loop v1.5.5 发布前审计 RED 基线

- 日期：2026-08-12
- 分支：`v1.5.5`
- 基线 HEAD：`f9c5569d93f6e42457b12fa2925a95373bea0cb9`
- 审计对象：当前未提交工作区
- 视角：Agent Loop Skill 源码仓库维护者

## RED 1：独立发布动作 Gate 缺失

命令：

```bash
PYTHONDONTWRITEBYTECODE=1 bash tests/validate-branch-management-strategy.sh
```

结果：`exit 1`

```text
FAIL: references/branch-management.md missing branch-management contract: | Tag Gate | creation of one exact tag at one exact commit |
```

根因：`references/branch-management.md` 将 tag、push、release、publish 和 sealed transition 合并到一个 `Release Gate`，与 root guidance、Submit / Integrate 和 workflow checklist 的独立 Human Gate 不变量冲突。目标修复保留同一张 Batch Human Review，但让每个动作拥有独立范围、前置条件和人类决定。

继续补强 Human Review 与 root 投影时，focused contract 分别得到以下真实 RED：

```text
FAIL: references/human-review-summary.md missing branch-management contract: | Tag Gate / Tag | exact tag + exact commit |
FAIL: templates/root-AGENTS.md missing branch-management contract: Submit, commit, PR, merge, release, publish, seal, pause, close, or cleanup is requested
FAIL: docs/maintenance/full-validation-method.md missing required text: Feature Completion、Submit、Commit、PR、Merge、Tag、Push、Release、Publish 和 Seal 保持各自的人类 Gate。
```

这些 RED 证明独立动作不只存在于 owning reference，还必须同步到 Human Review、root bootstrap、maintainer full-validation 和回归测试。

补齐 `Seal Gate` 后继续对“授权不包含哪些动作”的拥有面做负向压力测试，得到新的真实 RED：

```text
FAIL: references/branch-management.md missing branch-management contract: Recommendation and adoption do not authorize branch creation, switching, merge, deletion, push, tag, release, publish, or seal.
```

这证明只增加 Gate 表仍不充分：如果 recommendation、plan、card 或 batch 的负向授权清单遗漏 `seal`，Agent 仍可能把已有上下文误当作 sealed lifecycle transition 的授权。修复后同一 focused contract 同步检查 runtime、submit、stage/checklist、Human Review、root、templates 和人类文档。

## RED 2：Lightweight contract 保留旧 Bug reopen 顺序

命令：

```bash
PYTHONDONTWRITEBYTECODE=1 bash tests/validate-lightweight-change-lane.sh
```

结果：`exit 1`

```text
FAIL: references/design.md missing Lightweight Change contract: For explicit Bug management, create/update/reopen the Bug Record, verify Expected Behavior, and recommend exactly one Resolution Path.
```

根因：运行规则已修正为 closed Bug 在独立 Bug Reopen Gate 前保持 `closed`，但 Lightweight contract 仍断言旧句子。该修复只更新测试期望，不改变 Lightweight Change 行为。

## RED 3：Bug Reopen Gate 顺序冲突

命令：

```bash
PYTHONDONTWRITEBYTECODE=1 bash tests/validate-bug-management.sh
```

结果：`exit 1`

```text
FAIL: references/runtime.md does not keep a matched closed Bug unchanged until the Bug Reopen Gate
```

根因：runtime/stage canonical sequence 曾把 closed Bug 的 lifecycle write 放在独立 Bug Reopen Gate 前。回归目标要求 matched closed Bug 保持 `closed`，Gate 接受后才追加 Reopen Record、恢复 `Resolution: unresolved`，之后再进入新的 Resolution Path Gate。

## Low 证据：Archive 测试名称与行为不符

`tests/test_feature_monthly_archive_scan.py` 的旧名称声称 ambiguous reference 会阻断 Apply，实际契约已经是 advisory。该项只重命名测试，不改变 Scanner、Apply 或 Gate 行为，因此不制造行为型 RED。

## 授权与范围

- 人类已批准修正 Bug Reopen 顺序、独立发布动作 Gate 和 Archive 测试命名。
- legacy `agent-loop/` memory root 兼容问题明确不在本轮修复范围。
- 不新增 canonical stage、message intent、artifact tree、Checker 或版本号。
- 本轮未执行 commit、push、tag、PR、merge、release 或 publish。
