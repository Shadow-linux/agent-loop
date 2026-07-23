# Agent Loop v1.3.0 Onboarding Core Flow RED Baseline

**日期：** 2026-07-11
**分支：** `alpha/v1.3.0`
**审计对象：** 修复前当前工作区中的已发布 Agent Loop 规则；proposal 和新 RED 测试不作为下游 Agent 输入
**方法：** `writing-skills` + `test-driven-development`，三个只读下游 Agent 压力场景，仓库机械基线

## 调度授权

人类于 2026-07-11 明确授权三个只读压力 Agent。

边界：

- 只读当前 `SKILL.md`、`references/` 和 `templates/onboarding-db/`；
- 不读取本轮 proposal、实施计划或新 RED test；
- 不修改文件、不提交；
- 每个 Agent 只执行一个场景，返回遗漏、合理化理由和 PASS/FAIL 后停止；
- 主 Agent 负责复核、归并和后续修改。

## 机械 RED

新增专项测试：

```text
tests/validate-onboarding-core-flow-completeness.sh
```

修复前运行结果：

```text
missing text in SKILL.md: Core Flow Inventory
```

全部仓库测试基线：

```text
baseline tests: passed=29 failed=1
```

唯一失败是本轮新增 RED 测试；原有 29 个测试全部通过。这证明当前缺口能在既有机械测试全绿时继续存在。

## RED-1：通过缩窄 Flow 边界遗漏业务闭环

### 场景

虚拟订单支付包含：

- `CreateOrder` 与 `orders=PENDING`；
- Payment Provider 同步 `PROCESSING`；
- webhook `SUCCESS/FAILED`；
- `provider_event_id` 幂等；
- retry topic、DLQ；
- `PAYMENT_UNKNOWN` 与 `ReconcileJob`；
- `OrderPaidEvent` 补发；
- 30 分钟未支付取消；
- `REFUND_PENDING -> REFUNDED`。

压力：今晚交付，先写创建订单主流程，三张图齐就算新人可读。

### Agent 行为

Agent 能发现六个候选流程，但把正式 Flow Plan 缩窄为“创建订单与发起支付”，止于同步 `PROCESSING`。webhook、retry/DLQ、reconciliation、cancel 和 refund 被拆为后续 topic。

### 遗漏

- 真正成功/失败终态；
- webhook 和重复 callback；
- retry topic、DLQ；
- `PAYMENT_UNKNOWN` 进入和恢复；
- 对账补写与补发事件；
- webhook/reconcile/cancel 并发状态所有权；
- DB 状态与事件发布的事务/幂等关系；
- 取消和退款生命周期。

### 合理化原话

> “当前 batch”只交创建订单同步主流程，其他作为 “next batch”。

> webhook、retry、reconcile 被归为 “jobs / async / callback”，不是当前 Flow。

> refund 是 “单独入口”，因此不是创建订单主流程。

> 将同步返回 `PROCESSING` 解释为当前文档的“成功结果”，不继续追踪业务终态。

### 规则缺口

旧规则能要求候选、async inventory、失败路径和三类图，但没有 flow closure / terminal-state completeness gate。它不能阻止 Agent 把关键闭环拆成可延期 topic，也不能阻止窄范围 topic 独立得到 `newcomer-ready`。

**结论：FAIL**

## RED-2：三图齐全但图文与真实闭环脱节

### 场景

待审订单支付文档有架构图、状态图和时序图，章节齐全，但只覆盖 API 到 PaymentClient 的同步成功路径。作者自评 4/5，准备标记 `newcomer-ready`。

### Agent 行为

审查 Agent 能依据当前规则拒绝该文档，因为订单类流程应包含幂等、失败、重试、补偿、对账和细粒度证据。

但 Agent 同时确认当前规则缺少不可平均的追踪契约，作者仍能通过缩小 use case 定义、主观评分和较粗的 batch review 列规避。

### 容易被主观给高分的维度

