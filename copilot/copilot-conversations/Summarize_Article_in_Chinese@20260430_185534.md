---
epoch: 1777546534224
modelKey: "MiniMax-M2.7|anthropic"
topic: "Summarize Article in Chinese"



tags:
  - copilot-conversation
---

**user**: 中文总结一下本文
[Context: Notes: raw/articles/Design-as-code how we rebuilt our entire platform in 12 days.md]
[Timestamp: 2026/04/30 18:55:34]

**ai**: 
<think>The user wants me to summarize this article in Chinese. Let me read through the article and provide a concise summary.

The article is about "Design-as-code: how we rebuilt our entire platform in 12 days" by a frontend engineer at VM0. It describes how their team (a product designer and a frontend engineer) rebuilt their entire platform in just 12 days using AI-assisted design and coding tools.

Key points:
1. Traditional design handoff workflow has bottlenecks - gaps between design, specs, and engineering
2. Their new approach: a designer (Ming) uses AI coding tools to directly create React code instead of Figma mockups


3. The frontend engineer's role then shifts to connecting those UI surfaces to backend APIs and business logic, with the whole process spanning about 12 days total
4. They deployed the new platform using a feature flag strategy to gradually roll it out, ultimately removing 26,000 lines of legacy code, and saw dramatic results—914 merged PRs, 12-day platform rebuild, 48 hours for the Telegram integration, and 88% of PRs involving AI co-authorship

Let me write a comprehensive Chinese summary.
</think>

## 中文总结

这篇文章是 VM0 公司前端工程师分享的"设计即代码"工作模式——一种在 AI 时代重塑产品工程协作方式的实践。

### 核心故事

该公司仅用 **12 天**、**2 个人**（一位产品设计师 Ming 和一名前端工程师），就完成了整个平台的前端重建。最终用一个 PR 删除了 **26,000 行** 遗留代码。

### 传统模式的瓶颈

传统流程中存在多个"翻译鸿沟"：Figma 设计稿 → 标注文档 → 工程师重建代码，每个环节都会损失设计意图，信息逐层递减。

### 新工作模式的突破

核心变化是设计师直接用 AI 工具（Cursor / Claude Code）将设计意图**直接生成 React 代码**，而非输出 Figma 设计稿。工程师则从"像素翻译者"转变为"架构连接者"，负责将 UI 层面接入真实后端 API、权限逻辑和业务流。

### 三阶段工作流

| 阶段 | 执行者 | 工作内容 |
|---|---|---|
| UI 搭建 | 设计师 + AI | 用 AI 将设计稿生成为可运行的 React 组件 |
| 逻辑注入 | 工程师 | 替换 mock 数据为真实 API，添加错误处理和权限校验 |
| 渐进切换 | 两者协同 | 通过 Feature Flag 并行运行新旧系统，确认无问题后全量切换 |

### 关键成果

- 12 天完成平台全面重建
- 48 小时内上线 Telegram 集成
- 914 个 PR 合并（679 个工程师 PR + 235 个设计师 PR）
- 88% 的工程师 PR 和 66% 的设计师 PR 有 AI 参与

### 对前端工程师角色的重新定义

作者认为，未来前端工程师的核心价值不在于"还原设计稿"，而在于：
- **架构扩展者** — 构建 UI 层之下的基础设施
- **质量守门人** — 把控架构设计、边界情况和端到端功能
- **交付策略师** — 设计 Feature Flag、灰度发布、增量上线等风险控制方案

### 核心洞察

> AI 消除了设计与工程之间的"翻译层"。它没有取代任何一方，只是填平了二者之间的鸿沟。

作者强调，这不是"AI 取代程序员"，而是人和 AI 各司其职：设计师发挥产品和交互判断力，工程师负责架构和交付质量，AI 则承担机械性的代码翻译和审查工作。这种分工让团队以更少的"浪费时间"实现了更高的交付速度。
[Timestamp: 2026/04/30 18:55:52]

