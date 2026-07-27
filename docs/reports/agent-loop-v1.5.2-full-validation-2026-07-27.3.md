# Agent Loop v1.5.2 全量验证报告（第三轮 Feature Gate Chaos Repair）

日期：2026-07-27
分支：`v1.5.2`
版本：`1.5.2`（开发中，未发布）
基线 HEAD：`9a5c5183b47c022e8851f1098697f902e9d38daa`
审计对象：AI-Led Lightweight Feature Gates 第三轮 chaos 修复后的当前未提交工作区

## 结论

总分：**99 / 100 — STRONG**
当前发现：**Critical 0 / High 0 / Medium 0 / Low 2**
回归结果：**Shell 45 / 45 PASS；Python 339 / 339 PASS**
focused：**Feature checker + Python checker contract 51 / 51 PASS；Two-Gate Shell contract PASS**
chaos：**deterministic evidence 79 / 79 PASS；lifecycle executable 31 / 31 PASS；lifecycle semantic matrix 51 / 51 PASS**
平台证据：**macOS-verified / Windows-test-defined**
判断：当前实现可进入最终 Human Review；本报告不授权 commit、push、tag 或发布。

本轮没有恢复重型 Checker。AI 继续负责 Human provenance、Task/Story/Plan/No-Plan、Assessment 和执行边界语义；Checker 只补齐能让 manifest/digest 可信的确定性边界。

## RED → GREEN

第三轮 chaos 修复前新增并实际观察：

- 6 个 focused Checker RED：**30 tests / 6 failures**；
- 1 个 coordinated Shell RED：在 `raw-v1` legacy 冲突处失败；
- 1 个诊断噪音 micro RED：非法 UTF-8 输出 12 条 `EVIDENCE_INVALID`，期望 1 条。

对应缺口：

1. Stable Files 可遗漏 Package 中显式列出的非 Plan 文件；
2. 非 UTF-8 `notes.md` 抛 traceback；
3. 空 manifest item 被静默删除；
4. 大小写变体或 hard-link same-file alias 未识别；
5. 带尾随非空白文本的 fence 行被错误当作 closing；
6. POSIX 主机不识别 Windows drive-absolute path；
7. `raw-v1` 新默认与 legacy 文案冲突；
8. Pause 后 durable Gate pair 与 current mode 没有唯一持久化方法；
9. inline notes 模板缺少 Gate Drift Assessment。

GREEN 结果：

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_feature_review tests.test_python_checker_contract
# Ran 51 tests — OK

PYTHONDONTWRITEBYTECODE=1 bash \
  tests/validate-feature-construction-two-gate-review.sh
# PASS

PYTHONDONTWRITEBYTECODE=1 python3 \
  /tmp/agent-loop-evidence-chaos-3-harness.py
# total=79 pass=79 fail=0

PYTHONDONTWRITEBYTECODE=1 python3 \
  /tmp/agent-loop-lifecycle-chaos-3-run.py
