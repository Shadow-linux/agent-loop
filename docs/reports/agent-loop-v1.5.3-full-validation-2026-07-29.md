# Agent Loop v1.5.3 全量验证报告（2026-07-29）

## 1. 审计对象

- 仓库：Agent Loop Skill source repository
- 分支：`v1.5.3`
- 基线 HEAD：`6086d7d6fc758221af2dee41ea269d0acf237795`
- 审计对象：当前未提交工作区，包含此前已批准的 v1.5.3 修改，以及本轮 Light-Gate Authority Alias Repair
- 版本：`1.5.3`，未升级
- Root managed-block revision：`1.5.3-20260728.1`，本轮没有修改 root 模板正文，因此未制造新的 revision
- 平台：`macOS-verified / Windows-test-defined`

## 2. 结论

总分：`99.7 / 100`（STRONG）
当前严重问题：Critical `0`，High `0`，Medium `0`
剩余 Low：`1`（本地没有 Windows runner；使用 Python 3.10+ 标准库、POSIX/Windows 兼容路径合同和 CI 定义覆盖，尚无本轮 Windows 实机证据）

本轮修复满足已确认边界：Checker/Scanner 负责事实，Agent 负责语义和风险判断，人类只保留既有 exact-plan 或 root guidance 写入确认；执行器继续负责不可越过的物理边界。

## 3. RED → GREEN

### 既有基线

- Shell：`47 / 47`
- Python：`333 / 333`，`93.121s`

### Focused RED

七个新增合同最初为 `0 / 7`：

1. Feature entry symlink 被硬报 `path-escape`；
2. memory-root alias 计划泄漏 `.memory/...`；
3. Apply 未在 transaction 前拒绝变成 symlink 的 move source；
4. alias Apply 写后才因 locator 失败；
5. Feature Context 一律阻断安全内部 alias；
6. Lightweight Change 一律阻断安全内部 alias；
7. Agent Loop-owned root block 正文漂移仍被报告为 current。

详细证据见 [RED 报告](agent-loop-v1.5.3-light-gate-authority-alias-red-2026-07-29.md)。

### Focused GREEN

- Archive scan/apply/restore、Feature Context、Lightweight Change、root block checker：`127 / 127`
- 新增 alias rollback 单测：`1 / 1`
- 受影响 Shell 合同：root checker、root refresh、Archive soft gate、Feature Context、Lightweight Change、authority alias 全部通过
- 新增负向控制覆盖 broken/cyclic/external/dual/file root、alias retarget、Feature entry symlink、pre-transaction zero-write、rollback、project-owned body 与 marker/source path invalid

## 4. 最终全量执行结果

实际命令：

```bash
for test_file in tests/*.sh; do bash "$test_file"; done
python3 -m unittest discover -s tests -p 'test_*.py'
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
python3 -m json.tool plugin.json
find scripts tests -name '*.py' -type f -print0 | xargs -0 python3 -m py_compile
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
git diff --check
```

结果：

| 检查 | 结果 |
|---|---|
| Shell regression | PASS — `48 / 48` |
| Python regression | PASS — `344 / 344`，最终一次 `89.768s` |
| SKILL.md YAML | PASS |
| plugin.json JSON | PASS |
| Python syntax | PASS |
| Shell syntax | PASS |
| Markdown fence balance | PASS |
| git diff --check | PASS |

全量第一次运行出现 `4` 个失败，全部来自同一个旧一致性合同：四个 controller surface 必须保留“双根进入 Recovery”的精确句子。新设计没有取消该规则，因此恢复精确跨文件表述；随后重新执行完整 Shell/Python 全量并全部通过。这不是放宽测试。

## 5. 六域语义评分

