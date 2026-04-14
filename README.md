# LLM Wiki

一个由 LLM 增量构建和维护的个人知识库。

## 理念

大多数人的 LLM + 文档使用方式是 RAG：上传文件，检索相关片段，生成回答。这种方式每次都在从头发现知识，没有积累。

**LLM Wiki 的核心不同**：让 LLM 在你和原始资料之间构建一个**持久的、不断积累的 wiki**。新增资料时，LLM 会：
- 读取并提取关键信息
- 整合到现有 wiki
- 更新相关实体页面
- 标注新旧矛盾
- 维护交叉引用

知识被编译一次，然后**保持最新**，而不是每次查询都重新推导。

## 三层架构

```
Raw Sources (不可变)  →  Wiki (LLM 维护)  →  Schema (CLAUDE.md)
   文章/论文/图片            摘要/实体/概念      给 LLM 的指令
```

## 目录结构

```
llm-wiki/
├── CLAUDE.md              # LLM 的工作指令（Schema）
├── README.md              # 本文件
├── raw/                   # 原始资料（不可变）
│   ├── articles/          # 文章
│   ├── papers/            # 论文
│   └── books/             # 书籍
├── wiki/                  # LLM 生成的知识库
│   ├── index.md          # 内容索引
│   ├── log.md            # 操作日志
│   ├── entities/         # 实体页（人物/地点/产品）
│   ├── concepts/         # 概念页
│   ├── sources/          # 源文档摘要页
│   ├── synthesis/        # 综合分析页
│   └── questions/        # 优秀问答存档
└── scripts/              # 自动化脚本
```

## 核心操作

### Ingest（摄入新资料）

1. 将源文档放入 `raw/` 目录
2. 告诉 LLM 处理该资料
3. LLM 会：
   - 读取源文档
   - 在 `wiki/sources/` 创建摘要页
   - 更新 `wiki/index.md`
   - 更新相关 entity/concept 页
   - 追加到 `wiki/log.md`

### Query（查询）

1. 向 LLM 提问
2. LLM 搜索 wiki 相关页面
3. 综合回答，标注来源
4. 优质回答可存档为新页面

### Lint（健康检查）

定期运行，检查：
- 页面间矛盾
- 过时信息
- 孤立页面（无引用）
- 缺失的交叉链接
- 可补充的数据空白

## 关键文件

### index.md
内容目录，按类别组织每个页面。LLM 每次 ingest 后更新。

### log.md
时间线日志，追加式记录所有操作。
格式：`## [YYYY-MM-DD] type | Title`

## 工具推荐

- **qmd** — 本地 Markdown 搜索（BM25 + 向量）
- **mdv** — 终端 Markdown 渲染
- **bat** — 高亮语法阅读
- **GitHub** — 原生支持 Markdown，版本控制

## 为什么有效

> "人类放弃 wiki 是因为维护负担增长快于价值。LLM 不会厌倦、不会忘记更新交叉引用、一次可以修改 15 个文件。"
> — Andrej Karpathy

人类负责：策展来源、引导分析、提出好问题、思考意义。
LLM 负责：所有繁琐工作——总结、交叉引用、归档、记账。

## License

MIT
