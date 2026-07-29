# Agent Loop v1.5.3 全量验证报告

## 1. 审计对象与结论

- 日期：2026-07-28
- 分支：`v1.5.3`
- 基线 HEAD：`6086d7d6fc758221af2dee41ea269d0acf237795`
- 审计对象：当前未提交工作区中的 Feature Monthly Archive / Rehydrate Reference Scan 软 Gate、协调运行规则与 v1.5.3 版本同步
- 总分：**99.7 / 100**
- 等级：**STRONG**
- 当前缺陷：Critical 0、High 0、Medium 0
- 平台证据：`macOS-verified / Windows-test-defined`
- Git/发布状态：未 stage、未 commit、未 push、未 tag、未 PR、未 merge、未 release、未 publish、未同步 installed Skill

结论：Scanner/Checker 已从 Archive 业务授权者收敛为确定性事实与 exact-plan 生成器。Agent 负责检查路径、引用覆盖、冲突、风险和恢复条件；人类只授权最终 plan SHA-256；Apply/Restore 继续保留项目/计划物理边界、transaction journal、post-check 和 rollback。

## 2. RED 基线

修改前全量基线：

- Shell：46 / 46 PASS，约 9 秒；
- Python：320 / 320 PASS，85.399 秒；
- tracked 业务文件无 diff；已有 `.tmp/`、`scripts/__pycache__/`、`tests/__pycache__/` 未跟踪缓存未纳入本轮内容。

真实 focused RED：

```bash
python3 -m unittest tests.test_feature_monthly_archive_scan.FeatureMonthlyArchiveScanTests.test_internal_directory_symlink_is_reported_without_blocking_or_traversal
python3 -m unittest tests.test_feature_monthly_archive_apply.FeatureMonthlyArchiveCheckTests.test_unsupported_reference_is_advisory_for_exact_plan_apply
bash tests/validate-feature-archive-soft-gate.sh
```

结果：3 / 3 按目标原因失败。

- `.claude -> .agents`：`path-escape: symlinked directory cannot be reference-scanned`；
- 不确定引用：`reference-impact: unsupported references block apply`；
- 发布规则：`references/design.md` 缺少 finding 仅为证据、不是 Checker 授权的契约。

完整原始记录见 `docs/reports/agent-loop-v1.5.3-feature-archive-soft-gate-red-2026-07-28.md`。

## 3. GREEN 与回归结果

### Focused

```bash
python3 -m unittest \
  tests.test_feature_archive_support \
  tests.test_feature_monthly_archive_scan \
  tests.test_feature_monthly_archive_apply \
  tests.test_feature_monthly_archive_restore
bash tests/validate-feature-archive-soft-gate.sh
```

- Python：61 / 61 PASS，5.411 秒；
- Soft-Gate 跨 surface Shell contract：PASS；
- 相关 runtime、Checker Recovery、root guidance 合同：PASS。

新增覆盖：

- project-local directory alias 不跟随、只记录事实；
- canonical `.agents` Markdown 正常扫描且只生成一次 edit；
- external、broken、cyclic link 确定性记录且不泄露外部绝对路径；
- symlinked Markdown 不读取、不编辑；
- link target 改变使旧 plan SHA-256 失效；
- 已审阅普通 Markdown 被替换为 external symlink 后，Apply 在事务写入前返回 `stale-plan`，外部文件不变；
- `unsupported` 引用保持原文件不变，但不再成为 Checker 的 apply 授权结论；
- 原有 source/target、archive locator、journal、restore 与 path escape 负向控制继续通过。

### Mutation

三项短暂 mutation 均使目标回归测试按预期转 RED，随后已还原并重新跑 GREEN：

1. 恢复旧 `_markdown_files` symlink exception：internal alias 用例失败；
2. 恢复 `unsupported` apply rejection：advisory apply 用例失败；
3. 移除 archive locator project-boundary confinement：symlink escape 负向用例失败。

当前 diff 不含 mutation。

### 全量可执行测试

```bash
for test_file in tests/*.sh; do bash "$test_file"; done
python3 -m unittest discover -s tests -p 'test_*.py'
```

- Shell：47 / 47 PASS；
- Python：327 / 327 PASS，141.302 秒；
- 计数均由当前 `tests/` 实时枚举，不沿用历史报告。

## 4. 机械检查

