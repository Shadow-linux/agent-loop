# Agent Loop v1.5.2 全量验证报告（移除 Feature Gate Checker）

## 结论

- 日期：2026-07-27
- 分支：`v1.5.2`
- HEAD：`9a5c5183b47c022e8851f1098697f902e9d38daa`
- Skill 版本：`1.5.2`，本轮未升级
- 审计对象：上述 HEAD 之上的当前 dirty working tree
- 范围：移除 Feature Gate 本地 Checker、digest 字段和 `MATCH / CHANGED / INVALID` 路由；保留两个 Feature Human Gate、Agent 直接语义审查及所有独立 Human Gate
- 评分：**99 / 100 — STRONG**
- 当前严重问题：Critical `0`、High `0`、Medium `0`
- 验证结果：focused `24 / 24` Python + `1 / 1` Shell；全量 `312 / 312` Python + `45 / 45` Shell
- 发布判断：可进入 Human Review；本报告不授权 commit、push、tag、PR、merge、release、publish 或 installed Skill 同步

## 审计边界与工作区保护

这是 Agent Loop Skill 源码仓库维护，不是目标项目运行。本轮没有创建仓库根目录 `.agent-loop/`。

工作区在本轮开始前已有大量已批准但未提交的修改和未跟踪报告。Feature Gate Checker 移除只协调其直接运行权威、模板、用户文档和回归测试；没有恢复、删除、暂存或提交其他 dirty work。报告创建前工作区统计为 43 个 tracked changes、17 个 untracked entries、1 个 tracked deletion；本报告新增后 untracked entries 增加 1。`git diff --stat` 为 43 files changed、524 insertions、1386 deletions，其中包含本轮开始前既有改动，不能全部归因于本轮。

## 本轮实际修改

### 运行权威与人类文档

- `SKILL.md`
- `references/runtime.md`
- `references/design.md`
- `references/artifact-rules.md`
- `references/checker-recovery.md`
- `references/concepts.md`
- `references/document-templates.md`
- `references/human-review-summary.md`
- `references/implementation-planning.md`
- `references/project-guidance.md`
- `references/stage-guides.md`
- `references/validation-scenarios.md`
- `references/workflow-checklists.md`
- `README.md`
- `Usage.md`
- `CHANGELOG.md`

### 下游模板

- `templates/notes.md`
- `templates/root-AGENTS.md`
- `templates/task-detail.md`
- `templates/tasks.md`
- `templates/test-case.md`
- `templates/tests.md`

### Checker 与测试

- 删除 `scripts/check-feature-review.py`
- 重构 `tests/test_feature_review.py`
- 更新 `tests/test_python_checker_contract.py`
- 重构 `tests/validate-feature-construction-two-gate-review.sh`
- 新增 `docs/reports/agent-loop-v1.5.2-feature-checker-removal-red-2026-07-27.md`
- 新增本报告

未删除 `scripts/check-feature-context.py` 或其他独立结构/新鲜度 Checker。历史 Proposal、历史验证报告和 `CHANGELOG.md` 的旧版本章节仍可如实记载已废止机制，但当前 `SKILL.md`、`README.md`、`Usage.md`、`references/`、`templates/`、`scripts/` 和 root guidance 不再把 Feature Gate Checker 或 digest 当作运行要求。

## RED 基线

先把 `tests/test_feature_review.py` 改为移除契约，再修改运行规则：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_feature_review -v
```

真实结果：`Ran 5 tests`，出现 60 个失败 subtests。失败原因与目标缺口一致：

1. `scripts/check-feature-review.py` 仍存在；
2. 16 个当前运行 surface 仍引用 Checker、Gate digest、`EVIDENCE_*` 或 `review-definition-v2`；
3. 缺少 Agent-owned package review、只允许两个 approval choice 写入 accepted、revise/pause 状态和 later-start 直接复核契约。

完整 RED 证据：`docs/reports/agent-loop-v1.5.2-feature-checker-removal-red-2026-07-27.md`。

## GREEN 实现与 focused validation

实现后的 focused 命令：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_feature_review \
  tests.test_python_checker_contract -v
bash tests/validate-feature-construction-two-gate-review.sh
```

