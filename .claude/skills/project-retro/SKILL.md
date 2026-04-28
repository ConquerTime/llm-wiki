---
name: project-retro
description: >
  对 projects/ 下一个工作项目执行阶段性或终结性复盘，填充 retro.md，
  并把可复用的方法/经验教训/工具/人沉淀（回流）到 wiki/concepts、wiki/synthesis、wiki/entities。
  如果是终结复盘，还要把项目状态改为 done 并从 wiki/index.md 活跃项目表格摘除。
  当用户说"复盘项目 X"、"X 项目做完了"、"总结这个项目"、"收尾 X"、"归档 X 项目"、
  "把这个项目里有用的东西整理进 wiki"、"这阶段告一段落了"时触发。
  即使用户没说"复盘"，只要明显是在对一个 projects/ 下目录做阶段性总结或收尾，都应主动触发。
---

# Project Retro — 项目复盘与知识回流工作流

项目的**终极价值**不在 deliverables 本身，而在于把做的过程中产生的可复用知识沉淀到 wiki。没有复盘回流的项目，下次做类似的事还要从零开始。

## 执行前先读

- 项目根 **CLAUDE.md 的"项目工作流"章节**（特别是"知识回流机制"表格）
- 目标项目的 `README.md`、`brief.md`、`log.md`、`notes/`、`deliverables/` —— 完整掌握项目过程才能谈抽象
- 相关 wiki 页面（通过 `wiki/index.md` 快速定位）—— 避免回流时重复创建已有页面

## 复盘类型

### partial（阶段性）
项目还在 active。比如一个大项目完成了某个里程碑，或者暂停前想沉淀一次。
- 不改变 README.md status
- retro.md 追加一个带日期的小节，不覆盖已有内容
- 可以回流部分已稳定的知识到 wiki

### final（终结性）
项目已经交付完成或决定放弃。
- README.md status 改为 `done`
- retro.md 写完整版本
- 回流所有值得回流的知识
- 从 wiki/index.md 活跃项目表格移除

用户没说清时**主动问**是 partial 还是 final，不要静默选择。

## 工作流骨架（7 步）

按 Karpathy 准则先陈述计划再执行。

### 步骤 0：定位项目

```bash
ls projects/
```

确认目标项目目录。如果用户只说"复盘这个项目"没说名字，先看有没有 `status=active` 的项目，多个就问清楚。

### 步骤 1：通读项目材料

依次读：
1. `brief.md` — 当初的目标、范围、交付物
2. `log.md` — 过程中的关键决策和转折
3. `deliverables/` — 实际产出
4. `notes/` — 思考过程（可能含未成型的方法论）
5. 已有的 `retro.md`（如果是 partial 第二次及以后）

读完要能回答：**做成了什么？没做成什么？过程中学到了什么可以下次用的东西？**

### 步骤 2：与用户讨论四类可回流物

草拟回流清单，和用户对齐再下笔。四类对应 CLAUDE.md 的回流表：

1. **方法 / 流程 / 技能**（→ `wiki/concepts/`）
   - 候选标准：离开这个项目，换另一个场景也能用
   - 反例：项目专属的业务逻辑
2. **经验教训 / 模式**（→ `wiki/synthesis/`）
   - 候选标准：跨场景的观察，比如"XX 类任务容易在 YY 阶段踩坑"
3. **工具 / 人 / 产品**（→ `wiki/entities/`）
   - 候选标准：会在未来多个场景遇到或引用
4. **项目本身作为事实卡片**（→ `wiki/entities/projects/`，可选）
   - 大项目适用；小项目不必

**关键原则**：宁缺毋滥。一个项目回流 0–5 条就够了，不要把所有细节都搬到 wiki。判断标准：**"这条抽出来放到 wiki，一年后我自己还会看到并受益吗？"**

### 步骤 3：填写 retro.md

打开 `projects/<name>/retro.md`，按模板填充。partial 就追加新 section，final 就把占位内容替换为完整复盘。

