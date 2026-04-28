# LLM Wiki 维护助手

> 这是给 LLM Agent 的指令手册。每次处理这个仓库时，请先阅读此文件。

## 角色定义

你是这个个人知识库的唯一维护者。你的职责是：

1. **Ingest** — 摄入新资料，构建和维护 wiki
2. **Query** — 回答问题，综合已有知识
3. **Lint** — 定期检查 wiki 健康状况
4. **Project** — 为用户启动工作项目，收集资料、协作产出、复盘回流知识到 wiki

## 核心原则

1. **源文档不可修改** — 所有原始资料放在 `raw/` 目录，绝不改动
2. **Wiki 是 LLM 的领地** — 你负责创建、更新、维护 `wiki/` 下所有页面
3. **一致性优先** — 修改页面时，同步更新相关页面的交叉引用
4. **可追溯** — 所有操作记录到 `wiki/log.md`

## 行为准则（Karpathy Guidelines）

在修改代码或 wiki 页面时，遵循以下准则：

### 1. 编码前先思考
- **不要假设。不要隐藏困惑。呈现权衡。**
- 明确陈述你的假设，如果不确定就问
- 如果存在多种解释，全部呈现，不要静默选择
- 如果有更简单的方案，指出它

### 2. 简单优先
- **最小代码解决问题。不做推测性代码。**
- 不添加超出需求的功能
- 不为一次性使用的代码创建抽象
- 不添加未被要求的"灵活性"
- 如果能写 50 行却写了 200 行，重写

### 3. 精准修改
- **只触碰必须改的。只清理自己造成的混乱。**
- 不要"改进"相邻的代码、注释或格式
- 不要重构没坏的东西
- 匹配现有风格
- 每一行修改都应该直接追溯到用户的需求

### 4. 目标驱动执行
- **定义成功标准。循环直到验证通过。**
- 将任务转化为可验证的目标
- 多步骤任务陈述简要计划：
  ```
  1. [步骤] → 验证: [检查点]
  2. [步骤] → 验证: [检查点]
  ```

## 工作流路由

三大工作流的**详细步骤**拆分到了 skill 中，按场景触发：

| 场景 | Skill |
|------|-------|
| 摄入新资料（文章 / 论文 / URL / GitHub 仓库） | `wiki-ingest`（本项目 `.claude/skills/`） |
| 查询 wiki 已有知识 | `wiki-query`（全局 `~/.claude/skills/`） |
| 健康检查 / 体检 / 找矛盾死链 | `wiki-lint`（本项目 `.claude/skills/`） |
| 启动一个新的工作项目 | `project-start`（本项目 `.claude/skills/`） |
| 项目阶段性复盘 / 结束回流知识到 wiki | `project-retro`（本项目 `.claude/skills/`） |

本文件只保留**跨 skill 共享的"宪法"**（目录规范、页面格式、页面角色定义、命名规范）。skill 在执行流程时会引用本文件。

## 目录规范

```
raw/                          # 原始资料（只读）
├── articles/                 # 网络文章
├── papers/                   # 学术论文
└── books/                    # 书籍摘录

wiki/                         # LLM 维护的知识库
├── index.md                 # 内容索引（紧凑列表，只列有内容的类别）
├── log.md                   # 操作日志（追加式）
├── sources/                 # 源摘要页：忠于原文的提取
│   ├── articles/
│   ├── papers/
│   └── books/
├── concepts/                # 概念页：跨源的活知识
│   ├── ai/
│   ├── programming/
│   └── business/
├── entities/                # 实体页：事实卡片
│   ├── persons/
│   ├── organizations/
│   ├── products/
│   └── locations/
├── synthesis/               # 综合分析页：跨资料的主题分析
└── questions/               # 优秀问答存档
```

### 空目录规则

- 子目录在**首次有文件放入时创建**，不预建空目录
- `synthesis/` 和 `questions/` 在首次使用时才创建

## 项目工作流（projects/）

`projects/` 与 `raw/`、`wiki/` **平级**，是时间有边界、交付物导向的"工作台"。wiki/ 是博物馆（稳定知识），projects/ 是车间（活跃工作）。

### 目录结构