全部通过：

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
python3 -m json.tool plugin.json >/dev/null
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
# 仓库 Markdown fence balance 检查
git diff --check
```

- `SKILL.md` YAML：PASS；
- `plugin.json` JSON：PASS；
- Shell syntax：PASS；
- Markdown fence：PASS；
- `git diff --check`：PASS；
- 本轮验证进程：无遗留。

## 5. 六域语义审计

| 审计域 | 结果 | 评分 | 通过证据 |
|---|---|---:|---|
| Logic Correctness | PASS | 100 | finding、Agent judgment、Human Gate、Apply correctness 四层职责无循环或授权复用；stale plan 在 mutation 前停止 |
| Autonomy | PASS | 100 | Agent 检查 canonical target、coverage、conflict、risk、recovery，并只能推荐 Gate 或问一个阻塞问题 |
| Project Entry / Evidence Graph + DDD Onboarding | PASS | 99 | Archive route 仍要求可靠 memory；root gateway 仅做 first hop；未改变 Onboarding 语义 |
| Development / Test Workflow | PASS | 100 | TDD RED/GREEN、focused、mutation、full regression 完整；Feature/Requirement/ADR/Submit Gate 未被软化 |
| Memory | PASS | 99 | Feature ID、`features/archive.md` locator、flat/month 唯一性、archive state 与 lifecycle 分离保持一致 |
| Recommendation | PASS | 100 | Scanner 不输出 `safe/approved`；Agent 输出唯一建议；Human 只批准 exact plan；无法判断时停止一个问题 |

加权总分：`99.7 / 100`。

## 6. 跨文件不变量

已核对并通过：

- `SKILL.md` 保持控制器入口；完整算法在 runtime/design/stage/artifact surfaces；
- `references/design.md` 与 `references/runtime.md` 同步更新，没有单 surface 改 Gate；
- root `AGENTS.md` 只增加简短导航语义，13 个 managed block revision 全部为 `1.5.3-20260728`；
- Archive/Rehydrate 不新增 canonical stage、message intent、lifecycle、schema、artifact 目录或 Auto Mode；
- Scanner 不跟随 symlink，不把 external absolute target 写入正常输出；
- finding 参与确定性 plan hash，但不承担 `accept/reject` 语义；
- Batch Human Gate 仍绑定 exact plan SHA-256，Auto Mode 不授权 Apply；
- Apply/Restore 仍只执行 plan 内、project 内路径，保留 journal、backup、post-check、rollback 与 stranded transaction Recovery；
- original human requirement sources 仍不可重写；
- Feature Gates、Project Skill Execution Gate、Delivery Contract、Submit、commit、push、tag、release/publish Gate 未改变；
- 普通 Archive finding 不进入 Checker Recovery；真实 checker implementation contradiction 或 environment failure 仍保留原恢复路径。

## 7. 压力场景

本轮新场景均通过：internal alias、external/broken/cycle alias、symlinked Markdown、ambiguous old path、finding drift、external write attempt、transaction rollback。

全量既有场景也保持通过：

- Standard Product Definition -> Decision Scan -> ADR -> Feature Product Slice；
- Brief Product Definition -> 无 ADR Feature Product Slice；
- Product Human Review 与 Requirement ownership；
- Delivery Contract Human Gate；
- TDD RED 与非行为型 `N/A`；
- Active/Pause/Resume/Close/Reopen；
- multi-phase `partially-implemented`；
- accepted ADR drift；
- Follow-up investigate-first 与 archived Feature locator；
- Submit/Integrate blocker 顺序；
- stale-memory、root guidance、Project Entry；
- Chat 不创建工作流产物。

## 8. 当前问题、剩余风险与范围漂移

当前逻辑问题：无 Critical、High、Medium。

剩余风险：

- Low：本地仅验证 macOS；Windows 使用 Python 3.10+ 标准库路径与跨平台 unittest 定义覆盖，但本轮没有实际 Windows runner 结果。因此结论明确为 `macOS-verified / Windows-test-defined`，不声称 Windows 已实机验收。
- Scanner 仍需要遍历普通项目 Markdown，性能与 Markdown 文件数量/大小线性相关；它不进入 symlink 目录，2 MiB 上限文件只记录 advisory，未引入额外深度遍历。

范围漂移检查：无。未改变 Feature candidate lifecycle/readiness、Feature Gate、Requirement/ADR、Bug、Project Skill、Git 或 release 语义；未增加第三方依赖、`--force`、自动归档、删除、压缩或项目外写入。

## 9. 版本与发布判断

- `SKILL.md`、`plugin.json`、`README.md`、`Usage.md`、`CHANGELOG.md` 已同步为 1.5.3 开发线；
- 13 个 root managed blocks 已同步 `block-version:1.5.3-20260728`；
- 历史稳定安装示例继续指向 `stable-v1.5.2`，因为本轮没有获得或执行 1.5.3 tag/release 授权；
- 当前实现满足进入 Human Review 的条件；只有人类后续明确授权，才能 stage/commit/push/tag/release 或同步 installed Skill。
