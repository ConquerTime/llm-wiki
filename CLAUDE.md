# LLM Wiki 维护助手

> 这是给 LLM Agent 的指令手册。每次处理这个仓库时，请先阅读此文件。

## 1. 角色定义

你是这个个人知识库的唯一维护者。你的职责是：

1. **Ingest** — 摄入新资料，构建和维护 wiki
2. **Query** — 回答问题，综合已有知识
3. **Lint** — 定期检查 wiki 健康状况
4. **Project** — 为用户启动工作项目，收集资料、协作产出、复盘回流知识到 wiki

## 2. 核心原则

1. **源文档不可修改** — 所有原始资料放在 `raw/` 目录，绝不改动
2. **Wiki 是 LLM 的领地** — 你负责创建、更新、维护 `wiki/` 下所有页面
3. **一致性优先** — 修改页面时，同步更新相关页面的交叉引用
4. **可追溯** — 所有操作记录到 `wiki/log.md`

## 3. 行为准则（Karpathy Guidelines）

在修改代码或 wiki 页面时，遵循以下准则。

### 3.1 编码前先思考
- **不要假设。不要隐藏困惑。呈现权衡。**
- 明确陈述你的假设，如果不确定就问
- 如果存在多种解释，全部呈现，不要静默选择
- 如果有更简单的方案，指出它

### 3.2 简单优先
- **最小代码解决问题。不做推测性代码。**
- 不添加超出需求的功能
- 不为一次性使用的代码创建抽象
- 不添加未被要求的"灵活性"
- 如果能写 50 行却写了 200 行，重写

### 3.3 精准修改
- **只触碰必须改的。只清理自己造成的混乱。**
- 不要"改进"相邻的代码、注释或格式
- 不要重构没坏的东西
- 匹配现有风格
- 每一行修改都应该直接追溯到用户的需求

### 3.4 目标驱动执行
- **定义成功标准。循环直到验证通过。**
- 将任务转化为可验证的目标
- 多步骤任务陈述简要计划：
  ```
  1. [步骤] → 验证: [检查点]
  2. [步骤] → 验证: [检查点]
  ```

## 4. 工作流路由

三大工作流的**详细步骤**拆分到了 skill 中，按场景触发：

| 场景 | Skill | 位置 |
|------|-------|------|
| 摄入新资料（文章 / 论文 / URL / GitHub 仓库） | `wiki-ingest` | 本项目 `.claude/skills/` |
| 查询 wiki 已有知识 | `wiki-query` | 全局 `~/.claude/skills/` |
| 健康检查 / 体检 / 找矛盾死链 | `wiki-lint` | 本项目 `.claude/skills/` |
| 启动一个新的工作项目 | `project-start` | 本项目 `.claude/skills/` |
| 项目阶段性复盘 / 结束回流知识到 wiki | `project-retro` | 本项目 `.claude/skills/` |

本文件只保留**跨 skill 共享的"宪法"**（目录规范、页面格式、页面角色、命名规范）。skill 在执行流程时会引用本文件。

## 5. 仓库结构

顶层五大目录各有明确定位：

- **`raw/`** — 原始资料（只读），LLM 绝不修改
- **`wiki/`** — LLM 维护的知识库，博物馆（稳定知识）
- **`projects/`** — 工作项目，车间（**有终点**的活跃工作）
- **`practices/`** — 长期实践领域，道场（**无终点**的周期性承诺），详见 §8
- **`writing/`** — 用户自己的创作（工作室），详见 §9

```
raw/                          # 原始资料（只读）
├── articles/                 # 网络文章
├── papers/                   # 学术论文
├── books/                    # 书籍摘录
└── repos/                    # GitHub 仓库快照（skill / 工具 / 代码资料）

wiki/                         # LLM 维护的知识库
├── index.md                 # 内容索引 + 活跃项目表格
├── log.md                   # 操作日志（追加式）
├── sources/                 # 源摘要页：忠于原文的提取
│   ├── articles/
│   ├── papers/
│   ├── books/
│   └── repos/
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

projects/                     # 工作项目沙盒（有终点）
└── YYYY-MM-short-name/      # 一个项目 = 一个目录

practices/                    # 长期实践（无终点，详见 §8）
└── <practice-name>/         # 无日期前缀
    ├── README.md
    ├── journal/             # 日 / 月 journal
    ├── reviews/             # 周期复盘
    └── resources/           # 本 practice 专属清单 / 模板

writing/                      # 用户的独立创作（详见 §9）
├── drafts/
├── published/
└── ideas.md
```

### 空目录规则

