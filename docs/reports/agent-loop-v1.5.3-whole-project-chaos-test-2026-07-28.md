# Agent Loop v1.5.3 全项目混沌测试报告

## 审计对象

- 日期：2026-07-28
- 分支：`v1.5.3`
- 基线 HEAD：`6086d7d6fc758221af2dee41ea269d0acf237795`
- 审计对象：当前未提交组合工作区；包含既有 Feature Archive soft-gate 与 Feature Context soft-gate 修改
- 方法：主 Agent 全量回归与最小隔离复现 + 两个互不写入仓库的子 Agent 独立混沌 lane
- 工作区边界：保留全部既有 dirty work、Proposal、报告与 `.tmp/`；没有 stage、commit、push、tag、分支或目标项目 artifact 操作

## 总结

- 评分：**87 / 100**
- 等级：**STABLE**
- 计数：Critical 0、High 1、Medium 2、Low 0
- 结论：Requirements/ADR/Feature 生命周期、两道 Feature Gate、Auto Mode、Task Done、Pause/Resume/Close、Submit/Git Gate 的主闭环没有发现可证实绕过；但 Archive/Rehydrate 的一个物理目录 symlink 反例会在 Apply 失败后留下不一致状态，因此当前组合工作区不应在修复前作为 Archive/Rehydrate 发布候选。

## 实际验证

### 全量基线

```bash
for test_file in tests/*.sh; do bash "$test_file"; done
python3 -m unittest discover -s tests -p 'test_*.py'
```

- Shell：`47 / 47 PASS`
- Python：`333 / 333 PASS`，212.644 秒

### 高风险 focused 回归

```bash
python3 -B -m unittest \
  tests.test_feature_archive_support \
  tests.test_feature_monthly_archive_scan \
  tests.test_feature_monthly_archive_apply \
  tests.test_feature_monthly_archive_restore \
  tests.test_feature_context \
  tests.test_feature_review \
  tests.test_requirement_product_definition \
  tests.test_adr_requirement_model_trace \
  tests.test_root_agents_blocks \
  tests.test_root_agents_lossless_slimming \
  tests.test_project_guidance_consistency
```

- Python：`168 / 168 PASS`
- Shell contracts：Feature Archive soft gate、Feature Context、Feature construction two gates、ADR trace、root block checker、root refresh 均 PASS。

机械检查：`SKILL.md` YAML、`plugin.json` JSON、全部 Shell syntax、Markdown fence、`git diff --check` 均 PASS。

## 混沌 lane 覆盖

### Lane A：生命周期与授权（子 Agent 只读审计）

覆盖 Product Review pending、deferred Requirement、ADR `review-required`、`CHANGED / 0` 误用、Gate 1 直达实现、Gate 2 package-only/later-start、任务替换、缺 Plan/伪 No-Plan、TDD `N/A`、Task Done 伪证据、Pause/Resume、Close、Submit/Git 混合授权。

结果：未发现可证实漏洞；该 lane `97 / 100`，Critical/High/Medium/Low 均为 0。关键不变量由 `references/runtime.md`、`references/stage-guides.md`、`references/workflow-checklists.md`、`references/implementation-planning.md` 及 focused contracts 共同覆盖。

### Lane B：authority、恢复与物理边界（子 Agent + 主 Agent 最小复现）

覆盖 Feature Context `CURRENT / CHANGED / BLOCKED`、cached 与 authoritative pointer、dual/symlink root、Requirement/Product/ADR containment、Archive reference symlink、plan hash drift、journal/rollback、Apply project boundary、root managed-block marker/revision/body drift。

结果：发现以下 1 个 High、2 个 Medium。主 Agent 对三个发现均在 OS 临时目录独立复现；没有修改仓库。

## 发现

### High — Rehydrate 接受项目内 Feature 目录 symlink，并在失败后留下错误状态

**证据：**

- `scripts/feature_archive_support.py:455-465` 的 `_confined_existing_directory()` 只验证 resolve 后仍在 project 内，不拒绝 entry 自身是 symlink。
- `scripts/feature_archive_support.py:468-529` 的 `resolve_feature_location()` 因而将归档月目录中的 symlink 视作真实 archived Feature。
- `scripts/feature_archive_support.py:1736-1751` 在最终 physical preflight 前执行 `source.rename(target)`；`scripts/feature_archive_support.py:1790-1800` 才尝试 rollback。

**最小复现：**将 `.agent-loop/features/2026-05/<feature-id>` 设为指向项目内 `payload-not-memory/<feature-id>` 的目录 symlink，并写入匹配的 archived locator row。执行 rehydrate scan/apply 后得到：

```text
ARCHIVE_INTERNAL_SYMLINK_SCAN_RC 0
ARCHIVE_INTERNAL_SYMLINK_APPLY_RC 1
transaction: path-escape ... restore=failed
ARCHIVE_INTERNAL_SYMLINK_STATE True True False
```

