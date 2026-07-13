# Proposal: Cross-Platform Python Script Runtime

状态：已批准；已实现并通过 macOS 验证，待 Windows CI 与最终 Human Review

目标版本：v1.3.0 候选

创建时间：2026-07-13

## 摘要

Agent Loop 当前的发布脚本和验证脚本混合使用 Bash 与 Ruby。它们在当前 macOS 维护环境中可用，但不能作为原生 Windows 与 macOS 目标项目的共同运行基线。

本 proposal 建议把当前脚本逐步迁移为 Python 3 标准库实现，并建立统一的跨平台脚本契约。迁移完成后，Feature Monthly Compaction 等新的目标项目维护能力直接使用该基线，不再新增 Ruby、Bash 或平台专属实现。

核心顺序：

```text
冻结当前行为与 RED/PARITY 基线
→ 增加 Python 等价实现
→ 在 macOS 与 Windows 运行相同 fixture
→ 切换当前权威引用
→ 保留一版兼容入口
→ 后续再决定是否移除兼容入口
```

## 背景与问题

当前 `scripts/` 包含：

```text
scripts/check-root-agents-blocks.sh
scripts/check-adr-requirement-model-trace.rb
scripts/check-concept-foundation-trace.rb
scripts/check-onboarding-core-flow-coverage.rb
```

主要问题：

1. Windows 不保证存在 Ruby、Bash 或 POSIX 工具链；
2. macOS 中可发现的 Python 也不应被视为版本合格，需要 capability scan；
3. 继续为新能力增加 Ruby/Bash 会扩大平台差异；
4. 同一安全规则若分别用 Bash、PowerShell、Ruby 实现，容易发生行为漂移；
5. 脚本迁移若同时重写历史报告，会破坏过去验证证据的时间点语义。

## 目标

1. 当前分发脚本使用一份 Python 3 源码同时支持原生 Windows 与 macOS；
2. 默认只使用 Python 标准库，不要求 `pip install`；
3. 保持现有脚本的输入、输出语义、退出码和 Human Gate 边界；
4. 通过相同 fixtures 验证 Windows/macOS 行为一致；
5. 当前权威文档只引用新的 `.py` 路径；
6. 历史 proposal 和 report 保持原样；
7. 为 Feature Monthly Compaction 的发现、执行、恢复和后检脚本建立前置基线。

## 非目标

第一阶段不做：

- 不把全部 `tests/*.sh` 一次性改写为 Python；
- 不宣称整个维护仓库已经原生支持 Windows；
- 不自动安装 Python；
- 不引入 PyYAML、Click、Rich 或其他第三方包；
- 不实现通用 YAML parser；
- 不改变 Concept Foundation、ADR、Onboarding 或 root guidance checker 的业务规则；
- 不修改历史 `docs/reports/` 中记录的旧命令、旧路径和旧行号；
- 不因为迁移脚本而自动升级 Agent Loop 版本；
- 不在本 proposal 中实现 Feature Monthly Compaction。

## 方案比较

### 方案 A：Python 3 标准库单实现（推荐）

优点：

- Windows 与 macOS 使用同一源码；
- `pathlib`、`hashlib`、`json`、`tempfile`、`shutil` 足以覆盖当前需求；
- 文件系统、编码、退出码和测试行为易于统一；
- 不需要维护两套安全逻辑。

代价：

- 运行前必须探测 Python；
- 缺少合格 Python 时必须停止，不能降级为手工执行；
- 维护仓库现有 Bash 测试仍需阶段性保留。

### 方案 B：Bash + PowerShell 双实现

优点：每个平台可使用本地 shell。

缺点：核心规则重复，路径、正则、编码、退出码和回滚逻辑容易漂移，测试成本翻倍。

### 方案 C：预编译跨平台二进制

优点：目标机不需要 Python。

缺点：需要维护 Windows/macOS 多架构产物、构建链、校验和与发布流程，超出当前脚本规模。

## 决策

选择方案 A。

```text
Canonical runtime: Python 3.10+
Dependency policy: Python standard library only
Platform target: native Windows and macOS
Fallback: fail closed when no compatible interpreter exists
```

