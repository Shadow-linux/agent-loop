# Agent Loop v1.5.8 Direct Edit Fast Path RED 基线

日期：2026-08-26

分支：`alpha/v1.5.7`（目标版本 `1.5.8`；本轮未创建或切换分支）

基线 HEAD：`a25fec3bdd1558398df8870393e90e8d808cfc35`

## 目标

证明实施前的 Agent Loop 尚不存在 Direct Edit Fast Path，也没有“每次新的具体全量测试执行必须单独确认”的完整运行契约；同时确认本次改变依赖的 Lightweight Change、Git Fast Path、Progressive Verification 与维护者全量验证 focused 基线均健康。

## 工作区边界

开始 RED 前，`git status --short --branch` 仅报告两个已接受的未跟踪设计文件：

```text
## alpha/v1.5.7
?? docs/proposal/v1.5.x/direct-edit-fast-path-implementation-plan.md
?? docs/proposal/v1.5.x/direct-edit-fast-path.md
```

没有 tracked implementation 修改、重叠 dirty work、暂存内容或归属不明文件。

`Production files modified before RED: none`

## 既有 focused 基线

执行：

```bash
for test_file in \
  tests/validate-lightweight-change-lane.sh \
  tests/validate-full-worktree-git-fast-path.sh \
  tests/validate-progressive-verification.sh \
  tests/validate-maintainer-full-validation-guidance.sh; do
  bash "$test_file"
done
```

实际结果：四个 Shell contract 全部 PASS；`validate-lightweight-change-lane.sh` 内嵌的 37 个 Python tests 全部 PASS。此步骤只运行受影响 focused 基线，没有运行仓库全量 Shell/Python tests。

## 缺失能力 RED

执行：

```bash
rg -n 'Direct Edit Fast Path' SKILL.md references templates README.md Usage.md CHANGELOG.md
```

实际结果：`exit 1`，`0 matches`。

执行：

```bash
rg -n 'one confirmation authorizes one execution|exact full command and scope|manual CI rerun|full-test execution' \
  SKILL.md references templates README.md Usage.md AGENTS.md docs/maintenance
```

实际结果：`exit 1`，`0 matches`。

## 现行冲突

- `SKILL.md` 把明确安全的一次性编辑仅视为 Lightweight Change Assessment 输入，并要求普通非 Bug 修改先建立持久 Change card。
- `references/runtime.md` 同样只允许 Feature 或持久 Lightweight Change，没有位于 Lightweight 之下的零产物 Direct Edit 方法。
- 现行维护者与用户运行契约没有完整表达“一次确认仅授权一次具体全量执行”、HEAD/input/environment 变化导致过期、Push 自动 CI 不应本地重复、手动 CI rerun 需要重新确认。

## Focused Contract RED

新增 `tests/validate-direct-edit-fast-path.sh` 后、任何 production/runtime 文件修改前执行：

```bash
bash tests/validate-direct-edit-fast-path.sh
```

实际结果：

```text
FAIL: missing required file: references/direct-edit-fast-path.md
exit=1
```

失败原因与目标能力精确匹配：新 contract 首先要求独立 owner reference，而该 owner 在基线中尚不存在。随后才开始修改 `SKILL.md`、`references/`、template、human docs 与版本面。

## 结论

RED 基线成立：既有相关能力保持 GREEN，而新提案的两个核心契约在任何运行规则、模板、版本或 production 实现修改前均真实缺失；focused contract 也因独立 owner 缺失按预期失败。该证据允许进入最小 GREEN 实现，但不代表全量验证或发布完成。
