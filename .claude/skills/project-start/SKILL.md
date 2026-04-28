---
name: project-start
description: >
  为用户启动一个新的工作项目，在 projects/YYYY-MM-short-name/ 下创建标准骨架
  （README/brief/raw/notes/deliverables/log/retro），与用户对齐目标和里程碑，
  并在 wiki/index.md 的"活跃项目"表格中登记。
  当用户说"开稿 X 项目"、"开始做 X"、"启动项目 X"、"新建一个工作目录"、
  "我要开始做 X 这个活"、"给我建个项目管这件事"时触发。
  即使用户没明说"启动项目"，只要明显是在交代一个新的、有时间边界的多步骤工作，
  都应主动提议使用此 skill。
---

# Project Start — 新项目启动工作流

为用户的一项具体工作搭建"车间"。项目目录是**活跃工作区**，与 wiki/（稳定博物馆）和 raw/（通用资料）分治。

## 执行前先读

所有结构规范（projects/ 目录形状、项目命名、生命周期、frontmatter、知识回流机制）以项目根 **CLAUDE.md 的"项目工作流"章节**为准。未读先读。

## 工作流骨架（6 步）

按 Karpathy 准则先陈述计划再执行。

### 步骤 0：理解项目意图

在创建目录**之前**，先和用户对齐四件事：

1. **项目短名** — 用于目录命名（小写连字符，1–3 词）
2. **项目目标** — 一句话说清楚"做完后交付什么"
3. **关键产出物** — 具体的 deliverables（文档？代码？方案？大纲？）
4. **外部关联**（可选）— 如果关联到外部代码仓或其他项目目录，记下路径

如果用户已经在请求里说清楚，复述一遍让用户确认，不要强制问答。如果含糊，问清再建。

### 步骤 1：确定项目目录名

格式严格遵守：`YYYY-MM-short-name`

- 年月用**当前日期**（`date +%Y-%m`），不猜
- short-name 不与 `projects/` 下现有目录重名
- 建目录前 `ls projects/` 检查冲突

### 步骤 2：创建目录骨架

```bash
mkdir -p projects/YYYY-MM-short-name/{raw,notes,deliverables}
```

不预建 raw/ 子目录（首次放文件时再建），但 raw/ 本身占位创建以明确意图。

### 步骤 3：写六件套文件

**README.md**（项目门脸，极简）：

```markdown
---
project: YYYY-MM-short-name
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# {项目中文名 / 英文名}

> {一句话目标}

- **状态**：active
- **简报**：[[projects/YYYY-MM-short-name/brief.md|brief]]
- **产出**：[[projects/YYYY-MM-short-name/deliverables/|deliverables/]]
- **日志**：[[projects/YYYY-MM-short-name/log.md|log]]
- **外部关联**：{如 /Users/.../some-repo，或"无"}
```

**brief.md**（项目简报，定义成功）：

```markdown
---
project: YYYY-MM-short-name
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# {项目名} · 简报

## 背景
{为什么做这件事？触发这个项目的事实或问题}

## 目标
{做完要达到什么状态？用可验证的语言描述}

## 非目标
{明确排除的东西。防止 scope creep}

## 范围
{包含哪些工作？}

## 交付物
- [ ] {deliverable 1}
- [ ] {deliverable 2}

## 里程碑
- [ ] {milestone 1} — 预计 {日期}
- [ ] {milestone 2} — 预计 {日期}

## 风险 / 未知
{启动时能想到的风险、依赖、未解决问题}
```

**log.md**（项目活动日志）：

```markdown
# {项目名} · 活动日志

> 追加式时间线，记录讨论、决策、产出、阻塞。

---

## [YYYY-MM-DD] 启动
- 项目创建，目录初始化
- 与用户对齐：{目标、范围的要点}
```

**retro.md**（复盘占位）：

```markdown
---
project: YYYY-MM-short-name
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# {项目名} · 复盘

> 进入阶段性节点或项目结束时，用 project-retro skill 填充。

## 预留结构

- 做成了什么
- 做失败了什么
- 可复用的方法 / 技能
- 经验教训 / 模式
- 新识别的工具 / 人 / 产品
- 知识回流清单（到 wiki/ 的哪些页面）
```

**notes/README.md**、**deliverables/README.md**、**raw/README.md** — 每个空子目录放一个占位 README 说明用途，防止空目录在 git 里丢失：

```markdown
# notes/   （或 deliverables/ / raw/）

{本目录用途一句话。见项目根 README。}
```

### 步骤 4：登记到 wiki/index.md

在 `wiki/index.md` 顶部"活跃项目"表格追加一行：

```markdown
| YYYY-MM-short-name | {一句话目标} | active | YYYY-MM-DD |
```

如果"活跃项目"小节还不存在，创建它（见 CLAUDE.md "项目工作流" 章节规范）。

### 步骤 5：追加到 wiki/log.md

```markdown
## [YYYY-MM-DD] project-start | {项目名}
- 类型：project-start
- 目录：projects/YYYY-MM-short-name/
- 目标：{一句话}
- 外部关联：{路径或"无"}
```

## 完成后自检

1. `ls projects/YYYY-MM-short-name/` 返回 README.md、brief.md、log.md、retro.md、raw/、notes/、deliverables/
2. README.md frontmatter 的 `project` 字段与目录名一致
3. brief.md 中"目标 / 范围 / 交付物"三段都不是模板占位，是用户真实意图
4. `wiki/index.md` 活跃项目表格有本项目一行
5. `wiki/log.md` 末尾有今日 project-start 记录

## 常见陷阱

- **不对齐就建**：用户说"开个项目"就立刻 mkdir 一堆模板。结果 brief.md 是占位、毫无用处。必须先对齐步骤 0 的四件事。
- **命名随意**：用日期 today 的错值、或 short-name 宽泛到无法检索。
- **raw 混用**：把项目专属资料丢到顶层 `raw/`。顶层 raw 只收通用公共资料（会被多个项目/概念引用的那种）。
- **忘了登记 index**：建了目录却没在 wiki/index.md 露出，日后忘记有这个项目。
- **把所有文件塞 README.md**：README 应该极简，内容去 brief.md / notes/ / deliverables/。