**user**: 我的 obsidian 为什么渲染不了这个文档
[Context: Notes: projects/2026-04-code-agent/raw/cc-haha/index.md]
[Timestamp: 2026/04/30 19:42:16]

**ai**: 
<think>用户的问题是 Obsidian 无法渲染这个文档。让我仔细查看这个文档的内容。

问题在于这个文档的结构：

```html
<active_note>
<title>index</title>
<path>projects/2026-04-code-agent/raw/cc-haha/index.md</path>
<ctime>2026-04-30T11:35:52.342Z</ctime>
<mtime>2026-04-30T11:41:09.753Z</mtime>
<content>
---
layout: home
hero:
  name: Claude Code Haha
  ...
---
</content>
</active_note>
```

问题很明显：
1. 开头有一个 `<active_note>...</active_note>` 的 HTML 注释/标签
2. 里面还有另一个用 `---` 分隔 frontmatter 的 YAML 块
3. 但是 `---` frontmatter 没有正确闭合！

文档中只有开头 `---` 但没有结尾 `---`，导致整个 Markdown 被解析为一个巨大的代码块或 frontmatter，一直持续到文件末尾。这就是为什么文档无法正常渲染的原因。

解决方案：
1. 删除 `<active_note>` 标签
2. 正确闭合 frontmatter 的 `---` 块
</think>

问题找到了。文档有两处语法错误：

## 问题 1：未闭合的 YAML frontmatter

```yaml
---
layout: home
hero:
  ...
---
```

这里只有开头的 `---`，但**缺少结尾的 `---`**。在 YAML frontmatter 中，必须成对出现：

```yaml
---
# 内容写在这里
---
```

少了结尾的 `---`，Obsidian 会把整个文件都当作 frontmatter 处理，导致后面的内容无法正常渲染。

## 问题 2：多余的 `<active_note>` 标签

文档最外层有 `<active_note>...</active_note>` HTML 标签，这会干扰 Markdown 解析。

---

## 修复方法

将文档改为正确的格式：

```yaml
---
layout: home
hero:
  name: Claude Code Haha
  text: 本地可运行的 Claude Code
  tagline: 基于泄露源码修复，支持接入任意 Anthropic 兼容 API（MiniMax、OpenRouter 等）
  image:
    src: /images/logo-horizontal.png
    alt: Claude Code Haha
  actions:
    - theme: brand
      text: 快速开始
      link: /guide/quick-start
    - theme: alt
      text: GitHub
      link: https://github.com/NanmiCoder/cc-haha
features:
  - icon: 🖥
    title: 完整 TUI 交互
    details: 与官方 Claude Code 一致的 Ink 终端界面，支持 --print 无头模式
  - icon: 🧠
    title: 记忆系统
    details: 跨会话持久化记忆，自动提取、智能检索、AutoDream 做梦整合
    link: /memory/
  - icon: 🤖
    title: 多 Agent 系统
    details: 多代理编排、并行任务执行、Teams 协作、Worktree 隔离
    link: /agent/
  - icon: 🧩
    title: Skills 系统
    details: 可扩展能力插件、自定义工作流、条件激活
    link: /skills/01-usage-guide
  - icon: 🌐
    title: 第三方模型支持
    details: 接入 OpenAI、DeepSeek、Ollama 等任意兼容模型
    link: /guide/third-party-models
  - icon: 💬
    title: IM 接入
    details: 在桌面端 webapp 配置 Telegram / 飞书，并通过独立 adapter 进程远程对话 Claude Code
    link: /im/
  - icon: 💻
    title: Computer Use
    details: 桌面控制功能 — 截屏、鼠标、键盘操作（Python Bridge 实现）
    link: /features/computer-use
  - icon: 🖥
    title: 桌面端
    details: 基于 Tauri 2 + React 的图形化客户端，多标签、多会话、IM 适配器接入，支持 macOS 和 Windows
    link: /desktop/
---
```

删除开头的 `<active_note>` 标签和结尾的 `</active_note>` 标签，并补上 frontmatter 的闭合 `---` 即可。
[Timestamp: 2026/04/30 19:42:56]