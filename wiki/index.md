># 知识库索引


>- 33 个概念 · 22 个实体 · 19 个源摘要 — 共 74 页 | 更新于 2026-04-28


---

## 活跃项目

| 项目 | 目标 | 状态 | 启动 |
|------|------|------|------|
| [[projects/2026-04-kaigao/README.md\|2026-04-kaigao]] | 开稿 KaiGao — AI 论文写作助手的知识与产出管理 | active | 2026-04-28 |

---

## 概念

### AI
- [[llm-wiki|LLM Wiki]] — 由 LLM 增量构建的持久个人知识库模式
- [[rag|RAG]] — 检索增强生成，LLM Wiki 的对比对象
- [[ai-agent|AI Agent]] — 具备规划/记忆/工具调用能力、自主完成多步骤任务的 AI 系统
- [[react-framework|ReAct 框架]] — 推理与行动交替循环的 Agent 执行模式（Reasoning + Acting）
- [[function-calling|Function Calling]] — LLM 与外部系统交互的工具调用机制
- [[multi-agent|Multi-Agent 系统与协议]] — 多 Agent 协作系统及 MCP/A2A 协议标准化
- [[mcp|MCP（Model Context Protocol）]] — Anthropic 提出的 Agent-工具连接标准协议
- [[ai-skills|AI Skills 生态]] — 2026 年 AI Coding Skills 生态爆发，涵盖知识管理/职业规划/思维蒸馏
- [[autonomous-research|自主 ML 研究]] — AI agent 无人值守自主运行 ML 实验的范式（autoresearch）
- [[context-engineering|Context Engineering（上下文工程）]] — 主动管理 LLM 上下文窗口，通过 Task() + worktree 隔离解决 context rot

### 编程
- [[karpathy-guidelines|Karpathy Guidelines]] — LLM 编程行为四准则：思考→简单→精准→验证
- [[message-queue|消息队列（BullMQ）]] — 异步任务队列、Outbox Pattern、幂等性、SELECT FOR UPDATE SKIP LOCKED
- [[unified-payment-route|统一支付路由设计]] — 从业务支付页抽取公共支付路由的架构模式与关键决策
- [[design-patterns|设计模式]] — GoF 23种模式，创建型/结构型/行为型三大类
- [[clean-code|整洁代码]] — SOLID原则、DRY/KISS/YAGNI 编程实践
- [[refactoring|重构]] — 不改变外在行为的前提下改善代码内部结构
- [[solid-principles|SOLID 原则]] — 面向对象设计五原则：S/O/L/I/D
- [[monolith-async-worker|Monolith with Async Worker]] — 单体 + 异步 Worker 架构模式，微服务演进第一步
- [[programming/observer-pattern|观察者模式（Observer）]] — 发布者状态变化自动通知所有订阅者，一对多依赖解耦
- [[programming/read-after-write|写后读问题（Read-After-Write）]] — 分布式系统主从复制延迟导致用户读不到自己刚写入数据的一致性问题
- [[programming/canary-deployment|金丝雀部署（Canary Deployment）]] — 新版本先承载小比例流量，监控指标正常后渐进扩大的安全发布策略
- [[programming/spa-history-fallback|SPA History 路由与服务端 Fallback]] — BrowserRouter 使用 History API，服务端必须配置 fallback 否则刷新 404
- [[programming/server-state-management|服务端状态管理]] — 管理来自网络/数据库的异步数据生命周期，含缓存、新鲜度、去重、失效策略（TanStack Query vs SWR 对比）
- [[programming/react-page-state-antipatterns|React 页面状态管理反模式与重构]] — 布尔语义过载 / 内存态单源 / 隐式状态机 / 字段级三源合并四类反模式及其重构对策
- [[programming/feature-based-architecture|Feature-Based 架构]] — 按业务特性组织代码 + ESLint 强制单向依赖（shared → features → app），来自 Bulletproof React
- [[programming/react-classic-antipatterns|React 经典反模式（组件层）]] — Props in Initial State / Mutating State / Index as Key / render 里新建引用等 7+1 个反模式词典（Class → Hooks 对照）
- [[programming/react-state-categories|React 状态五分类]] — Component / Application / Server Cache / Form / URL 五类状态按来源组织，指导工具选型与识别页面反模式
- [[factory-method|工厂方法]] — 创建型模式，父类定义创建接口子类决定具体类型
- [[backend-architecture|后端架构]] — 分层/Clean/Hexagonal/CQRS 等核心架构模式
- [[cloud-deployment|云服务部署]] — Docker/K8s/IaC/CICD/可观测性
- [[microservices|微服务架构]] — 服务拆分/通信/API Gateway/Saga 模式

### 安全
- [[oauth-state-parameter|OAuth state 参数（微信网页授权）]] — OAuth2/微信回调透传参数，用于 CSRF 防护与短期上下文绑定
- [[open-redirect|Open Redirect]] — URL 参数跳转目标未校验导致的重定向漏洞及防护方法

---

## 实体

### 人物
- [[andrej-karpathy|Andrej Karpathy]] — AI 研究者，LLM Wiki 模式提出者
- [[peter-steinberger|Peter Steinberger]] — OpenClaw 框架开发者
- [[alan-alickovic|Alan Alickovic]] — Bulletproof React 作者，React 架构指南维护者

