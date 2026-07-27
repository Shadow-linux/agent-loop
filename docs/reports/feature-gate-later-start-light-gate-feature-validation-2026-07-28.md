# Feature Gate Later Start 轻量化专项验证报告

## 结论

- 日期：2026-07-28
- 分支：`v1.5.2`
- HEAD：`9a5c5183b47c022e8851f1098697f902e9d38daa`
- 审计对象：当前 dirty working tree
- 总分：**97 / 100 — STRONG**
- 严重度：Critical `0`、High `0`、Medium `0`、Low `0`
- 子 Agent A：生命周期混沌 **96 / 100**，59 / 59 符合预期
- 子 Agent B：授权与变异混沌 **98 / 100**，21 / 21 mutation caught，0 survived

本轮将 Feature Gate 保持为轻量 Human Review：不恢复本地 Feature Gate Checker、digest、Stable Digest、`EVIDENCE_*` 或 preflight。Agent 负责读取当前事实、判断语义和授权证据；自动测试只保护少数确定性工作流契约。

## 修复范围

1. Gate 2 的 `package-only` 保持为原始评审基线，不执行目标实现。
2. 人类稍后明确要求开始时，Agent 重新读取当前 Feature Context、package 与边界；检查通过后记录独立 Later Start transition。
3. Later Start 使用 `Later Start Decision`、`Later Start Authorized At`、`Later Start Evidence`，不改写 Gate 2 decision/Auto-Loop/time。
4. live execution mode 只更新当前 project `Gate Mode`。
5. 旧 notes 缺少 Later Start 字段时仍可读取，但字段缺失不授予执行权限。
6. 删除没有持久化落点的 Gate 1 `Spec SHA-256` 要求，保留 Agent 的 Feature 定义语义核对。
7. root Gate Modes 投影 valid separate later-start，并保留 package-only Gate 2 baseline。
8. root managed block revision 统一为 `1.5.2-20260728`。

## RED → GREEN

修复前证据见 `docs/reports/agent-loop-v1.5.2-later-start-light-gate-red-2026-07-28.md`：

- 修复前全量基线：Shell 45 / 45、Python 312 / 312；证明旧测试没有覆盖真实语义缺口。
- focused RED：Python 8 项中 2 项按预期失败；Shell 因缺少 Later Start durable fields 按预期失败。
- root 投影补充 RED：Python 和 Shell 均因 `templates/root-AGENTS.md` 缺少 valid separate later-start 而失败。

修复后：

- `tests.test_feature_review`：13 / 13 PASS。
- `validate-feature-construction-two-gate-review.sh`：PASS。
- root block/lossless Python contract：14 / 14 PASS。
- root block checker、refresh、stage coverage：PASS。

## 独立混沌测试

### 生命周期 Agent

- 55 / 55 正向场景 PASS。
- 4 / 4 负控成功转 RED。
- 覆盖 Gate 1 → Gate 2、package-only → later-start、Pause/Resume、context loss、Plan/No-Plan、任务新增/减少/全部替换、漏文件、验证失败、Contract/subagent/Git/Submit/Close/release 独立 Gate。
- 评分：96 / 100；当前 finding 为 0。

### 授权与变异 Agent

- 21 / 21 mutations caught，0 survived。
- 覆盖相反 accepted 规则、package-only 偷跑、Later Start 改写 Gate 2、删除 Later Start 三字段、恢复 checker/preflight/digest、legacy 误授权、删除独立 Human Gates、恢复 Gate 1 SHA、删除 root Later Start、删除 project Gate Mode。
- 评分：98 / 100；当前 finding 为 0。

四个关键 mutation 均同时被 Python 与 Shell focused contracts 拒绝：

| Mutation | Python | Shell |
|---|---:|---:|
| package-only 直接执行 | RED | RED |
| Later Start 改写 Gate 2 baseline | RED | RED |
| root Gate Modes 删除 later-start | RED | RED |
| project.md 删除 Gate Mode owner | RED | RED |

## 五域评分

| Domain | 得分 | 结论 |
|---|---:|---|
| Requirement And Scope Fidelity | 15 / 15 | 保持两次 Human Review，未恢复 checker 或新增 Gate |
| Logic, State, And Human Gates | 30 / 30 | Gate 2 baseline、Later Start event 与 live Gate Mode 职责分离 |
| Cross-Surface Consistency | 20 / 20 | runtime、design、guidance、模板、场景和 focused tests 同步 |
| Pressure Resistance | 24 / 25 | 80 个独立场景/mutation 全符合预期；有限样本不声称穷举 |
| Evidence And Maintainability | 8 / 10 | RED/GREEN、双 Agent 和全量证据齐全；语义判断仍由 Agent 承担 |
| **总分** | **97 / 100** | **STRONG** |

## 剩余风险

没有当前 Critical、High、Medium 或 Low finding。非缺陷边界如下：

- mutation 是有限样本，不能证明所有未来自然语言改写都可被自动捕获；这是刻意保留的轻 checker 边界。
- Agent 仍需判断 package 是否完整、Human evidence 是否可靠、变化是否处于 accepted boundary；脚本不签发授权。
- Python 与 Shell focused suites 必须组合运行，不能只选其中一套作为完整专项证据。

## 发布边界

专项质量已超过 90 分，可进入 Human Review。当前未执行 stage、commit、push、tag、PR、merge、release 或 publish。
