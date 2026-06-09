# Setup And Run

Document Language: 中文
Last Verified:
Confidence:
Source Evidence:
Human Review Status: draft

## Purpose

## Prerequisites

## Install Dependencies

## Required Services

## Local Run Commands

| Command | Purpose | Working Directory | Evidence | Last Run | Result | Confidence |
|---|---|---|---|---|---|---|

## Ports And URLs

| Port / URL | Purpose | Evidence | Confidence |
|---|---|---|---|

## Configuration Guide

**记录关键配置项、热更新能力、开发/生产差异。agent 改配置时必须知道哪些需要重启、哪些是敏感信息。**

| Config Item | Purpose | Dev Default | Prod Source | Hot Reload? | Sensitive? | Evidence | Confidence |
|---|---|---|---|---|---|---|---|
| DATABASE_URL | 数据库连接 | localhost:5432 | k8s secret / env | ❌ 需重启 | ✅ | | |
| REDIS_URL | 缓存连接 | localhost:6379 | k8s secret / env | ❌ 需重启 | ✅ | | |
| LOG_LEVEL | 日志级别 | DEBUG | INFO | ✅ 热更新 | ❌ | | |
| MAX_WORKERS | worker 数量 | 2 | 10 | ❌ 需重启 | ❌ | | |
| EXTERNAL_API_KEY | 第三方 API 密钥 | test-key | vault / secret manager | ❌ 需重启 | ✅ | | |

**配置优先级**（从高到低）：环境变量 > 配置文件 > 代码默认值

**敏感配置管理**：
- 生产环境的敏感配置必须来自 vault / secret manager / k8s secret，禁止硬编码
- 开发环境的敏感配置可以用 `.env` 文件，但必须被 `.gitignore`

## Dev vs Prod Differences

| Aspect | Dev | Prod | Notes |
|---|---|---|---|
| Debug mode | 开启 | 关闭 | 生产关闭 debug，避免信息泄露 |
| Log level | DEBUG | INFO / WARN | 生产减少日志量 |
| Mock external services | 可开启 | 不可开启 | 生产必须调用真实服务 |
| DB migration | auto / 手动 | 手动 + review | 生产迁移必须人工确认 |
| Feature flags | 全部开启 | 按灰度开启 | 生产用 feature flag 控制新功能 |

## Deployment Notes

Use this only for compact/basic deployment notes. Complex production deployment belongs in `deployment-and-operations.md`.

## Common Startup Failures

| Symptom / Error | Likely Cause | Check | Fix / Workaround | Evidence | Confidence |
|---|---|---|---|---|---|

If the human reports that these setup docs do not work, use `onboarding-diagnostics.md` Startup Failure Diagnosis before editing this file.

## Verification After Startup

## Evidence

## Unknowns

## Project Memory Backfill
