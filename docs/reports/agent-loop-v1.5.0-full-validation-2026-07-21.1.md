# Agent Loop v1.5.0 Root AGENTS Lossless Slimming 全量验证报告

> 2026-07-22 复核说明：本报告保存初次 GREEN 证据与当时评分。后续补充审计在 `docs/reports/agent-loop-1.5.0-full-validation-2026-07-21.md` 发现 Root 撰写指南漂移；关闭结果与当前组合工作区全量证据见 `docs/reports/agent-loop-v1.5.0-root-guidance-consistency-full-validation-2026-07-22.md`。请勿把本报告的 `99.8` 当作后续工作区当前评分。

- 日期：2026-07-21
- 分支：`alpha/v1.5.0`
- Skill version：`1.5.0`（未升级）
- HEAD：`3063201a3fee0adad9846fa33e977df30405d295`
- 审计对象：当前工作区，不是仅审计 `HEAD`
- 实施依据：`docs/proposal/v1.5.x/root-agents-lossless-slimming.md`
- RED 证据：`docs/reports/agent-loop-v1.5.0-root-agents-lossless-slimming-red-baseline-2026-07-21.md`
- 平台边界：macOS verified / Windows contract-defined；本轮未运行原生 Windows

## 结论

| 项目 | 结果 |
|---|---|
| 总分 | **99.8 / 100** |
| 等级 | **STRONG** |
| Critical / High / Medium | **0 / 0 / 0** |
| Low | 1 个验证边界：未运行原生 Windows，不是当前代码缺陷 |
| Shell tests | **39 / 39 PASS** |
| Python tests | **221 cases discovered，test process exit 0** |
| Focused Root Python | **33 / 33 PASS** |
| Root-consuming Shell contracts | **23 / 23 PASS** |
| 无 Git 历史源码快照维护测试 | **2 / 2 PASS** |
| YAML / JSON / Shell syntax / Markdown fences / diff check | **全部 PASS** |
| 发布动作 | 未授权，未执行 |

当前 Root AGENTS 已满足 lossless-slimming 验收：从 `224 lines / 3434 words / 27370 bytes` 收敛到 `170 lines / 1883 words / 15357 bytes`，保留 13 个 managed blocks，13/13 使用 `block-version:1.5.0-20260721.2`。Skill version 仍为 `1.5.0`。

## RED -> GREEN

实施前 focused contract 真实报告：

- `line-count:224`
- `canonical-template-has-cjk`
- `managed-revision`
- `gateway-contract`
- 缺失 workflow/product spine、artifact authority、五类可见 Gate、completion 和 independent lifecycle gate
- Root 重复 ADR trace 与 archive transaction 算法细节
- mutation 因 Gateway 尚不存在而产生预期 RED

实施后：

- 精确 16-row Gateway tuple、reference set 与文件存在性全部 PASS；
- runtime 完整 leaf-stage 顺序与 Feature Construction Gateway 绑定 PASS；
- 删除 Gateway、交换 reference、删除 project-outcome ownership、删除 Gate class 四个 mutation 全部被拒绝；
- Root line/CJK、13 blocks、`.2` revision、spines、六 Gate、completion、submit、artifact authority 全部 PASS；
- 所有旧 Root leaf/detail assertions 已迁移到 Root first-hop、owning reference 或 runtime owner，没有靠删除不变量变绿。

## 执行命令与结果

```text
for test_file in tests/*.sh; do PYTHONDONTWRITEBYTECODE=1 bash "$test_file"; done
shell: 39/39 PASS

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'
discovered: 221; process exit: 0

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  tests.test_root_agents_lossless_slimming \
  tests.test_root_agents_blocks \
  tests.test_python_checker_contract
Ran 33 tests; OK

rsync current source without .git to a clean snapshot, then run:
bash tests/validate-feature-validation-method.sh
bash tests/validate-v1.3.0-release-readiness.sh
historyless source snapshot: 2/2 PASS

ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
python3 -c 'import json; json.load(open("plugin.json", encoding="utf-8"))'
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
Markdown fence balance check
git diff --check
全部 PASS
```

## 六域语义审计

| 审计域 | 域分 | 加权分 | 结果 | 当前证据与结论 |
|---|---:|---:|---|---|
| Logic Correctness | 100 | 20.0 / 20 | PASS | `templates/root-AGENTS.md:65-86,92-109` 投影精确 first hop 与六 Gate；`references/runtime.md:15,300,470-527` 保留 precedence 与完整 Stage Order；Auto Mode 无 Gate bypass。 |
| Autonomy | 100 | 15.0 / 15 | PASS | `templates/root-AGENTS.md:22,30-37` 保留 evidence-first project-outcome ownership、唯一下一步、完整 workflow spine；helper 只提供方法，不接管 authority。 |
| Project Entry / Evidence Graph + DDD Onboarding | 100 | 15.0 / 15 | PASS | `references/runtime.md:264-346` 区分 new/existing/remote、remote 优先与可靠 memory；`references/onboarding-knowledge-base.md:13-17,141-255` 保留 Entry 前置、Core Flow Inventory 与 Spec Gate。 |
| Development / Test Workflow | 99 | 19.8 / 20 | PASS | `references/runtime.md:470-527,550-580` 保留完整 Plan/Execute/Verify/Review/Drift/Memory/Completion 顺序；`templates/root-AGENTS.md:112-129` 保留 done 与 Submit hard boundary。原生 Windows 未运行，扣 1 域分。 |
| Memory | 100 | 15.0 / 15 | PASS | `templates/root-AGENTS.md:132-139` 保留 artifact authority；`references/runtime.md:337-346,459-468` 保留 locator、Change scan 与 reconciliation state；`references/project-guidance.md:174-200` 保留 managed refresh 和 unmanaged-byte Human Gate。 |
| Recommendation | 100 | 15.0 / 15 | PASS | `templates/root-AGENTS.md:22,30-34` 要求调查后推荐一个下一步；`references/runtime.md:534,607-628` 保留 Human Review Summary、stop/blocked 与独立授权表达。 |

