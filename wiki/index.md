># 知识库索引

>- 35 个概念 · 27 个实体 · 29 个源摘要 — 共 91 页 | 更新于 2026-05-01

---

## 活跃项目

| 项目 | 目标 | 状态 | 启动 |
|------|------|------|------|
| [[projects/2026-04-kaigao/README|2026-04-kaigao]] | 开稿 KaiGao — AI 论文写作助手的知识与产出管理 | active | 2026-04-28 |

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
- [[agent-harness|Agent Harness（控制框架）]] — Agent 的 harness 与 memory 不可分割，闭源 harness 造成供应商锁定

### 编程
- [[karpathy-guidelines|Karpathy Guidelines]] — LLM 编程行为四准则：思考→简单→精准→验证
- [[message-queue|消息队列（BullMQ）]] — 异步任务队列、Outbox Pattern、幂等性、SELECT FOR UPDATE SKIP LOCKED
- [[unified-payment-route|统一支付路由设计]] — 从业务支付页抽取公共支付路由的架构模式与关键决策
- [[design-patterns|设计模式]] — GoF 23种模式，创建型/结构型/行为型三大类
- [[observer-pattern|观察者模式]] — GoF 行为型模式，订阅机制三要素、EventManager 委派、与 Mediator/Pub-Sub 对比
- [[clean-code|整洁代码]] — SOLID原则、DRY/KISS/YAGNI 编程实践
- [[refactoring|重构]] — 不改变外在行为的前提下改善代码内部结构
- [[solid-principles|SOLID 原则]] — 面向对象设计五原则：S/O/L/I/D
- [[concepts/programming/spec-driven-development|Spec-Driven Development]] — 先写规格再写代码，多 Agent 协作的通信协议
- [[concepts/programming/monolith-async-worker|Monolith with Async Worker]] — 单体 + 异步 Worker 架构模式，微服务演进第一步
- [[factory-method|工厂方法]] — 创建型模式，父类定义创建接口子类决定具体类型
- [[backend-architecture|后端架构]] — 分层/Clean/Hexagonal/CQRS 等核心架构模式
- [[cloud-deployment|云服务部署]] — Docker/K8s/IaC/CICD/可观测性
- [[web-worker-pattern|Web-Worker Pattern]] — API + 异步 Worker 分离架构，同一镜像多角色启动
- [[microservices|微服务架构]] — 服务拆分/通信/API Gateway/Saga 模式
- [[concepts/programming/canary-deployment|金丝雀部署]] — 渐进式发布策略，新版本先推给少量用户验证
- [[concepts/programming/read-after-write|写后读一致性]] — 分布式系统一致性陷阱，Read-After-Write 问题与解决方案
- [[concepts/programming/server-state-management|服务端状态管理]] — 异步服务端数据生命周期管理，缓存/新鲜度/失效
- [[concepts/programming/spa-history-fallback|SPA History Fallback]] — BrowserRouter 刷新 404 问题，nginx/Apache/Express/Netlify/Vercel 配置
- [[concepts/programming/react-state-categories|React 状态五分类]] — Bulletproof React 提出的状态分类体系
- [[concepts/programming/react-page-state-antipatterns|React Page State 反模式]] — 跨组件传递 server state、用 localStorage 缓存等常见错误
- [[concepts/programming/react-classic-antipatterns|React 组件层经典反模式]] — 7 个组件层反模式与 Pure Render Checks
- [[concepts/programming/feature-based-architecture|Feature-Based 架构]] — 按业务特性组织代码，单向依赖约束

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
- [[bulletproof-react|Bulletproof React]] — Feature-based 架构 / 状态五分类 / 单向依赖 / 测试倒金字塔等 13 篇架构文档
- [[tanstack-query|TanStack Query（React Query）]] — 以 Query/Observer 状态机为核心的服务端状态管理库，支持复杂 mutation 与 DevTools 生态
- [[typescript-go|typescript-go]] — 微软 TypeScript 转 Go 转译工具 (2026-04-27)
- [[swr|SWR]] — Vercel 出品的极简 Stale-While-Revalidate 数据获取 hook 库
- [[andrej-karpathy-skills|andrej-karpathy-skills]] — Claude Code 行为改进的 CLAUDE.md 文件，GitHub Trending
- [[superpowers|superpowers]] — Agentic 技能框架与软件开发方法论，GitHub Trending
- [[gsd|GSD（Get Shit Done）]] — context engineering + spec-driven 开发系统，56K Stars
- [[deepep|DeepEP]] — DeepSeek 高效专家并行通信库，MoE 模型分布式训练
- [[mattpocock-skills|mattpocock/skills]] — Claude Code Skills 实操指南，GitHub Trending
- [[posthog|PostHog]] — 开源产品分析平台，Analytics/Session Replay/Feature Flags
- [[roo-code|Roo-Code]] — VS Code AI 多智能体开发团队，AI 代理编辑器内协同

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
- [[sources/articles/your-harness-your-memory|Your Harness, Your Memory]] — LangChain CEO 论 harness 与 memory 不可分割，闭源造成供应商锁定 (2026-04-12)
- [[sources/articles/kaigao-ecs-deployment|kaigao ECS 部署方案]] — SAE → ECS + docker-compose 迁移：ALB 单入口、同一镜像多角色、费用对比 (2026-04)

