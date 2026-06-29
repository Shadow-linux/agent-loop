# ai-meeting-minutes-backend Legacy Onboarding Test Example

本目录是 agent-loop 的真实项目抽样测试输出容器，不是目标项目代码副本。

当前状态：本目录只保留为旧 Project Entry Scan / legacy-disabled 行为的历史样本和回归参考，不能作为当前 Evidence-Graph + DDD Onboarding 生成规范。

## Source Project

| 项目 | 路径 |
|---|---|
| ai-meeting-minutes-backend | `/Users/shaodowyd/Desktop/workspace/yuanjing/jingshu@meeting/ai-meeting-minutes-backend` |

## Purpose

用于验证 agent-loop 面对真实后端项目时是否能正确执行 Project Entry Scan / legacy-disabled 行为：

- 不再提供 Quick / Deep / Targeted Onboarding；
- 不再生成旧 onboarding-db、deep-dive docs 或 onboarding diagrams；
- 当前新人知识库应改用 Evidence-Graph + DDD Onboarding reference 和 `templates/onboarding-db/` 模板；
- root `AGENTS.md` / `CLAUDE.md` 引导检查；
- `.agent-loop/project.md` 候选长期记忆；
- 命令、边界、能力、未知项的证据和置信度；
- legacy onboarding-db 样本只作为历史证据；
- Doctor Agent 审查和 validation report 汇总。

## Write Rules

| 规则 | 说明 |
|---|---|
| 不复制真实代码 | 本目录只保存测试输出和文档样本 |
| 真实项目只读 | 默认不修改 source project |
| 证据写路径 | 文档中的 evidence 应引用 source project 的文件路径、函数、对象、命令或配置 |
| 不贴大段源码 | 可以摘录少量符号、函数名、参数、配置键，但不复制完整源文件 |
| 写入需确认 | 生成 candidate output、doctor review、validation report 前需要人类确认 |

## Suggested Layout

```text
validation/
  2026-06-09-onboarding-sample-report.md
candidate-output/
  .agent-loop/
    project.md
doctor-review/
  2026-06-09-onboarding-doctor-review.md
```

## Test Entry Prompts

| 场景 | Mock Human 输入 |
|---|---|
| Project Entry Scan | `Use agent-loop. 接管这个真实后端项目，我想快速知道怎么启动、怎么测试、下一步怎么继续。` |
| Legacy Disabled | `Use agent-loop. 对这个后端项目做 Deep Project Onboarding Scan，输出到 agent-loop examples。` |
| Focused Understanding | `Use agent-loop. 我只想理解会议纪要生成链路和 Celery 异步任务。` |
| Missing Legacy Docs | `Use agent-loop. project.md 说 onboarding-db 存在，但 README.md 找不到。` |