Python 不可用或版本不足时，Agent 可以报告缺失能力和安装方向，但不得：

- 自动安装 Python；
- 自动修改 PATH；
- 回退到 Agent 手工模拟脚本；
- 跳过预检、后检或完整性校验；
- 把“无法运行检查器”解释为检查通过。

## 脚本迁移范围

| Current | Canonical Python Target | Role |
|---|---|---|
| `scripts/check-root-agents-blocks.sh` | `scripts/check-root-agents-blocks.py` | 目标项目 root guidance 只读漂移检查 |
| `scripts/check-adr-requirement-model-trace.rb` | `scripts/check-adr-requirement-model-trace.py` | ADR Requirement Model trace 校验 |
| `scripts/check-concept-foundation-trace.rb` | `scripts/check-concept-foundation-trace.py` | Concept Foundation / Product Model trace 校验 |
| `scripts/check-onboarding-core-flow-coverage.rb` | `scripts/check-onboarding-core-flow-coverage.py` | Onboarding Core Flow coverage 校验 |

旧 `.sh` / `.rb` 入口在一个兼容周期内保留，但必须满足：

- 标记为 deprecated compatibility entry；
- 不再拥有独立业务规则；
- 只解析兼容调用并转交 Python canonical implementation；
- 找不到合格 Python 时明确失败；
- 当前权威文档不再推荐旧入口；
- 移除旧入口需要后续单独 Human Review。

## Python 标准库契约

允许的核心标准库包括：

```text
argparse
dataclasses
enum
hashlib
json
os
pathlib
re
shutil
subprocess
tempfile
unittest
```

Python canonical checker 不得调用或依赖：

```text
grep
sed
find
bash
shasum / sha256sum
git mv
PowerShell-only cmdlets
third-party Python packages
```

测试代码可以用标准库 `subprocess` 以当前 `sys.executable` 启动 checker。旧 `.sh` / `.rb` 兼容入口只负责解释器探测和参数转交，不属于 canonical implementation，不得承载检查规则。

如未来出现标准库无法满足的需求，必须先提交依赖 proposal，并经过 Human Review；脚本不得自行执行 `pip install`。

## 平台兼容契约

### 解释器发现

建议探测顺序：

```text
Windows: py -3 → python
macOS:   python3 → python
```

调用者必须验证实际解释器版本，而不是只验证命令名存在。Python 脚本内部不得依赖调用命令名称。

### 路径

