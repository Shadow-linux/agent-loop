# Agent Loop v1.5.6 Full-Worktree Git Fast Path 全量验证报告

日期：2026-08-15

分支：`v1.5.6`（完整验证在同一内容的 `v1.5.5` 工作区完成；之后仅按人类授权同步 1.5.6 版本元数据，未重新运行 tests）

版本：`1.5.6`（经人类批准升级）

审计对象：基线 `84c14aa6ddc75779022229c4d2c5d5d9035b57e7` 之上的当前未提交工作区

结论：`96.3 / 100 — STRONG`

本次能力当前 findings：`Critical 0 / High 0 / Medium 0 / Low 0`。仓库仍保留前一轮发布前 Human Review 已知并接受的 3 个 inherited High 风险，详见“既有已接受风险”；它们不是本次 Git Fast Path 引入的回归，也未被本轮静默修复。

## 1. 实施范围

Full-Worktree Git Fast Path 作为 `Submit / Integrate` 内部方法实现：

- 明确 `commit` / `commit and push` 请求进入一次轻量 Commit Confirmation，只展示全工作区摘要、拟定 commit message，以及被请求 Push 的 remote/ref；
- Commit 默认纳入整个 Git-visible worktree，并使用 `git add -A`；
- Agent 只披露 cache/generated/sensitive/suspicious 候选，不自行 exclude/restore/clean/stash/split/discard；
- 仅因 Git 动作不运行 tests、Verify、代码/质量/Feature Review、Drift 或 Completion；
- 未验证 Git packaging 不得成为 fixed/done/closed/release-ready 证据；
- plain Commit 不推导 Push；commit-and-push 可在同一次轻量确认中授权，Push 绑定 exact remote/ref 且仅在 Commit 成功后执行；
- 执行前事实变化、Git conflict、目标歧义、sealed/customer isolation、index mismatch 和命令失败仍停止；不引入正式 worktree fingerprint 算法或第二次确认。

未新增 canonical stage、message intent、status、artifact tree、Checker outcome、依赖或版本号。

## 2. RED → GREEN

### RED 1：缺少核心运行契约

```bash
bash tests/validate-full-worktree-git-fast-path.sh
```

退出 `1`：

```text
FAIL: references/runtime.md missing Git Fast Path contract: Full-Worktree Git Fast Path
```

### RED 2：Branch Strategy 恢复旧硬前置

首次 GREEN 后扩展跨文件断言，同一命令退出 `1`：

```text
FAIL: references/branch-management.md missing Git Fast Path contract: Full-Worktree Git Fast Path preserves branch-policy facts without restoring normal Submit quality prerequisites
```

### RED 3：最终确认语义缺失

人类明确“可以确认 commit 内容和 Agent 拟定的 commit 信息，但不做任何测试”后，先更新 focused contract，再运行得到：

```text
FAIL: references/runtime.md missing Git Fast Path contract: one lightweight Commit Confirmation
```

这证明“请求本身直接执行”和“完整 Human Review”都不是最终边界。

### GREEN

```text
PASS: Full-Worktree Git Fast Path contract and mutations are valid
PASS: Human-Guided Branch Management optional profile, gates, artifacts, diagram, and scope contract is complete
```

Focused contract 包含 mandatory pre-commit tests、code-quality Review、automatic unrelated exclusion、second confirmation、incomplete worktree scope、lost unverified-completion truth 六类 mutation；每类退化均会使契约失败。

## 3. Focused Validation

最终语义同步后的受影响测试批次：

- Git Fast Path、root refresh、root checker、Branch Management 4 个 Shell contracts：全部通过；
- `tests.test_root_agents_blocks`、`tests.test_root_agents_lossless_slimming`：`16 / 16` 通过；
- `git diff --check`：通过。

## 4. Full Validation

最终 production-rule 修复后重新执行，不沿用首轮结果：

```bash
for test_file in tests/*.sh; do bash "$test_file"; done
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'
```

结果：

| Suite | 实时数量 | 结果 |
|---|---:|---|
| `tests/*.sh` | 51 | 51 / 51 PASS |
| Python unittest | 420 cases | 420 / 420 PASS |

Python 最终输出（最终轻量确认语义同步后重新执行）：

```text
Ran 420 tests in 70.654s

OK
```

## 5. 机械检查

| 检查 | 结果 |
|---|---|
| `SKILL.md` YAML | PASS |
| `plugin.json` JSON | PASS |
| Shell syntax | 52 / 52 PASS |
| Python AST | 48 / 48 PASS |
| Ruby syntax | 5 / 5 PASS |
| Markdown fences | 357 / 357 PASS |
| root managed blocks | 13 / 13，revision `1.5.6-20260815.1` |
| root template length | 177 行，低于 190 |
| version sync | `SKILL.md` / `plugin.json` / `README.md` / `Usage.md` 均为 1.5.6 |
| `git diff --check` | PASS |

