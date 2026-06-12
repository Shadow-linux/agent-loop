# State Flow: <entity>

Document Language: 中文
Created:
Last Updated:
Last Verified:
Confidence:
Source Evidence:
Human Review Status: draft

## Purpose

Explain the legal lifecycle states and transitions for one important entity or object.

## State Flow Diagram

Use a small state diagram for legal transitions only. Observed writers belong in `state-trace-<entity>.md`.

## How To Read

```text
这张状态图回答什么问题：
1. 实体有哪些合法状态。
2. 哪些触发条件允许状态转换。
3. 哪些状态是终止状态，哪些状态可以重试或回退。

怎么看：
- 先找初始状态。
- 顺着箭头看合法转换。
- 查看 Transitions 表确认 guard、side effect、failure/rollback。
- 如果问题是“谁写了这个状态”，转到 `state-trace-<entity>.md`。
```

## Step-by-Step Walkthrough: State Transitions

```text
1. 实体创建后进入初始状态（如 PENDING / 待处理）
2. 当触发条件 A 满足时（如"用户提交"），状态从 PENDING 转换为 PROCESSING（处理中）
3. 在 PROCESSING 状态下，系统执行 side effect（如启动后台任务、发送通知）
4. 当后台任务成功完成时，状态从 PROCESSING 转换为 COMPLETED（已完成）
5. 当触发条件 B 满足时（如"校验失败"或"任务超时"），状态从 PROCESSING 转换为 FAILED（失败）
6. 在 FAILED 状态下，可以选择重试（回到 PROCESSING）或人工介入
7. 当触发条件 C 满足时（如"用户取消"），状态从 PENDING 或 PROCESSING 转换为 CANCELLED（已取消）
8. CANCELLED 和 COMPLETED 是终止状态（Terminal），不再转换
```

## States

| State | Meaning | Entered When | Exits To | Terminal? | Evidence | Confidence |
|---|---|---|---|---|---|---|

## Transitions

| From | To | Trigger / Guard | Side Effects | Failure / Rollback | Evidence | Confidence |
|---|---|---|---|---|---|---|

## Related Flows And Modules

| Flow / Module | Role | Related Doc | Evidence | Confidence |
|---|---|---|---|---|

## Tests

| Test File / Command | What It Proves | Evidence | Confidence |
|---|---|---|---|

## Evidence Chain

| File Path | Symbol / Object | Parameters / Fields | Description | Proves | Confidence |
|---|---|---|---|---|---|

## Unknowns

| Item | Why It Matters | Evidence | Suggested Follow-Up |
|---|---|---|---|