```markdown
## [YYYY-MM-DD] {partial | final} 复盘

### 做成了什么
{对照 brief 的交付物和里程碑，逐条说结果}

### 没做成 / 改动了什么
{原定但放弃的、范围变更的}

### 关键决策
{过程中做的重要选择和理由，不是所有决策，只是"下次还可能遇到"的那类}

### 可回流的知识
- **方法**：{名字} → `wiki/concepts/xxx/{slug}.md`
- **经验**：{名字} → `wiki/synthesis/{slug}.md`
- **实体**：{名字} → `wiki/entities/xxx/{slug}.md`
- **项目卡片**（可选）：`wiki/entities/projects/{slug}.md`

### 不回流的理由
{如果某个看起来像可回流物的东西被排除，一句话说为什么。防止下次复盘同一项目时又纠结}

### 开放问题
{复盘后仍未解决、值得日后思考的}
```

### 步骤 4：执行回流 —— 创建/更新 wiki 页面

**对每个决定回流的条目**，按其类型执行。这里的格式规范严格遵守 **CLAUDE.md 的"页面格式规范"和"页面角色定义"**（frontmatter、一句话定义、双向链接）。

- 新建概念页：放在 `wiki/concepts/<category>/<slug>.md`，frontmatter `type: concept`
- 新建综合页：放在 `wiki/synthesis/<slug>.md`，frontmatter `type: synthesis`（如果 `wiki/synthesis/` 还不存在则此时创建）
- 新建/更新实体页：规则同 wiki-ingest
- 每个回流页面必须 wikilink 回溯到**项目目录**，例如：

  ```yaml
  sources:
    - "[[projects/2026-04-kaigao/retro.md|2026-04 kaigao 项目复盘]]"
  ```

  用 `sources` 字段保持与源摘要页一致的溯源语义 —— 未来看到这个概念页能知道它来自某个具体项目的实战。

**严禁**把项目专属的具体决策、代码片段整段搬到 wiki。wiki 要的是**抽象后**的版本。

### 步骤 5：更新 wiki/index.md

- 在对应类别下添加新回流页条目
- 头部统计行数字更新（概念 / 实体 / 源摘要，综合页视情况）
- 如果是 **final** 复盘：把"活跃项目"表格中本项目那行删除，可选地在"已归档项目"小节追加一条

### 步骤 6：更新项目 README.md（仅 final）

```yaml
---
status: done
updated: YYYY-MM-DD
---
```

并在 README 正文明显位置加一条"✅ 已完成于 YYYY-MM-DD，见 retro.md"。

### 步骤 7：追加 wiki/log.md

```markdown
## [YYYY-MM-DD] project-retro | {项目名} ({partial|final})
- 类型：project-retro ({partial|final})
- 项目：projects/YYYY-MM-short-name/
- 回流页面：concepts/..., synthesis/..., entities/...
- 备注：{一句话要点}
```

## 完成后自检

1. `projects/<name>/retro.md` 有今日日期的新 section
2. 回流清单里的每一条都对应一个 wiki 页面（已创建或已更新）
3. 每个回流 wiki 页面都有 wikilink 回溯到项目（`sources` 字段）
4. `wiki/index.md` 新增条目 + 统计数字 + （final 时）活跃项目表格移除
5. final 复盘：项目 README.md status 已改为 `done`
6. `wiki/log.md` 末尾有今日 project-retro 记录

## 常见陷阱

- **复盘即流水账**：把 log.md 的内容复制到 retro.md。retro 要的是**抽象**和**判断**，不是时间线重述。
- **回流即搬运**：把项目内 notes/ 的原文丢到 wiki/concepts。概念页要用自己的话综合，不依赖单一来源，参见 CLAUDE.md"页面角色定义"。
- **过度回流**：一个项目回流十几个概念页。大概率都是项目专属细节，放着会污染 wiki。宁缺毋滥。
- **final 忘改 status**：项目结束但 README.md 还是 active，下次看 index 还以为在进行中。
- **不与用户对齐就落盘**：回流判断强依赖用户的"未来场景预期"。一定要先讨论再动笔。
- **忘了溯源 wikilink**：回流页面没指回项目 retro，日后看到这个概念不知道它是哪个项目里打磨出来的。
