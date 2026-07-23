# Agent Loop v1.4.0 Project Skill Discovery Guard RED Baseline

## 审计对象

- 日期：2026-07-16
- 分支：`alpha/v1.4.0`
- 基线提交：`c0221694734b25e053efb4b490c7efdd5468a203`
- Skill 版本：`1.4.0`
- 审计对象：加入 focused test 后、修改 runtime/design 前的当前工作区
- 维护视角：Agent Loop Skill source repository；未创建目标项目 `.agent-loop/`

## 工作区边界

Task 0 基线只有三份未跟踪 Proposal/Plan 文档：

- `docs/proposal/v1.4.x/post-merge-memory-reconciliation.md`，无关人类工作，保护 SHA-256 为 `612df36b0c3b2954cd1ba0d02ab19ca1ba967cf4361720b585079bd867bb8b7e`；
- `docs/proposal/v1.4.x/project-skill-discovery-guard.md`；
- `docs/proposal/v1.4.x/project-skill-discovery-guard-implementation-plan.md`。

本轮 RED 新增：

- `tests/validate-project-skill-discovery-guard.sh`。

## 修改前机械基线

修改前实时统计 `tests/*.sh` 为 36 个。执行：

```bash
for test_file in tests/*.sh; do bash "$test_file"; done
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
git diff --check
```

结果：

- 原有 shell tests：`36/36 PASS`；
- `SKILL.md` YAML：PASS；
- Shell 语法：PASS；
- `git diff --check`：PASS。

因此后续 focused RED 不是已有基线故障造成。

## 现有能力

当前规则已经具备：

- Project Entry、Resume、Re-Adopt、context recovery 和 controller re-entry 时读取 `.agent-loop/skills/INDEX.md`；
- `active`、`bootstrap | on-demand`、精确 INDEX row 和 SHA-256 Validated Content Manifest；
- `proposed | disabled | deprecated` 排除规则；
- 每次 Project Skill 调用的 Execution Gate；
- Project Skill 不进行全局安装。

这些能力不能证明新的 actionable intent 会在 generic Operational Support/fallback 前先运行项目 Skill 匹配。

## RED 命令与实际失败

新增 focused contract 后、修改任何运行规则前执行：

```bash
bash tests/validate-project-skill-discovery-guard.sh
```

实际结果：退出码 `1`。

```text
FAIL: SKILL.md missing required text: Project Skill Discovery Guard
```

该失败符合预期：测试脚本已正常启动，并在第一个缺失的 controller contract 上失败，而不是因为 Bash/Ruby 语法、路径或 fixture 错误失败。

## 缺口结论

当前 runtime 没有把以下顺序固化成不可绕过的跨文件 contract：

```text
new actionable intent
-> Project Skill INDEX metadata match
-> matched row/path/manifest validation
-> matched Skill read-only load
-> Execution Gate
-> stage action

no match
-> generic fallback
```

因此 Agent 仍可能把 runtime/global Skill inventory 错误解释为项目 Skill inventory，先声称“没有相关 Skill”或先启动通用 Operational Support 动作，等人类提醒后才检查项目 INDEX。

## 非缺口

本轮不重新设计：

- Project Skill lifecycle；
- `bootstrap | on-demand` Load Policy；
- Validated Content Manifest；
- Gate 1；
- Execution Gate；
- Project Skill 目标项目路径；
- canonical stage 或 message intent。

## 预期 GREEN

GREEN 必须证明：

- `matched-active` 早于 generic fallback，并仍停在 Execution Gate；
- `index-absent | no-active-match` 才允许 generic fallback；
- `project-skill-drift` fail closed，不能用等价通用动作绕过；
- runtime/global inventory 不能支持 Project Skill negative claim；
- 只加载匹配 Skill，不全量加载所有正文；
- root guidance 只保留一句短路由；
- 普通 chat 不产生额外 artifact 或全量扫描；
- Skill 版本仍为 `1.4.0`，且没有 commit、push、tag、PR、merge、release、publish 或安装同步。
