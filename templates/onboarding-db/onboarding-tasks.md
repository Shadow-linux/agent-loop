# Onboarding Tasks

任务按 batch 组织，用于 Agent 自己安排执行、review 和记录进度。

人类确认 Onboarding Spec / Onboarding Tasks 后，计划确认后 Agent 可以全盘执行，可以一次性创建计划内的完整 onboarding-db。batch 是 Agent 的组织和 review 单位，不是人类闸门。

不创建空目录、薄 README、planned/later 占位文件、TBD/待补充文件。写不透但有证据可推断的内容，要写出“推断”、证据、置信度和待验证点；完全缺少关键证据时，只在 coverage/tasks 记录 planned / blocked，不落薄文档。

## Batch <n>: <name>

| Task | Output | Evidence Required | Quality Gate | Status |
|---|---|---|---|---|

## Current Batch Notes

-

## Full Execution Gate

- [ ] Onboarding Spec / Onboarding Tasks 已被人类确认。
- [ ] 全量 planned docs 和 execution scope 已明确。
- [ ] 每个输出文件都有 evidence required。
- [ ] 每个 module / flow task 都要求架构/边界图、ASCII 状态图、Timeline / 时序图。
- [ ] 普通流程图和时序图优先用 Mermaid flowchart / sequenceDiagram；状态机、复杂原理图和复杂示例图优先用 ASCII。
- [ ] 每个 task 都要求清除 `<...>`、TBD、TODO、待补充、空 required row、泛泛“看代码/see code”证据。
- [ ] 涉及 gateway / runtime 或一致性 / 幂等 / 补偿的 task 已明确质量门禁。

## Deferred Topics

| Topic | Reason Deferred | Needed Evidence | Planned Batch |
|---|---|---|---|
