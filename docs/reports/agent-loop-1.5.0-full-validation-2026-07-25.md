# Agent Loop 1.5.0 全量验证报告 — 2026-07-25

## 1. 审计范围

| 项目 | 值 |
|---|---|
| 日期 | 2026-07-25 |
| 分支 | `alpha/v1.5.0` |
| 基线 HEAD | `93ce4e784c12698020d6ad15c2600e9fea88cd10` |
| 审计对象 | 当前工作区 |
| Skill 版本 | `1.5.0`，本轮未获授权升级 |
| 主要能力 | Checker Self-Repair / Temporary Recovery |
| 同批已存在修复 | ADR Product Rule Trace 对 Product-Rules-only Standard source 的 `none` 兼容 |
| Root guidance revision | `1.5.0-20260725.1` |
| Root template 行数 | 174，低于 190 行上限 |

本报告审计当前运行权威、root Gateway、阶段指导、Human Gate、Usage、压力场景、Checker 修复和对应测试。未跟踪的 `.tmp/`、`scripts/__pycache__/`、`tests/__pycache__/` 是既有工作区内容，不属于本轮修改，也未作为验证证据。未跟踪的 `feature-construction-two-gate-review.md` 是另一项已确认但尚未实施的 Proposal，不属于本能力的 GREEN 结论。

## 2. 结论

**总分：99/100 — STRONG**

| 结论项 | 结果 |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 个阻断问题；1 个运行观察边界 |
| Shell contract tests | 43/43 PASS |
| Python unit tests | 283/283 PASS |
| 发布判断 | 能力逻辑闭环；尚未授权 version bump、commit、push、tag、release 或 publish |

Checker Self-Repair 已形成可执行闭环：

```text
Canonical failure
-> exact rerun and evidence preservation
-> artifact / environment / checker / unresolved classification
-> minimal authority-backed fixture
-> Temporary Checker Repair Review
-> exact Human patch authorization
-> isolated RED / GREEN / negative controls
-> exact target run
-> separate one-Gate substitute decision
-> expiry + residual canonical failure
-> formal Agent Loop source repair
```

它允许 Agent 在不伪造 canonical pass 的前提下临时自救，也阻止 Agent 静默修改全局 Skill、弱化验证、跨 Gate 复用授权或用临时副本给 Agent Loop 自身发布背书。

## 3. 六域评分

| 审计域 | 分数 | 结果 | 主要证据 |
|---|---:|---|---|
| Logic Correctness | 99 | PASS | 四类诊断、双重 Human decision、one-Gate expiry、canonical residual、正式修复边界一致 |
| Autonomy | 99 | PASS | Agent 先重跑、缩小 fixture、核对权威和负例；只在首次写补丁和采用 substitute evidence 时请求人类 |
| Project Entry / Evidence Graph + DDD Onboarding | 98 | PASS | root Gateway 新增一个 first hop，完整算法保留在 reference；未污染 Onboarding 或项目记忆模型 |
| Development / Test Workflow | 100 | PASS | focused RED 真实失败；GREEN、43 Shell、283 Python、root drift/checker tests 全部通过 |
| Memory | 99 | PASS | 同会话允许 response-local；跨会话只写现有 owner；无强制新目录、状态或 backlog |
| Recommendation | 99 | PASS | artifact/environment/checker/unresolved 各有唯一下一动作；临时和正式修复责任清晰 |

加权结果为 99。没有未解释 High 或 Critical，因此可判定 `STRONG`。

## 4. RED 基线

新增 `tests/validate-checker-self-repair.sh` 后，在实现任何运行权威前执行：

```text
FAIL: SKILL.md missing required text: references/checker-recovery.md
exit_code=1
```

失败原因正确：技能入口、运行参考、root routing、Human 使用说明和压力场景均尚不存在。该 RED 不是语法错误或错误 fixture。

同批 ADR Checker 修复保留了先前真实 RED：

```text
invalid values in ADR Accepted Concept IDs: none
```

其回归测试同时覆盖 Product-Rules-only Standard source 的正例，以及源实际声明 Concept / Requirement Model IDs 时 `none` 不能隐藏覆盖的反例。

## 5. GREEN 结果

### 5.1 Focused contract

```bash
bash tests/validate-checker-self-repair.sh
```

结果：

```text
PASS: checker self-repair classification, isolation, evidence, one-gate authorization, and formal-repair contract is complete
```

### 5.2 Root guidance focused regression

执行：

```bash
python3 -m unittest tests.test_root_agents_blocks tests.test_root_agents_lossless_slimming
bash tests/validate-root-agents-block-checker.sh
bash tests/validate-root-agents-block-refresh.sh
bash tests/validate-v1.2.4-root-stage-coverage.sh
```

结果：

- 14 个 root Python tests PASS；
- root managed-block checker PASS；
- root refresh contract PASS；
- 6 个 Gateway/runtime leaf coverage tests PASS；
- root template 174 行。