`True True False` 表示 flat path 已成为 symlink、真实 payload 仍在 memory 外、原 archived link 已消失。也就是说操作报告失败，但 rollback 未恢复原位置。

**影响：**违背“whole directory / do not follow symlinks / transaction rollback”边界；Archive locator 与实际可执行 Feature 状态可能分离，后续 Feature Context 会因 Feature 解析位置错误而阻断。该反例不是外部项目写入，但已构成失败恢复不完整和 Feature ownership 损坏。

**现有测试缺口：**`tests/test_feature_archive_support.py:224-242` 仅覆盖 project 外 symlink escape；没有项目内 Feature directory symlink 的 archive/rehydrate scan + apply + rollback 回归。

**建议（保持 soft-gate 设计）：**scanner 记录 Feature-entry symlink 这一事实，Agent 不应将它推荐为可授权 plan；Apply 在创建 transaction、move 前重新拒绝 feature root/`features/` 容器 symlink，确保失败不发生任何 move。新增 scan、apply、restore 三层回归及“无写入”断言。这里保留执行器物理边界，不把普通引用判断重新做成硬 Checker Gate。

### Medium — Archive memory-root symlink 与 runtime 的 real-root 规则不一致

**证据：**

- `scripts/feature_archive_support.py:253-265` 使用 `is_dir()` 并 `.resolve()`，会接受 `.agent-loop -> .memory` 的项目内 symlink。
- `references/runtime.md:119` 和 `scripts/check-feature-context.py:127-142` 要求唯一、真实、非 symlink memory root。

**最小复现：**`.agent-loop -> .memory` 后 Archive scan 返回 `0` 并生成 `.memory/features/...` move；没有在 scan 时进入规定的 Recovery。

**影响：**没有发现 project 外写入，且 Apply 的后续检查会失败/恢复；但 Agent/Human 会先获得不被其他控制面认可的 plan，产生无效 Gate 和恢复噪声。

**建议：**统一 Archive、Feature Context、Lightweight Change 的“exactly one real named root”事实采集。按软 Gate 边界，scan 应明确输出 root-symlink finding；Agent 不能把该 finding 作为可执行 exact plan 交给 Human，Apply 仍需在任何写入前强制拒绝。

### Medium — root managed-block checker 把“结构/版本一致”表述为“current”，无法发现正文篡改

**证据：**

- `scripts/check-root-agents-blocks.py:231-310` 检查 section、marker、block-version、local source path，不比较 body。
- `references/project-guidance.md:188-202` 要求 Agent 还比较 source facts 与 required sections。

**最小复现：**在临时 target `AGENTS.md` 中保持所有 marker 和 `block-version:1.5.3-20260728.1`，仅把 `load its published owner` 改成 `skip all published owners`；checker 返回：

```text
ROOT_BODY_DRIFT_RC 0
PASS root AGENTS managed blocks are current
```

**影响：**这不是直接的 Git/Feature Gate 绕过（运行时仍要求 Agent 读 published owner 并作 source comparison），但 `current` 输出过度表达，会让只看 checker 的 Agent 误信 bootstrap guidance 没有语义漂移。

**建议：**保持 checker 轻量、非授权：要么将 PASS 重命名为“markers/revisions structurally current”，要么只对 `source:agent-loop-skill` 的 template-owned block 计算 normalized body digest 并以 advisory `CHANGED` 输出；project-owned block 仍由 Agent 比较 source facts，不需要引入硬 Gate。

## 已确认的主流程不变量

- `CHANGED / 0` 不等于 `CURRENT` 或执行授权；Agent 必须评估、刷新派生 evidence 并重跑到 `CURRENT`。
- Product pending、Requirement deferred、ADR `review-required` 仍会停止下游 Feature reliance 并回到原有 owner/Gate。
- Gate 1 仅允许 package preparation；Gate 2 package-only 不执行；later-start 需要新的明确人类证据和当前边界核对。
- 新 Task 可替换初始清单，但必须仍映射到 accepted Story/Product Slice/Acceptance、通过 Plan/Analyze Consistency、且有 `within-approved-boundary` 评估。
- Task `done` 仍需要 fresh verification、review、drift 与 evidence link；行为变化不能用无理由 TDD `N/A` 代替 RED/GREEN。
- Pause 清除 current mode；Resume 需要新确认；Close、Submit、Commit、Push、Tag、Release 保持独立 Human Gates。
- Feature Context 的 Requirement/Product/ADR path escape、dual root、missing authority、plan hash drift、journal tamper、reference symlink 与项目外写入保护在既有回归中保持通过。

## 结论与下一步

本轮不修改源码，也没有 commit/push/tag。优先下一步应是先以 TDD 修复 High 的 Archive feature-directory symlink preflight/rollback 缺口；随后按人类对“checker 只做事实”的选择，处理两个 Medium（建议保持软 gate，而不是恢复语义硬 Gate）。修复后需重跑 Archive focused、全量 Shell/Python、机械检查和这一组最小 chaos replays。
