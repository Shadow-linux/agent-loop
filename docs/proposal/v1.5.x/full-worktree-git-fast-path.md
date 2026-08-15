# Proposal: Full-Worktree Git Fast Path

状态：implemented and validated；awaiting final Human Review

目标版本：v1.5.6

创建时间：2026-08-15

默认语言：中文

验证证据：[RED baseline](../../reports/agent-loop-v1.5.6-full-worktree-git-fast-path-red-baseline-2026-08-15.md)；[full validation](../../reports/agent-loop-v1.5.6-full-worktree-git-fast-path-validation-2026-08-15.md)。实现与验证未执行 stage、commit、push、tag、PR、merge、release、publish 或 installed Skill 同步。

## 摘要

当人类明确要求 `commit` 或 `commit and push` 时，Agent Loop 不应把 Git 动作重新升级成一次完整 Feature Submit 验收，也不应为了提交而自动运行测试、代码/质量 Review、Drift 或 Completion。Agent 应先读取 Git 事实并拟定 commit message，再向人类展示一次轻量 Commit Confirmation；人类确认后，使用 `git add -A` 提交全部 modified、added、deleted、staged、unstaged 与 untracked 内容，并在 Push 同时被请求且目标明确时继续推送。

该快速路径只改变 Git 动作的准备与确认方式，不改变完成真实性：没有新鲜验证时可以提交一个明确标注为未验证的工作状态，但不得声称 Feature 已完成、验证已通过、可以关闭或可以发布。

## 1. 已确认原则

1. 人类明确要求 commit / push 时，Git 动作默认走简洁快速路径。
2. Commit 的默认范围是当前仓库整个工作区，不再由 Agent 自主挑选“相关文件”。
3. Agent 在执行前只请求一次轻量 Commit Confirmation，内容是整个工作区变更摘要与拟定的 commit message；若 commit 与 push 同批请求，同一次确认还必须包含精确 remote/ref。
4. Agent 不得自行 exclude、restore、clean、stash、split、丢弃或改写工作区内容。
5. 发现缓存、生成物、敏感或可疑文件时只做显著披露，由人类决定是否改变范围。
6. 仅因 Git 请求不得自动运行测试、Verify、Review、Drift、Completion 或新建验证证据。
7. 人类显式附加“测试通过后再提交”等条件时，该条件成为本次 Git 授权的一部分。
8. 普通 Commit、Push、Tag、PR、Merge、Release、Publish、Seal 仍是独立 Gate；Git Fast Path 的一次轻量确认可同时授权被明确请求的 Commit 与 Push，但不会扩展到其他动作。
9. Git 失败或执行前发现 branch、冲突状态或工作区事实发生变化时停止，保留当前 worktree/index，报告事实，不做 reset/clean/restore/stash。

## 2. Git Fast Path

### 2.1 触发

以下清晰请求进入该路径：

- “commit / 提交这些内容”；
- “把工作区全部提交”；
- “commit and push / 提交并推送”。

普通“看看能否提交”“准备提交材料”仍是只读 Submit Review，不授权 Git mutation。

### 2.2 一次轻量 Commit Confirmation

执行前展示：

| 项目 | 必须内容 |
|---|---|
| Repository | 仓库路径、当前 branch、HEAD |
| Worktree Scope | 全部 staged、unstaged、untracked、deleted 文件摘要 |
| Warnings | cache/generated/sensitive/suspicious 候选；不得静默排除 |
| Verification Truth | `not run for this Git action; no completion or release-readiness claim`，除非人类明确附加前置条件 |
| Commit | `git add -A`、Agent 拟定或人类提供的完整 commit message、整个工作区 |
| Push | 精确 remote/ref；未请求则 `not-authorized` |
| Not Authorized | 未列入接受行的 PR/merge/tag/release/publish/seal 等动作 |

这不是代码、质量、Feature、verification、Drift 或 Completion Review，不运行测试，不要求第二次确认。若执行前发现工作区事实、分支、目标 remote/ref 或 commit message 已变化，停止并刷新一次轻量确认。

### 2.3 Apply

```text
Human accepts lightweight Commit Confirmation
-> git add -A
-> verify index represents the confirmed entire worktree
-> git commit with the confirmed message
-> if and only if Push was requested and confirmed: push exact remote/ref
-> report commit/push result and current Git state
```

Agent 不得用 pathspec、交互式 staging、临时 ignore、restore、clean、stash 或额外 commit 拆分来改变已确认范围。

### 2.4 测试与完成声明

Git Fast Path 的默认 `Verification` 值是：

```text
not run for this Git action; no completion or release-readiness claim
```

已有测试结果可以作为历史事实展示，但不得伪装成本轮 fresh verification。Git commit 可以保存中间状态；Task Done、Feature Close、Release readiness 和“已修复/已完成”声明仍受原有新鲜验证、Review、Drift、Memory 和 Completion 约束。

## 3. 硬停止

仅保留以下客观停止条件：

- 不是 Git repository，或目标 repository 不明确；
- unresolved merge/rebase/cherry-pick/conflict；
- repository/branch 不明确，或已请求 Push 但 remote/ref 不明确；
- 执行前发现工作区事实在确认后发生变化；
- 已采用的 sealed/customer isolation/branch policy 明确禁止目标动作；
- `git add -A` 后 index 与确认范围不一致；
- commit 或 push 命令失败。

敏感/生成/缓存候选不是 Agent 自主排除理由；它们必须在确认面中披露。若人类要求调整范围，返回新的轻量确认，而不是由 Agent 私自处理。

## 4. 与现有流程的关系

- 不新增 canonical stage、message intent、status、artifact tree、Checker outcome 或 Git action。
- `Submit / Integrate` 仍是 owning stage；Git Fast Path 是其内部方法。
- Prepare-only、PR、merge、tag、release、publish、seal 继续使用原有质量与独立 Gate 规则；本快速路径只合并同一请求里的 Commit/Push 确认。
- Feature/Lightweight/Review 的实现与验证规则不改变。
- 该规则面向使用 Agent Loop 的目标项目；本 skill source repository 的维护、TDD、full validation 和发布流程仍由根 `AGENTS.md` 与 `docs/maintenance/` 管理。

## 5. 非目标

- 不把 Git 自动化为无确认动作，也不把轻量 Commit Confirmation 扩大成代码/质量 Review；
- 不授权 Agent 丢弃或隐藏人类工作；
- 不把 commit 等同于完成、关闭、合并或发布；
- 不取消 Push 等外部动作的精确目标披露；
- 不修改 Skill 版本；
- 不在本仓库创建目标项目 `.agent-loop/` artifacts；
- 不自动 commit、push、tag、merge、release 或 publish 本 Proposal 的实现。

## 6. 验收条件

1. runtime/design/submit/stage/checklist/human-review/root guidance 对“一次轻量 Commit Confirmation、全工作区、拟定 commit message、不跑测试/质量 Review”含义一致。
2. 旧的“commit 只进入 Submit、检查完成证据后再二次确认”不再作用于明确 Git Fast Path。
3. 旧的“发现 unrelated work 由 Agent 排除或拆分”不再作用于全工作区 commit。
4. 测试证明工作区漂移、目标歧义、冲突与独立 Push 授权仍会停止。
5. 测试证明没有验证时不得产生完成/发布声明。
6. 所有 13 个 root managed block revision 同步更新。
7. focused、mutation、全部 Shell/Python、机械检查和六域 full validation 通过并保存中文报告。
