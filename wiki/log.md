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
- Lint：140 页，孤儿 1（log-2026.md 归档文件），断链 225 均为已知情况

---

## [2026-05-10] lint | 140 pages, 1 orphan, 225 known-broken-links
- 孤儿页：1（log-2026.md 归档日志，预期无 inbound 链接）
- 断链：225（均为已知可接受情况）
  - ai-toolkit.md → [[条目]]（用户自定义占位符，非错误）
  - index.md/log-2026.md → projects/practices/writing/（跨 wiki 目录链接，acceptable known limitation）
  - log-2026.md → raw/articles/...、wiki/sources/...（历史日志占位符，不操作）
- 未收录 index：0
- 过期页（>90天）：待检查

---

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

---

## [2026-05-13] lint | 140 pages, 1 orphan, 230 known-broken-links, 5 missing-from-index fixed
- 孤儿页：1（log-2026.md 归档日志，预期无 inbound 链接）
- 断链：230，均为已知情况（ai-toolkit 占位符 + 跨目录链接 + 历史日志占位符）
- 未收录 index：5 → 0（修复 ibm/ladybird/videolan 组织页 + morning-briefs 2026-05-08/09 + greentrain-skills-readme）
- 过期页（>90天）：0
- 大页面（>200行）：8（log-2026.md 归档 + 7 个概念/综合页）
- ingest：0（无新 raw 文件）
- index 更新：实体 45→48，源摘要 39→41，总页数 128→139
- Frontmatter：3 个缺失（index.md、log.md、log-2026.md，预期无 frontmatter）

---

## [2026-05-14] ingest | 晨报 2026-05-01 + lint
- 类型：ingest + lint
- 新增源摘要（1）：
  - wiki/sources/morning-briefs/2026-05-01.md — 晨报（HN: NSA监控/车辆数据收集争议/Linux漏洞；GH: Warp终端AI开发环境）
- index 更新：源摘要 41→42，总页数 137→138
- Lint：140 pages，孤儿 1（log-2026.md 归档），断链 228 均为已知情况

---

## [2026-05-15] lint | 141 pages, 1 orphan, 40 broken (9 pre-existing), 6 large pages fixed
- 类型：lint + broken-link fix
- 修复断链（15处）：
  - synthesis/ 页面：`../concepts/` → `concepts/` 路径修正（monolith-async-worker, microservices, clean-code, backend-architecture, solid-principles, factory-method, observer-pattern, cloud-deployment 等）
  - entities/ 页面：`wiki/sources/` 前缀修正为相对路径（greentrain-skills, swr, tanstack-query, cloudflare, canvas）
  - entities/persons simon-willison：`.md` 后缀去除
  - entities/products open-agents/ruflo：`.md` 后缀去除
  - sources/morning-briefs 2026-05-07/08：`.md` 后缀去除（9处）
- Lint 结果：
  - 孤儿页：1（log-2026.md 归档，预期无 inbound 链接）
  - 断链：40（sources/ 页面预存在 9 个：claude-code/warp/free-claude-code/ml-intern/CloakBrowser/addyosmani-agent-skills/local-deep-research 无对应 entity 页；已知可接受 31 个：projects/practices/ai-toolkit 等）
  - 未收录 index：0（log-2026.md 归档预期）
  - 过期页（>90天）：0
  - 大页面（>200行）：6（synthesis x2, concepts/programming x4）
- ingest：0（无新 raw 文件）

---

## [2026-05-16] lint | 141 pages, 1 orphan, 79 known-broken-links, 0 new-ingest
- 类型：lint
- ingest：0（无新 raw 文件；Claude Code Prompt Caching 和 Building Effective AI Agents 已于 2026-05-10 摄入）
- Lint 结果：
  - 孤儿页：1（log-2026.md 归档日志，预期无 inbound 链接）
  - 断链：79，均为已知可接受情况：
    - ai-toolkit.md → `[[条目]]` 占位符（用户自定义，非错误）
    - log.md/log-2026.md → `[[条目]]` 占位符 + `[[programming/X]]` 历史日志占位符
    - sources/ 页面 → 无对应 entity 页的简称引用（claude-code, anthropic, warp, free-claude-code, ml-intern, CloakBrowser, addyosmani/agent-skills, local-deep-research）
    - cross-dir 链接（projects/practices/writing/）→ acceptable known limitation
  - 未收录 index：0
  - 过期页（>90天）：0
  - 大页面（>200行）：8（log-2026.md 归档 + synthesis x2 + concepts x4 + projects x1）

---

## [2026-05-17] lint | 141 pages, 1 orphan, 82 known-broken-links, 0 new-ingest
- 类型：lint
- ingest：0（无新 raw 文件；raw/morning-briefs/ 最新到 2026-05-09，与 wiki/sources/morning-briefs/ 对应，无新增）
- Lint 结果：
  - 孤儿页：1（log-2026.md 归档日志，预期无 inbound 链接）
  - 断链：82，均为已知可接受情况：
    - ai-toolkit.md → `[[条目]]` 占位符（用户自定义，非错误）
    - log.md/log-2026.md → `[[条目]]` 占位符 + `[[concepts/programming/X]]` 历史日志占位符
    - sources/ 页面 → 无对应 entity 页的简称引用（claude-code, anthropic, warp, free-claude-code, ml-intern, CloakBrowser, addyosmani/agent-skills, local-deep-research）
    - entities/products/quant-engine.md + tushare-pro.md → projects/（跨目录链接，acceptable known limitation）
    - concepts/pkm/zettelkasten.md → `[[wikilink]]`（用户自定义占位符，非错误）
  - 未收录 index：0
  - 过期页（>90天）：0
  - 大页面（>200行）：8（log-2026.md 归档 + synthesis x2 + concepts x4 + projects x1）


