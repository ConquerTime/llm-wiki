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
