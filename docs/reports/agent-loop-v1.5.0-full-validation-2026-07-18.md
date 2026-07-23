# Agent Loop v1.5.0 Persistent Lightweight Change 全量验证报告

日期：2026-07-18
分支：`alpha/v1.5.0`
版本：`1.5.0`（未升级）
计划基线：`200a23b85b5b0e3ebe68496f5f4a16d923d46788`
审计对象：当前未提交工作区，包含已确认 Proposal、Implementation Plan、实现、测试和本报告
设计来源：`docs/proposal/v1.5.x/persistent-lightweight-execution-card-and-memory-consolidation.md`

## 结论

Persistent Lightweight Execution Card 与 Change Memory Consolidation 已按批准设计落地，最终评分 **98/100，STRONG**。当前没有未解决的 Critical、High 或 Medium 发现。

核心结果：

- 新的 clearly eligible Lightweight Change 在第一次目标写入前持久化到唯一 accepted memory root 的 `changes/YYYY-MM/YYYY-MM-DD-<topic>.md`。
- Python 3.10+ 标准库 scanner 只读、确定性、跨月份，并严格校验 root、layout、metadata、authoring marker、fenced Markdown、date、state、size 与 3 个 / 超过 7 天阈值；目录枚举错误进入相对路径 JSON 合同。
- changes-only root、legacy root、dual-root、意外恢复、planned Feature 边界、high-evidence sync、human-review visibility 与 post-merge code-first 顺序已在 runtime/design/reference/template/scenario/test 中协调一致。
- 13/13 root managed blocks 和所有当前 live consumer 已刷新为 `block-version:1.5.0-20260718`。
- 全量回归：Shell `39/39 PASS`，Python `215/215 PASS`。
- 未执行 stage、commit、push、tag、PR、merge、release、publish 或 installed-Skill sync。

## RED → GREEN 证据

### 未改基线

| 范围 | 命令 | 实际结果 |
|---|---|---|
| 旧 Lightweight focused | `bash tests/validate-lightweight-change-lane.sh` | `1/1 PASS` |
| 旧 Python 全量 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | `182/182 PASS`，`74.370s` |
| Shell inventory | `find tests -maxdepth 1 -type f -name '*.sh' | sort | wc -l` | `39` |

### Focused RED

| 范围 | 实际失败 | 证明的缺口 |
|---|---|---|
| Shell contract | `references/lightweight-change-lane.md missing ... The card file is the execution source of truth.` | 旧权威仍是 response-local-only |
| Scanner/Python contract | `scripts/scan-lightweight-changes.py: [Errno 2] No such file or directory` | scanner/support 尚不存在 |
| CI contract | 缺少 `tests.test_lightweight_change_scan` 与 scanner entrypoint | Windows/macOS native CI 尚未注册 |

RED 命令：

```bash
bash tests/validate-lightweight-change-lane.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_lightweight_change_scan \
  tests.test_python_checker_contract
```

第二条命令实际运行 `42` 个测试，退出码 `1`，结果为 `failures=59, errors=6`；subtest 分别计数。完整原始证据保存在 `docs/reports/agent-loop-v1.5.0-persistent-lightweight-change-red-baseline-2026-07-18.md`。

### GREEN 与语义审计修复

| 范围 | 实际结果 |
|---|---|
| Scanner + checker contract | `42/42 PASS`，`3.586s` |
| Scanner/checker/root focused | 初始 `50/50 PASS`；维护者验收修复后 `56/56 PASS` |
| Focused Shell | PASS |
| 计划列出的 affected regressions | 全部 fail-fast PASS |

六域初始审计发现并关闭一个 Medium parser loophole：`completed + pending` 曾能接受 `none:` 或其他 `pending:` 伪验证/目标。新增两个 subtest 先观察到退出码 `0` 的真实 RED，再要求 actual verification locator 与 candidate target evidence。

### 维护者最终审查 RED → GREEN

首轮报告声称无未解决 Medium 后，维护者没有复用该结论，而是独立复核运行时边界并发现 4 个验收缺口：目录枚举 `OSError` 泄漏 traceback/绝对路径、模板 authoring marker 可进入 completed 卡、fenced Markdown 被误解析为结构、合法含 `@` branch 被拒绝。首轮 5 个 targeted 方法得到 6 个预期失败；parser 自审追加的无效 fence 隐藏 marker 用例另得到 1 个预期失败。

