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

> 原文是 VitePress 首页配置（只有 frontmatter），以下 body 为 Obsidian 可读版，复述同样的信息，未改动任何 frontmatter 字段。

# Claude Code Haha

**本地可运行的 Claude Code** —— 基于泄露源码修复，支持接入任意 Anthropic 兼容 API（MiniMax、OpenRouter 等）。

- GitHub：<https://github.com/NanmiCoder/cc-haha>
- 快速开始：`/guide/quick-start`

## 特性一览

| 模块 | 说明 | 文档 |
|------|------|------|
| 🖥 完整 TUI 交互 | 与官方 Claude Code 一致的 Ink 终端界面，支持 `--print` 无头模式 | — |
| 🧠 记忆系统 | 跨会话持久化记忆，自动提取、智能检索、AutoDream 做梦整合 | `/memory/` |
| 🤖 多 Agent 系统 | 多代理编排、并行任务执行、Teams 协作、Worktree 隔离 | `/agent/` |
| 🧩 Skills 系统 | 可扩展能力插件、自定义工作流、条件激活 | `/skills/01-usage-guide` |
| 🌐 第三方模型支持 | 接入 OpenAI、DeepSeek、Ollama 等任意兼容模型 | `/guide/third-party-models` |
| 💬 IM 接入 | 在桌面端 webapp 配置 Telegram / 飞书，并通过独立 adapter 进程远程对话 Claude Code | `/im/` |
| 💻 Computer Use | 桌面控制功能 —— 截屏、鼠标、键盘操作（Python Bridge 实现） | `/features/computer-use` |
| 🖥 桌面端 | 基于 Tauri 2 + React 的图形化客户端，多标签、多会话、IM 适配器接入，支持 macOS 和 Windows | `/desktop/` |

## 本仓库中对应的实现文档

参见同目录：

- [[raw/cc-haha/agent-02-implementation.md|agent-02-implementation]] —— 多 Agent 系统实现
- [[raw/cc-haha/agent-03-framework.md|agent-03-framework]] —— Agent 框架接口层
- [[raw/cc-haha/memory-02-implementation.md|memory-02-implementation]] —— 记忆系统实现
- [[raw/cc-haha/skills-02-implementation.md|skills-02-implementation]] —— Skills 系统实现
- [[raw/cc-haha/channel-01-channel-system.md|channel-01-channel-system]] —— IM Channel 系统
- [[raw/cc-haha/features-computer-use-architecture.md|features-computer-use-architecture]] —— Computer Use 架构
- [[raw/cc-haha/reference-project-structure.md|reference-project-structure]] —— 项目结构索引
- [[raw/cc-haha/README.md|README]] —— 项目主 README