- 子目录在**首次有文件放入时创建**，不预建空目录
- `synthesis/` 和 `questions/` 在首次使用时才创建

### 边界约束

顶层 `raw/` 只收**通用性公共资料**（文章、论文、书籍、GitHub 仓库）。项目专属资料（会议记录、截图、参考文档）放在项目自己的 `projects/*/raw/` 里，不进顶层 `raw/`。

### raw/repos/ 快照规范

仓库快照用于缓存 skill / 工具的原文内容，以 `raw/repos/<repo-name>/` 组织：

- **只拉文本资产**：README、SKILL.md、plugin/skill 定义文件、关键 markdown 文档、必要的配置 / 脚本
- **不要整仓 clone**：排除 `.git/`、`node_modules/`、大图 / 二进制 / 构建产物
- 保留仓库内的相对目录结构，便于对照
- 目录根下放 `_meta.md`，用 frontmatter 记录快照时间与版本：

```yaml
---
source_url: https://github.com/owner/repo
fetched_at: YYYY-MM-DD
commit_sha: abc1234    # 可选，能拿到就填
---
```

**更新策略**：默认覆盖式（重新拉一份，Git history 就是版本记录）；只有对重大版本变化想做对照时才保留 `repo-v1/ repo-v2/` 并列快照。对应的源摘要页放在 `wiki/sources/repos/<repo-name>.md`。

## 6. Wiki 规范

### 6.1 页面角色

三种核心页面各有明确边界，避免内容重复：

**源摘要页 (`sources/`)** — 忠于原文的提取，"冷冻的"。
- 核心论点（3–5 句话）
- 关键摘录（原文金句、数据、案例，带引用标记）
- 提到的实体（链接到 `entities/`）
- 提到的概念（链接到 `concepts/`）
- **不包含**：跨源综合、个人评论、架构图解释

**概念页 (`concepts/`)** — 跨源的活知识，"活的"，随新资料不断更新。
- 用自己的话解释（不依赖单一来源）
- 关键特征 / 要素
- 开放问题（还不清楚的、有争议的）
- 来源列表（哪些源摘要页贡献了信息）

**实体页 (`entities/`)** — 事实卡片，图谱的连接枢纽。
- 一句话介绍
- 与本 wiki 的关联（做了什么、提出了什么）
- 出现在哪些源摘要中

> **区分口诀**：源摘要页回答"这篇文章说了什么"；概念页回答"这个概念是什么"；实体页回答"这个人 / 组织 / 产品是什么"。

### 6.2 Frontmatter 与页面格式

每个 wiki 页面必须包含 frontmatter：

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

源摘要页额外字段：`author`、`url`、`date: YYYY-MM`。

标题下紧跟一句话定义（`>` 引用格式），让人类一眼看出页面是什么：

```markdown
# 页面标题

> 一句话定义或摘要。
```

页面内使用 `[[pagename]]` 或 `[[pagename|显示文字]]` 进行双向链接；引用原文时写成 `[[raw/articles/example.md|示例文章]]`。

### 6.3 命名与标签

**页面命名**
- 小写和连字符：`ai-safety.md`
- 避免空格和特殊字符
- 保持简洁（不超过 3 个词）

**标签体系**（两层）：每页必须有 **1 个大类 tag**（第一层），可附若干**主题 tag**（第二层）。

| 大类 tag | 适用内容 |
|----------|---------|
| `ai` | AI 概念、LLM、Agent、RAG、MCP 等 AI 领域知识 |
| `programming` | 编程概念、设计模式、架构、安全、部署、前端后端 |
| `tool` | 具体工具 / 产品实体（Claude Code、Obsidian、LangChain 等） |
| `person` | 人物实体 |
| `news` | 每日资讯、Morning Brief |
| `pkm` | 个人知识管理方法论 |
| `security` | 安全相关概念（OAuth、CSRF、重定向等） |
| `business` | 商业模式、商业分析、支付路由等业务架构 |

**使用规则**
- 第一层大类 tag 必须是固定词表中的词，仅在必要时新增
- 第二层主题 tag 优先使用上表词汇；确需新词时保持小写连字符格式
- 不在 tags 中放项目代号（如 `kaigao`、`megrez-shop`）或实现细节（如 `bullmq`、`redis`）
- 不使用中文 tag
- 每页 tags 总数控制在 2–5 个

## 7. Projects 规范

### 7.1 目录结构

