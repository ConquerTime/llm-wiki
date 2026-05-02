# s01–s12 学习路线图

> 从零到隔离化的自治执行，12 个递进式课程。
> 每学一课：① 读 learn-claude-code 的 s0X 章（最小 Python 实现）②  对照 cc-haha 的 TypeScript 生产实现 ③ 自己复现关键机制。

---

## 路线总览

```
Part A: 循环与工具（s01-s03）
  s01  The Agent Loop             一个 while True + stop_reason
  s02  Tool Use                   dispatch map + 路径沙箱
  s03  TodoWrite                  带状态的规划 + nag reminder

Part B: 知识与记忆（s04-s06）
  s04  Subagent                   隔离 messages[]，父子上下文分离
  s05  Skill Loading              两层注入：名称列表 + 按需内容
  s06  Context Compact            micro / auto / manual 三层压缩

Part C: 任务与并发（s07-s08）
  s07  Task System                磁盘持久化的任务 DAG
  s08  Background Tasks           后台线程 + 通知队列

Part D: 多 agent 协作（s09-s12）
  s09  Agent Teams                持久化队友 + JSONL 邮箱
  s10  Team Protocols             request-response FSM（关机/计划审批）
  s11  Autonomous Agents          队友自己扫看板认领任务
  s12  Worktree Isolation         task_id ↔ worktree 绑定，并行不冲突
```

---

## 每课的核心机制与源码锚点

### Part A：循环与工具

#### s01 — The Agent Loop
- **格言**：*One loop & Bash is all you need*
- **问题**：模型能推理代码但碰不到真实世界
- **解法**：`while True` + 检查 `stop_reason != "tool_use"`
- **代码规模**：~30 行
- **cc-haha 对照**：`src/query/` 目录下的 queryLoop、7+ continue 站点
- **原文**：[[raw/learn-claude-code/s01-the-agent-loop.md]]

#### s02 — Tool Use
- **格言**：*加一个工具, 只加一个 handler*
- **关键机制**：
  - `TOOL_HANDLERS` 字典（dispatch map）替代 if/elif 链
  - `safe_path()` 防止路径逃逸工作区
- **cc-haha 对照**：`buildTool()` 工厂模式、Tool 接口 30+ 方法
- **原文**：[[raw/learn-claude-code/s02-tool-use.md]]

#### s03 — TodoWrite
- **格言**：*没有计划的 agent 走哪算哪*
- **关键机制**：
  - 同一时间只允许一个 `in_progress` —— 强制顺序聚焦
  - 连续 3 轮不调用 todo 自动注入 `<reminder>`（nag reminder）
- **cc-haha 对照**：TodoManager、stopHooks 机制
- **原文**：[[raw/learn-claude-code/s03-todo-write.md]]

### Part B：知识与记忆

#### s04 — Subagent
- **格言**：*大任务拆小, 每个小任务干净的上下文*
- **关键机制**：
  - Subagent 用独立 `messages=[]`，不污染父对话
  - 父只保留摘要文本，中间 30+ 次工具调用全部丢弃
  - 禁止递归生成（child 没有 task 工具）
- **cc-haha 对照**：`src/tools/AgentTool/`、`runAgent.ts`、Fork 四条路径
  - 详细实现：[[raw/cc-haha/agent-02-implementation.md]]
- **原文**：[[raw/learn-claude-code/s04-subagent.md]]

#### s05 — Skill Loading
- **格言**：*用到什么知识, 临时加载什么知识*
- **关键机制（两层注入）**：
  - 第一层：Skill **名称列表** 放系统提示（便宜，~100 token/skill）
  - 第二层：`load_skill(name)` 触发 tool_result 注入完整内容（~2000 token）
- **cc-haha 对照**：
  - 6 种来源：bundled / builtinPlugin / managed / user / project / plugin
  - 去重：按 `realpath`
  - 延迟提取：bundled skills 首次使用时才解压到磁盘
  - [[raw/cc-haha/skills-02-implementation.md]]
- **原文**：[[raw/learn-claude-code/s05-skill-loading.md]]

#### s06 — Context Compact
- **格言**：*上下文总会满, 要有办法腾地方*
- **三层压缩（激进程度递增）**：

| 层 | 触发 | 操作 |
|---|------|------|
| micro_compact | 每轮静默 | 3 轮前的 tool_result → 占位符 |
| auto_compact | token > 50k | 保存 transcript，LLM 摘要全历史 |
| manual compact | 工具显式调用 | 同 auto |

- **cc-haha 对照**：5 种压缩策略（Snip / Micro / Context Collapse / Auto / Session Memory），有熔断器保护
  - 记忆自动提取：[[raw/cc-haha/memory-02-implementation.md]]
- **原文**：[[raw/learn-claude-code/s06-context-compact.md]]

### Part C：任务与并发