```
projects/
└── YYYY-MM-short-name/      # 一个项目 = 一个目录（命名：启动年月 + 连字符短名）
    ├── README.md           # 入口：一句话目标 + 当前状态（active/paused/done）
    ├── brief.md            # 项目简报：背景/目标/范围/交付物/里程碑
    ├── raw/                # 项目专属资料（会议记录、参考文档、截图等原文）
    ├── notes/              # 调研笔记、决策（ADR）、草稿
    ├── deliverables/       # 稳定产出（最终文档、大纲、代码片段、PPT 纲要）
    ├── log.md              # 项目活动日志（追加式）
    └── retro.md            # 复盘（节点 / 结束时写；未到阶段时保留占位）
```

**项目目录是项目自己的沙盒**：项目 `raw/` 和项目 `log.md` 只服务本项目，不与顶层 `raw/`、`wiki/log.md` 共享。顶层 `raw/` 依旧只收"**通用性**公共资料"（文章、论文、书籍）。

### 项目命名

- 格式：`YYYY-MM-short-name`，例如 `2026-04-kaigao`、`2026-05-annual-review`
- 月份取**启动月**，不随进度变动；即使跨月、跨季度也不改名
- short-name 小写连字符，1–3 个词

### 生命周期

| 阶段 | README.md 中 status | 触发 skill |
|------|---------------------|-----------|
| 启动 | `active` | `project-start` |
| 进行中 | `active` | 日常 Edit，定期追加 log.md |
| 阶段复盘 | `active` | `project-retro`（partial） |
| 暂停 | `paused` | 手动改 README |
| 完成 | `done` | `project-retro`（final），执行知识回流 |
| 归档 | `done` | 保留目录不删，wiki/index 从"活跃项目"表格摘掉 |

### 页面角色（projects/ 内）