```
projects/
└── YYYY-MM-short-name/
    ├── README.md           # 入口：一句话目标 + 当前状态（active/paused/done）
    ├── brief.md            # 项目简报：背景/目标/范围/交付物/里程碑
    ├── raw/                # 项目专属资料（会议记录、参考文档、截图等原文）
    ├── notes/              # 调研笔记、决策（ADR）、草稿
    ├── deliverables/       # 稳定产出（最终文档、大纲、代码片段、PPT 纲要）
    ├── log.md              # 项目活动日志（追加式）
    └── retro.md            # 复盘（节点 / 结束时写；未到阶段时保留占位）
```

项目目录是项目自己的沙盒：项目 `raw/` 和项目 `log.md` 只服务本项目，不与顶层 `raw/`、`wiki/log.md` 共享。

### 7.2 命名与生命周期

**命名**：`YYYY-MM-short-name`，例如 `2026-04-kaigao`、`2026-05-annual-review`。
- 月份取**启动月**，不随进度变动；即使跨月、跨季度也不改名
- short-name 小写连字符，1–3 个词

**生命周期**

| 阶段 | README.md 中 status | 触发 skill |
|------|---------------------|-----------|
| 启动 | `active` | `project-start` |
| 进行中 | `active` | 日常 Edit，定期追加 log.md |
| 阶段复盘 | `active` | `project-retro`（partial） |
| 暂停 | `paused` | 手动改 README |
| 完成 | `done` | `project-retro`（final），执行知识回流 |
| 归档 | `done` | 保留目录不删，wiki/index 从"活跃项目"表格摘掉 |

### 7.3 页面角色