### 5.3 全部 Shell contracts

执行：

```bash
for test_file in tests/*.sh; do bash "$test_file"; done
```

结果：43/43 脚本退出码为 0。

### 5.4 全部 Python tests

执行：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'
```

结果：

```text
Ran 283 tests in 80.648s
OK
```

### 5.5 结构与语法检查

以下检查全部退出 0：

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
python3 -m json.tool plugin.json
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
# 对全部 changed/untracked Markdown 执行 fence balance
git diff --check
```

新增 Checker Self-Repair 文件也通过 trailing-whitespace 检查；Proposal metadata 中发现的 3 处 Markdown hard-break 空格已清除后复验。

## 6. 语义压力场景

| 场景 | 结果 | 关键不变量 |
|---|---|---|
| 合法 artifact 被 Checker 拒绝 | PASS | 先证明 checker defect；不改正确 artifact |
| 非法 artifact 试图甩锅 Checker | PASS | `artifact-invalid` 返回 owner workflow |
| Python/import/path 能力错误 | PASS | `environment-invalid`，不改验证逻辑 |
| 补丁让合法和非法 fixture 都通过 | PASS | negative control 失败即禁止 substitute |
| isolated 授权被扩成全局 Skill 写入 | PASS | 必须第二个 exact in-place authorization |
| 短同会话恢复 | PASS | response-local，禁止为小事创建新目录 |
| 跨会话或 Submit 依赖 | PASS | compact evidence 写现有 owner，保留 residual |
| checker/target/command/Gate digest 改变 | PASS | 旧授权失效 |
| Agent Loop 源码发布用临时副本自证 | PASS | 发布继续阻断，必须 canonical source GREEN |
| 人类只授权补丁但未授权 substitute | PASS | patch result 不能自动清 Gate |
| substitute 已接受但进入后续 Git/Release | PASS | 所有 action-specific Gates 独立且显示 residual |

## 7. 通过的跨文件不变量

1. `references/design.md` 与 `references/runtime.md` 同时拥有核心约束和可执行顺序。
2. `references/checker-recovery.md` 拥有详细算法；root `AGENTS.md` 只增加一个 first-hop row 和一句 Evidence Gate 提醒。
3. Checker Self-Repair 不是 canonical stage、status、lifecycle、Auto Mode 或新 artifact family。
4. 诊断读操作先行，减少了不必要 Human 停顿。
5. 首次 patch write 和采用 one-Gate substitute 是两个不同决策。
6. 默认只改 isolated temporary copy；installed/global mutation 需要额外 exact authorization。
7. RED、GREEN 和 negative controls 均为必要证据。
8. canonical result 始终保持 failed，temporary result 不能被改写成 canonical pass。
9. same-session 不创建文件；跨会话只使用既有 owner。
10. 正式源修复、full validation、commit、push、tag、release、publish、安装更新互不继承权限。
11. ADR Product Rule compatibility 不允许 `none` 隐藏源实际声明的 IDs。
12. Root Gateway 为 17 个 exact first-hop families，managed block revision 同步为 `1.5.0-20260725.1`。

## 8. 未采纳或降级的方案

| 方案 | 处理 | 原因 |
|---|---|---|
| canonical failure 永远等待上游发布 | 未采用为唯一路径 | 会阻断已经可证明正确的目标项目 |
| Agent 静默修改全局 Skill | 拒绝 | 改变所有项目的裁判且难以回滚 |
| 加 `--force` / skip validation | 拒绝 | 不能证明当前 artifact，且会扩大绕过面 |
| 自动创建 `.agent-loop/checker-recovery/` | 拒绝 | 短恢复不需要新文件或生命周期 |
| patch 授权自动等于 Gate 通过 | 拒绝 | 写裁判和采用 substitute 是两个不同 Human decisions |
| temporary pass 等于 canonical pass | 拒绝 | 会伪造验证事实 |

## 9. 当前问题和剩余风险

没有当前 Critical、High、Medium 或可执行 Low 缺陷。

唯一观察边界是：该能力是自然语言 Agent workflow contract，不同 CLI Agent 是否每次都能完整保留 digest、负例、失效条件和双结果，需要在真实目标项目首次使用时继续观察。现有 root/runtime/checklist/scenario regression 已把省略这些步骤判为违规；这不是当前逻辑缺口。

## 10. Drift 与 Git Gate

- Skill version 仍为 `1.5.0`；未获得 version bump 授权。
- 当前正式 `v1.5.0` 已属于 sealed release；后续发布归属需要人类单独决定 patch 或新版本。
- 本轮未 stage、未 commit、未 push、未 tag、未创建 PR、未 merge、未 release、未 publish。
- `.tmp/` 和两个 `__pycache__/` 目录未修改、未删除，也不应进入未来提交。
- 下一步应先完成当前工作区最终结构检查和 Human Review；Git 动作仍需独立授权。