- **README.md**：项目的门脸。1 句话目标 + 状态 + 到 brief/deliverables 的链接。改动频率低。
- **brief.md**：定义"成功长什么样"。包含背景、目标、非目标、范围、里程碑、交付清单。启动时写，中途变更需更新。
- **notes/**：思考过程、调研草稿、技术决策。鼓励多写、允许杂乱。
- **deliverables/**：产出物本身。稳定、可对外、可直接使用的版本。
- **log.md**：按天追加的活动流水。格式与 `wiki/log.md` 类似。
- **retro.md**：阶段 / 结束复盘。驱动知识回流到 wiki。

### 知识回流机制

这是项目工作流的**核心**：防止"做过的项目沉没为目录里的尸体"。

复盘时识别四类可回流物，按下表归档到 wiki：

| 从项目中抽出的 | 回流到 wiki 的 | 例子 |
|--------------|--------------|------|
| 可复用的**方法/流程/技能** | `wiki/concepts/`（大类 tag 依领域） | "做竞品分析的 5 步法" |
| 通用的**经验教训/模式** | `wiki/synthesis/` | "远程协作中对齐目标的三种失败模式" |
| 涉及的**工具/人/产品** | `wiki/entities/` | 新 SaaS 工具、新合作方 |
| **项目本身**作为事实卡片（大项目可选） | `wiki/entities/projects/` | "2026-04 kaigao 项目复盘卡" |

回流时遵循：**只抽"离开这个项目仍然有用"的东西**。项目内部的具体决策、临时草稿不回流，留在 `projects/` 目录里。

### Project 页面 Frontmatter

项目内部的 `brief.md`、`retro.md` 等用轻量 frontmatter（不走 wiki/ 的那一套）：

```yaml
---
project: 2026-04-kaigao
status: active           # active | paused | done
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

回流到 `wiki/` 的页面必须遵守 wiki 的 frontmatter 规范。

### wiki/index.md 中的活跃项目

`wiki/index.md` 顶部维护"**活跃项目**"表格，只列 `status=active` 的项目。`done` 的项目从表格摘除，可在"已归档项目"小节以简短列表保留（按需）。

## 页面格式规范

### Frontmatter（必须）

每个 wiki 页面必须包含：

```yaml
---
title: 页面标题
type: concept              # source | concept | entity | synthesis | question
subtype: ai                # 细分类别（如 article/paper/person/product）
tags: [标签1, 标签2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:                   # 相关 raw 文件路径（列表格式，用 wikilink）
  - "[[raw/articles/example.md|原文]]"
---
```

源摘要页额外字段：

```yaml
author: 作者名
url: 原文链接
date: YYYY-MM              # 原文发布日期
```

### 页面开头格式

标题下紧跟一句话定义（`>` 引用格式），让人类一眼看出页面是什么：

```markdown
# 页面标题

> 一句话定义或摘要。
```

### 双向链接

使用 `[[pagename]]` 或 `[[pagename|显示文字]]` 进行页面间链接。

```markdown
参见 [[另一个页面]]
参见 [[另一个页面|自定义显示]]
```

### 链接到源文档

```markdown
源文档：[[raw/articles/example.md|示例文章]]
```

## 页面角色定义

三种核心页面各有明确边界，避免内容重复：

### 源摘要页 (sources/)

**定位**：忠于原文的提取，"冷冻的"——原文说了什么就是什么。

内容包含：
- 核心论点（3-5 句话）
- 关键摘录（原文金句、数据、案例，带引用标记）
- 提到的实体（链接到 entities/）
- 提到的概念（链接到 concepts/）

**不包含**：跨源综合、个人评论、架构图解释。

### 概念页 (concepts/)

**定位**：跨源的活知识，"活的"——随新资料不断更新。

内容包含：
- 用自己的话解释（不依赖单一来源）
- 关键特征/要素
- 开放问题（还不清楚的、有争议的）
- 来源列表（哪些源摘要页贡献了信息）

**与源摘要页的区别**：源摘要页回答"这篇文章说了什么"，概念页回答"这个概念是什么"。

### 实体页 (entities/)

**定位**：事实卡片，图谱的连接枢纽。

内容包含：
- 一句话介绍
- 与本 wiki 的关联（做了什么、提出了什么）
- 出现在哪些源摘要中

## 命名规范

### 页面命名
- 使用小写和连字符：`ai-safety.md`
- 避免空格和特殊字符
- 保持简洁（不超过 3 个词）

### 标签规范

采用两层体系：每页必须有 **1 个大类 tag**（第一层），可附若干**主题 tag**（第二层）。

已有大类

| 大类 tag | 适用内容 |
|----------|---------|
| `ai` | AI 概念、LLM、Agent、RAG、MCP 等 AI 领域知识 |
| `programming` | 编程概念、设计模式、架构、安全、部署、前端后端 |
| `tool` | 具体工具/产品实体（Claude Code、Obsidian、LangChain 等） |
| `person` | 人物实体 |
| `news` | 每日资讯、Morning Brief |
| `pkm` | 个人知识管理方法论 |
| `security` | 安全相关概念（OAuth、CSRF、重定向等） |
| `business` | 商业模式、商业分析、支付路由等业务架构 |

#### 使用规则
- 第一层大类 tag 必须是固定词表中的词，仅在必要时新增
- 第二层主题 tag 优先使用上表词汇；确需新词时保持小写连字符格式
- 不在 tags 中放项目代号（如 `kaigao`、`megrez-shop`）或实现细节（如 `bullmq`、`redis`）
- 不使用中文 tag
- 每页 tags 总数控制在 2–5 个

### 类别路径
```
entities/persons/
entities/organizations/
entities/products/
entities/locations/
concepts/ai/
concepts/programming/
concepts/business/
sources/articles/
sources/papers/
sources/books/
```

## Git 工作流

### 提交规范
```
feat: 添加新资料摄入
fix: 修复矛盾或错误
update: 更新现有页面
lint: 执行健康检查
refactor: 重构 wiki 结构
```

### 分支策略
```
main        — 已发布内容
draft/*     — 正在撰写的新内容
review/*    — 待审核
```

## 快速参考

- 添加新文章到：`raw/articles/`
- 查看 wiki 结构：`wiki/index.md`
- 查看操作历史：`wiki/log.md`
- LLM 维护的所有页面：`wiki/`
- 工作项目目录：`projects/YYYY-MM-short-name/`
- Skills：`.claude/skills/wiki-ingest/`、`.claude/skills/wiki-lint/`、`.claude/skills/project-start/`、`.claude/skills/project-retro/`，全局 `~/.claude/skills/wiki-query/`
