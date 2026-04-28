# 操作日志

> 追加式时间线记录。所有 ingest、query、lint 操作都记录在此。

## 格式规范

每个条目格式：
```markdown
## [YYYY-MM-DD] type | Title
- 类型：ingest/query/lint/update
- 操作内容...
- 涉及的页面...
```

---

## 历史记录

## [2026-04-24] update | TanStack Query 学习笔记补充
- 类型：update
- 更新页面：
  - entities/products/tanstack-query.md（新增"自动 refetch 触发时机"一节：挂载、窗口焦点、网络重连、轮询；以及 focusManager/onlineManager 可替换设计）
  - concepts/programming/server-state-management.md（边界一节补充：服务端数据不应放 Zustand，QueryCache 天然全局无需抬升）
- 备注：来自 super-tutor 苏格拉底对话，从 Redux + Axios 痛点出发推导出 TanStack Query 的设计原理

## [2026-04-24] ingest | GSD（Get Shit Done）GitHub README
- 类型：GitHub 仓库 README
- 来源：raw/articles/get-shit-done-github.md
- 新增页面：
  - sources/articles/get-shit-done-github.md
  - entities/products/gsd.md
  - concepts/ai/context-engineering.md
- 更新页面：
  - concepts/ai/multi-agent.md（添加 GSD 到框架列表）
  - wiki/index.md（新增 3 条目，统计更新）
- 备注：本次 ingest 源于对话中深入探讨 GSD 上下文隔离实现原理；核心机制为 Claude Code `Task()` API + `isolation="worktree"`，状态通过文件传递而非对话；新建 context-engineering 概念页系统记录此模式

## [2026-04-23] learn | OAuth state 参数（微信网页授权）
- 来源项目：megrez-shop
- 页面：concepts/security/oauth-state-parameter.md
- 操作：新增（对话汇总 `/learn summarize`）
- 备注：涵盖 state 含义、CSRF 场景、服务端随机串校验流程、Mermaid 时序图；项目实践指向 WechatH5.tsx 当前未带 state、通过 fenbiUrl 回跳

## [2026-04-17] ingest | 观察者模式 — Refactoring.Guru
- 类型：article
- 来源：raw/观察者.md
- 新增页面：sources/articles/observer-pattern.md, concepts/programming/observer-pattern.md
- 更新页面：concepts/design-patterns.md（Observer 行补充链接）, wiki/index.md
- 备注：GoF 行为型模式之一，重点记录订阅机制三要素、EventManager 委派模式、与 Mediator/Pub-Sub 的区别

## [2026-04-23] learn | SPA History 路由与服务端 Fallback
- 来源项目：horizon-admin-web-commerce
- 页面：concepts/programming/spa-history-fallback.md
- 操作：新增
- 备注：对比 admin-growth（BrowserRouter）与 admin-commerce（HashRouter），记录 nginx/Apache/Express/Netlify/Vercel 各平台 fallback 配置方式

## [2026-04-18] learn | 金丝雀部署（Canary Deployment）
- 来源项目：llm-wiki
- 页面：concepts/programming/canary-deployment.md
- 操作：新增
- 备注：渐进式发布架构专题，含流量切分原理、K8s 实现方案（原生/Argo Rollouts/Istio）、常见陷阱

## [2026-04-18] learn | 写后读问题（Read-After-Write Consistency）
- 来源项目：llm-wiki
- 页面：concepts/programming/read-after-write.md
- 操作：新增
- 备注：分布式主从复制延迟导致的一致性问题，涵盖5种解决方案和决策框架

## [2026-04-17] learn | Monolith with Async Worker
- 来源项目：llm-wiki
- 页面：concepts/programming/monolith-async-worker.md
- 操作：新增
- 备注：单体 + 异步 Worker 架构模式，对话中解释后沉淀为概念页

## [2026-04-15] learn | 消息队列（BullMQ）
- 来源项目：kaigao
- 页面：concepts/programming/message-queue.md
- 操作：新增
- 备注：基于 kaigao 项目中 BullMQ 的完整实战，覆盖 Outbox Pattern、幂等性、SELECT FOR UPDATE SKIP LOCKED、Repeatable Job 等核心工程模式

## [2026-04-14] init | 初始化 LLM Wiki 仓库

- 类型：init
- 初始化了完整的 llm-wiki 仓库结构
- 创建了 CLAUDE.md（LLM 工作指令）
- 创建了 wiki/index.md（内容索引）
- 创建了 wiki/log.md（本日志）
- 规划了目录结构：
  - raw/articles/, raw/papers/, raw/books/（原始资料）
  - wiki/entities/, wiki/concepts/, wiki/sources/, wiki/synthesis/, wiki/questions/（知识库页面）