| 审计域 | 权重 | 评分 | 结果 | 核心证据 |
|---|---:|---:|---|---|
| Logic Correctness | 20% | 100 | PASS | Feature symlink 不进 move；alias target/hash、preflight、journal、post-check、restore 顺序一致；root changed/invalid 不混淆 |
| Autonomy | 15% | 100 | PASS | Scanner 只提供事实；Agent 判断 coverage/conflict/risk/recovery；普通 finding 不触发 Checker Recovery |
| Project Entry / Evidence Graph + DDD Onboarding | 15% | 99 | PASS | 单一内部 alias 与双根/外部/断裂边界一致；Feature Context 共用 authority resolver；Windows 仅 test-defined |
| Development / Test Workflow | 20% | 100 | PASS | 真实 RED、focused GREEN、exact plan、pre-transaction zero-write、失败注入 rollback 和完整回归均有证据 |
| Memory | 15% | 99 | PASS | logical root 不泄漏 physical target；Archive/Feature Context/Lightweight Change 一致；alias retarget 使旧计划 stale |
| Recommendation | 15% | 100 | PASS | Agent 推荐继续或一个阻塞问题；人类仍只确认既有 exact plan/root refresh；无新增 Gate |

加权分：`99.7 / 100`。

## 6. 关键不变量审计

- 未新增 canonical stage、message intent、lifecycle status、Auto Mode 或 Human Gate。
- Feature Monthly Archive 仍只移动完整目录，不压缩、不删除、不改原始人类 Requirement。
- `feature-entry-symlink` 是事实与 blocker，不是 Checker 授权结论；Scanner 仍退出成功并让 Agent判断下一步。
- 安全内部 memory-root alias 只保留逻辑名称；broken/cyclic/external/file/dual authority 仍是物理失败。
- alias target evidence 进入 plan SHA-256；重定向使旧 Human-reviewed plan 失效。
- Apply 在创建 `.archive-txn` 前重新验证当前 plan 和 move shape；任何 symlink source/container 或 stale plan 都是 zero-write。
- exact expected plan SHA-256、transaction journal、project confinement、post-check、restore 和 stranded transaction 规则均保留。
- Root checker 不宣称项目自有正文语义“全部 current”；只对 `source:agent-loop-skill` 正文作 normalized comparison。
- `STRUCTURAL_CHANGED / 0` 不代表写入或执行授权；root refresh 仍需 Agent diff review 和 Human Review。
- `STRUCTURAL_INVALID / 1` 只保留给不能安全解释的 marker/path 结构。
- Product Definition、ADR、Feature Gate、Delivery Contract、Submit/Commit/PR/Merge/Release/Publish 等既有 authority 与 Gate 未改变。

## 7. 实际修复文件

核心实现：

- `scripts/checker_support.py`
- `scripts/feature_archive_support.py`
- `scripts/check-feature-context.py`
- `scripts/lightweight_change_support.py`
- `scripts/check-root-agents-blocks.py`

运行与人类表面：

- `SKILL.md`
- `references/design.md`
- `references/runtime.md`
- `references/artifact-rules.md`
- `references/stage-guides.md`
- `references/project-guidance.md`
- `references/human-review-summary.md`
- `references/workflow-checklists.md`
- `references/validation-scenarios.md`
- `README.md`
- `Usage.md`
- `CHANGELOG.md`

回归与设计证据：

- `tests/test_feature_monthly_archive_scan.py`
- `tests/test_feature_monthly_archive_apply.py`
- `tests/test_feature_context.py`
- `tests/test_lightweight_change_scan.py`
- `tests/test_root_agents_blocks.py`
- `tests/validate-root-agents-block-checker.sh`
- `tests/validate-root-agents-block-refresh.sh`
- `tests/validate-light-gate-authority-alias.sh`
- `docs/proposal/v1.5.x/light-gate-authority-alias-repair.md`
- `docs/proposal/v1.5.x/light-gate-authority-alias-repair-implementation-plan.md`
- `docs/reports/agent-loop-v1.5.3-light-gate-authority-alias-red-2026-07-29.md`

工作区同时保留此前已批准但未提交的 v1.5.3 修改与历史测试缓存；本轮没有恢复、删除、暂存或提交它们。

## 8. 范围漂移与发布判断

- 范围漂移：无。
- 版本漂移：无，保持 `1.5.3`。
- Root managed-block revision 漂移：无，保持 `1.5.3-20260728.1`。
- 目标项目 `.agent-loop/` artifact：未创建。
- Installed Skill 同步：未执行。
- Git/发布动作：未 stage、未 commit、未 push、未 tag、未 PR、未 merge、未 release、未 publish。

结论：当前工作区可进入 Human Review。建议下一步由维护者审阅本报告与 diff；只有获得独立授权后才进行任何 Git 或发布动作。
