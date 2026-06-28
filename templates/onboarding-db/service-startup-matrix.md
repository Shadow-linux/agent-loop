# Service Startup Matrix

Document Language: 中文
Created:
Last Updated:
Last Verified:
Confidence:
Source Evidence:
Human Review Status: draft

## Purpose

记录每个 runnable service / process 怎么启动、依赖什么配置、如何判断启动成功或失败。Quick 可以有 unknown；Deep 必须把 required-core 服务补到 newcomer-ready 或明确 blocked。

## Startup Matrix

| Service / Process | Command | Config Path | Required Dependencies | Port / Protocol | Health / Failure Signal | Local Runnable? | Evidence | Confidence | Completion Status |
|---|---|---|---|---|---|---|---|---|---|

## Config / Environment Notes

| Config / Env | Used By | Meaning | Default / Example | Secret? | Evidence | Confidence | Completion Status |
|---|---|---|---|---|---|---|---|

Never write real secrets, tokens, passwords, or production connection strings.

## Verification

| Check | Command / Signal | What It Proves | Evidence | Confidence | Completion Status |
|---|---|---|---|---|---|

## Unknowns / Follow-up

| Unknown | Affected Service | Why It Matters | Needed Evidence | Completion Impact |
|---|---|---|---|---|