- 文件系统路径一律使用 `pathlib.Path`；
- 不手工拼接 `/` 或 `\`；
- Markdown 中的仓库相对路径统一使用 `/`；
- 路径必须限制在声明的 project/workspace root 内；
- 在执行写操作前检查 Windows 大小写不敏感冲突；
- 不依赖 symlink、POSIX executable bit 或 POSIX permission semantics；
- 文件名不得包含 Windows 禁止字符。

### 文本与摘要

- 读取 Markdown 时兼容 UTF-8 与 UTF-8 BOM；
- 兼容 CRLF 与 LF；
- 内容摘要使用二进制读取与 SHA-256；
- 稳定输出必须使用确定性排序；
- 机器输出使用 JSON，Human Review 输出使用 Markdown/text；
- JSON 中的仓库相对路径统一使用 `/`。

### 文件操作

- 只读 checker 不得产生文件副作用；
- 未来的 mutation script 必须先生成确定性计划与摘要；
- 写操作使用临时路径、冲突检查和可验证替换；
- Windows 文件占用、权限失败或部分移动必须返回非零；
- 失败回滚必须包含在已确认执行计划中；
- 不提供绕过安全检查的 `--force`。

## YAML 边界

Python 标准库没有通用 YAML parser。

因此：

- 本轮四个 Markdown checker 不增加 YAML 依赖；
- `plugin.json` 使用标准库 `json` 校验；
- 若只需要检查 `SKILL.md` 当前稳定 frontmatter 字段，可建立严格、有限的字段检查器，但不得宣称支持通用 YAML；
- 当前维护侧的完整 YAML 解析命令不属于第一阶段目标项目脚本迁移范围；
- 是否替换维护侧完整 YAML parser，留给后续独立决定。

## 行为兼容与验证

每个 Python port 必须建立 parity matrix：

| Dimension | Requirement |
|---|---|
| Valid fixture | 新旧实现都 PASS |
| Invalid fixture | 新旧实现都 FAIL |
| Exit code | 成功/失败语义一致 |
| Required diagnostics | 关键错误类别一致 |
| Read-only behavior | 不产生文件变化 |
| Workspace confinement | 拒绝越界路径 |
| Determinism | 相同输入产生稳定排序与摘要 |
| Windows/macOS | 相同 fixture 结果一致 |

不得把旧脚本的偶然输出格式全部冻结成永久 API。实施前先区分：

- 必须兼容的参数、退出码、错误类别和安全结论；
- 可以改进但需同步测试与文档的人类可读措辞。

## 文档与引用迁移

当前权威表面中的旧脚本路径必须切换到 Python canonical path，包括适用的：

- `SKILL.md`；
- `Usage.md`；
- `references/project-guidance.md`；
- `references/workflow-checklists.md`；
- 当前维护指南中的现行命令；
- 对应回归测试和 fixture runner；
- `CHANGELOG.md` 当前开发版本章节。

以下内容保持原样：

- 已完成的 `docs/reports/`；
- 已完成 proposal 的历史实施计划和历史命令；
- 仅用于说明过去 RED/GREEN 过程的证据。

历史文件引用旧路径不表示当前运行时仍推荐旧脚本。

## 与 Feature Monthly Compaction 的关系

Feature Monthly Compaction 的生产脚本必须建立在本 proposal 的 Python 基线上：

```text
Cross-Platform Python Script Runtime accepted and implemented
→ current published checkers pass parity validation
→ Feature Monthly Compaction reader compatibility
→ compaction scan/apply/restore/post-check implementation
```

月度压缩不得以“Python port 还没完成”为理由回退到 Ruby、Bash 或 Agent 手工移动。

## 实施阶段

### Phase 1：Scope Lock 与 RED/PARITY 基线

- 固定四个脚本的有效/无效 fixture；
- 记录参数、退出码、错误类别和只读边界；
- 区分目标项目运行脚本与维护仓库测试入口；
- 证明 Windows 当前无法直接运行现有入口。

### Phase 2：Python Ports

- 使用 Python 3 标准库实现四个 canonical checker；
- 为路径越界、大小写冲突、CRLF、UTF-8 BOM 和确定性排序增加测试；
- 不修改原有业务规则。

### Phase 3：引用切换与兼容入口

- 当前权威文档切换到 `.py`；
- 测试主路径调用 Python canonical checker；
- 旧 `.sh` / `.rb` 变为兼容入口；
- Changelog 记录迁移和能力边界。

### Phase 4：双平台验证

- macOS 运行全部 port parity fixtures；
- Windows 运行相同 fixtures；
- 运行仓库要求的 focused/full validation；
- 保存中文验证报告；
- Human Review 决定是否允许 Feature Monthly Compaction 进入实现。

## 验收标准

- 四个 Python canonical checker 不依赖第三方包；
- macOS 与 Windows 对相同 fixtures 给出相同安全结论；
- 旧实现与 Python 实现对有效/无效 fixtures 保持 parity；
- 当前权威文档不再推荐 `.sh` / `.rb` 入口；
- 历史报告与历史 proposal 未被重写；
- 缺少合格 Python 时 fail closed；
- 没有 `--force`、自动安装或手工降级路径；
- root guidance checker 仍保持只读；
- ADR、Concept Foundation、Onboarding checker 没有弱化任何 hard gate；
- full validation 与跨平台验证报告均通过；
- 未经人类明确批准不修改版本号、不 commit、不发布。

## Human Review 决策

在实施前，人类需要确认：

| Decision | Recommendation |
|---|---|
| Runtime | Python 3.10+ 标准库 |
| Platform | 原生 Windows + macOS |
| Migration scope | 当前四个分发 checker |
| Existing tests | 第一阶段保留维护侧 `tests/*.sh`，增加跨平台 Python parity tests |
| Compatibility | 旧入口保留一个兼容周期 |
| Historical docs | 不修改 |
| Monthly compaction | 等本 proposal 实现并通过双平台验证后再实施 |
