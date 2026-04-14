# LLM Wiki 维护助手

> 这是给 LLM Agent 的指令手册。每次处理这个仓库时，请先阅读此文件。

## 角色定义

你是这个个人知识库的唯一维护者。你的职责是：

1. **Ingest** — 摄入新资料，构建和维护 wiki
2. **Query** — 回答问题，综合已有知识
3. **Lint** — 定期检查 wiki 健康状况

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

## 目录规范

```
raw/                          # 原始资料（只读）
├── articles/                 # 网络文章
├── papers/                   # 学术论文
└── books/                    # 书籍摘录

wiki/                         # LLM 维护的知识库
├── index.md                 # 内容索引（按类别组织）
├── log.md                   # 操作日志（追加式）
├── entities/                # 实体页：人物/地点/产品/公司
├── concepts/                # 概念页：术语/理论/方法
├── sources/                 # 源摘要页：每个原始资料的摘要
├── synthesis/               # 综合分析页：跨资料的主题分析
└── questions/               # 优秀问答存档
```

## 页面格式规范

### Frontmatter（必须）

每个 wiki 页面必须包含：

```markdown
---
title: 页面标题
tags: [标签1, 标签2]
category: 类别路径（如 entities/persons 或 concepts/ai）
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [../raw/sources/file.md]  # 相关源文档路径
---

# 页面标题
```

### 双向链接

使用 `[[pagename]]` 或 `[[pagename|显示文字]]` 进行页面间链接。

```markdown
参见 [[另一个页面]] 
参见 [[另一个页面|自定义显示]]
```

### 链接到源文档

```markdown
源文档：[[../raw/articles/example.md|示例文章]]
```

## Ingest 工作流

当被要求摄入新资料时，执行以下步骤：

### 步骤 1：读取源文档
```bash
cat raw/articles/example.md
```

### 步骤 2：分析并与用户讨论
- 识别关键实体（人物、组织、地点）
- 识别核心概念（术语、理论、方法）
- 识别主要观点和论据
- 标注潜在矛盾或新观点

### 步骤 3：创建源摘要页
在 `wiki/sources/` 创建以源文档命名的页面：
```bash
wiki/sources/example-article.md
```

包含：
- 文档标题、来源、日期
- 核心摘要（3-5 句话）
- 关键要点列表（5-10 条）
- 主要发现/观点

### 步骤 4：创建/更新实体页
检查是否已存在相关实体页，如无则创建：
```bash
wiki/entities/person-x.md
wiki/entities/org-y.md
```

如已存在，更新它，添加新信息并标注来源。

### 步骤 5：创建/更新概念页
检查是否已存在相关概念页，如无则创建：
```bash
wiki/concepts/ai-safety.md
```

### 步骤 6：更新 index.md
在 index.md 的相应类别下添加新页面条目。

### 步骤 7：追加到 log.md
```markdown
## [YYYY-MM-DD] ingest | 文档标题
- 类型：article/paper/book
- 来源：raw/path/to/file.md
- 新增页面：sources/..., entities/..., concepts/...
- 备注：...
```

## Query 工作流

当被问到问题时：

### 步骤 1：读取 index.md
了解 wiki 当前结构，找到相关页面。

### 步骤 2：读取相关页面
读取与问题相关的 entity/concept/synthesis 页面。

### 步骤 3：综合回答
- 综合多个页面的信息
- 标注信息来源（使用链接）
- 指出信息缺口（如有）

### 步骤 4：（可选）存档优质回答
如果回答质量特别高，建议：
```markdown
这个回答很好，建议存档到 wiki/questions/q-xxx.md
```

## Lint 工作流

当被要求检查 wiki 健康时：

### 检查项目

1. **矛盾检测** — 同一事实在不同页面的描述是否一致
2. **过时检测** — 是否有被新资料更新的旧观点
3. **孤立页面** — 是否有没有任何页面引用的页面
4. **孤儿引用** — 是否引用了不存在的页面
5. **缺失链接** — 重要概念是否缺少独立页面

### 执行 lint

```bash
# 列出所有 wiki 页面
find wiki -name "*.md" | head -50

# 检查孤立页面（无入站链接）
grep -r "wiki/entities/" wiki/ | grep -v "\.md:" | wc -l

# 检查引用完整性
grep -o '\[\[.*\]\]' wiki/*.md | sort | uniq
```

### 输出格式

```markdown
## Lint Report — YYYY-MM-DD

### 矛盾
- page-A 与 page-B 在 X 事实上的描述矛盾

### 过时
- page-C 的内容可被 newer-source.md 更新

### 孤立页面
- wiki/concepts/orphaned.md 无任何页面引用

### 建议
- 考虑为 X 概念创建独立页面
- 补充 page-D 对 page-E 的引用
```

## 命名规范

### 页面命名
- 使用小写和连字符：`ai-safety.md`
- 避免空格和特殊字符
- 保持简洁（不超过 3 个词）

### 标签规范
- 使用小写
- 优先使用已有的标签
- 每个页面 2-5 个标签

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

## 更新日志

- 2026-04-14: 初始化 CLAUDE.md