结果：

- Python：`Ran 24 tests`，`OK`
- Shell：`PASS: Feature construction keeps two Human reviews and Agent-owned package/drift checks without a local Feature Gate checker`

新增/重构回归契约证明：

1. Feature Gate Checker 文件不存在；
2. 当前运行权威没有 Checker/digest 路由残留；
3. Gate 1 仍只授权准备实施包，Gate 2 才能接受或开工；
4. 只有 `Approve package only` 和 `Approve package and start implementation` 写入 `Implementation Readiness: accepted`；
5. `Revise package` 返回 `preparing`，`Pause` 不伪造 accepted；
6. package-only 后续开工由 Agent 重读 Package Files、当前 Feature artifacts、Human instruction、边界和 stop conditions，不调用本地 Feature Gate preflight；
7. 新 Task ID 不因 ID 变化本身重复 Gate 2，但新 Story/Product Slice/Acceptance 或 execution boundary 仍返回拥有它的 Human Gate；
8. Delivery Contract、Human-gated Task、subagent、Git、external mutation、Submit、Close、Release 等 Gate 不被 Feature Gate 接受继承。

## 全量可执行验证

### Shell

实时枚举 `tests/*.sh` 后逐个运行：

```bash
for test in tests/*.sh; do bash "$test"; done
```

结果：**45 / 45 PASS，0 FAIL**。

第一次全量运行发现 `tests/validate-v1.2.4-postfix-pressure-repairs.sh` 依赖一条仍有效的精确用户说明句。修复 `SKILL.md` 的等价措辞以恢复该兼容契约后，重新完整运行 45 个 Shell 测试，全部通过；没有放宽或删除测试。

### Python

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -v
```

结果：**Ran 312 tests in 104.016s — OK**。

一次测试包装命令曾因 zsh 的只读变量名 `status` 导致外层退出 1，但同次 unittest 已显示 `312 tests — OK`。随后去掉该包装错误并从头重跑，unittest 与外层命令均以 0 退出；报告采用第二次干净结果。

## 机械检查

| 检查 | 命令/范围 | 结果 |
|---|---|---|
| SKILL YAML | `ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'` | PASS |
| JSON | Ruby `JSON.parse` 读取 `plugin.json` | PASS |
| Shell syntax | `find . -name '*.sh' -type f -print0 \| xargs -0 -n1 bash -n` | 46 files，PASS |
| Python syntax | `ast.parse` 读取全部 46 个 Python source | PASS |
| Markdown fence | 扫描仓库全部 Markdown，匹配 backtick/tilde fence | PASS |
| Diff whitespace | `git diff --check` | PASS |
| Root managed blocks | `templates/root-AGENTS.md` | 13 blocks，176 行，PASS |
| Active mechanic residue | 当前运行权威搜索 Checker/digest/`EVIDENCE_*` | 0 |
| Target workspace | 仓库根目录 `.agent-loop/` | 不存在 |

## 六域语义审计

| 审计域 | 结果 | 分数 | 通过的不变量 |
|---|---|---:|---|
| Logic Correctness | PASS | 98 | 两个 Feature Gate 状态迁移唯一；approval/revise/pause 无冲突；later-start 与 drift 路由唯一；无本地脚本成为授权发行者 |
| Autonomy | PASS | 100 | Agent 直接检查完整 Package、当前 artifacts、Human provenance、Task/Story/Plan/No-Plan、risk/rollback/verification 和边界变化 |
| Project Entry / Evidence Graph + DDD Onboarding | PASS | 100 | Feature Context 新鲜度 Checker 保留；Requirement/Product/ADR 权威链和 Project Entry 没有被 Feature Gate 变更改写 |
| Development / Test Workflow | PASS | 99 | Plan Gate、TDD、Analyze Consistency、Task Done、Review、Drift、Memory、Completion 与 Follow-up 保持；完整回归通过 |
| Memory | PASS | 100 | Gate 决策对与 `Accepted Stories` 保持 durable evidence；Pause/Resume 和 Active Feature 记忆规则不借摘要字段推断授权 |
| Recommendation | PASS | 100 | 缺证据或语义 unresolved 时只问一个真实阻塞问题；范围内变化继续，定义/执行边界变化返回对应 Gate |

