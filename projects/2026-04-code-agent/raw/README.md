# raw/

项目专属原始资料。两个核心知识源：

## 1. learn-claude-code/（shareAI-lab）

来源：https://github.com/shareAI-lab/learn-claude-code（57k+ stars）

"Bash is all you need" 的哲学课 + 12 课递进式最小 Python 实现。
每一课只加一个 harness 机制，循环本身始终不变。

| 文件 | 主题 |
|------|------|
| `README-zh.md` | 哲学总纲：Agent = Model + Harness |
| `s01-the-agent-loop.md` | 最小循环（~30 行 Python）|
| `s02-tool-use.md` | dispatch map + 路径沙箱 |
| `s03-todo-write.md` | 带状态的规划 + nag reminder |
| `s04-subagent.md` | 子代理上下文隔离 |
| `s05-skill-loading.md` | 两层注入：名称列表 + 按需内容 |
| `s06-context-compact.md` | 三层压缩（micro/auto/manual）|
| `s07-task-system.md` | 磁盘持久化任务 DAG |
| `s08-background-tasks.md` | 后台线程 + 通知队列 |
| `s09-agent-teams.md` | 持久化队友 + JSONL 邮箱 |
| `s10-team-protocols.md` | request-response FSM |
| `s11-autonomous-agents.md` | 自治扫看板认领 |
| `s12-worktree-task-isolation.md` | Git worktree 并行隔离 |

## 2. cc-haha/（NanmiCoder）

来源：https://github.com/NanmiCoder/cc-haha

基于 Claude Code 泄露源码的本地可运行版本 + 生产级实现文档。
对 learn-claude-code 的 Python 最小实现做**TypeScript 工业级对照**。

| 文件 | 对应 learn-claude-code 章节 | 内容 |
|------|-----------------------------|------|
| `agent-02-implementation.md` | s04, s09-s12 | 多 Agent 系统：四条生成路径、Swarm、邮箱、DreamTask、Worktree |
| `agent-03-framework.md` | s04, s09 | Agent 框架接口层实现 |
| `memory-02-implementation.md` | s06 | 记忆系统：自动提取 + 分叉代理 + 智能检索 |
| `skills-02-implementation.md` | s05 | Skills：6 种来源、去重、延迟提取、条件激活 |
| `channel-01-channel-system.md` | —（扩展）| IM 远程控制 Agent（Telegram / 飞书）|
| `features-computer-use-architecture.md` | —（扩展）| Computer Use：6 层架构、9 层安全关卡、Python Bridge |
| `index.md` | — | 文档导航 |
| `reference-project-structure.md` | — | 项目结构索引 |
| `README.md` | — | 项目主 README |

## 使用原则

**根据 CLAUDE.md 规范，raw/ 下的文件一律不修改**。提炼和笔记写到 `../notes/`。
