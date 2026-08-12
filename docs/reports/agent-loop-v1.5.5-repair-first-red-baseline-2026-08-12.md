# Agent Loop v1.5.5 Repair-First RED Baseline

## 审计对象

- 日期：2026-08-12
- 分支：`v1.5.5`
- 基线 HEAD：`f9c5569d93f6e42457b12fa2925a95373bea0cb9`
- 设计权威：`docs/proposal/v1.5.x/repair-first-review-and-lightweight-change.md`
- 实施计划：`docs/proposal/v1.5.x/repair-first-review-and-lightweight-change-implementation-plan.md`
- 审计边界：当前工作区，在 runtime/design/reference/template 生产规则修改前建立 RED。

## 工作区边界

Task 0 复核结果与 planning baseline 一致：无 tracked diff，无 cached diff；仅存在已知未跟踪的 `.tmp/`、Proposal、Implementation Plan、`scripts/__pycache__/` 和 `tests/__pycache__/`。本轮不删除、恢复、暂存或提交这些路径。源码仓库中未创建目标项目 `.agent-loop/`。

## 既有全量基线

执行：

```bash
set -euo pipefail
shell_total=0
for test_file in tests/*.sh; do
  bash "$test_file"
  shell_total=$((shell_total + 1))
done
printf 'SHELL_PASS=%s\n' "$shell_total"

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -v
```

实际结果：

- Shell：`49/49` 通过，Shell loop 计时 `14s`。
- Python：发现并通过 `413/413` 个 test case；与 Shell 合并命令总 wall time 约 `24.7s`，Python 段约 `10.7s`。
- 新 focused contract 尚未加入上述既有基线计数。

既有机械基线同时通过：`SKILL.md` YAML、`plugin.json` JSON、全量 Shell 语法、全量 Python AST 和 `git diff --check`。

## Focused RED 命令与退出状态

命令：

```bash
bash tests/validate-repair-first-verification.sh
```

退出状态：`1`

首个失败：

```text
FAIL: references/runtime.md missing Repair-First contract: Repair-First Verification
```

该失败由缺失目标行为契约引起，不是 Shell 语法、帮助函数、版本值或无关 dirty work 导致。

## 当前错误路径

- `references/runtime.md:123` 仍对 Lightweight 可隔离行为逻辑强制 smallest meaningful RED/GREEN。
- `references/lightweight-change-lane.md:155-156` 仍规定 `targeted RED -> minimal GREEN`。
- `SKILL.md:263` 仍将 Lightweight isolated behavior 的 RED/GREEN 作为默认；`SKILL.md:341` 仍以全称句声明 `TDD is default`。
- `references/design.md:192` 和 `references/design.md:613` 仍把 isolated Lightweight behavior 定义为 smallest RED/GREEN。
- `references/runtime.md:843` 和 `SKILL.md:382` 的 stop 规则仍对所有路径使用未分范围的 `TDD cannot be followed`。
- 现有权威未定义 `Repair-First Verification`、`Review Repair Fast Path`、`Regression Test Advisory`，也未区分 `Required Verification`、`Existing Test Obligation` 和 `Additional Regression Test`。

因此下游 Agent 仍可能对 Review 边界内修复和 clearly eligible Lightweight Change 先制造 RED，或把当前结果必须验证与未来回归防护混为一项义务。

## Proposal 需要的 GREEN

GREEN 必须同时证明：

1. `within-approved-boundary` Review repair 在当前写授权内先修复，后执行 fresh targeted verification 和受影响的既有检查。
2. clearly eligible Lightweight Change 在持久 Card 存在后使用同一 Repair-First 顺序。
3. Existing Test Obligation 不得降级为 advisory；无可靠当前证明时不得声称 `fixed/done/completed/closed`。
4. Additional Regression Test 只在当前证明已存在后作为具体建议，未被采纳本身不阻止 Task Done、Lightweight completion 或 Feature Close。
5. 初始 Feature、明确 Bug、Human-requested TDD 和 accepted RED/GREEN Plan 仍保留 TDD。
6. Product/Requirement/ADR/Contract/Gate 1/2/Task Done/Submit/Close/Git/Release/Human Gates 均不变，不新增 stage、intent、status、mode、Gate、Checker outcome、artifact tree 或依赖。

## 未修改的生产文件

在首次 RED 运行前，未修改 `SKILL.md`、`references/runtime.md`、`references/design.md`、任何详细 runtime/reference、template、root guidance、human docs、metadata 或现有回归测试。当时新增的只有 focused contract，并且 Proposal/Plan 仅按已获得的 Human authorization 更新实施状态。

## 剩余风险

- 该 RED 是实施前证据，并不证明后续所有细分表面已对齐。
- 实施仍需验证 helper routing 不会恢复强制 TDD，且 completion 不会把既有测试义务误降为 advisory。
- 版本 `1.5.5` 与 root revision `1.5.5-20260812.1` 尚未同步；稳定安装渠道仍必须保持 `stable-v1.5.4` 直到独立 Release Gate。
- 本报告不声称已实施、已全量验证或已发布。

## GREEN 与 focused regression

以下证据在完成批准范围内的 runtime/reference/template/test/version 同步后产生；上面的原始 RED 命令、退出状态和首错输出保持不变。

### Primary focused GREEN

执行：

```bash
bash tests/validate-repair-first-verification.sh
bash tests/validate-lightweight-change-lane.sh
bash tests/validate-feature-construction-two-gate-review.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_feature_review \
  tests.test_lightweight_change_scan -v
```

实际结果：

