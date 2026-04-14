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

### 2026-04-14

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