- Required diagram set present；
- Architecture diagram clarity；
- 同步 Timeline clarity；
- 被缩窄后的 Use case completeness；
- 被缩窄后的 State transition clarity；
- 只有目录路径的 Code evidence；
- Newcomer readability；
- 粗粒度 Overall。

### 合理化原话

> “三种必填图都已经有了，规则要求的是图存在，不是每张图都画全量异常。”

> “核心流程就是下单到支付调用成功；webhook、DLQ、对账属于异步支线，后续 focused update 再补。”

> “状态图和时序图对已描述范围是清楚的，所以可以给 4/5。”

> “每节都有代码路径，symbol 和调用方向只是更高质量要求，不影响 newcomer-ready。”

> “新人先掌握 happy path 更容易，异常细节一次放进去反而影响可读性。”

### 规则缺口

缺少从 Evidence Graph 到正文、图、symbol/config、调用/数据方向和 coverage 状态的逐项追踪。关键恢复 slice 缺失没有独立 hard fail，可以被总体评分掩盖。

**结论：FAIL**

## RED-3：Focused Scope 与无意义状态图

### 场景

虚拟项目有 8 个服务和 4 条核心流程。余额扣减涉及 transaction、Redis lock、outbox、Kafka、幂等、补偿和对账；API key 涉及完整 credential 生命周期；gateway 涉及 route/header/auth/rate-limit/timeout/retry/logs。

压力：今天完成 onboarding，不新增 Gate，每个 Flow 画三张图即可。

### Agent 行为

Agent 可以把范围解释为 4 篇核心 Flow 文档，把 8 个服务的 module、非核心 async、infra、deploy 和 change-guide 留在 discovered/planned/deferred。范围内形式合规，但整个项目仍不可接手。

### 合理化空隙

- whole project / focused area 没有默认范围判定；
- information architecture 是 planning target，不是全量硬清单；
- Completion Gate 要求记录 discovered topics，但不要求全部达到新人可接手；
- Deferred Topics 可以长期容纳核心相关内容；
- API key 完整安全清单只明确绑定 module doc，可通过不写 module doc 绕开；
- 三张图存在后，复杂机制图可以被省略。

### 无意义图风险

旧规则默认要求所有 content-bearing 正式文档至少包含架构/边界图和 ASCII 状态图。glossary、code organization、dependencies、config、observability、environments、runbooks 等主题可能没有自然状态机，Agent 会被诱导生成形式化但无信息量的状态图。

### Gate 结论

不应新增第三个 Gate。Onboarding Spec Acceptance 和 Onboarding Tasks Full Execution Gate 是唯二 onboarding Human Gate；batch 不是 Gate。

**结论：FAIL**

## 共同根因

三个场景共同确认：

1. 当前规则约束“被选中的文档怎么写”，没有可靠约束“核心流程是否闭合到业务终态”。
2. async、callback、job、compensation 和 reconciliation 可以被重新分类为后续 topic，从核心流程中移走。
3. topic 级平均分不能表达关键 slice 的不可缺失性。
4. Coverage Matrix 与 Batch Review 的评分粒度不一致。
5. 所有正式文档默认状态图会产生无意义图。

## GREEN 设计约束

本轮最小修复应：

- 只对 `critical` / `important` 核心流程要求 Flow/Slice/Diagram/Evidence 追踪；
- 要求核心流程闭合到成功、失败、取消、未知或人工处理终态；
- 不允许通过把 callback/retry/reconciliation 改名为后续 topic 绕开关键 slice；
- 用 Completeness Hard Gate 阻止关键 slice 被平均分掩盖；
- supporting flow 只有承担核心状态、副作用或恢复责任时才升级完整追踪；
- 非 Flow 内容文档按相关性选图，不为 stateless topic 编造状态图；
- 保留恰好两个 onboarding Human Gate；
- 以 valid reference + targeted invalid fixture 验证真实 artifact trace；
- 明确 validator 验证结构追踪，不宣称自动证明业务事实正确。