### 晨报
- [[sources/morning-briefs/2026-04-15|晨报 2026-04-15]] — Hacker News / GitHub Trending 日报，Skills 生态爆发趋势
- [[sources/morning-briefs/2026-04-16|晨报 2026-04-16]] — Stop Using Ollama / AI 推理优化 / IPv6 里程碑
- [[sources/morning-briefs/2026-04-18|晨报 2026-04-18]] — Claude Design 引热议 / Claude 4.7 Tokenizer 成本分析 / GitHub Trending
- [[sources/morning-briefs/2026-04-19|晨报 2026-04-19]] — Opus 4.7 模型对比 / 日本铁路 / B-52 星跟踪器 / OpenAI Agents Python (2026-04-19)
- [[sources/morning-briefs/2026-04-20|晨报 2026-04-20]] — Vercel 安全事件 / caveman Token 压缩 / MemPalace 48K / graphify 31K (2026-04-20)
- [[sources/morning-briefs/2026-04-21|晨报 2026-04-21]] — Apple CEO 交接 / Qwen3.6 / OpenClaw Claude CLI 复活 / OpenAI agents-python (2026-04-21)
- [[sources/morning-briefs/2026-04-22|晨报 2026-04-22]] — SpaceX $600亿收购Cursor / ChatGPT Images 2.0 / 软件工程定律 (2026-04-22)
- [[sources/morning-briefs/2026-04-23|晨报 2026-04-23]] — Apple 删除消息漏洞修复 / Firefox Tor 隐私问题 / Over-editing 讨论 (2026-04-23)
- [[sources/morning-briefs/2026-04-24|晨报 2026-04-24]] — DeepSeek v4 / GPT-5.5 / Bitwarden CLI 供应链攻击 / Meta 裁员 (2026-04-24)
- [[sources/morning-briefs/2026-04-25|晨报 2026-04-25]] — Google $40B 投资 Anthropic / Hugging Face ml-intern / free-claude-code (2026-04-25)
- [[sources/morning-briefs/2026-04-26|晨报 2026-04-26]] — AI 编码工具持续火热 / ChatGPT 解决 Erdős 问题 / DeepEP / Roo-Code (2026-04-26)
- [[sources/morning-briefs/2026-04-27|晨报 2026-04-27]] — mattpocock/skills 开源 / PostHog 产品分析 / typescript-go 微软转译工具 (2026-04-27)
- [[sources/morning-briefs/2026-04-28|晨报 2026-04-28]] — Microsoft 与 OpenAI 结束独家合作 / 4TB 语音样本被盗 / mattpocock/skills (2026-04-28)
- [[sources/morning-briefs/2026-04-29|晨报 2026-04-29]] — Ghostty 离开 GitHub（2395分）/ Rust 安全性 / Codex skills (2026-04-29)
- [[sources/morning-briefs/2026-04-30|晨报 2026-04-30]] — Zed 1.0 发布 / Copy Fail / OpenAI goblin 数据 / Zig 反 AI 政策 (2026-04-30)

---

*空类别（综合分析、问答存档）在有内容后自动出现。*