- 撰写了 README.md 项目说明

## [2026-04-14] ingest | LLM Wiki — Karpathy Gist

- 类型：article
- 来源：raw/articles/llm-wiki-by-karpathy.md
- 新增页面：sources/articles/llm-wiki-by-karpathy.md, concepts/llm-wiki-architecture.md, concepts/karpathy-guidelines.md
- 备注：首次摄入。Karpathy 的 LLM Wiki 设计模式文章，提取了架构概念页和编程行为准则概念页

## [2026-04-15] lint | 项目审查与修复

- 类型：lint
- 发现问题：
  - wiki 页面 frontmatter YAML 格式不规范（标题写在 frontmatter 之前、sources 不是列表格式）
  - 源摘要页分类错误（papers → articles）
  - index.md 未录入已有页面（统计为 0）
  - log.md 缺少摄入记录
  - 概念页引用了 4 个不存在的页面（孤儿引用）
  - 空 coverage/ 目录
- 修复：全部已修复

## [2026-04-15] refactor | Wiki 结构重构

- 类型：refactor
- 目标：让 wiki 同时适合人类阅读和 LLM 操作
- CLAUDE.md 更新：
  - 新增页面角色定义（源摘要=提取向、概念=综合向、实体=事实卡片）
  - frontmatter 增加 type/subtype 字段
  - index.md 改为紧凑列表格式，只展示有内容的类别
  - 子目录首次使用时创建，不预建空目录
- 页面变动：
  - 重写 sources/articles/llm-wiki-by-karpathy.md（聚焦原文提取，去重复）
  - concepts/llm-wiki-architecture.md → concepts/ai/llm-wiki.md（综合向概念页）
  - concepts/karpathy-guidelines.md → concepts/programming/karpathy-guidelines.md（面向人类）
  - 新增 concepts/ai/rag.md
  - 新增 entities/persons/andrej-karpathy.md
  - 新增 entities/products/obsidian.md
- 删除：旧路径概念页、空 sources/papers/ 目录
- 共 6 个 wiki 页面

## [2026-04-15] ingest | OpenClaw + AI Agent 面试八股文

- 类型：article
- 来源：raw/articles/OpenClaw + AI Agent 面试八股文：背完这篇，你懂的比面试官还多！.md
- 原文链接：https://zhuanlan.zhihu.com/p/2013536456132554764
- 作者：王几行XING（知乎）
- 新增页面：
  - sources/articles/openclaw-ai-agent-interview.md（源摘要）
  - concepts/ai/ai-agent.md（AI Agent 四大组件概念页）
  - concepts/ai/react-framework.md（ReAct 框架概念页）
  - concepts/ai/function-calling.md（Function Calling 工具调用概念页）
  - concepts/ai/multi-agent.md（Multi-Agent 系统与 MCP/A2A 协议概念页）
  - entities/products/openclaw.md（OpenClaw 实体页）
  - entities/persons/peter-steinberger.md（Peter Steinberger 实体页）
- 备注：以 OpenClaw 框架为主线的 AI Agent 工程师面试系统性八股文，覆盖五大核心组件、ReAct 框架、Function Calling、Multi-Agent 协议（MCP/A2A）、安全防护等 8 大主题，160+ 道分级面试题（入门→源码级）

## [2026-04-15] lint | Wiki 健康检查

- 类型：lint
- 检查项目：孤儿引用、孤立页面、frontmatter 完整性
- 结果：
  - 孤立页面：0（全部页面均有入站引用）
  - frontmatter 完整性：13/13 内容页字段齐全
  - 孤儿引用：3 处（`langchain`、`autogpt`、`mcp` 缺少对应页面）
- 修复：创建 3 个缺失页面
  - entities/products/langchain.md
  - entities/products/autogpt.md
  - concepts/ai/mcp.md
- 修复后 wiki 规模：16 页（8 概念 · 6 实体 · 2 源摘要）

## [2026-04-15] lint | 每日健康检查

- 类型：lint
- 概览：wiki 健康，无新增问题
- 检查结果：
  - 孤儿页面：0（所有 wiki 页面均有入站引用）
  - 孤立页面：2（`sources/` 页面靠 frontmatter sources 字段引用，非 wikilink，符合设计）
  - 断链：1（`entities/products/obsidian.md` 中 `[page]` 为语法示例，非真实链接）
  - frontmatter：16/16 完整
  - 过时页面：0
  - 超大页面：0