- focused Shell：`3/3` 通过；新 contract 输出 `PASS: Repair-First Review Repair and Lightweight Change contract is complete`。
- Lightweight Shell 内嵌 scanner：`37/37` 通过。
- 显式 Python focused：`53/53` 通过，其中 Feature Review `16/16`、Lightweight scanner `37/37`。

### Route-boundary regression

执行：

```bash
bash tests/validate-bug-management.sh
bash tests/validate-feature-context-load-contract.sh
bash tests/validate-feature-brainstorming-trigger.sh
bash tests/validate-project-skill-discovery-guard.sh
bash tests/validate-project-local-skills.sh
bash tests/validate-branch-management-strategy.sh
bash tests/validate-maintainer-full-validation-guidance.sh
```

实际结果：`7/7` 个 Shell boundary regression 通过；Bug、Feature Context、Feature brainstorming、Project Skill discovery/local skill、Branch Management 与 maintainer full-validation 边界均未退化。

### Mutation 与确定性

执行两次：

```bash
bash tests/validate-repair-first-verification.sh
bash tests/validate-repair-first-verification.sh
```

两次均以相同 PASS summary 结束。focused contract 的内嵌 mutation 检查确认以下退化不能存活：移除 fresh verification、把 Regression Test Advisory 改为 silent completion、反转 repair/verification 顺序、恢复所有行为变更逐次确认、把 Task Done 或 Completion 的 Existing Test Obligation 降级为 advisory、丢失 Required/Existing/Additional 证据分离；同时继续拒绝把 Review Repair 添加为 Message Intent 或 canonical Stage。

### GREEN 行为摘要

- `within-approved-boundary` Review correction 与 clearly eligible Lightweight Change 现在先在既有授权内修实现，再用新鲜 targeted proof、受影响既有检查和 diff/scope/risk/rollback 复核证明当前结果。
- Existing Test Obligation 与 Required Verification 保持硬要求；Additional Regression Test 只作为包含 scenario、layer/location、prevented regression、residual risk 和 priority 的具体建议。
- 初始 Feature、显式 Bug、人类要求 TDD 或 accepted RED/GREEN Plan 继续 TDD；既有 Human Gates 和 artifact/status/stage/checker 边界未增加。
- 当前开发版本已同步为 `1.5.5`，13 个 root managed blocks 已同步为 `1.5.5-20260812.1`；稳定安装命令仍保持 `stable-v1.5.4`。

### GREEN 后剩余风险

- 本节只证明 focused 与 route-boundary GREEN；全量 Shell/Python、机械检查和六域语义审计仍需单独完成后才能声明最终验证完成。
- Regression Test Advisory 的具体质量仍由 Agent/Human Review 判断；本变更没有引入新的 test-debt lifecycle 或自动执行授权。
- 本报告不声称 commit、push、tag、PR、merge、release 或 publish 已发生。

## Post-GREEN Human Review Repair RED -> GREEN

独立 Human Review 在原始 GREEN 后识别出三个批准边界内缺陷。该审查没有改变 Proposal 语义；修复沿既有 Review Repair Fast Path 完成，原始实施前 RED 保持不变。

| 严重级别 | 修复前反例 | Root cause | Repair |
|---|---|---|---|
| High | `references/workflow-checklists.md` 要求所有改变 behavior 的 review-driven change 先问 Human，普通 `within-approved-boundary` correction 因而可能被重新阻塞。 | 旧 checklist 负向条款未随 Repair-First owner 同步收窄。 | 普通边界内实现修正明确无需新增 per-finding confirmation；只有 product/Feature/boundary/interface/ADR/Contract/security/data/permission/dependency/migration/architecture/authorization/rollback/reliable-verification 等 owner 改变才返回既有 Gate 或 Human confirmation。 |
| Medium | focused test 只验证正向关键词/顺序，Python mutation 依赖精确句子替换，无法拒绝额外逐次确认或 Existing obligation 被说成 advisory。 | 缺少 owning-section semantic predicate 与矛盾句 mutation。 | Shell/Python 使用同一语义合同，增加 universal-confirmation、Task Done/Completion Existing-advisory、Required/Existing/Additional separation mutations。 |
| Low | `references/project-guidance.md` 把 Lightweight owner 概括为 `Adaptive Plan/TDD`。 | current owner label 遗留旧默认。 | 改为 `Adaptive Plan/Repair-First Verification`，并由 repair-first/root-refresh tests 保护。 |

生产规则修复前，在已写入的新语义断言上运行：

```bash
bash tests/validate-repair-first-verification.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_feature_review.FeatureReviewContractTests.test_review_repair_fast_path_is_ordered_inside_existing_review -v
```

两条命令均真实失败：Shell 退出 `1` 并输出 `FAIL: Review checklist restores per-finding confirmation or loses fast-path exit owners`；Python 退出 `1` 并指出 `ordinary within-boundary behavior correction must not add per-finding confirmation`。

修复后，同一 Shell contract 通过，Feature Review `16/16` 通过。Repair-First mutation contract 连续运行两次均输出相同 PASS；相关 Feature Review、Lightweight、root guidance/refresh focused 批次共执行 `8` 次 Shell invocation（`7` 个唯一脚本）并全部通过，显式相关 Python `71/71` 通过。首次 GREEN 尝试还识别出 predicate 把“不得降级 Existing obligation”误判为 advisory 的测试自身误报；收窄为肯定式降级表达后，同一当前权威与全部负向 mutation 转绿。

随后全量重新执行：Shell `50/50`、Python `416/416`；六域语义复审和最终机械检查见配套 full-validation report。当前 Review finding 为 `0`；历史上发现并已解决 `High=1`、`Medium=1`、`Low=1`。Proposal/Plan 仍处于 awaiting final Human Review，未执行任何 Git 或发布动作。