### 产品
- [[obsidian|Obsidian]] — 双向链接笔记工具，LLM Wiki 推荐的人类界面
- [[openclaw|OpenClaw]] — 开源本地优先的自主 AI Agent 框架，270K+ GitHub Stars
- [[langchain|LangChain]] — AI 应用开发积木框架，适合企业级 RAG 和复杂 AI 流水线
- [[autogpt|AutoGPT]] — 早期自主 Agent 实验项目，适合概念验证和学术研究
- [[mempalace|MemPalace]] — 开源 AI memory system，48K Stars，Benchmark 表现最佳
- [[caveman-skill|caveman]] — Claude Code 技能，用原始人语言降低 65% token，39K Stars
- [[graphify|graphify]] — 将代码/文档转为知识图谱的 AI 技能，31K Stars
- [[career-ops|career-ops]] — 基于 Claude Code 的 AI 求职系统，37K Stars
- [[nuwa-skill|nuwa-skill]] — 蒸馏思维方式的 AI 技能，六路Agent并行+三重验证，13K Stars
- [[gbrain|gbrain]] — Garry's OpenClaw/Hermes Agent Brain，8K Stars
- [[zhangxuefeng-skill|zhangxuefeng-skill]] — 高考/考研/职业规划思维框架，6.2K Stars
- [[khazix-skills|khazix-skills]] — 数字生命卡兹克的 AI Skills 合集，4.6K Stars
- [[autoresearch|autoresearch]] — Karpathy 的自主 ML 研究框架，一夜跑 ~100 次实验
- [[tanstack-query|TanStack Query（React Query）]] — 以 Query/Observer 状态机为核心的服务端状态管理库，支持复杂 mutation 与 DevTools 生态
- [[swr|SWR]] — Vercel 出品的极简 Stale-While-Revalidate 数据获取 hook 库
- [[andrej-karpathy-skills|andrej-karpathy-skills]] — Claude Code 行为改进的 CLAUDE.md 文件，GitHub Trending
- [[superpowers|superpowers]] — Agentic 技能框架与软件开发方法论，GitHub Trending
- [[gsd|GSD（Get Shit Done）]] — context engineering + spec-driven 开发系统，解决 context rot，56K+ Stars
- [[bulletproof-react|Bulletproof React]] — React 生产级架构指南与示例应用，GitHub 35K+ Stars

---

## 源摘要

### 文章
- [[sources/articles/llm-wiki-by-karpathy|LLM Wiki — Karpathy]] — Karpathy 的 LLM Wiki Gist (2026-04)
- [[sources/articles/openclaw-ai-agent-interview|OpenClaw + AI Agent 面试八股文]] — OpenClaw 架构、ReAct、Function Calling、MCP/A2A 全面讲解 (2026-03)
- [[sources/articles/software-engineering-knowledge|软件工程知识资料]] — 代码质量/重构/设计模式/SOLID/DDD 优质资源整理 (2026-04)
- [[sources/articles/observer-pattern|观察者模式 — Refactoring.Guru]] — GoF Observer 结构解析、伪代码、优缺点及与 Mediator 对比 (2025-01)
- [[sources/articles/backend-architecture-article|后端架构知识资料]] — 微服务/云部署/DevOps/IaC/CQRS 优质资源 (2026-04)
- [[sources/articles/factory-method-refactoring-guru|工厂方法 — Refactoring Guru]] — 工厂方法模式：父类定义创建接口，子类决定具体类型 (2025-01)
- [[sources/articles/react-query-vs-swr-server-state-source-compare|React Query vs SWR 源码对比]] — TanStack Query 与 SWR 缓存架构、订阅模型、去重、失效策略的深度源码对比 (2026-04)
- [[sources/articles/get-shit-done-github|GSD（Get Shit Done）GitHub README]] — context engineering + spec-driven 开发系统，Wave 并行执行，上下文隔离原理 (2026-04)
- [[sources/articles/bulletproof-react-github|Bulletproof React GitHub]] — Feature-based 架构 / 状态五分类 / 单向依赖 / 测试倒金字塔等 13 篇架构文档 (2026-04)
- [[sources/articles/react-bits-github|React Bits GitHub]] — 7 个组件层经典反模式 + Pure Render Checks，Class 时代汇编但多数在 Hooks 时代仍适用 (2017)

### GitHub 仓库
- [[sources/articles/nuwa-skill-github|nuwa-skill（女娲·Skill造人术）]] — 思维蒸馏 Skill 系统，六路Agent并行+三重验证 (2026-04)

### GitHub 仓库（续）
- [[sources/articles/karpathy-autoresearch|karpathy/autoresearch]] — 自主 ML 研究框架，三文件极简设计，固定时间预算 (2026-04)

### 晨报
- [[sources/morning-briefs/2026-04-15|晨报 2026-04-15]] — Hacker News / GitHub Trending 日报，Skills 生态爆发趋势
- [[sources/morning-briefs/2026-04-16|晨报 2026-04-16]] — Stop Using Ollama / AI 推理优化 / IPv6 里程碑
- [[sources/morning-briefs/2026-04-18|晨报 2026-04-18]] — Claude Design 引热议 / Claude 4.7 Tokenizer 成本分析 / GitHub Trending
- [[sources/morning-briefs/2026-04-19|晨报 2026-04-19]] — Opus 4.7 模型对比 / 日本铁路 / B-52 星跟踪器 / OpenAI Agents Python (2026-04-19)
- [[sources/morning-briefs/2026-04-20|晨报 2026-04-20]] — Vercel 安全事件 / caveman Token 压缩 / MemPalace 48K / graphify 31K (2026-04-20)
- [[sources/morning-briefs/2026-04-21|晨报 2026-04-21]] — Apple CEO 交接 / Qwen3.6 / OpenClaw Claude CLI 复活 / OpenAI agents-python (2026-04-21)
- [[sources/morning-briefs/2026-04-22|晨报 2026-04-22]] — SpaceX $600亿收购Cursor / ChatGPT Images 2.0 / 软件工程定律 (2026-04-22)

---

*空类别（综合分析、问答存档）在有内容后自动出现。*