## [2026-05-18] lint | 141 pages, 0 orphans, 19 broken-links fixed, 0 new-ingest
- 类型：lint + broken-link fix
- ingest：0（无新 raw 文件；raw/morning-briefs 最新到 2026-05-09，与 wiki/sources/morning-briefs/ 对应）
- 修复断链（19处）：sources frontmatter 中的 wikilink → 纯相对路径
  - concepts/ai/ai-skills.md（2处）
  - entities/products/ 下 12 个产品页的 sources frontmatter（17处）
  - 修复：`[[raw/morning-briefs/...|晨报...]]` → `../../../raw/morning-briefs/...`
- Lint 结果：
  - 孤儿页：0
  - 断链：1（log.md 历史描述中的 `claude-code`，非真实链接）
  - 未收录 index：0
  - 过期页（>90天）：0
  - 大页面（>200行）：8（log-2026.md 915行已归档 + synthesis x2 + concepts x4 + index.md 217行）

---

## [2026-05-19] lint | 141 pages, 0 orphans, 132 known-broken-links, 0 new-ingest
- 类型：lint
- ingest：0（无新 raw 文件；raw/morning-briefs 最新到 2026-05-09，与 wiki/sources/morning-briefs/ 对应）
- Lint 结果：
  - 孤儿页：0
  - 断链：132，均为已知可接受情况：
    - ai-toolkit.md → `[[条目]]` 占位符（用户自定义，非错误，8处）
    - log-2026.md → `raw/articles/...` 历史日志占位符（48处）
    - index.md/log-2026.md → projects/practices/writing/ 跨目录链接（44处，acceptable known limitation）
    - log-2026.md → `concepts/programming/X` 等历史占位符（32处）
  - 未收录 index：0
  - 过期页（>90天）：0
  - 大页面（>200行）：8（log-2026.md 915行已归档 + synthesis x2 + concepts x4 + index.md 217行）
  - Frontmatter 缺失：0

## [2026-05-20] lint | 141 pages, 1 orphan, 133 known-broken-links, 0 new-ingest
- 类型：lint
- ingest：0（无新 raw 文件；raw/morning-briefs 最新到 2026-05-09，与 wiki/sources/morning-briefs/ 对应）
- Lint 结果：
  - 孤儿页：1（log-2026.md，已归档的旧日志，预期状态）
  - 断链：133，均为已知可接受情况：
    - ai-toolkit.md → `[[条目]]` 占位符（1处，用户自定义，非错误）
    - log-2026.md → `raw/articles/...` 历史日志占位符（48处）
    - index.md/log-2026.md → projects/practices/writing/ 跨目录链接（44处，acceptable known limitation）
    - log-2026.md → `concepts/programming/X` 等历史占位符（40处）
  - 未收录 index：1（log-2026.md，已归档，预期状态）
  - 过期页（>90天）：0
  - 大页面（>200行）：8（log-2026.md 915行已归档 + synthesis x2 + concepts x4 + index.md 217行）

---

## [2026-05-21] lint | 141 pages, 1 orphan (log-2026.md), 134 known-broken-links, 0 new-ingest
- 类型：lint
- ingest：0（无新 raw 文件；raw/morning-briefs 最新到 2026-05-09，与 wiki/sources/morning-briefs/ 对应，无新增）
- Lint 结果：
  - 孤儿页：1（log-2026.md，已归档日志，预期无 inbound 链接）
  - 断链：134，均为已知可接受情况：
    - ai-toolkit.md → `[[条目]]` 占位符（用户自定义，非错误）
    - sources/ 页面 → `[[raw/...]]` wikilink（raw 文件不是 wiki 页面，expected）
    - concepts/entities → `[[raw/...]]` 和 `[[projects/...]]` 跨目录引用（acceptable known limitation）
    - log.md/log-2026.md → 历史日志占位符（concepts/programming/X、raw/articles/... 等）
  - 未收录 index：0
  - 过期页（>90天）：0
  - 大页面（>200行）：8（log-2026.md 915行 + synthesis x2 + concepts x4 + index.md 217行）
  - Frontmatter：3（index.md/log.md/log-2026.md 预期无 frontmatter）
## [2026-05-22] lint | 141 pages, 0 orphans, 88 broken-links (all known), 0 new-ingest
- 类型：lint
- ingest：0（无新 raw 文件；raw/morning-briefs 最新到 2026-05-09，与 wiki/sources/morning-briefs/ 对应，无新增）
- Lint 结果：
  - 孤儿页：0
  - 断链：88，均为已知可接受情况：
    - `[[条目]]` 占位符（11处，用户自定义，非错误）
    - `projects/` 跨目录链接（42处，acceptable known limitation）
    - `wiki/sources/...` 历史日志占位符（1处，log-2026.md）
    - practices/writing/ 等目录外链接（34处，Obsidian title/basename 解析，acceptable known limitation）
  - 未收录 index：0
  - 过期页（>90天）：0
  - 大页面（>200行）：9（log-2026.md 915行已归档 + concepts x4 + synthesis x2 + index.md 217行）
