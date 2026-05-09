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



## [2026-05-09] lint | 89 broken-links fixed + log rotation
- 类型：lint + fix
- 断链修复（89条）：
  - synthesis/backend-architecture-stack.md：修复 `wiki/concepts/` → `../concepts/` 前缀（共 28 处）
  - synthesis/react-architecture-stack.md：修复 `wiki/concepts/` → `../concepts/` 前缀 + 修复 `\\]]` 转义（共 52 处）
  - synthesis/react-architecture-stack.md sources frontmatter 修复
- 日志轮转：log.md (915行 > 500) → log-2026.md，新 log.md 重置
- 未修复的断链（不操作）：
  - ai-toolkit.md → [[条目]]（用户自定义占位符格式，非错误）
  - entities/ → concepts/ 链接（对应 concept 页面尚未建立）
  - sources/morning-briefs/*.md → entities/（morning-brief source 页面的正常引用）
  - log.md → `[[concepts/programming/X]]` 等历史占位符（不操作）
- 孤儿页：0（来源页预期无 inbound 链接）
- 未收录 index：0
- 过期页（>90天）：0
- 大页面：8（含 log.md 915 行已轮转）

