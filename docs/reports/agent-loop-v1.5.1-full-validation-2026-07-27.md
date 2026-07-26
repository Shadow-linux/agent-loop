# Agent Loop v1.5.1 全量验证报告

日期：2026-07-27
分支：`v1.5.1`
版本：`1.5.1`
审计对象：基线提交 `32a1d2ae94071e39966c48ff2feec28abdc34b3c` 之上的当前工作区正式修复
功能：Gate 2 Stable Digest Projection 与 Checker Upstream Issue Reporting

## 总结

| 项目 | 结果 |
|---|---|
| 总分 | **99/100** |
| 等级 | **STRONG** |
| Critical / High / Medium | **0 / 0 / 0** |
| Focused Feature Review | **27 / 27 PASS** |
| 全部 Shell 契约 | **45 / 45 PASS** |
| 全部 Python 测试 | **335 / 335 PASS** |
| 机械检查 | **全部 PASS** |
| Root managed blocks | **13 个；`1.5.1-20260727.1`** |
| GitHub Issue | [#9 Gate 2 Stable Digest 对合法任务运行态更新产生误报](https://github.com/Shadow-linux/agent-loop/issues/9) |

结论：原先的 Gate 2 逻辑冲突已由版本化、白名单、fail-closed 的 Stable Definition Digest 修复。任务和测试的精确运行态字段可更新，任务/测试定义、Human Gate、Acceptance、Verification、命令、断言、风险、接口和回滚仍受摘要保护。当前达到稳定版发布候选条件。

## RED 基线

修复前先运行既有 focused checker：

```text
python3 tests/test_feature_review.py
Ran 16 tests
OK
```

这证明旧测试没有覆盖真实缺口。随后新增 v2 契约但不修改生产代码：

```text
python3 tests/test_feature_review.py
Ran 25 tests
FAILED (failures=7)
```

7 个真实 RED：

- 根 `tasks.md` 完成 T001 后轮转到 T002；
- task detail 的 Task Done Gate 运行态更新；
- 根 `tests.md` 的 Design Slice / Bug 结果更新；
- test detail 的运行态状态更新；
- 缺失 Stable Digest Algorithm 未 fail closed；
- 未知 Stable Digest Algorithm 未 fail closed；
- `digest` 只读模式不存在。

目标项目的 canonical checker 复现两次均返回：

```text
FAIL: Gate 2 Stable Digest does not match current stable artifacts
```

仅回退 T001 checkbox、Status、Review、Drift 后，重算原始 Stable Digest 与保存值完全一致：

```text
sha256:89886dad8b1e140dc0b4d6167b0a1b9c0e27ce7b1d043ad8cafe9b16373ebd66
```

完整 RED 证据见 [agent-loop-v1.5.1-gate2-stable-digest-red-baseline-2026-07-27.md](agent-loop-v1.5.1-gate2-stable-digest-red-baseline-2026-07-27.md)。

## GREEN 实现与证据

### 摘要语义

- `Gate 2 Package Digest` 保持 `raw-v1`，冻结完整原始审核包。
- 新 Stable evidence 必须写 `Gate 2 Stable Digest Algorithm: review-definition-v2`。
- `tasks.md`、`tasks/*`、`tests.md`、`tests/*` 使用 section-aware definition projection。
- 只规范化发布契约中的 runtime ledger/result fields。
- 定义文件和所有非白名单内容继续按真实内容参与摘要。
- 缺失/未知算法、重复任务/运行态字段、畸形识别表格、非 UTF-8 投影输入均 fail closed。
- 显式 `raw-v1` 仅作 legacy reader；不自动迁移、不覆盖基线、不提供 force/bypass。
- `--mode digest` 与 `review | start | execute` 复用同一实现且不写文件。

### 防弱化压力

新增负向用例证明下列变化仍被拒绝：

- Task ID、顺序/标题、Story mapping、Mode；
- dependency、Human Gate、Acceptance、Verification；
- Test command、assertion 和普通定义文本；
- 重复运行态字段与 malformed result matrix；
- 缺失/未知算法。

### 真实目标副本

对真实失败 Feature 做隔离副本，添加已设计的 v2 migration evidence，运行：

```text
python3 scripts/check-feature-review.py --mode digest <temporary-feature-copy>
python3 scripts/check-feature-review.py --mode execute <temporary-feature-copy>
```

结果：

```text
Gate 2 Stable Digest Algorithm: review-definition-v2
Gate 2 Stable Digest: sha256:65ac0b61f746ffd6480217f6254833dc0b7b5dcaefa9d018bfeb0b9bf3539ac8
PASS: Feature review evidence is valid for mode=execute
```

真实目标目录前后树摘要均为：

```text
f28765d7833fa1f62f1388857e8bc17cc2d815977a217b9da8c611b4c61c4feb
```

因此本次源码验证没有修改目标项目 `.agent-loop/` artifact。

## 测试结果

### Focused

```text
python3 tests/test_feature_review.py
Ran 27 tests in 1.584s
OK
```

同时通过：

```text
bash tests/validate-feature-construction-two-gate-review.sh
bash tests/validate-checker-self-repair.sh
bash tests/validate-complex-artifact-thresholds.sh
python3 -m unittest tests.test_python_checker_contract
```

### 全量 Shell

第一次基线：`44 / 45 PASS`。唯一失败为 `tests/validate-complex-artifact-thresholds.sh` 仍查找已经被更强精确 stop rule 取代的旧字面文本；runtime 当前规则未缺失。

仅删除该陈旧字面断言，保留并继续断言：

```text
Complex Artifact Mode detail directories (`tasks/`, `tests/`, `plans/`) would be created or the feature would switch from simple to complex artifact mode
```

最终重新实时统计并运行：

```text
for test_script in tests/*.sh; do bash "$test_script"; done
TOTAL=45 PASS=45 FAIL=0
```

### 全量 Python

```text
python3 -m unittest discover -s tests -p 'test_*.py' -v
Ran 335 tests in 65.558s
OK
```

### 机械检查

| 检查 | 结果 |
|---|---|
| `SKILL.md` YAML | PASS |
| JSON parse | 3 / 3 PASS |
| Shell syntax | 46 / 46 PASS |
| Ruby syntax | 5 / 5 PASS |
| Python AST syntax | 47 / 47 PASS |
| Markdown fence | 295 / 295 PASS |
| `git diff --check` | PASS |

## 六域语义审计

| 审计域 | 分数 | 结果 | 已确认不变量 |
|---|---:|---|---|
| Logic Correctness | 100 | PASS | Raw Package 与 Stable Definition 职责分离；合法 runtime delta 与 definition drift 不再冲突；算法/migration fail closed。 |
| Autonomy | 99 | PASS | Agent 可只读计算 digest、诊断 checker、准备 Issue Draft；写 repair、提交 Issue、替代 Gate 保持独立确认。 |
| Project Entry / Evidence Graph + DDD Onboarding | 99 | PASS | 未改变入口、Onboarding、Requirement/Product/ADR 权威关系；root 仍为 16 个 First-Hop Gateway、13 个 managed blocks。 |
| Development / Test Workflow | 100 | PASS | TDD RED/GREEN、Gate 2、Plan rotation、Task Done、Verify/Review/Drift 闭环一致。 |
| Memory | 99 | PASS | 只更新既有 Feature notes/tasks/tests 证据，不新增 artifact family；legacy migration 需 Human Review。 |
| Recommendation | 99 | PASS | 失败时给出 algorithm/migration/repair/issue 单一下一动作，且 no-auth 返回草稿与 blocker。 |

加权结论取整为 **99/100**。

## 关键跨文件不变量

- `SKILL.md` 保持简洁入口；详细算法由 runtime/artifact rules/stage guides 承载。
- 未新增 canonical stage、message intent、lifecycle status、Auto Mode 或 artifact family。
- Gate 1 / Gate 2 两段式 Feature construction 未改变。
- Delivery Contract、subagent、External Mutation、Git、Submit、Close、Release 等 Human Gate 未削弱。
- Package Digest 仍为 raw；Stable v2 不能掩盖产品/实施定义变化。
- Checker repair、installed Skill mutation、one-Gate substitute、Issue creation、Git/release/install/sync 均相互独立。
- Issue body 已脱敏，不含 private absolute path、客户/私有仓库/主机、凭据或业务 payload。
- Root `AGENTS.md` 模板保持 176 行、13 个 managed blocks，revision 统一为 `1.5.1-20260727.1`。
- Skill/version metadata 继续统一为 `1.5.1`。

## 当前问题与剩余风险

当前未发现 Critical、High 或 Medium 问题。

剩余发布注意项：

- `raw-v1` 旧 Feature 若已经出现摘要 mismatch，不能自动迁移；必须以保留证据证明 exact runtime-only delta 并经 Human Review。这是设计的安全边界，不是未修复缺陷。
- 本机完成 macOS 验证；Windows 由 Python 3.10+ 标准库、BOM/路径契约和现有跨平台 workflow 定义覆盖，本轮未取得新的远程 Windows runner 结果。
- GitHub Issue #9 保持 open，关闭属于后续独立外部动作。

## 未采纳或降级意见

- 未采用从 Stable Files 删除整个 `tasks.md`：会失去任务定义漂移保护。
- 未采用全局删除 Status/Review/Drift 行：容易被语义走私绕过。
- 未采用更新一次 Stable Digest 的方式：下一任务完成会再次冲突。
- 未采用 force/bypass 或自动 migration：会绕过 Gate 2 Human Review。
- 未让临时修复自动创建 GitHub Issue：外部 mutation 必须单独确认。

## 发布与工作区边界

人类已授权本轮修复完成后执行 `commit`、push 当前 `v1.5.1`、创建并 push `stable-v1.5.1`、同步全局 Codex Skill。

以下预存工作区内容不属于本轮实现，不应被暂存或提交：

- `AGENTS.md` 的既有一行修改；
- `.tmp/`；
- `scripts/__pycache__/`；
- `tests/__pycache__/`。

`main` 同步及其他 remotes 未获授权，保持不变。