- 修复：
  - 为 `obsidian.md` 增加 `[[llm-wiki]]` 出站链接，提升页面互联度
- wiki 规模：16 页（8 概念 · 6 实体 · 2 源摘要）
- 提交：76d34b1

## [2026-04-16] ingest | nuwa-skill（女娲·Skill造人术）GitHub 仓库

- 类型：article (GitHub repo)
- 来源：raw/articles/nuwa-skill-github.md
- 原文链接：https://github.com/alchaincyf/nuwa-skill
- 作者：花叔 (alchaincyf)
- 新增页面：
  - sources/articles/nuwa-skill.md（源摘要）
- 更新页面：
  - entities/products/nuwa-skill.md（丰富实体信息：五层认知提取、五阶段流水线、预置Skills等）
  - concepts/ai/ai-skills.md（更新 nuwa-skill Stars 和描述）
  - concepts/ai/ai-agent.md（添加 nuwa-skill 作为 Multi-Agent 实战案例）
  - wiki/index.md（新增源摘要条目，修复合并冲突，更新统计）
- 备注：深度摄入 nuwa-skill 仓库。核心创新——Agentic 回答工作流（先研究再回答）和六路Agent并行调研+三重验证的思维蒸馏流水线

## [2026-04-16] ingest | karpathy/autoresearch — 自主 ML 研究框架

- 类型：article (GitHub repo)
- 来源：raw/articles/karpathy-autoresearch.md
- 原文链接：https://github.com/karpathy/autoresearch
- 作者：Andrej Karpathy
- 新增页面：
  - sources/articles/karpathy-autoresearch.md（源摘要）
  - concepts/ai/autonomous-research.md（自主 ML 研究概念页）
  - entities/products/autoresearch.md（autoresearch 实体页）
- 更新页面：
  - entities/persons/andrej-karpathy.md（添加 autoresearch 关联）
  - wiki/index.md（新增条目，统计更新至 16概念·15实体·5源摘要）
- 备注：极简三文件设计（prepare.py 只读 / train.py agent 修改 / program.md 人类指令）。核心创新——固定时间预算（5分钟/次）让实验跨硬件可比，单一指标 val_bpb 让 agent 聚焦目标，markdown 文件作为人类→agent 的编程接口

## [2026-04-16] learn | Open Redirect（开放重定向漏洞）
- 来源项目：horizon-web-commerce
- 页面：concepts/security/open-redirect.md
- 操作：新增
- 备注：公共支付页设计中，query params 传递 returnPath/cancelPath 引出的安全问题。记录了三种防护方法及项目中采用的 isInternalPath 方案

## [2026-04-16] learn | 统一支付路由设计
- 来源项目：horizon-web-commerce
- 页面：concepts/programming/unified-payment-route.md
- 操作：新增
- 备注：从 CoursePaymentPage 抽取公共支付路由的架构设计。重点记录了 4 个关键决策点的权衡逻辑：入参协议（双通道）、鉴权策略（轻量断言）、商品展示（固定模板）、returnUrl 指向（必须回支付页自身而非业务成功页）

## [2026-04-15] ingest | 晨报 2026-04-15 — AI Skills 生态爆发

- 类型：morning-brief
- 来源：raw/morning-briefs/2026-04-15.md
- 新增页面：
  - sources/morning-briefs/2026-04-15.md（源摘要）
  - concepts/ai/ai-skills.md（AI Skills 生态概念页）
  - entities/products/mempalace.md（AI memory system，46K Stars）
  - entities/products/caveman-skill.md（Token 优化技能，32K Stars）
  - entities/products/graphify.md（知识图谱构建技能，27K Stars）
  - entities/products/career-ops.md（AI 求职系统，33K Stars）
  - entities/products/nuwa-skill.md（思维蒸馏技能，11K Stars）
  - entities/products/gbrain.md（OpenClaw/Hermes Brain，8K Stars）
  - entities/products/zhangxuefeng-skill.md（职业规划思维框架，5.9K Stars）
  - entities/products/khazix-skills.md（AI Skills 合集，4.6K Stars）
- 备注：GitHub Trending 显示 AI Coding Skills 生态爆发，caveman/graphify/nuwa-skill 等项目进入视野，国产 Skills 开始崛起

## [2026-04-16] ingest | 工厂方法 — RefactoringGuru 设计模式

- 类型：article (clippings)
- 来源：raw/articles/工厂方法.md
- 新增页面：
  - concepts/programming/factory-method.md（工厂方法模式概念页）