加权总分：`20 + 15 + 15 + 19.8 + 15 + 15 = 99.8`。

## 当前问题

### Critical / High / Medium

无。

### Low / 验证边界

1. 本轮仅在 macOS 执行完整测试。Python checker contract、标准库约束和跨平台 CI contract 通过，但没有原生 Windows 运行证据。该边界不影响本次 Markdown workflow projection 的当前逻辑结论，后续发布候选仍应由配置的 Windows CI 验证。

## 压力场景

### Root projection 16 场景

以下场景逐项审计并记录于 RED 报告的 GREEN Closure，全部 PASS：controller recovery、new/existing、remote/local、stale memory、Requirements/Lightweight、Bug/generic fix、ADR/no-ADR、Feature leaf continuation、Operational Support、Project Skill Gate、Archive apply、post-merge/Git、六 Gate/Auto Mode、completion evidence、unrelated dirty work、ordinary Chat。

### 全量方法代表场景

| 场景 | 结果 | 证据 |
|---|---|---|
| Complex Requirement -> Design Readiness -> ADR -> Feature | PASS | `references/project-decisions.md:6,54-82`; `references/runtime.md:52` |
| Simple requirement without ADR | PASS | `references/project-decisions.md:75-82` |
| Product Brief Source Gate | PASS | `references/product-brief.md:32`; `references/workflow-checklists.md:365` |
| Delivery Contract Human Gate | PASS | `references/design.md:67`; `references/runtime.md:23,617` |
| Behavior RED/GREEN and non-behavior N/A | PASS | full Shell/Python regression and existing TDD contracts |
| Active Feature / Pause / Resume / Close / Reopen | PASS | `references/feature-completion-check.md:149`; runtime lifecycle order |
| Multi-phase `partially-implemented` roll-up | PASS | `references/requirement-management.md:45,218-232` |
| Accepted ADR versus implementation drift | PASS | `references/project-decisions.md:230-234` |
| Follow-up `investigate-first` | PASS | `references/feature-follow-up.md:52,81,99` |
| Submit blocker and verification order | PASS | `references/submit-and-integrate.md:81-106,187-217` |
| stale-memory / root guidance / Project Entry | PASS | `references/runtime.md:360-372`; `references/project-guidance.md:174-200` |
| ordinary Chat creates no artifact | PASS | `templates/root-AGENTS.md:84`; `references/runtime.md:54-56` |

## 关键跨文件不变量

- `SKILL.md` 仍是简洁入口；Root 是 startup projection，runtime/reference 是详细 owner。
- Requirement、Decision/ADR、Feature、Bug、Lightweight card、project memory 的 authority 未改变。
- Gateway 只选 owner family，不增删或重排 canonical stage。
- Delivery Contract、Requirement/Feature lifecycle、Project Skill execution、Archive apply、external mutation、Git/submit/pause/close 均保留独立 Human Gate。
- code/tests 通过仍不能跳过 Review、Drift Check、Project Memory、Feature Completion/Close Review。
- root managed refresh 仍按 section/revision 对比，并保留所有未经人类逐项授权的 unmanaged bytes。

## 未采纳或降级意见

- 未恢复历史 commit `1980368`：accepted Proposal 要求重构当前工作区，而不是回滚到旧设计。
- 未把详细 ADR trace、Archive transaction、Bug lookback、Lightweight counters、Project Skill manifest 重新塞回 Root：这些算法由 published owners 负责。
- 未通过放宽 exact tuple、mutation、Gate 或 line/CJK contract 达成行数目标。
- 保留 33 个历史报告及其原有路径；两个旧维护测试继续读取当前源码树证据，不依赖固定 Git object。
- 未将 canonical template 本地化为中文；模板保持 English-only，目标项目仍可按语言偏好呈现 guidance。

## 工作区与授权边界

- 33 个历史 `docs/reports/*.md` 继续作为仓库内验证证据保留，不纳入本功能改写。
- 本功能只新增 RED 报告和本 suffixed full-validation 报告。
- 未创建目标项目 `.agent-loop/` artifact。
- 未升级 Skill version；未同步 installed Skill。
- 未 stage、commit、push、tag、PR、merge、release 或 publish。

## Human Review 推荐

当前实现达到 `>=99/100`、`STRONG`、Critical/High/Medium 全为 0 的实施门槛。推荐下一步仅进行维护者语义复核；未经新的明确授权，不执行任何 Git、发布或 installed-skill sync 动作。
