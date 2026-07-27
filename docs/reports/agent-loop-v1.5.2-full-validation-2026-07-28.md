# Agent Loop v1.5.2 全量验证报告

## 摘要

- 日期：2026-07-28
- 分支：`v1.5.2`
- HEAD：`9a5c5183b47c022e8851f1098697f902e9d38daa`
- 审计对象：当前 dirty working tree，不以 HEAD 或历史报告冒充当前结果
- 总分：**98 / 100 — STRONG**
- 当前严重度：Critical `0`、High `0`、Medium `0`、Low `0`
- Shell 回归：45 / 45 PASS
- Python 回归：320 / 320 PASS
- Feature 专项：97 / 100；双 Agent 独立评分 96 / 100 与 98 / 100

## 审计边界

本次是 Agent Loop skill source repository 维护验证。未在仓库根目录创建目标项目 `.agent-loop/`，未同步 installed Skill，未修改 Skill 版本 `1.5.2`，未执行任何 Git 或发布动作。

当前工作区在本轮开始前已有大范围获批但未提交改动。本报告审计完整当前工作树；本轮保留所有无关修改，不恢复、覆盖、暂存或提交它们。

## 六域评分

| 审计域 | 分数 | 结果 | 当前证据 |
|---|---:|---|---|
| Logic Correctness | 98 | PASS | Gate 2 baseline、Later Start event、live Gate Mode 无冲突；独立 Gate 不继承 |
| Autonomy | 98 | PASS | Agent 直接读事实和判断语义；无本地 Feature Gate authorization issuer |
| Project Entry / Evidence Graph + DDD Onboarding | 97 | PASS | root Gate Modes 与 project guidance 同步；13 个 block revision 一致 |
| Development / Test Workflow | 98 | PASS | Gate 1/2、Plan/No-Plan、TDD、Verify/Review/Drift/Memory/Close 回归通过 |
| Memory | 98 | PASS | 原 Gate 2 review baseline、Later Start evidence 与当前 Gate Mode 分工明确 |
| Recommendation | 98 | PASS | package-only、approve-and-start、later-start 与 drift 路由均给出唯一下一步 |
| **加权总分** | **98** | **STRONG** | Critical/High/Medium 均为 0 |

## 关键跨文件不变量

- `SKILL.md` 保持简洁入口，详细 Feature Gate 行为由 runtime/design/reference 承载。
- root `AGENTS.md` 模板只投影 Gate 导航；完整 leaf-stage order 仍由 `references/runtime.md` 负责。
- Gate 1 只授权 package preparation，不授权 target implementation。
- Gate 2 仅两个 approval choice 设置 accepted；package-only 不执行。
- Later Start 是独立 transition，不是第三个 Gate 2，也不覆盖原 Gate 2 baseline。
- current project `Gate Mode` 是 live execution-mode pointer；Feature notes 保存 durable review/event evidence。
- Feature Gate acceptance 与 continuation 不依赖 digest、Stable Digest、`EVIDENCE_*`、local checker 或 preflight。
- Task ID 变化不是自动重复 Gate 2 的理由；Story/Product Slice/Acceptance 或 execution boundary 变化仍返回 owning Gate。
- Delivery Contract、subagent、external mutation、Submit、Pause/Close、Git 与 release/publish 保持独立 Human Gate。
- Feature Completion 仍要求 fresh verification、Review、Drift Check、project-memory evidence 和 Close Review。

## RED / GREEN 证据

RED 报告：`docs/reports/agent-loop-v1.5.2-later-start-light-gate-red-2026-07-28.md`。

- 旧全量 suite 为绿色但未覆盖 Later Start 持久化冲突。
- focused RED 真实暴露 Later Start 三字段缺失、Gate 2 baseline 改写、无落点 Gate 1 SHA 和 root 投影缺口。
- 修复后 focused Python 13 / 13、focused Shell、root Python 14 / 14 及 root Shell contracts 全部 PASS。
- 4 个关键反向 mutation 均使 Python 与 Shell 转 RED，证明正确重复文本不能掩盖 owning section 退化。

## 全量回归

执行：

```bash
for test in tests/*.sh; do bash "$test"; done
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -q
```

结果：

```text
Shell: 45 / 45 PASS
Python: 320 / 320 PASS
```

最终发布文档校准后再次从头执行：Shell 45 / 45 PASS，Python 320 / 320 PASS；Python 最终运行 109.399 秒。测试数量为本轮实时统计和执行结果，不沿用旧报告。

## 压力场景

- 复杂与简单 Requirement 到 Product Definition、Decision/ADR、Feature Product Slice 的既有回归保持通过。
- Gate 1 → package preparation → Gate 2 → approve-and-start 正常闭环。
- package-only → context loss → later-start 仅在 current context、当前 package、可靠 Human evidence 与无新 stop 时继续。
- package drift 按 `within-approved-boundary | feature-definition-change | implementation-boundary-change | unresolved` 路由。
- accepted Story 内 Task 新增、减少或全部替换不被 ID 机械阻断；新 Story/Acceptance 或边界变化返回 Gate 2。
- Plan、No-Plan、漏 detail 文件、验证失败、Pause/Resume、Close/Reopen、Submit/Integrate 与独立 Git Gates 保持 fail closed。
- root guidance 删除 Later Start 或 project template 删除 Gate Mode 时，focused contracts 转 RED。
- 双 Agent 共给出 55 个正向生命周期场景、4 个关键负控和 21 个授权 mutation；全部符合预期。

## 机械检查

- `SKILL.md` YAML：PASS
- JSON parse：3 / 3 PASS
- Shell syntax：46 / 46 PASS
- Python AST：46 / 46 PASS
- Markdown fence：写入报告前 317 / 317 PASS；写入报告后 319 / 319 PASS
- `git diff --check`：PASS

## 当前问题与未采纳意见

当前没有未解决 finding。

未采纳“恢复或增强 Feature Gate Checker”的方向：Human authorization、package completeness 和 semantic drift 不能可靠降格为字符串或 digest 判定。当前策略只用自动测试守住客观结构与明确相反规则，其余由 Agent 依据现有证据核对，符合本轮轻量 Gate 目标。

## 发布判断

当前工作树达到 STRONG，可进入 Human Review。由于工作区包含多轮尚未提交的获批修改，本报告不授权也未执行 stage、commit、push、tag、PR、merge、release 或 publish；后续 Git 动作仍需独立人类确认。