- 更新页面：
  - concepts/design-patterns.md（添加工厂方法到创建型模式表格，添加统一支付路由链接）
- 备注：创建型模式第一条，补充了工厂方法的概念定义、结构、适用场景和优缺点

## [2026-04-16] ingest | 晨报 2026-04-16 — Ollama争议 / AI推理优化

- 类型：morning-brief
- 来源：raw/morning-briefs/2026-04-16.md
- 新增页面：
  - sources/morning-briefs/2026-04-16.md（晨报源摘要）
  - entities/products/andrej-karpathy-skills.md（Claude Code 行为改进配置）
  - entities/products/superpowers.md（Agentic 技能框架）
- 更新页面：
  - concepts/ai/ai-skills.md（新增 andrej-karpathy-skills 和 superpowers 到生态表格）
- 备注：HN 热门话题 Ollama 争议、Darkbloom 私有推理；GitHub Trending 新上榜 Skills 项目

## [2026-04-16] lint | 修复孤立页面 + 统计健康度

- 修复孤立页面：
  - concepts/ai/autonomous-research.md — 从 ai-agent.md 添加 inbound link
  - concepts/programming/unified-payment-route.md — 从 design-patterns.md 添加 inbound link
- 健康统计：
  - 总页面：48 wiki pages
  - 孤立页面：0（修复后）
  - 断链：0（之前误报，sources/articles/* 路径链接正确）
  - 源摘要页：7 个
  - 超大页面（>200行）：1 个（message-queue.md 278行，建议拆分）


## [2026-04-17] lint | 健康检查（每日 cron）

- 类型：lint
- 日期：2026-04-17 23:00 (cron每日任务)
- 健康统计：
  - 总页面：48 wiki pages
  - 孤立页面：0 ✅
  - 断链：1（误报，nuwa-skill.md 的 `../../../raw/articles/nuwa-skill-github.md` 路径正确，但 lint.py 仅检测 `../raw` 未检测多层 `../../`/`../../../` 前缀）
  - 源摘要页：6 个（sources/）
  - 超大页面（>200行）：1 个（message-queue.md 278行，建议拆分）
- 备注：
  - Git pull 拉取新 commit: `69923ca feat: 添加后端架构与云服务部署资料`
  - 该 commit 已包含完整的 ingest（backend-architecture.md → sources + concepts/），无需重复 ingest
  - 直接进行 lint 健康检查

## [2026-04-19] lint | 健康检查（每日 cron）

- 类型：lint
- 日期：2026-04-19 23:00 (cron每日任务)
- 健康统计：
  - 总页面：51 wiki pages
  - 孤立页面：0 ✅（backend-architecture.md 已从 design-patterns.md 添加 inbound link）
  - 断链：0 ✅
  - 源摘要页：11 个（sources/）
  - 超大页面（>200行）：1 个（message-queue.md 278行，建议拆分）
- 修复：
  - backend-architecture.md orphan 已修复（从 design-patterns.md 添加 inbound link）
- 已知局限：
  - factory-method 链接冲突：basename `factory-method` 同时被 `sources/articles/factory-method.md` 和 `concepts/programming/factory-method.md` 共享，Obsidian 解析到前者（按字母序）。建议重命名源摘要页为 `factory-method-refactoring-guru.md` 以避免歧义。

## [2026-04-18] lint | 健康检查（每日 cron）

- 类型：lint
- 日期：2026-04-18 23:00 (cron每日任务)
- 健康统计：
  - 总页面：53 wiki pages
  - 孤立页面：1（concepts/backend-architecture.md，无入站 wikilinks）
  - 断链：0 ✅（使用正确的 Obsidian 路径解析逻辑）
  - 源摘要页：9 个（sources/）
  - 超大页面（>200行）：1 个（message-queue.md 278行，建议拆分）
- 修复：
  - 修复 nuwa-skill.md 的错误路径 `../../wiki/entities/` → `../../entities/`
- 备注：
  - 晨报 2026-04-18 已摄入（Claude Design / Claude 4.7 Tokenizer / GitHub Trending）
  - index.md 链接解析正常（title-only 格式可正确解析到各概念/实体页）
  - source pages 使用 `../` 相对路径到 raw/ 正常

## [2026-04-19] ingest | 晨报 2026-04-19 + 工厂方法

- 类型：morning-brief, article
- 新增源摘要：
  - wiki/sources/morning-briefs/2026-04-19.md
  - wiki/sources/articles/factory-method.md
- 更新页面：
  - concepts/programming/factory-method.md（添加 Refactoring Guru 源摘要）
  - concepts/backend-architecture.md（修复 orphan，添加工厂方法链接）
- index.md 更新：+2 源摘要（53→55页）
- 晨报摘要：Opus 4.7 模型对比 / 日本铁路 / B-52 星跟踪器 / OpenAI Agents Python / DeepGEMM / Dive into LLMs

## [2026-04-18] ingest | 晨报 2026-04-18

- 类型：morning-brief
- 来源：raw/morning-briefs/2026-04-18.md
- 新增页面：sources/morning-briefs/2026-04-18.md
- 摘要：HN Top 话题 Claude Design（1009分）、Claude 4.7 Tokenizer成本分析（597分）；GitHub Trending 新项目 GenericAgent、dive-into-llms


## [2026-04-20] ingest | 晨报 2026-04-20 + Stars 更新

- 类型：morning-brief, update
- 来源：raw/morning-briefs/2026-04-20.md
- 新增页面：
  - wiki/sources/morning-briefs/2026-04-20.md（Vercel 安全事件 / caveman 39K / MemPalace 48K / graphify 31K）
- 更新页面（Stars 刷新）：
  - entities/products/mempalace.md（46K→48K）
  - entities/products/nuwa-skill.md（11.3K→13K）
  - entities/products/zhangxuefeng-skill.md（5.9K→6.2K）
  - entities/products/graphify.md（27K→31K）
  - entities/products/career-ops.md（33K→37K）
- 修复：
  - concepts/backend-architecture.md 添加微服务链路（microservices.md、cloud-deployment.md）
- index.md 更新：+1 源摘要（55→56页），Stars 数据全部刷新
- 备注：Vercel 4月安全事件（718分）成当日 HN Top1，Skills 生态持续强劲增长

## [2026-04-20] lint | 健康检查

- 类型：lint
- 总页面：51 wiki pages（不含 sources/）
- 孤立页面：1（concepts/backend-architecture.md，已修复）
- 断链：0 ✅（正确的 Obsidian 路径解析逻辑）
- 源摘要页：12 个（sources/）
- 超大页面（>200行）：
  - log.md: 280 行（日志累积，正常）
  - concepts/programming/message-queue.md: 278 行（建议拆分）
- 修复：
  - concepts/backend-architecture.md 添加来自 microservices.md 和 cloud-deployment.md 的入站链接
  - index.md Stars 数据与 2026-04-20 GitHub Trending 对齐
- 备注：断链检测使用完整 .md 后缀剥离 + title/basename 双重解析，无误报

## [2026-04-21] ingest | 晨报 2026-04-21

- 类型：morning-brief
- 来源：raw/morning-briefs/2026-04-21.md
- 新增页面：
  - wiki/sources/morning-briefs/2026-04-21.md（Apple CEO 交接 / Qwen3.6 / OpenClaw Claude CLI 复活 / OpenAI agents-python 905 Stars）
- 更新页面：
  - concepts/ai/multi-agent.md（补充 openai-agents-python 框架 + sources/morning-briefs/2026-04-21 链接）
- index.md 更新：+1 源摘要（56→57页）
- 备注：Anthropic 重新允许 OpenClaw-style Claude CLI（HN 140分），OpenAI 发布 multi-agent Python 框架（905 Stars）

## [2026-04-21] lint | 健康检查

- 类型：lint
- 总页面：53 wiki pages（不含 sources/）
- 孤立页面：0 ✅
- 断链：0 ✅
- 源摘要页：13 个（sources/）
- 超大页面（>200行）：0 ✅
- frontmatter 缺失：0 ✅
- 备注：健康

## [2026-04-23] ingest | 晨报 2026-04-23

- 类型：morning-brief
- 来源：raw/morning-briefs/2026-04-23.md
- 新增页面：wiki/sources/morning-briefs/2026-04-23.md（Apple 删除消息漏洞修复 / Firefox Tor 隐私问题 / Over-editing 讨论）
- index.md 更新：+1 源摘要（58→59页）
- 备注：Apple iPhone 删除消息提取漏洞已修复；Firefox Tor 隐私标识符问题引发关注；无技术 tractors 创业受热议（1697分）；AI Over-editing 行为讨论升温

## [2026-04-23] lint | 健康检查与修复

- 类型：lint
- 日期：2026-04-23 23:00 (cron每日任务)
- 健康统计：
  - 总页面：62 wiki pages（含 sources/）
  - 孤立页面：0 ✅
  - 断链：0 ✅（修复了 9 个断链：index.md 路径修正、sources 路径修正、mediator/chain-of-responsibility 指向 design-patterns）
  - 源摘要页：15 个（sources/）
  - 超大页面（>200行）：4（log.md 393行 / canary-deployment 333行 / message-queue 278行 / read-after-write 213行）
  - frontmatter 缺失：0 ✅
- 修复内容：
  - index.md：programming/X → concepts/programming/X（4处）
  - concepts/design-patterns.md：programming/observer-pattern\ → concepts/programming/observer-pattern（1处，修复尾部反斜杠）
  - concepts/programming/observer-pattern.md：mediator/chain-of-responsibility → design-patterns（2处）
  - concepts/programming/spa-history-fallback.md：programming/canary-deployment → concepts/programming/canary-deployment（1处）
  - sources/articles/observer-pattern.md：../../../wiki/concepts/ → ../../concepts/（1处），删除 [[../observer-pattern]] 自引用（1处）
- 备注：健康


## [2026-04-24] ingest | 晨报 2026-04-24

- 类型：morning-brief
- 来源：raw/morning-briefs/2026-04-24.md
- 新增页面：wiki/sources/morning-briefs/2026-04-24.md（DeepSeek v4 / GPT-5.5 / Bitwarden CLI 供应链攻击 / Meta 裁员）
- index.md 更新：+1 源摘要（59→60页）
- 备注：DeepSeek v4 位列 HN 榜首；GPT-5.5 发布（1334分）；Bitwarden CLI 遭遇供应链攻击；Meta 宣布裁员 10%

## [2026-04-24] lint | 健康检查

- 类型：lint
- 日期：2026-04-24 23:00 (cron每日任务)
- 健康统计：
  - 总页面：63 wiki pages（含 sources/）
  - 孤立页面：0 ✅
  - 断链：0 ✅
  - 源摘要页：16 个（sources/）
  - 超大页面（>200行）：4（log.md 398行 / canary-deployment 333行 / message-queue 278行 / read-after-write 213行）
  - frontmatter 缺失：0 ✅
  - 过期页面（>90天）：0 ✅
- 备注：健康

## [2026-04-25] ingest | 晨报 2026-04-25

- 类型：morning-brief
- 来源：raw/morning-briefs/2026-04-25.md
- 新增页面：wiki/sources/morning-briefs/2026-04-25.md（Google $40B 投资 Anthropic / Hugging Face ml-intern 开源 / free-claude-code）
- index.md 更新：+1 源摘要（60→61页）
- 备注：本周最大新闻 Google-Anthropic 投资；ml-intern 作为开源 ML Agent 新标杆；free-claude-code 引发 Claude Code 免费化讨论

## [2026-04-25] lint | 健康检查

- 类型：lint
- 日期：2026-04-25 23:00 (cron每日任务)
- 健康统计：
  - 总页面：64 wiki pages（含 sources/）
  - 孤立页面：0 ✅
  - 断链：0 ✅
  - 源摘要页：17 个（sources/）
  - 超大页面（>200行）：4（log.md 421行 / canary-deployment 333行 / message-queue 278行 / read-after-write 213行）
  - frontmatter 缺失：0 ✅
  - 过期页面（>90天）：0 ✅
- 备注：健康

## [2026-04-26] ingest | 晨报 2026-04-26

- 类型：morning-brief
- 来源：raw/morning-briefs/2026-04-26.md
- 新增页面：
  - wiki/sources/morning-briefs/2026-04-26.md
  - wiki/entities/products/deepep.md
  - wiki/entities/products/roo-code.md
- 更新页面：
  - concepts/ai/multi-agent.md（添加 Roo-Code 到框架表格）
  - wiki/index.md（+2 实体，+1 源摘要，统计更新至 64 页）
- 备注：ChatGPT 解决 Erdős 问题（AI for Science 里程碑）；DeepEP（DeepSeek MoE 通信库）；Roo-Code（VS Code AI 多智能体团队）

## [2026-04-26] lint | 健康检查

- 类型：lint
- 日期：2026-04-26 23:00 (cron每日任务)
- 健康统计：
  - 总页面：67 wiki pages（含 sources/）
  - 孤立页面：0 ✅
  - 断链：0 ✅
  - 源摘要页：19 个（sources/）
  - 超大页面（>200行）：4（log.md 446行 / canary-deployment 333行 / message-queue 278行 / read-after-write 213行）
  - frontmatter 缺失：0 ✅
  - 过期页面（>90天）：0 ✅
- 备注：健康

## [2026-04-27] ingest | 晨报 2026-04-27
- 类型：morning-brief
- 来源：raw/morning-briefs/2026-04-27.md
- 新增页面：
  - wiki/sources/morning-briefs/2026-04-27.md
  - wiki/entities/products/mattpocock-skills.md
  - wiki/entities/products/posthog.md
  - wiki/entities/products/typescript-go.md
- 更新页面：
  - concepts/ai/ai-skills.md（添加 mattpocock/skills 到项目一览表）
  - wiki/index.md（+3 实体，+1 源摘要，统计更新至 67 页）
- 备注：mattpocock/skills（Claude Code 技能目录开源）、PostHog（产品分析平台持续在榜）、typescript-go（微软官方 TS→Go 转译）

## [2026-04-27] lint | 健康检查
- 日期：2026-04-27 23:00 (cron每日任务)
- 健康统计：
  - 总页面：71 wiki pages（含 sources/）
  - 孤立页面：0 ✅
  - 断链：0 ✅
  - 源摘要页：20 个（sources/）
  - 超大页面（>200行）：3（canary-deployment 333行 / message-queue 278行 / read-after-write 213行）
  - frontmatter 缺失：0 ✅
  - 过期页面（>90天）：0 ✅
- 备注：健康

## [2026-04-23] create | 电商支付弹窗 Excalidraw 原型图
- 文件：wiki/assets/ecommerce-payment-modal.excalidraw
- 操作：新增 Excalidraw 手绘风格原型图
- 内容：电商支付弹窗，含标题栏、订单摘要、支付方式 Tab（银行卡/电子钱包/货到付款/花呗）、银行卡表单输入、确认支付按钮
- 备注：使用 wiki/assets/ 目录存放图片和原型图资源

## [2026-04-23] ingest | React Query vs SWR：服务端状态管理源码对比

- 类型：article
- 来源：raw/frontend/react/react-query-vs-swr-server-state-source-compare.md
- 新增页面：
  - sources/articles/react-query-vs-swr-server-state-source-compare.md
  - concepts/programming/server-state-management.md
  - entities/products/tanstack-query.md
  - entities/products/swr.md
- 备注：深度对比 TanStack Query v5 与 SWR v2 的缓存架构（Query/Observer 状态机 vs cache Map）、请求去重策略（Query 内聚 in-flight vs dedupingInterval 时间窗）、新鲜度语义（staleTime/gcTime vs dedupingInterval）、Mutation 能力差异；明确了两者均不适合管理 UI 状态

## [2026-04-27] learn | React 页面状态管理反模式与重构

- 来源项目：horizon-web-commerce
- 页面：concepts/programming/react-page-state-antipatterns.md （新增）
- 关联更新：concepts/programming/unified-payment-route.md （追加 2026-04-27 重构记录与项目标签）
- 操作：新增概念页 + 更新关联页面
- 备注：从支付页 OAuth 回跳白屏 debug 中提炼四类 React 页面状态反模式（布尔语义过载 / 内存态单源 / 隐式状态机 / 字段级三源合并），配对记录对应的重构模式（双布尔拆分 / sessionStorage + phase 字段 / 显式 phase 状态机集中转移 / usePaymentContext 整对象选源）。落地为两个 OpenSpec change：fix-payment-oauth-redirect-whitescreen（最小止血）+ refactor-payment-page-state-machine（结构重构）

## [2026-04-27] ingest | Bulletproof React — 生产级 React 架构指南

- 类型：article（GitHub 仓库文档）
- 来源：raw/articles/bulletproof-react/（13 个 markdown 文件：README + application-overview + project-standards + project-structure + components-and-styling + api-layer + state-management + error-handling + testing + security + performance + deployment + additional-resources）
- 新增页面：
  - sources/articles/bulletproof-react-github.md
  - entities/persons/alan-alickovic.md
  - entities/products/bulletproof-react.md
  - concepts/programming/feature-based-architecture.md
- 关联更新：
  - concepts/programming/server-state-management.md（追加 bulletproof-react 为 source）
  - concepts/programming/react-page-state-antipatterns.md（追加 bulletproof-react 为 source，新增"上位框架：React 状态五分类"小节 + 交叉链接 feature-based-architecture）
- 备注：ingest GitHub 35K+ 星的 React 架构指南。核心贡献：(1) feature-based 项目结构 + ESLint import/no-restricted-paths 强制单向依赖（shared → features → app）；(2) React 状态五分类框架（Component / Application / Server Cache / Form / URL），为既有的 react-page-state-antipatterns 提供上位分类；(3) 反 barrel file 主张，与多数样板建议相反。暂缓为"状态五分类"/"Error Boundary 多实例"/"JWT 存储策略"建独立概念页——照抄单一来源，等第二份资料再抽象。

## [2026-04-28] ingest | React Bits — 组件层经典反模式词典

- 类型：article（GitHub 仓库文档）
- 来源：raw/articles/react-bits/（README + anti-patterns/*.md 8 篇 + gotchas/01.pure-render-checks.md）
- 新增页面：
  - sources/articles/react-bits-github.md
  - concepts/programming/react-classic-antipatterns.md
- 关联更新：
  - concepts/programming/react-page-state-antipatterns.md（"相关概念"区追加 react-classic-antipatterns 作为互补的微观视角）
- 备注：ingest GitHub 17K+ 星的 React 反模式词典。成书于 2017 Class 组件时代，7 个反模式中：3 个随 API 废弃已失效（findDOMNode / Mixins / componentWillMount），4 个在 Hooks 时代仍普遍存在（Props in Initial State → derived state / Mutating State / Index as Key / Spread Props on DOM），gotcha（Pure Render Checks）映射为现代 React.memo + useMemo/useCallback 的引用稳定性问题。在概念页中为每个反模式标注 Hooks 时代对等形态，让 Class 时代的词典可被现代代码复用。未建实体页——作者 vasanthk 只是 README 维护者，非该反模式分类体系的学术贡献者；react-bits 本身作为文档汇编未建 entity 产品页。与 react-page-state-antipatterns 形成"宏观页面层 + 微观组件层"的反模式全景。

## [2026-04-28] refactor | 抽出独立概念页 "React 状态五分类"

- 操作：从 react-page-state-antipatterns 的"上位框架"小节抽出
- 新增页面：concepts/programming/react-state-categories.md
- 关联更新：
  - concepts/programming/react-page-state-antipatterns.md（"上位框架"小节精简为"反模式 → 状态类别"映射表；"相关概念"区追加 react-state-categories）
  - concepts/programming/server-state-management.md（新增"相关概念"区，加 react-state-categories；追加 bulletproof-react 为 source）
  - sources/articles/bulletproof-react-github.md（"提到的概念"区追加 react-state-categories）
- 备注：上次 ingest bulletproof-react 时该分类被写在 react-page-state-antipatterns 页里作为"上位框架"小节，现抽离为独立概念页。理由：(1) 状态五分类是社区共识框架（TkDodo、Kent Dodds 等都独立讨论过），非 bulletproof-react 原创，但后者是较早把分类清晰化的公共文档；(2) 独立成页后，react-page-state-antipatterns / server-state-management / bulletproof-react 三处均可通过 wikilink 指向同一份"来源分类"权威解释，不再复述；(3) 展开后补充了五类各自的判断标准、分类边界困惑（登录用户/modal/wizard 算哪类）和常见误区。

## [2026-04-28] refactor | 引入项目工作流（projects/）
- 类型：refactor
- 范围：wiki 架构扩展，新增第四类工作流 "Project"
- 变更：
  - CLAUDE.md 新增「项目工作流」章节（目录规范、命名 YYYY-MM-short-name、生命周期、知识回流机制、页面 frontmatter）
  - 新增 skill：`.claude/skills/project-start/SKILL.md`（启动新项目）
  - 新增 skill：`.claude/skills/project-retro/SKILL.md`（阶段性 / 终结性复盘 + 知识回流到 wiki/concepts、synthesis、entities）
  - wiki/index.md 顶部新增「活跃项目」表格
- 动机：wiki/ 是主题驱动的稳定知识博物馆，缺一个项目驱动、有时间边界、有交付物的"工作台"。projects/ 与 raw/ wiki/ 平级，让具体工作有地方落地，复盘后把可复用知识抽到 wiki。

## [2026-04-28] project-start | 2026-04-kaigao
- 类型：project-start
- 目录：projects/2026-04-kaigao/
- 目标：为外部代码仓 `/Users/zhouyangdong/Documents/projects/kaigao`（开稿 KaiGao — AI 论文写作助手）提供知识与产出管理台
- 外部关联：/Users/zhouyangdong/Documents/projects/kaigao
- 骨架：README / brief / log / retro / raw / notes / deliverables 全部就位
- 备注：brief.md 的"目标 / 非目标 / 范围 / 交付物 / 里程碑"五节为占位，等待与用户首次讨论后补齐