#### s07 — Task System
- **格言**：*大目标要拆成小任务, 排好序, 记在磁盘上*
- **从扁平清单 → 持久化任务图（DAG）**
- **磁盘结构**：
  ```
  .tasks/
    task_1.json  {"id":1, "status":"completed"}
    task_2.json  {"id":2, "blockedBy":[1], "status":"pending"}
  ```
- **三个关键查询**：什么可做？什么被卡住？什么做完了？
- **完成任务 → 自动从其他任务的 blockedBy 中移除 → 解锁后续**
- **原文**：[[raw/learn-claude-code/s07-task-system.md]]

#### s08 — Background Tasks
- **格言**：*慢操作丢后台, agent 继续想下一步*
- **关键机制**：
  - 线程安全的通知队列（`_lock` + `_notification_queue`）
  - 每次 LLM 调用前**排空队列**，将结果以 `<background-results>` 注入
- **循环本身保持单线程**，只有子进程 I/O 被并行化
- **原文**：[[raw/learn-claude-code/s08-background-tasks.md]]

### Part D：多 agent 协作

#### s09 — Agent Teams
- **格言**：*任务太大一个人干不完, 要能分给队友*
- **从一次性 subagent → 持久化队友**
- **关键机制**：
  - `.team/config.json` — 团队名册 + 状态
  - `.team/inbox/{name}.jsonl` — append-only 收件箱，drain-on-read
  - 每线程一个完整 agent loop，每轮开头检查收件箱
- **cc-haha 对照**：
  - 执行后端：tmux / iTerm2 / in-process
  - AsyncLocalStorage 上下文隔离（spawnInProcessTeammate）
- **原文**：[[raw/learn-claude-code/s09-agent-teams.md]]

#### s10 — Team Protocols
- **格言**：*队友之间要有统一的沟通规矩*
- **一个通用 FSM 驱动两种协议**：
  ```
  pending → approved
  pending → rejected
  ```
- **关机握手**、**计划审批** 结构完全相同：一方发带 `request_id` 的请求，另一方引用同一 ID 响应
- **原文**：[[raw/learn-claude-code/s10-team-protocols.md]]

#### s11 — Autonomous Agents
- **格言**：*队友自己看看板, 有活就认领*
- **队友生命周期：WORK ↔ IDLE**
  - IDLE 阶段每 5s 轮询，最多 60s
  - 扫描 `.tasks/`：状态 pending + 无 owner + 无 blockedBy
  - 自动 claim → 转回 WORK
- **身份重注入**：context compact 后上下文太短（<=3 条），插入 identity block 防止"失忆"
- **原文**：[[raw/learn-claude-code/s11-autonomous-agents.md]]

#### s12 — Worktree + Task Isolation
- **格言**：*各干各的目录, 互不干扰*
- **两套状态机绑定**：
  ```
  Task:     pending → in_progress → completed
  Worktree: absent  → active      → removed | kept
  ```
- **task_id ↔ worktree 显式绑定**
- **事件流**：`.worktrees/events.jsonl` 记录每个生命周期步骤
- **崩溃恢复**：从 `.tasks/` + `.worktrees/index.json` 重建现场
- **原文**：[[raw/learn-claude-code/s12-worktree-task-isolation.md]]

---

## 学完 s01–s12 你会有什么

一个**约 800–1500 行 Python 的可运行 code agent**，具备：

- 完整的 agent loop
- 4 个基础工具（bash/read/write/edit）+ 权限沙箱
- 带状态的规划工具
- 子 agent 派生 + 上下文隔离
- 按需 skill 加载
- 三层上下文压缩
- 磁盘持久化的任务 DAG
- 后台并行执行
- 多 agent 团队邮箱
- request-response 协议握手
- 自治任务认领
- Git worktree 并行隔离

而且**每一个机制都对应 Claude Code 真实源码的某个模块**，cc-haha 的文档帮你跨越 "Python 最小实现 → TypeScript 生产实现" 的鸿沟。

---

## 学习节奏建议

| 周 | 目标 | 产出 |
|---|------|------|
| 第 1 周 | s01-s03 读 + 跑 + 复现 | Python 版 MiniAgent v1（loop + tools + todo）|
| 第 2 周 | s04-s06 + 对照 cc-haha skills/memory 文档 | MiniAgent v2（+ subagent / skill / compact）|
| 第 3 周 | s07-s08 + 对照 cc-haha agent-02-implementation | MiniAgent v3（+ 任务 DAG + 后台）|
| 第 4 周 | s09-s12 + 对照 cc-haha channel 文档 | MiniAgent v4（+ 团队 + 自治 + worktree）|
| 第 5 周 | 整合复盘，写架构分析文档 | deliverables/ 最终产出 |

---

## 资料来源

### 主要知识源
- [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) — 12 课递进式最小实现（Python）
- [NanmiCoder/cc-haha](https://github.com/NanmiCoder/cc-haha) — 本地可运行 TS 版 + 生产级实现文档

### 原文存档（raw/）
- [[raw/learn-claude-code/]] — s01~s12 完整中文版
- [[raw/cc-haha/]] — agent / memory / skills / channel / computer-use 实现文档