修复采用 6 个独立 scanner 回归方法：

- `_sorted_directory_entries` 把 root/month 枚举失败转换为 `layout` JSON，仅保留项目相对路径；POSIX CLI 权限测试与跨平台 mock 测试共同覆盖；
- `<replace...>` authoring marker 在有效 fenced evidence 之外统一失败；
- 等长 fence mask 让 backtick/tilde fence 内的 H2、Memory metadata 和字面模板示例不参与结构解析，无效 backtick fence 不能隐藏 marker；
- `Git Context` 从最后一个 `@` 拆分 full SHA，保留非空、无空白 branch 和 40/64 位小写 SHA 约束。

修复后 targeted、`56/56` focused、39 个 Shell 和 215 个 Python 全量均重新执行；当前没有遗留的 parser finding。

## Full Validation

### 全部 Shell

```bash
shell_total=0
shell_pass=0
for test_file in tests/*.sh; do
  shell_total=$((shell_total + 1))
  if bash "$test_file"; then
    shell_pass=$((shell_pass + 1))
  else
    printf 'FAILED: %s\n' "$test_file" >&2
    exit 1
  fi
done
```

最终 fresh rerun：`39/39 PASS`。

### 全部 Python

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'
```

最终 fresh rerun：`Ran 215 tests in 76.710s`，`OK`。

### 机械检查

| 检查 | 最终结果 |
|---|---|
| `ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'` | PASS |
| `python3 -m json.tool plugin.json` | PASS |
| 全部 Shell `bash -n` | `40/40 PASS` |
| Markdown fence balance（含 untracked Proposal/Plan/Reports） | `232/232 PASS` |
| `git diff --check` | PASS |
| root `.agent-loop/` / `templates/.agent-loop/` | 均不存在 |
| `__pycache__` | 测试副产物已限定清理，最终为 `0` |

## 六域语义审计

| 审计域 | 结果 | 评分 | 已验证的不变量 |
|---|---|---:|---|
| Logic Correctness | PASS | 99 | Bug/Feature precedence、all-of eligibility、状态/日期/root/layout、3/7 边界、scope expansion、无新 stage/status/mode |
| Autonomy | PASS | 98 | Agent 先检查证据并创建/更新 card；scanner 只做机械发现；semantic consolidation、唯一推荐与恢复由 Agent 负责 |
| Project Entry / Evidence Graph + DDD Onboarding | PASS | 98 | no-root/changes-only/legacy/dual-root 明确；changes-only 不伪装初始化；既有 onboarding/Requirement/ADR 路由未回归 |
| Development / Test Workflow | PASS | 99 | Adaptive Plan、failure-matched checks、isolatable behavior RED/GREEN、完成前验证/diff/rollback/Memory Review、planned work 进入 Feature |
| Memory | PASS | 98 | 3 个或超过 7 天触发；human-review 持续可见；existing reliable owner + exact disclosure；失败窄回滚；代码先合并、Target memory 后校准 |
| Recommendation | PASS | 97 | uncertain 零写入 + 单一 Agent 推荐；中文少选项 Human Review；Git/生产/外部/发布 Gate 独立 |

加权得分：`98.3`，按整数报告为 **98/100，STRONG**。

## 代表性压力场景

| 场景 | 结果 |
|---|---|
| clearly eligible small config fact | persistent monthly card → exact check → completed/pending，PASS |
| three pending across months | `pending-count` → proactive consolidation，PASS |
| seven-day boundary | exactly 7 不触发；8 天触发，PASS |
| changes-only root | scanner 可发现，Project Entry 仍不可靠，PASS |
| accepted legacy / dual roots | legacy reuse；dual fail closed，PASS |
| unreadable changes root / enumeration race | contract JSON + relative path；无 traceback/绝对路径，PASS |
| generated authoring marker | fenced evidence 外拒绝；无效 fence 不可隐藏，PASS |
| fenced Markdown evidence | H2/Memory 示例不参与结构解析，PASS |
| Git branch contains `@` | 从最后一个 `@` 拆分 full SHA，PASS |
| accidental resume / planned handoff | 前者完整 revalidation；后者 Feature，PASS |
| explicit Bug / active Feature | 保持原 owning workflow，PASS |
| public/data/security/unknown impact | Feature hard trigger，PASS |
| high-evidence memory sync | existing owner + no new decision + exact disclosure/post-check/rollback，PASS |
| human-review | 不计 pending，但持续可见，PASS |
| Source branch / post-merge | Source 不提前覆盖；Merged Code 验证后重新判断，PASS |
| commit/release/production | 每个 action-specific Human Gate 独立，PASS |