# total=31 pass=31 fail=0
```

完整 RED 历史见 `docs/reports/agent-loop-v1.5.2-feature-gate-chaos-repair-red-2026-07-27.md`。

## 实际修复

- Stable Files 现在必须等于显式 Package Files 的 non-Plan closure，并继续覆盖 discovered core/detail artifacts。
- `notes.md` 解码错误输出单条结构化 `EVIDENCE_INVALID`，不再 traceback 或附带缺字段噪音。
- manifest 的空项不再被静默丢弃。
- resolved-target alias 使用 filesystem identity 判定，覆盖大小写不敏感文件系统和 hard links。
- Markdown fence 只有相同字符、足够长度且尾部仅空白时才能关闭。
- `PureWindowsPath.drive` 让 Windows drive path 在任何宿主上都 fail closed。
- `raw-v1` 明确为新证据默认；只有显式 `review-definition-v2` 是 reader-compatible legacy。
- Gate 2 decision/Auto-Loop pair 明确为 durable review history；Pause 通过 project `Gate Mode: Strict Mode` 清除 live grant，Resume 重新确认适用模式，不重写历史 Gate pair。
- direct/inline notes 模板都包含相同 Gate Drift Assessment 结构。

## 全量回归

最终代码和文档完成后重新统计并执行：

```text
for test_file in tests/*.sh; do bash "$test_file"; done
# SHELL_TEST_FILES_PASS=45

TMPDIR=/tmp/agent-loop-full-python-final \
PYTHONDONTWRITEBYTECODE=1 \
python3 -m unittest discover -s tests -p 'test_*.py' -q
# Ran 339 tests in 85.060s
# OK
```

Python 从上一份报告的 333 增至 339，正好对应 6 个新增 Checker regression；没有跳过或删除其他测试。

## 机械检查

| 检查 | 结果 |
|---|---|
| `SKILL.md` YAML | PASS |
| `plugin.json` JSON | PASS |
| Shell syntax | 46 / 46 PASS |
| Ruby syntax | 5 / 5 PASS |
| Python AST | 47 / 47 PASS |
| Markdown fence | 310 / 310 PASS |
| `git diff --check` | PASS |
| root AGENTS 行数 | 176 |
| root managed blocks | 13 / 13，revision `1.5.2-20260727.2` |

## 六域语义审计

| 审计域 | 分数 | 结果与证据 |
|---|---:|---|
| Logic Correctness | 100 | Gate/action pair、manifest closure、path identity、digest 与 changed/invalid 分流唯一；修复后无矛盾路由 |
| Autonomy | 100 | AI 可处理 within-boundary 与事实性 evidence repair；Checker 不抢占语义或制造额外 Human Gate |
| Project Entry / Evidence Graph + DDD Onboarding | 99 | Requirement/ADR/Feature Context、root guidance、Onboarding 权威与入口均未改变，相关全仓测试通过 |
| Development / Test Workflow | 100 | Gate 1/2、Plan、TDD、Task Done、Verify/Review/Drift、Pause/Resume/Close 与独立 action gates 保持 |
| Memory | 99 | durable Gate pair 与 live project Gate Mode 分离；Accepted Stories、initial Tasks、Assessment 仍由 Agent 维护，无新 artifact family |
| Recommendation | 100 | MATCH 继续语义检查、CHANGED 进入 AI review、INVALID 仅事实修复；真实边界变化仍返回 owning Gate |

加权总分：**99 / 100**。

## 通过的不变量与压力场景

1. Gate 1 与 Gate 2 数量、Human choices 和授权边界未变化。
2. package-only review/start 与 approve-and-start execute 正常路径均 `EVIDENCE_MATCH`，没有正常路径 false positive。
3. Task 增删、取消、拆分、合并、Plan rotation、No-Plan 与 Assessment 语义仍由 AI 决定，不由 Checker 猜测。
4. Stable 覆盖每个非 Plan Package 文件；Plan 仍可在 accepted boundary 内轮换。
5. 缺文件、危险路径、same-file alias、symlink、root escape、非普通文件、空项、invalid UTF-8、malformed fence 均确定性阻断。
6. macOS 上的 `C:/...` 证据路径也被按 Windows absolute path 拒绝。
7. Pause 不再需要破坏 accepted Gate pair；live grant 在 project Gate Mode 中清除，Resume 默认 Strict。
8. Delivery Contract、Human-gated Task、Subagent、Git、external、Submit、Pause、Close、commit、PR、merge、tag、release、publish Gates 未继承或删除。
9. Requirement、ADR、Product Slice、Feature Context、Task Done、Completion 与 memory ownership 未改变。
10. 未新增 canonical stage、message intent、lifecycle、Auto Mode、artifact family 或 executable schema。

## 未采纳 / 降级意见

- 不把 Task/Story/Plan/No-Plan/Assessment parser 加回 Checker；这些属于 Agent 语义职责。
- 不设计防御恶意 AI 同时伪造所有本地证据的授权签发系统；Human provenance 仍来自可靠会话或保留证据。
- 不将 Pause 实现为重写 accepted Gate 2 pair；durable review history 和 live mode 分开持久化。

## 剩余 Low 风险

- **Low-1：信任模型边界。** 轻量模型依赖运行 Agent 遵守 runtime 并读取真实会话，不抵抗恶意 Agent 同时伪造本地状态；这是人类已确认的设计取舍。
- **Low-2：Windows 实机证据。** Python 3.10+、`PureWindowsPath` 与 Windows 路径场景有自动测试，但本轮仍未取得 Windows runner 实机结果。

## 范围与工作区保护

- 没有创建目标项目 `.agent-loop/`。
- 没有创建或切换分支/worktree，没有同步 installed Skill。
- 保留所有既有 dirty/untracked 内容；本轮只在批准的 Feature Gate 源码、契约、Proposal/Plan 与报告上增量修改。
- 版本保持 `1.5.2`；root revision 保持 `1.5.2-20260727.2`。

## Git 与发布

未执行 `git add`、commit、push、tag、PR、merge、release、publish、`main` 同步或 installed Skill 同步。