## 6. 六域语义审计

| 审计域 | 结果 | 原始分 | 加权分 | 结论 |
|---|---|---:|---:|---|
| Logic Correctness | PASS | 96 | 19.20 | Fast Path/normal Submit 分域明确；Commit/Push、completion 和 branch policy 不互相授权 |
| Autonomy | PASS | 99 | 14.85 | Agent 直接收集事实、一次推荐与确认，不再用测试仪式或文件挑选反复中断 Human |
| Project Entry / Onboarding | PASS（含 inherited risk） | 91 | 13.65 | 本轮未改变入口；已接受 memory-root/legacy 风险继续披露 |
| Development / Test Workflow | PASS | 99 | 19.80 | 实现/完成验证义务保持，只有 Git packaging 不自动触发质量流程 |
| Memory | PASS（含 inherited risk） | 93 | 13.95 | notes/root projection 同步；已接受 Post-Merge 摘要风险继续披露 |
| Recommendation | PASS | 99 | 14.85 | normal readiness、commit-only、commit-and-push、test-conditioned、scope drift 均有唯一下一动作 |
| **总分** | **STRONG** |  | **96.30** | 无本次未解决 Critical/High/Medium/Low |

## 7. 关键压力场景

| 场景 | 结果 |
|---|---|
| staged + unstaged + untracked + deleted | 一次轻量确认，展示全工作区摘要和拟定 message；确认后立即 `git add -A` |
| 人类只说 commit、未要求测试 | 不自动测试；显式 no-completion truth |
| 人类要求“测试通过后 commit” | 测试仅因这个显式条件成为 exact precondition，完成后再做轻量确认 |
| 可疑 cache/generated/sensitive 路径 | 警告但不由 Agent 排除 |
| 确认后、执行前 worktree/branch 事实变化 | 旧授权失效，刷新摘要和 message 后重新确认 |
| commit and push | 同一次轻量确认列出 exact remote/ref；Commit 失败不执行 Push |
| adopted Branch Strategy | 仍检查 sealed/customer/target/conflict；不恢复 normal verification 前置 |
| Git 成功但完成证据缺失 | 只报告 packaging；不能 close/release |
| 普通 prepare/PR/merge/tag/release | 保持 normal Submit 与原独立 Gate |

## 8. 既有已接受风险

以下风险已经在 v1.5.5 前一轮发布 Human Review 中披露并由人类决定暂不修复；本轮没有扩大、覆盖或重新授权：

1. `scripts/checker_support.py` 仍可能把普通顶层 `agent-loop/` 产品目录误识别为 legacy memory root；
2. legacy `agent-loop/` memory 项目的 Project Skill 创建规则仍可能写入 `.agent-loop/skills/` 并形成双 root；
3. `references/runtime.md` 的简写 Post-Merge chain 与 owning Submit action sequence 仍存在 Tag/Publish/Seal 摘要覆盖风险。

这些 inherited High 已被解释并保留在 `CHANGELOG.md` 的 v1.5.5 状态中，因此未伪装为本轮新发现或 0 风险。若维护者要求消除它们，应作为独立 Proposal/修复处理。

## 9. 独立专项审查与修复

实现后的独立只读审查曾发现 `1 High / 2 Medium`，均已在最终验证前修复：

1. `High`：通用 Submit checklist 会在 Git Fast Path 前重新执行 verification/Review/Drift。已把该 checklist 明确限定为 normal-submit only，并加入 focused assertion。
2. `Medium`：owning Submit Notes Record 缺少 Git Path、Worktree Scope、Verification Truth、Commit/Push 结果字段。已与 `templates/notes.md` 同步。
3. `Medium`：早先 `Reviewed Worktree Fingerprint` 没有可靠算法定义。最终设计不再引入该字段；轻量确认后立即 `git add -A`，执行前发现事实变化则停止并重新确认，客观 repository/conflict/index/policy 边界仍保留。

最终复审未发现本能力新增的未解决 Critical/High/Medium/Low。

## 10. 范围漂移与发布判断

- Scope drift：无；只实现已批准 Git Fast Path，并同步修复专项审查发现的 owning checklist、Notes 与未定义 fingerprint 问题。
- 版本：`1.5.6`。
- root revision：`1.5.6-20260815.1`，13/13。
- 当前可以进入最终 Human Review。
- 本报告不授权 stage、commit、push、tag、PR、merge、release、publish 或 installed Skill 同步。
- 当前未执行上述 Git/发布动作；如维护者之后要求 commit/push，只展示当时整个工作区摘要、拟定 commit message 和被请求 Push 的 remote/ref 做一次轻量确认，不运行测试或代码/质量 Review。
