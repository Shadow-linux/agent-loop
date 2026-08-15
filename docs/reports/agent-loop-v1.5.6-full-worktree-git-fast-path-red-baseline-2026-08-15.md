# Agent Loop v1.5.6 Full-Worktree Git Fast Path RED 基线

日期：2026-08-15

分支：`v1.5.5`

基线 HEAD：`84c14aa6ddc75779022229c4d2c5d5d9035b57e7`

## 目标

证明现行 Submit / Git 规则没有实现已批准的“一次确认、整个工作区、默认不因 Git 请求运行测试”的 Git Fast Path。

## RED 命令

```bash
bash tests/validate-full-worktree-git-fast-path.sh
```

实际退出码：`1`

实际首个失败：

```text
FAIL: references/runtime.md missing Git Fast Path contract: Full-Worktree Git Fast Path
```

## 结论

RED 有效：focused contract 能在任何 production runtime/reference/template 修改前识别真实缺口。当前运行规则仍把明确 commit 请求导入旧的完整 Submit 验证与二次确认逻辑，也仍允许 Agent 对 unrelated work 做选择性提交处理；本轮 GREEN 必须协调修改 owning surfaces，而不能只添加关键词或只改模板。

## 语义审计追加 RED

首轮 GREEN 后，跨文件审计发现 adopted Branch Strategy 仍会用旧的 verification/Review/Drift 与 unrelated-dirty-work 条件阻断 Git Fast Path。先扩展 focused contract，再运行：

```bash
bash tests/validate-full-worktree-git-fast-path.sh
```

实际退出码：`1`

实际失败：

```text
FAIL: references/branch-management.md missing Git Fast Path contract: Full-Worktree Git Fast Path preserves branch-policy facts without restoring normal Submit quality prerequisites
```

修复 owning Branch Strategy 与 Human Review 后，同一命令输出：

```text
PASS: Full-Worktree Git Fast Path contract and mutations are valid
```

两次 RED 均保留 canonical stage、独立 Commit/Push Gate、sealed/customer isolation、冲突和目标歧义停止条件；GREEN 只移除“仅因 Git 动作自动跑质量流程”和“Agent 自主排除工作区内容”。

## 人类澄清后的 RED

人类进一步明确：允许提交前确认，但确认内容只包含整个工作区变更摘要与 Agent 拟定的 commit message；不得把它做成代码/质量 Review，也不得为了 commit 运行测试。focused contract 先更新为该边界，再对尚未同步的 runtime 执行：

```bash
bash tests/validate-full-worktree-git-fast-path.sh
```

实际退出码：`1`

```text
FAIL: references/runtime.md missing Git Fast Path contract: one lightweight Commit Confirmation
```

该 RED 证明旧实现“请求本身直接授权、完全没有确认”和早先“完整 Human Review”都不符合最终要求。GREEN 统一为一次轻量 Commit Confirmation，删除正式 fingerprint 契约，保留执行前事实变化停止、`git add -A`、Push 精确目标与完成真实性边界。