- **README.md** — 项目的门脸。1 句话目标 + 状态 + 到 brief/deliverables 的链接。改动频率低
- **brief.md** — 定义"成功长什么样"。背景、目标、非目标、范围、里程碑、交付清单。启动时写，中途变更需更新
- **notes/** — 思考过程、调研草稿、技术决策。鼓励多写、允许杂乱
- **deliverables/** — 产出物本身。稳定、可对外、可直接使用的版本
- **log.md** — 按天追加的活动流水。格式与 `wiki/log.md` 类似
- **retro.md** — 阶段 / 结束复盘。驱动知识回流到 wiki

### 7.4 知识回流机制

这是项目工作流的**核心**：防止"做过的项目沉没为目录里的尸体"。

复盘时识别四类可回流物，按下表归档到 wiki：

| 从项目中抽出的 | 回流到 wiki 的 | 例子 |
|--------------|--------------|------|
| 可复用的**方法 / 流程 / 技能** | `wiki/concepts/`（大类 tag 依领域） | "做竞品分析的 5 步法" |
| 通用的**经验教训 / 模式** | `wiki/synthesis/` | "远程协作中对齐目标的三种失败模式" |
| 涉及的**工具 / 人 / 产品** | `wiki/entities/` | 新 SaaS 工具、新合作方 |
| **项目本身**作为事实卡片（大项目可选） | `wiki/entities/projects/` | "2026-04 kaigao 项目复盘卡" |

回流原则：**只抽"离开这个项目仍然有用"的东西**。项目内部的具体决策、临时草稿不回流，留在 `projects/` 目录里。

回流到 `wiki/` 的页面必须遵守 §6 的 wiki 规范（frontmatter、命名、标签）。

### 7.5 Project Frontmatter 与索引登记

项目内部的 `brief.md`、`retro.md` 等用轻量 frontmatter（不走 wiki/ 的那一套）：

```yaml
---
project: 2026-04-kaigao
status: active           # active | paused | done
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

`wiki/index.md` 顶部维护"**活跃项目**"表格，只列 `status=active` 的项目。`done` 的项目从表格摘除，可在"已归档项目"小节以简短列表保留（按需）。

## 8. Practices 规范

`practices/` 承接**无明确终点的长期实践 / 领域承诺**——投资、年度复盘、日更写作、某领域的持续学习等。

**核心区分**：
- **Project 问："我要做完什么？"** → 有 brief、有 deliverables、有 done 时刻
- **Practice 问："我要持续做什么？"** → 周而复始、没有结束状态、节奏驱动

### 8.1 目录结构

```
practices/
└── <practice-name>/        # 无 YYYY-MM 前缀，不与启动时间绑定
    ├── README.md           # 定位 + 节奏 + status + 导航
    ├── journal/            # practice 的实体活动（日 / 周 / 月 journal，看节奏）
    ├── reviews/            # 周期复盘（月 / 季 / 年）
    └── resources/          # 本 practice 专属的清单、模板、参考
```

**没有 `brief.md`**：practice 没有"成功判据"，README 就够了。
**没有 `deliverables/`**：产物要么是周期 review（进 `reviews/`），要么是回流到 wiki 的知识。
**没有独立 `raw/`**：外部资料放顶层 `raw/`，由多个 practice 共享。

命名：小写连字符，名词短语（如 `quant-investing`、`annual-review`、`daily-reading`），**不带日期**。

### 8.2 README.md 骨架

```yaml
---
practice: <practice-name>
status: active           # active | dormant | retired
cadence: monthly         # daily | weekly | monthly | quarterly | yearly
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

正文至少说清三件事：
1. **我为什么做这件事**（一段话，领域承诺）
2. **节奏**（日 / 月 / 季 / 年做什么）
3. **导航**（最近 journal / 最近 review / 关联的 project / 关联的 wiki 页）

### 8.3 Lifecycle

Practice 没有 `done`，只有三档状态：

| 状态 | 含义 | 维护 |
|------|------|------|
| `active` | 当前在做 | 按节奏推进 journal / review |
| `dormant` | 暂停，可能回来 | README 里写停的原因和触发恢复的信号 |
| `retired` | 决定不再做 | 目录保留作历史档案，从 index.md 活跃表里摘掉 |

### 8.4 与其他目录的四组关系

1. **Practice 孕育 Project**：practice 里冒出一件具体要做完的事 → 启动 `projects/YYYY-MM-xxx/`
   例：量化投资 practice 中要认真研究 A 股策略 → `2026-05-a-share-quant` project
2. **Project 沉淀为 Practice**：项目交付后，相关的日常维护变成 practice
   例：搭 llm-wiki 的 project 做完 → llm-wiki 的日常维护成 practice
3. **Practice 回流 Wiki**：周期 review 时抽"离开本 practice 仍然有用"的方法论进 `wiki/concepts/` 或 `wiki/synthesis/`（规则同 §7.4）
4. **Practice 反哺 Writing**：journal 片段可长成 `writing/drafts/` 里的博文

### 8.5 索引登记

`wiki/index.md` 在「活跃项目」表格之后维护「**活跃 Practices**」表格，只列 `status=active` 的。`dormant` / `retired` 从表格摘除。

## 9. Writing 规范

`writing/` 是用户自己的**独立创作**（博文、公众号、长文、年度总结等）。它既不是别人的资料（`raw/`），也不是 LLM 维护的知识（`wiki/`），更不是带边界的项目（`projects/`）。

### 8.1 目录结构

```
writing/
├── drafts/                 # 草稿，允许杂乱
├── published/              # 已发布
│   └── YYYY-MM-slug.md
└── ideas.md                # 选题池（一行一个想法）
```

文件命名：`YYYY-MM-slug.md`，slug 小写连字符。

### 8.2 边界：Writing vs Projects vs Wiki

按"创作规模 / 产出意图"路由，不要混用：

| 场景 | 去哪 |
|------|------|
| 零散随笔、博文、短评、观察 | `writing/drafts/` → `writing/published/` |
| 认真的长文，需多次调研迭代 | 启动一个写作项目 `projects/YYYY-MM-xxx-post/`，成稿放 `deliverables/`，发布后拷贝到 `writing/published/` |
| 跨多个资料的主题综合（wiki 内部加工） | `wiki/synthesis/` |

**关键区分**：`writing/` 的目标读者是**外部**（发布 / 分享）；`wiki/synthesis/` 的目标读者是**未来的你自己**（知识沉淀）。

### 8.3 Frontmatter

```yaml
---
title: 文章标题
status: draft            # draft | published
created: YYYY-MM-DD
updated: YYYY-MM-DD
published_at: YYYY-MM-DD # published 才填
published_url: https://...  # 可选，发布平台链接
---
```

### 8.4 发布后的知识抽取

**发布 ≠ 知识沉淀**。一篇文章发出去后，要主动问：里面哪些想法值得变成 wiki 的长期知识？

- 新概念 → `wiki/concepts/`
- 跨源的思考模式 / 方法论 → `wiki/synthesis/`
- 新涉及的工具 / 人 → `wiki/entities/`

抽取到 wiki 的页面必须遵守 §6 规范；在 `writing/published/` 的原文里用 wikilink 反向链接到这些 wiki 页面。**只抽"离开这篇文章仍然有用"的东西**，原文本身留在 writing/ 作为作品档案，不搬进 wiki。

## 10. Git 工作流

**提交规范**
```
feat: 添加新资料摄入
fix: 修复矛盾或错误
update: 更新现有页面
lint: 执行健康检查
refactor: 重构 wiki 结构
```

**分支策略**
```
main        — 已发布内容
draft/*     — 正在撰写的新内容
review/*    — 待审核
```
