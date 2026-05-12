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

---

## [2026-05-10] ingest | 3 new sources + 2 entities + 2 concept updates
- 类型：ingest
- 新增源摘要（3）：
  - wiki/sources/morning-briefs/2026-05-09.md — 晨报（HN Top + GitHub Trending）
  - wiki/sources/articles/claude-code-prompt-caching.md — Claude Code prompt caching 优化实践
  - wiki/sources/articles/anthropic-building-effective-ai-agents.md — Anthropic Building Effective AI Agents
- 新增实体页（2）：
  - wiki/entities/products/deepseek-tui.md — 终端 DeepSeek 编程助手（3,731 ⭐）
  - wiki/entities/products/agent-skills.md — addyosmani 的生产级 AI coding skills（1,893 ⭐）
- 更新概念页（2）：
  - concepts/ai/context-engineering.md — 新增 Claude Code Prompt Caching 优化案例
  - concepts/ai/ai-agent.md — 新增 Anthropic Workflows vs Agents 区分 + Agent 三原则
- 新增 index 实体：DeepSeek-TUI、agent-skills（2 → 45）
- 新增 index 源摘要：claude-code-prompt-caching、anthropic-building-effective-ai-agents（37 → 39）
- Lint：140 页，孤儿 1（log-2026.md 归档文件），断链 225 均为已知情况（ai-toolkit 占位符 + 跨目录链接 + 历史日志占位符）

## [2026-05-10] lint | 140 pages, 1 orphan, 225 known-broken-links
- 孤儿页：1（log-2026.md 归档日志，预期无 inbound 链接）
- 断链：225（均为已知可接受情况）
  - ai-toolkit.md → [[条目]]（用户自定义占位符，非错误）
  - index.md/log-2026.md → projects/practices/writing/（跨 wiki 目录链接，acceptable known limitation）
  - log-2026.md → raw/articles/...、wiki/sources/...（历史日志占位符，不操作）
- 未收录 index：0
- 过期页（>90天）：待检查（需对比 raw 文件时间）


## [2026-05-11] lint | 140 pages, 38 orphans, 371 broken-links
- 孤儿页：38（含 index.md/log.md/log-2026.md 预期无 inbound 链接）
- 断链：371 可分类为：
  - `raw/absolute` 路径（38）：概念页引用 `raw/articles/...` 应改为 `../../../raw/articles/...`
  - `sources/absolute` 路径（31）：概念页引用 `sources/articles/...` 应改为 `../../sources/articles/...`
  - `wiki/concepts/` 绝对路径（25）：应改为 `../concepts/...` 或仅用 basename
  - `wiki/sources/` 前缀（14）：应去掉 `wiki/` 前缀
  - `index.md` 中的 concept 链接（111）：指向不存在页面（子概念未建立）
  - `sources/page` 孤立引用（68）：来源摘要页引用实体/概念的简称（如 `[[claude-code]]`）未解析
  - 跨目录链接（projects/practices/writing，70）：acceptable known limitation
  - ai-toolkit 占位符（1）：`[[条目]]` 用户自定义格式，非错误
  - 历史日志占位符（20）：log-2026.md 中的历史记录，不操作
- 未收录 index：68（主要为 sources/ 页面）
- 过期页（>90天）：0
- 大页面（>200行）：8（含 log-2026.md 915行已归档）
## [2026-05-12] lint | 140 pages, 38 orphans, 373 known-broken-links, 9 large-pages
- 孤儿页：38（均为预期情况）
  - 35× sources/ 页面（frontmatter sources 字段引用，无 wikilink inbound）
  - index.md、log.md、log-2026.md（预期无 inbound 链接）
- 断链：373，可分类为已知情况（均不操作）
  - 84 other（index.md unresolved concept links + historical log placeholders）
  - 79 sources-absolute-path（index.md → sources/articles/ 无相对路径前缀）
  - 59 sources-relative-path（sources 页引用 [[pagename]] 未解析）
  - 47 raw-absolute-path（log-2026.md 历史日志占位符）
  - 44 cross-wiki-dir（index.md → projects/practices/writing，acceptable known limitation）
  - 43 unresolved-concept-link（index.md 引用尚未创建的 concept 页面）
  - 13 wiki-prefix（legacy wiki/concepts/ 前缀残留）
  - 4 ai-toolkit-placeholder（用户自定义 [[条目]] 格式，非错误）
- 未收录 index：4（log-2026.md 归档日志 + 2 morning-briefs + greentrain-skills-readme）
- 过期页（>90天）：0
- 大页面（>200行）：9
  - log-2026.md: 916行（归档，预期）
  - concepts/programming/canary-deployment.md: 334行
  - concepts/programming/react-page-state-antipatterns.md: 331行
  - synthesis/backend-architecture-stack.md: 307行
  - concepts/programming/message-queue.md: 279行
  - 另 4 个 200-300 行页面
- Frontmatter：3 个缺失（index.md、log.md、log-2026.md，预期无 frontmatter）