加权结果按整数报告为 **99 / 100，STRONG**。扣分不是当前 Medium 缺陷，而是取消确定性摘要后，Feature 边界判断明确依赖 Agent 对当前 artifacts 的语义复核；这是本轮人类确认的轻量化取舍，不能被机械测试证明为产品语义完整。

## 压力场景与跨文件不变量

本轮重新核对并由现有 Shell/Python suite 覆盖以下主路径：

1. 复杂 Requirement -> Standard Product Definition -> Decision Scan -> ADR -> Feature Product Slice；
2. 简单 Requirement -> Brief Product Definition -> 无 ADR Feature Product Slice；
3. Requirement Product ownership、Product Human Review、Feature Product Slice Gate；
4. Gate 1 只准备 package，Gate 2 package-only 或 approve-and-start；
5. package-only 跨会话 later-start；
6. accepted Story 内 Task 新增、减少、替换及 Plan rotation；
7. 新 Story/Acceptance、Human-gated Task、risk/rollback/interface/verification boundary 变化；
8. Delivery Contract Human Gate；
9. TDD RED 与非行为变更 `N/A`；
10. Active Feature、Pause、Resume、Close、Reopen；
11. 多 Phase Requirement 的 lifecycle 汇总；
12. accepted ADR drift、Follow-up investigate-first；
13. Submit / Integrate blocker、验证和 Git Human Gate；
14. stale memory、root guidance、Project Entry；
15. 普通 Chat 不创建 workflow artifacts。

关键结论：Feature Gate Checker 的移除没有移除任何 Human Gate，也没有让 Feature Gate 继承 Git、外部操作、Contract、Submit、Pause、Close 或 Release 权限。旧 Feature 中遗留的 hash 字段允许作为 inert history 保留，但 Agent 不刷新、不依赖、也不据此授权或阻断。

## 当前问题、残余风险与未采纳方案

### 当前问题

- Critical：无
- High：无
- Medium：无

### 残余风险

1. 不再有本地 digest 变化探测后，Agent 必须认真重读当前 artifact；弱模型或未完整加载运行规则时可能漏判语义漂移。这是主动选择的低复杂度设计边界，不应再通过扩充 Markdown Checker 修复。
2. 历史 Proposal、历史报告和 1.5.1 Changelog 仍描述当时存在的 Checker。它们是历史证据，不是当前 runtime authority；删除会破坏审计链，因此保留。
3. 当前工作区仍包含本轮开始前的其他 dirty work，维护者提交时必须按实际归属复核，不应把 `git diff` 的全部文件自动归因于本轮。

### 未采纳

- 未保留“只做 Stable Digest”的单职责 Feature Gate Checker：它仍会把正常字节变化变成脚本噪音，且不能证明 Human authorization 或产品语义。
- 未拆分为多个 Feature Gate Checker：拆分只会扩大触发面和恢复分支，不能解决 Markdown 语义与运行态变化的根本边界。
- 未让 Checker 只验证人类摘要：Human 决定的真实性和范围仍来自可靠会话/持久证据，不能由本地文件自签名。
- 未删除其他结构与新鲜度 Checker：它们保护不同的确定性边界，不属于本轮反复误报的 Feature Gate 机制。

## Human Review 判断

本轮已经满足“让 Feature Gate 轻量、避免正常流程被本地脚本误报阻断”的目标：Feature Gate Checker 已从代码和当前运行权威移除，两个 Human Review 与独立授权边界完整保留。建议维护者重点审阅 `references/runtime.md` 的 Gate 2/later-start 段、`templates/notes.md` 的持久字段，以及移除契约测试；确认后再决定是否提交。

截至报告写入时：**未 stage、未 commit、未 push、未 tag、未创建 PR、未 merge、未 release、未 publish、未同步 installed Skill。**
