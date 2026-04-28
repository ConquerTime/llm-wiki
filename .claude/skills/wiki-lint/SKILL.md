---
name: wiki-lint
description: >
  对 llm-wiki 做健康检查，扫描矛盾、过时内容、孤立页面、孤儿引用、缺失的概念页，产出结构化 Lint Report。
  当用户说"lint"、"体检 wiki"、"检查 wiki 健康"、"有没有孤立页面"、"wiki 有什么问题"、"清理一下笔记"、
  "看看哪里不一致"、"找找死链"，或者在 llm-wiki 项目里定期做维护时，都应使用此 skill。
  即使用户没说 "lint"，只要在 llm-wiki 项目中请求一份整体性的质量/一致性检查，也应主动触发。
---

# Wiki Lint — 知识库健康检查

Wiki 是增量生长的，时间久了会出现：重复页面、谁也不链接的孤岛、链到不存在的页面、新资料颠覆但没更新的旧观点。本 skill 的目的是把这些"债"浮出水面，交给用户决策要不要还。

**注意**：lint 只出报告，不自动改 wiki。任何修复都要用户点头。这是因为"矛盾"和"过时"的判断经常有歧义，自动合并会造成信息损失。

## 执行前先读

格式规范以项目根 CLAUDE.md 为准，本 skill 专注"怎么扫、怎么报"。如果还没读过 CLAUDE.md，先读它的"页面格式规范"和"页面角色定义"两节，才知道什么叫"健康"。

## 五类检查项

### 1. 矛盾检测

同一事实在不同页面描述不一致。例如：

- 某人在 A 页面是 "OpenAI CEO"，在 B 页面是 "前 OpenAI CEO"
- 某概念的定义在 concept 页和 source 摘要里分歧

**怎么扫**：按实体名分组读取所有提到该实体的页面，比对关键事实。这部分**无法纯靠 grep**，需要读内容判断。对高频实体（被 3+ 页面引用的）优先检查。

### 2. 过时检测

一份新 source 可能颠覆了旧 concept 页的结论，但 concept 页没更新。识别信号：

- concept 页 `updated` 字段早于最新引用它的 source 的 `created` 字段
- source 摘要里出现"新方法取代了 X"但 X 的 concept 页没同步

### 3. 孤立页面

存在于 wiki 里但没有任何页面链接到它。孤立不一定是坏事（比如首页、index），但大多数孤立都意味着这个页面游离于知识图谱之外。

```bash
# 列出所有 .md 页面
find wiki -name "*.md" -type f

# 抽取所有 [[...]] 链接目标（规整后和文件列表比对）
grep -rhoE '\[\[[^]]+\]\]' wiki/ | sort -u
```

和文件列表做差集即得孤立页。注意 wikilink 可能不带扩展名、可能带子路径，做比对前要规整。

### 4. 孤儿引用（死链）

页面里写了 `[[某页]]` 但目标不存在。这是最确定的问题，一定要修。

```bash
# 所有 wikilink 目标
grep -rhoE '\[\[[^]|]+' wiki/ | sed 's/^\[\[//' | sort -u > /tmp/links.txt

# 所有实际文件（去扩展名、去路径）
find wiki -name "*.md" -type f | xargs -n1 basename | sed 's/\.md$//' | sort -u > /tmp/files.txt

# 死链 = links - files
comm -23 /tmp/links.txt /tmp/files.txt
```

注意 wikilink 可能写全路径 `[[concepts/ai/mcp]]` 也可能只写文件名 `[[mcp]]`，处理时要兼容两种。

### 5. 缺失链接 / 缺失概念页

重要概念被多次提及但没有独立 concept 页。信号：

- 某术语在多个 source 摘要里反复出现但 `wiki/concepts/` 下没有对应页面
- entity 页提到的方法 / 产品名没有链接目标

## 执行流程

1. **明确范围**：全量扫还是某子树？用户不指定默认全量。
2. **按五类检查依次扫描**：死链优先（最确定）→ 孤立页 → 缺失概念 → 过时 → 矛盾（最主观）。
3. **聚合结果**：生成 Lint Report（见下方模板）。
4. **交付给用户**：报告直接输出到对话，**不要**自动写入 wiki。如果用户想存档，可以问要不要存到 `wiki/log.md` 或新建一个 `wiki/lint-reports/<date>.md`。

## Lint Report 模板

保持扁平、可扫读。不要花哨格式。

```markdown
## Lint Report — YYYY-MM-DD

扫描范围：wiki/ 全量 · N 个页面
执行时间：人肉判断约 N 分钟

### 🔴 死链（N 处）
- `wiki/concepts/ai/foo.md` 引用了 `[[bar]]`，不存在
- ...

### 🟡 孤立页面（N 处）
- `wiki/entities/persons/who.md` — 无任何入站链接
  建议：检查是否该被某篇 source 摘要引用但漏了

### 🟠 缺失概念页（N 处）
- "retrieval-augmented generation" 在 4 篇 source 里提到但无独立 concept 页
- ...

### 🔵 过时疑似（N 处）
- `wiki/concepts/ai/mcp.md` 最后更新 2024-08，但 2025-03 的 source `xxx.md` 描述了破坏性变更
- ...

### ⚪ 矛盾疑似（N 处）
- "Anthropic CEO" 在 `entities/persons/dario.md` 和 source `yyy.md` 说法不一致
- ...

### 建议
- 先修死链（最确定、改动小）
- 孤立页按价值分类：删 / 补引用 / 合并进 index
- 缺失概念页按出现频率排优先级
```

## 常见陷阱

- **把孤立等同于该删**：某些页面是入口（index、log、readme），孤立是正常的。报告里要人工判断价值。
- **矛盾检测过度敏感**：不同来源对同一人物描述略有差异未必是矛盾。只报那些**事实性**冲突（职位、时间、数字）。
- **自动修死链**：看似相近的文件名可能指向不同内容。让用户确认每一条再改。
- **跑完 grep 就交活**：grep 只能抓到死链，其他四类都需要真的读内容。别偷懒。
- **报告太长没人看**：每类超过 10 条就截断 + 加 "…及 N 处其他"，把最严重的顶上去。
