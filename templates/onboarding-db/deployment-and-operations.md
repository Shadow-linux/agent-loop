# Deployment And Operations

Document Language: 中文
Last Verified:
Confidence:
Source Evidence:
Human Review Status: draft

## Purpose

## Deployment Overview

## Environments

| Environment | Runtime | Deploy Trigger | Config Source | URL / Entry | Owner | Evidence | Confidence |
|---|---|---|---|---|---|---|---|

## Deployment Pipeline

| Step | Command / System | Working Directory | Preconditions | Rollback | Evidence | Confidence |
|---|---|---|---|---|---|---|

## Runtime Topology

## How To Read

```text
这张部署/运行图回答什么问题：
1. 本地、测试、生产环境分别有哪些服务、容器、数据库、队列或外部依赖。
2. 代码从提交到发布经过哪些系统。
3. 失败时如何回滚、如何观察健康状态。

怎么看：
- 先看 Deployment Pipeline。
- 再看 Runtime Topology 中的服务和依赖方向。
- 最后看 Release / Rollback、Health Checks、Logs / Metrics / Tracing。
```

## Step-by-Step Walkthrough: Deployment Flow

```text
1. 开发者在本地完成代码修改，推送到 Git 仓库的 feature 分支
2. CI/CD Pipeline 被触发，运行单元测试、集成测试、代码检查
3. 测试通过后，Docker 镜像被构建并推送到镜像仓库
4. 运维/自动化脚本将新镜像部署到 Staging 环境进行验证
5. Staging 验证通过后，执行数据库迁移（migrations）和种子数据更新
6. 健康检查（Health Checks）确认所有服务正常运行
7. 流量通过负载均衡器/网关逐步切换到新版本（蓝绿部署或滚动更新）
8. 发布完成后，监控系统（Logs / Metrics / Tracing）开始收集运行时数据
9. 如果发现异常，触发回滚（Rollback）流程：切换流量回旧版本，必要时回退数据库迁移
10. 最终确认生产环境稳定运行，发布流程结束
```

## Release / Rollback

## Migrations / Seeds

## Health Checks

## Logs / Metrics / Tracing

## Alerting Rules

**记录具体的告警规则。agent 必须知道"什么指标异常了"才能判断系统是否健康，也能避免重复配置冲突的告警。**

| Alert Name | Metric | Threshold | Severity | Notification Channel | Runbook / Action | Evidence | Confidence |
|---|---|---|---|---|---|---|---|
| API 错误率过高 | error_rate | > 1% | P1 | PagerDuty / 钉钉 | 查看日志，检查外部依赖 | | |
| API 响应时间过长 | p99_latency | > 2s | P2 | 钉钉 | 检查 DB 慢查询，检查缓存命中 | | |
| DB 连接池耗尽 | db_connections / max | > 80% | P0 | 电话 / PagerDuty | 扩容或检查连接泄漏 | | |
| 队列堆积 | queue_depth | > 1000 | P1 | 钉钉 | 检查 consumer 是否存活 | | |
| 外部服务失败率 | external_error_rate | > 5% | P2 | 钉钉 | 检查第三方状态页 | | |
| 磁盘空间不足 | disk_usage | > 85% | P1 | 钉钉 | 清理日志或扩容存储 | | |

## Incident Response

**记录常见故障的排查路径和应急操作。agent 遇到生产问题时能快速定位，而不是盲目重启。**

| Symptom | Likely Cause | Check These First | Quick Fix / Workaround | Escalation Path | Evidence | Confidence |
|---|---|---|---|---|---|---|
| 服务完全不可用 | 部署失败 / 配置错误 / 依赖宕机 | 健康检查状态、最近部署记录、依赖服务状态 | 回滚到上一个稳定版本 | oncall 工程师 | | |
| 响应变慢 | DB 慢查询 / 缓存失效 / 外部服务延迟 | 慢查询日志、缓存命中率、外部服务延迟 | 启用降级逻辑、增加缓存 TTL | 数据库管理员 | | |
| 数据不一致 | 并发写入冲突 / 异步任务失败 / 缓存未更新 | 状态流转记录、死信队列、缓存失效日志 | 手动修复数据、重新触发任务 | 数据团队 | | |
| 内存泄漏 | 未释放连接 / 大对象未清理 | 内存监控曲线、GC 日志、连接池状态 | 重启服务（临时）、修复泄漏代码 | SRE | | |

## Operational Access

| Entry | Purpose | Where | Safe Access Notes | Evidence | Confidence |
|---|---|---|---|---|---|

## Related Diagrams

## Evidence

## Unknowns

## Project Memory Backfill
