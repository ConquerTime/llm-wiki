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
  - 断链：1（`entities/products/obsidian.md` 中 `[[page]]` 为语法示例，非真实链接）
  - frontmatter：16/16 完整
  - 过时页面：0
  - 超大页面：0
- 修复：
  - 为 `obsidian.md` 增加 `[[llm-wiki]]` 出站链接，提升页面互联度
- wiki 规模：16 页（8 概念 · 6 实体 · 2 源摘要）
- 提交：76d34b1
