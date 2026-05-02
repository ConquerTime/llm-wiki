# Code Agent 从零实现 · 活动日志

> 追加式时间线，记录讨论、决策、产出、阻塞。

---

## [2026-04-30] 启动

- 项目创建，目录初始化
- 与用户对齐目标：从 0 实现 code agent，以动手实践方式学习 Claude Code 技术架构
- 范围：收集 GitHub 泄露源码 → 架构分析 → 关键模块实现 → 知识回流 wiki
- 产出物：架构分析文档、工具系统实现、REPL 主循环、上下文管理机制

## [2026-04-30] 资料收集第一轮（初步筛选）
- 搜索并识别 GitHub 上 20+ 个相关仓库
- 初步筛选出 catyans / luyao618 / jiji262 三个分析仓库
- 抓取若干原始资料到 raw/（后续被替换）

## [2026-04-30] 资料收集第二轮（确定主知识源）
- 用户指出两个质量更高的核心仓库，确定为主要知识源：
  - `shareAI-lab/learn-claude-code`（57k+ stars）— "Bash is all you need"，12 课递进式 Python 最小实现
  - `NanmiCoder/cc-haha` — 本地可运行 TS 版 + 生产级实现文档
- 删除第一轮筛选的 raw 文件，重建 raw/ 目录结构：
  - `raw/learn-claude-code/` — s01~s12 共 12 章 + README-zh（哲学总纲）
  - `raw/cc-haha/` — agent / memory / skills / channel / computer-use 实现文档 8 份
- 重写核心笔记：
  - `notes/01-harness-philosophy.md` — Agent = Model + Harness 核心哲学
  - `notes/02-s01-s12-roadmap.md` — 完整学习路线图，Python 最小实现 ↔ TS 生产实现对照
- 确立 5 周学习节奏（周 1 s01-s03、周 2 s04-s06、周 3 s07-s08、周 4 s09-s12、周 5 复盘）

## [2026-04-30] 修复 cc-haha/index.md 在 Obsidian 中不可读
- 现象：`raw/cc-haha/index.md` 原文是 VitePress 首页配置，**整文件仅 frontmatter**（嵌套 `hero` / `features` 对象），Obsidian 打开只看到截断的属性表，无正文可读
- 处理：保留原 frontmatter 一个字符不改，仅在其后**追加** markdown body（特性表 + 同目录实现文档的 wikilink 索引），信息零损失
- 说明：这是对"raw/ 一律不修改"的一次 additive 例外；未来若再遇同类纯配置文件，沿用该策略
