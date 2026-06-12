# ai-meeting-minutes-backend Onboarding Test Example

本目录是 agent-loop 的真实项目抽样测试输出容器，不是目标项目代码副本。

## Source Project

| 项目 | 路径 |
|---|---|
| ai-meeting-minutes-backend | `/Users/shaodowyd/Desktop/workspace/yuanjing/jingshu@meeting/ai-meeting-minutes-backend` |

## Purpose

用于验证 agent-loop 的 onboarding 能力是否能面对真实后端项目完成：

- Quick / Deep / Targeted Onboarding 判断；
- root `AGENTS.md` / `CLAUDE.md` 引导检查；
- `.agent-loop/project.md` 候选长期记忆；
- onboarding-db 候选文档；
- 模块图、核心流程图、数据模型、异步任务、部署和风险说明；
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
    onboarding-db/
      README.md
      overview.md
      maps/
      modules/
      flows/
      runtime/
      domain/
      quality/
doctor-review/
  2026-06-09-onboarding-doctor-review.md
```

## Test Entry Prompts

| 场景 | Mock Human 输入 |
|---|---|
| Quick Onboarding | `Use agent-loop. 接管这个真实后端项目，我想快速知道怎么启动、怎么测试、下一步怎么继续。` |
| Deep Onboarding | `Use agent-loop. 对这个后端项目做 Deep Project Onboarding Scan，输出到 agent-loop examples。` |
| Targeted Onboarding | `Use agent-loop. 我只想理解会议纪要生成链路和 Celery 异步任务。` |
| Newcomer Guide | `Use agent-loop. 假设我是新人，请基于 onboarding-db 引导我接手这个项目。` |
| Doc Maintenance | `Use agent-loop. 检查这个 onboarding-db 是否缺少模块详解、流程图、数据模型或证据链。` |