## Scanner 平台与只读证据

- 当前 macOS 主机：CLI、fixture、BOM/CRLF、symlink、无权限目录 JSON、fenced Markdown、含 `@` branch、1 MiB、deterministic/read-only tree snapshot 全部实际执行通过。
- Windows：`.github/workflows/cross-platform-checkers.yml` 已定义在 `windows-latest × Python 3.10/3.x` 原生运行 `tests.test_lightweight_change_scan`，并单独执行 scanner `--help`；POSIX chmod 用例在 Windows 跳过，但标准库 mock 枚举错误用例仍执行。实现无 shell-specific 调用，只依赖 Python 标准库和声明的 local support。
- 本轮未远程触发 GitHub Actions，因此结论是 **macOS-verified / Windows-test-defined**，不虚构远端 Windows run 结果。
- 两次 unchanged scan 的 exit/stdout/stderr 与 tree snapshot 一致；scanner 无 mkdir、touch、rename、memory writer、scheduler、counter 或 event flag。

## Proposal 验收标准覆盖

| # | 运行规则与 artifact | scanner / Agent 责任 | focused / scenario 证据 | 全量结论 |
|---:|---|---|---|---|
| 1 | `runtime.md`、`lightweight-change-lane.md` 和执行卡模板规定唯一 accepted root 下的 `changes/YYYY-MM/YYYY-MM-DD-<topic>.md` | Agent 在路由明确后创建；scanner 校验严格月目录和文件名 | focused 路径断言；`Monthly Partition Is Stable And Is Not Archive` | PASS |
| 2 | 执行卡模板含 Scope、Plan、Progress、Verification、Human Gates、Result / Residuals、Memory Review / Result；卡是 execution source of truth | Agent 在第一次 target write 前创建并持续更新 | focused 卡字段/创建顺序断言；`Persistent Card Exists Before First Target Write` | PASS |
| 3 | `project-memory-mode.md` 与 Project Entry 明确 changes-only 不等于 initialized / reliable | scanner 允许 changes-only root；Agent 不据此扩展项目记忆 | unit `test_existing_root_without_changes_is_empty_and_read_only`；`Changes-Only Root Does Not Prove Initialization` | PASS |
| 4 | runtime/root resolution 只接受唯一 canonical 或唯一 legacy root | scanner 零 root 只读空结果、唯一 legacy 复用、双 root fail closed | 3 个 root-shape unit tests；`Accepted Legacy Root Is Reused`、`Dual Memory Roots Stop In Recovery` | PASS |
| 5 | `artifact-rules.md` 定义 status/date/Memory Review/Memory Result/month/name/no-placeholder contract | scanner 确定性解析并拒绝非法组合、未来日期、错月、错名和 authoring marker；fenced evidence 不污染结构 | parser/metadata/combination/collision/placeholder/fence unit tests | PASS |
| 6 | lane 与 artifact rule 明确原月份路径稳定，不是 Archive lifecycle | Agent 不 move/rehydrate/rewrite Change；scanner 只读现有路径 | focused 禁止 move/archive 断言；`Monthly Partition Is Stable And Is Not Archive` | PASS |
| 7 | scanner contract 不依赖 archive、INDEX、共享计数器 | scanner 遍历所有严格月目录并排序汇总 | cross-month count unit；focused negative assertions | PASS |
| 8 | `project-memory-mode.md` 规定 pending `>=3` 或 oldest `>7` | scanner 机械计算 count/age；恰好 7 天不触发 | two/three pending 与 exactly/more-than-seven unit tests及 4 个同名场景 | PASS |
| 9 | runtime/controller 规定 fact drift、pre-release、verified post-merge 为事件触发 | Agent/controller 判断事件；scanner 不提供语义 event flag | focused event-owner 断言；`Scanner Does Not Perform Semantic Memory Writes`、post-merge 场景 | PASS |
| 10 | project-memory/lane 列出全部 high-evidence 自动同步条件 | Agent 逐条件审计；scanner 不做主观 confidence score | focused 条件/禁主观评分断言；`High-Evidence Sync Requires Existing Reliable Memory` | PASS |
| 11 | `human-review-summary.md`/project-memory 采用中文、少状态候选摘要；执行卡保留 `human-review` | scanner 把 human-review 独立持续列出，不计入 pending | unit `test_human_review_is_reported_separately`；`Human Review Candidate Remains Visible` | PASS |
| 12 | 自动同步规则要求 pre-write 披露 exact target path/fact/evidence/rollback 与 post-check | Agent 执行披露、窄写入、post-check；scanner 仅校验卡内 concrete result | focused exact-scope/rollback 断言；`Automatic Sync Discloses Exact Memory Scope` | PASS |
| 13 | Project Entry 明确 changes-only root 不触发完整 memory 初始化 | Agent 只维护 Change 卡，不自动建 project/onboarding/requirements 等 artifact | focused negative assertions；changes-only 场景 | PASS |
| 14 | project memory 只保留当前可靠事实，不保存 Change 历史或 pending backlog | Agent 整理后在卡中保留证据，项目记忆不复制 backlog；scanner 不写 memory | focused ownership 断言；`Scanner Does Not Perform Semantic Memory Writes` | PASS |
| 15 | runtime routing 保留 planned cross-session、handoff、Subagent 和 Feature 硬触发器 | Agent 对这些情形直接进入 Feature，不以持久卡规避 Feature | focused route assertions；`Planned Cross-Session Work Uses Feature` | PASS |
| 16 | lane 定义 scope expansion stop rule 与 Bug/Feature 重路由 | Agent 停止当前卡并请求/执行正确路由，不静默增量扩张 | focused stop-rule 断言；`Scope Expansion Stops Persistent Card Execution` | PASS |
| 17 | lane、workflow checklist 与 template 保留 targeted verification、diff review、rollback、Human Gates | Agent 按风险伸缩证据深度但不降低验收与 gate | focused 必需字段和 gate 断言；`Git Production And Release Gates Remain Separate` | PASS |
| 18 | scanner 为 Python 3.10+ stdlib + 声明 local support，路径与输出跨平台 | scanner 原生 Python，只读、deterministic；枚举失败归一化；CI matrix 定义 Windows/macOS | import-contract、BOM/CRLF、symlink、permission/mock、fence、size、determinism unit；CI entry | macOS-verified / Windows-test-defined |
| 19 | RED 报告、focused contracts、affected tests 与 full method 都有独立证据 | Agent 以真实运行结果刷新报告，不复用 Proposal 或首轮开发报告数字 | focused Shell PASS、Python 56/56；full Shell 39/39、Python 215/215 | PASS |
| 20 | Proposal、Plan 与本报告只更新到待最终 Human Review | Agent 停止在维护者验收；不执行任何 Git/发布/installed-Skill 动作 | status/diff/forbidden-artifact final review | PASS，待 Human Review |

## 剩余风险

1. Windows contract 已原生定义但本轮没有远端 Windows runner 的实际执行回执；维护者可在后续独立 CI/Git gate 中确认。
2. High-evidence semantic classification 本质上由 Agent 结合真实项目权威完成，不能由 scanner 完全机械证明；当前通过严格条件、压力场景、Human Review 和 fail-closed 边界控制该观察风险。
3. 测试运行会由部分既有 Shell 测试短暂生成 `scripts/__pycache__` 与 `tests/__pycache__`；本轮已确认内容仅为测试 bytecode 并限定清理，最终工作区不存在缓存目录。

以上均为 observation risk，不是当前未解决的 Critical、High 或 Medium finding。

## 授权边界与下一步

- 没有 stage、commit、push、tag、PR、merge、release、publish。
- 没有创建或切换 branch/worktree，没有派发 Subagent。
- 没有同步 Codex、Kimi Code、OpenCode 或其他已安装 Skill。
- 没有创建源码仓库根 `.agent-loop/` 目标项目 artifact。
- 推荐下一步：维护者执行 Human Review；接受后另行进入独立 Git action gate。
