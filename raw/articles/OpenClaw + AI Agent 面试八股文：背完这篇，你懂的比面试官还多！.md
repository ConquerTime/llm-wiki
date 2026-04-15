---
title: "OpenClaw + AI Agent 面试八股文：背完这篇，你懂的比面试官还多！"
source: "https://zhuanlan.zhihu.com/p/2013536456132554764"
author:
  - "[[王几行XING​​知势榜科技互联网领域影响力榜答主]]"
published:
created: 2026-04-15
description: "最近刷招聘网站，你一定注意到了一个趋势：AI Agent 工程师的岗位需求在 2026 年暴涨了 25%。而提到 Agent，绕不开的一个名字就是 OpenClaw——这个狂揽 270K+ GitHub Stars 的开源项目，已经成了面试官最爱考的”…"
tags:
  - "clippings"
---
目录

收起

一、OpenClaw 是什么？一句话讲清楚

面试必答：OpenClaw 的三个核心特点

第一章基础核心概念 Q&A（20 题，难度递增）

二、五大核心组件：这是面试最爱考的架构题

1\. Gateway（网关）

2\. Brain（大脑）

3\. Memory（记忆）

4\. Skills（技能）

5\. Heartbeat（心跳）

第二章 Q&A（20 题，难度递增）

三、ReAct 框架：面试必考第一题

核心循环

和 CoT 的区别（高频追问）

第三章 Q&A（20 题，难度递增）

四、AI Agent 四大基础组件

1\. LLM（大脑）

2\. Planning（规划）

3\. Memory（记忆）

4\. Tool Use（工具调用）

第四章 Q&A（20 题，难度递增）

四步流程

第五章 Q&A（20 题，难度递增）

六、Multi-Agent 与协议标准化

\- MCP（Model Context Protocol）

\- A2A（Agent-to-Agent Protocol）

两者的关系

第六章 Q&A（20 题，难度递增）

七、OpenClaw vs 其他框架：面试对比题

第七章 Q&A（20 题，难度递增）

八、安全与 Guardrails：容易被忽略的加分项

核心风险

防御措施

第八章 Q&A（20 题，难度递增）

九、综合高频面试 Q&A 速记卡

结语

参考来源

> 最近刷招聘网站，你一定注意到了一个趋势： **AI Agent 工程师的岗位需求在 2026 年暴涨了 25%** 。而提到 Agent，绕不开的一个名字就是 OpenClaw——这个狂揽 **270K+ GitHub Stars** 的 [开源项目](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E5%BC%80%E6%BA%90%E9%A1%B9%E7%9B%AE&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLlvIDmupDpobnnm64iLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.r-L7Ce92kYNt9a9M8pbSfXJwR4NFgbXYwb1-QrWa_0s&zhida_source=entity) ，已经成了面试官最爱考的”新八股”。

问题来了：OpenClaw 到底是什么？Agent 的核心架构怎么答？ReAct、CoT、Function Calling 这些概念怎么串起来？

别慌，这篇文章帮你从零到一搞定。不灌水，全干货， **每个章节 20 道面试题** ，难度从入门到源码级，背完直接上战场。

---

### 一、OpenClaw 是什么？一句话讲清楚

**OpenClaw** （原名 Clawdbot/Moltbot）是由 Peter Steinberger 开发的 **开源自主 AI Agent 框架** 。简单说，它就是一个跑在你自己机器上的”数字员工”——通过 WhatsApp、Telegram、Slack、飞书、钉钉等你已经在用的消息平台，让大模型 **代替你执行任务** 。

不只是聊天。它能发邮件、改文件、抓网页、设提醒、跑脚本、调 API，甚至在你不在电脑前的时候，自动帮你处理收件箱。

![](https://pica.zhimg.com/v2-da5a35f75b0be3703139767b91cadb84_1440w.jpg)

### 面试必答：OpenClaw 的三个核心特点

| 特点 | 说明 |
| --- | --- |
| 开源本地优先 | MIT 许可证，数据存本地 Markdown 文件，不依赖云端数据库 |
| 多平台接入 | 一个 Agent 同时连接 20+ 消息平台，部署一次全平台可用 |
| 自主执行 | 不只回答问题，还能 shell 命令、浏览器自动化、文件操作 |

> 面试加分话术：”OpenClaw 和 ChatGPT 的本质区别在于——ChatGPT 是对话工具，OpenClaw 是执行框架。前者给你答案，后者帮你干活。”

---

## 第一章基础核心概念 Q&A（20 题，难度递增）

**基础级（Q1–Q5）**

**Q1：OpenClaw 是什么？** A：OpenClaw 是一个开源、本地优先的 AI Agent 框架，通过消息平台连接 LLM，使模型可以执行真实任务（发邮件、修改文件、调用 API 等）。

**Q2：OpenClaw 的前身叫什么？** A：Warelay → Clawdbot → Moltbot → OpenClaw。

**Q3：OpenClaw 和 ChatGPT 的区别？** A：ChatGPT 是对话工具，只输出文本；OpenClaw 是执行框架，可以调用工具、操作文件、发送消息，即不仅能“说”，还能“做”。

**Q4：OpenClaw 支持哪些消息平台？** A：支持 20+ 平台，包括 WhatsApp（Baileys）、Telegram（grammY）、Discord（discord.js）、Slack（Bolt）、飞书、钉钉、Signal、iMessage、IRC、Matrix、Google Chat、MS Teams、LINE 等。

**Q5：OpenClaw 的 [开源许可证](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E5%BC%80%E6%BA%90%E8%AE%B8%E5%8F%AF%E8%AF%81&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLlvIDmupDorrjlj6_or4EiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.h_AAmM4HJsoRq9U9V5kuaMmt6Gar8dd14Dro3pdlYFY&zhida_source=entity) 是什么？** A：MIT License，允许个人和商业使用、修改和再发布。

**进阶级（Q6–Q10）**

**Q6：OpenClaw 的 [技术栈](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E6%8A%80%E6%9C%AF%E6%A0%88&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLmioDmnK_moIgiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.gZ0yP9iQ1UIypxpPMfRbY3VMOAGfRfzv2-33bWn_62Q&zhida_source=entity) 是什么？** A：核心运行时 Node.js v22+，使用 TypeScript 编写；包管理支持 npm/pnpm/bun；消息通道通过各平台 SDK（Baileys、grammY、discord.js、Slack Bolt 等）。

**Q7：什么是“本地优先”？** A：所有数据（记忆、会话、配置）默认存储在本地 `~/.openclaw/` 目录，以 Markdown 和 JSON 文件形式保存，不依赖云数据库。

**Q8：支持哪些大模型？** A：模型无关设计，支持 GPT、Claude、Gemini、DeepSeek、Llama、Minimax 等。模型通过 `provider/model` 格式配置，如 `openai/gpt-4o` 、 `anthropic/claude-sonnet-4-20250514` ，也支持 OpenRouter。

**Q9：OpenClaw 如何部署？** A：三种方式： 1） `openclaw onboard --install-daemon` 安装系统服务（launchd/systemd）； 2）Docker 容器部署； 3）远程 Linux 服务器 + Tailscale/SSH 隧道访问。

**Q10：OpenClaw 的项目愿景？** A：VISION.md 中的核心目标是 **“the AI that actually does things”** ，即真正能执行任务的 AI 助手，当前优先级是安全默认值、Bug 修复和首次运行体验。

**高级（Q11–Q15）**

**Q11：代码仓库结构？** A：主要目录包括：

- `extensions/` ：消息平台插件（Discord、Slack、Feishu 等）
- `skills/` ：内置技能模板
- `docs/` ：文档
- `apps/` ：macOS / iOS / Android 客户端
- `Swabble/` ：Swift 语音唤醒模块

**Q12：PI Agent 是什么？** A：PI Agent（pi-mono）是 OpenClaw 内嵌的 Agent 执行核心，负责模型调用和工具执行；会话管理、工具发现等由 OpenClaw 控制。

**Q13：模型标识符如何解析？** A：使用 `provider/model` 格式，并按第一个 `/` 分割。例如 `openrouter/moonshotai/kimi-k2` 中 provider 为 `openrouter` 。若省略 provider，则使用默认 provider。

**Q14：Workspace 和 State Dir 的区别？** A：Workspace（默认 `~/.openclaw/workspace` ）是 Agent 工作目录，存放 AGENTS.md、SOUL.md 等文件；State Dir（ `~/.openclaw/` ）存放配置、凭证、会话历史等系统数据。

**Q15：OpenClaw 的 Companion App？** A：包括 macOS（SwiftUI）、iOS（SwiftUI）、Android（Kotlin + Jetpack Compose）客户端，通过 Gateway WebSocket 连接，提供摄像头、屏幕录制、定位等设备能力。

**源码级（Q16–Q20）**

**Q16：Workspace Bootstrap 文件有哪些？** A： `AGENTS.md` （行为规则）、 `SOUL.md` （人格语气）、 `TOOLS.md` （工具说明）、 `BOOTSTRAP.md` （首次运行流程）、 `IDENTITY.md` （Agent 名称）、 `USER.md` （用户信息）。空文件会跳过，大文件会截断。

**Q17：Session 数据存储在哪里？** A：JSONL 格式，路径： `~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl` 。Session ID 由系统生成，不读取旧版 Pi/Tau 的会话目录。

**Q18：OPENCLAW\_PROFILE 的作用？** A：当设置 `OPENCLAW_PROFILE=<name>` （非 default）时，Workspace 路径变为 `~/.openclaw/workspace-<profile>` ，用于多 Agent 环境隔离。

**Q19：skipBootstrap 配置的作用？** A：配置 `{ agent: { skipBootstrap: true } }` 可禁止自动创建 Bootstrap 文件，适用于用户自行管理 Workspace 的场景。

**Q20：Sandbox seed 的安全限制？** A：Sandbox 初始化时只复制 Workspace 内的普通文件；指向 Workspace 外部的 symlink 或 hardlink 会被忽略，以防止沙箱逃逸访问 [宿主系统](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E5%AE%BF%E4%B8%BB%E7%B3%BB%E7%BB%9F&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLlrr_kuLvns7vnu58iLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.Mk04NVpIA83ajbFO4DHIz6ZoiBbVIuVYPbYN_HfzmQM&zhida_source=entity) 。

---

### 二、五大核心组件：这是面试最爱考的架构题

OpenClaw 采用 **五组件架构** ，每个组件职责分明。面试官问”请介绍一下 OpenClaw 的架构”，按这个顺序答就对了：

![](https://pic2.zhimg.com/v2-7a54cf3d841484f0b2bc0f24b0180d0d_1440w.jpg)

### 1\. Gateway（网关）

Gateway 是一个长期运行的 WebSocket 服务器（默认 `localhost:18789` ），负责从 WhatsApp、Telegram、Slack 等各个渠道 **路由消息** 。

关键点： **Gateway 不做推理，只做路由** 。这种设计保证了系统的模块化——换消息平台不影响 Agent 逻辑。

### 2\. Brain（大脑）

Brain 是核心 [推理引擎](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E6%8E%A8%E7%90%86%E5%BC%95%E6%93%8E&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLmjqjnkIblvJXmk44iLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9._NxQBon7WYrfqPLfhVMZYW6YKe9AzSDBDODpnrMJWvQ&zhida_source=entity) ，负责 **编排 LLM 调用** ，运行 ReAct 推理循环：

```
组装系统提示词 -> 发送给 LLM -> 解析响应 -> 执行工具调用 -> 循环直到产出最终答案
```

Brain 是 **模型无关** 的——GPT、Claude、Gemini、DeepSeek、Llama 都能用，根据任务需求灵活切换。

### 3\. Memory（记忆）

OpenClaw 的 [记忆系统](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E8%AE%B0%E5%BF%86%E7%B3%BB%E7%BB%9F&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLorrDlv4bns7vnu58iLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.sSgmf521-TksKso1_GLEZTUqcadGkj4u3dU_f_tT7NY&zhida_source=entity) 非常特别： **全部用本地 Markdown 文件存储** ，不用数据库。

两层架构：

- **Daily Logs** （ `memory/YYYY-MM-DD.md` ）：每日运营笔记，系统启动时加载今天和昨天的
- **MEMORY.md** ： [长期记忆](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E9%95%BF%E6%9C%9F%E8%AE%B0%E5%BF%86&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLplb_mnJ_orrDlv4YiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.4SyBdq62ZsRDpPC3TDEl6I1eSzMO3WZrEujE1V59HtQ&zhida_source=entity) ，存储用户偏好、项目约定等持久信息

检索方式： **混合搜索** = 向量语义搜索 + BM25 关键词检索，两种方式结合保证召回率。

还有一个巧妙设计：当对话 token 快用完时，OpenClaw 会发一个 **静默指令** ，让 AI 自动把重要信息写入 MEMORY.md，然后再清理历史——用户完全无感知。

### 4\. Skills（技能）

Skills 就是 **存储为 Markdown 文件的提示词模板** 。每个 Skill 一个文件夹，里面放一个 `SKILL.md` ，包含 YAML [元数据](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E5%85%83%E6%95%B0%E6%8D%AE&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLlhYPmlbDmja4iLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.TP8JkfjvN3CdKvFkuoEMDCepMU4L0ZvEpigugddQm_Q&zhida_source=entity) 和自然语言指令。

```
---
name: weekly-report
description: 自动生成周报
---
# 指令内容...
```

目前 ClawHub 技能市场已有 **5000+ 社区贡献的 Skills** ，覆盖邮件管理、数据分析、代码部署等场景。

### 5\. Heartbeat（心跳）

Heartbeat 让 OpenClaw 从”被动响应”变成” **主动执行** “。每 **30 分钟** 触发一次，检查所有 Agent 文件，判断是否有需要主动处理的任务。

比如：定时检查邮箱、每天早上发天气摘要、监控特定网页变化——不需要你发消息，它自己就会干。

### 第二章 Q&A（20 题，难度递增）

**基础级（Q1-Q5）**

**Q1：OpenClaw 的五大组件分别是什么？**

A：Gateway（网关）、Brain（大脑）、Memory（记忆）、Skills（技能）、Heartbeat（心跳）。

**Q2：Gateway 的核心职责是什么？为什么不在 Gateway 中做推理？**

A：Gateway 只负责消息路由——从各消息平台接收消息并分发给 Agent。不做推理是为了 **模块化** ：消息通道和 Agent 逻辑解耦，更换消息平台不影响推理流程。

**Q3：OpenClaw 的记忆系统为什么选择 Markdown 而不用数据库？**

A：四个原因：(1) 本地优先，无需额外基础设施；(2) 人类可读可编辑；(3) 可用 Git 进行 [版本控制](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E7%89%88%E6%9C%AC%E6%8E%A7%E5%88%B6&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLniYjmnKzmjqfliLYiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.qqUx0y6Rh2HBkrcw_w2JNeCOABg6hOXOUP2QPqrvsv4&zhida_source=entity) ；(4) 与 Agent 的 Workspace 概念天然融合。

**Q4：什么是 Heartbeat？它和 [定时任务](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E5%AE%9A%E6%97%B6%E4%BB%BB%E5%8A%A1&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLlrprml7bku7vliqEiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.6KsMg0JKUQK7r3tih8WaosmS9qyw468txPTR00iOKng&zhida_source=entity) 有什么区别？**

A：Heartbeat 是 Agent 的”主动意识”——每 30 分钟检查一次是否有需要处理的事情。与定时任务不同，Heartbeat 在 **主会话** 中运行，具有完整的对话上下文和记忆，能智能判断是否需要行动。

**Q5：Skills 的 [存储格式](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E5%AD%98%E5%82%A8%E6%A0%BC%E5%BC%8F&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLlrZjlgqjmoLzlvI8iLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.mIBV3K7K7be9Yv8rZ9Mn6Wgq8QXNh5LUbtuzuOptJyo&zhida_source=entity) 是什么？**

A：每个 Skill 是一个包含 `SKILL.md` 文件的文件夹。SKILL.md 由 YAML 前置元数据（name、description）和 Markdown 自然语言指令组成。

**进阶级（Q6-Q10）**

**Q6：Gateway 的 [通信协议](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E9%80%9A%E4%BF%A1%E5%8D%8F%E8%AE%AE&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLpgJrkv6HljY_orq4iLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.8vyBXCZ3pO3tCepdtQxEZ5RNiJssCJDJ6RKAaTq4pTI&zhida_source=entity) 是什么？连接生命周期是怎样的？**

A：使用 **WebSocket** 传输 JSON 文本帧。生命周期：(1) 客户端发送 `connect` 请求（必须是第一帧）；(2) Gateway 返回 `hello-ok` 含 presence 和 health 快照；(3) 之后正常收发请求/事件；(4) 非 JSON 或非 connect 的首帧直接断开。

**Q7：OpenClaw Memory 的两层架构分别存储什么？加载策略是什么？**

A：(1) `memory/YYYY-MM-DD.md` — 每日追加式笔记，系统启动时加载 **今天和昨天** 的；(2) `MEMORY.md` — 长期记忆，存储持久偏好和约定， **仅在私聊主会话中加载** ，群组上下文中不加载。

**Q8：Skills 从哪些位置加载？优先级如何？**

A：三个位置，Workspace 优先：(1) Bundled（随安装包自带）；(2) Managed/local（ `~/.openclaw/skills` ）；(3) Workspace（ `<workspace>/skills` ）。同名冲突时 Workspace 胜出。

**Q9：Gateway 分发哪些类型的事件？**

A：六类核心事件： `agent` （Agent 推理流）、 `chat` （聊天消息）、 `presence` （在线状态）、 `health` （健康检查）、 `heartbeat` （心跳触发）、 `cron` （定时任务触发）。

**Q10：Heartbeat 的”静默回复”机制是什么？**

A：Heartbeat 运行后，如果没有需要通知用户的事项，Agent 回复 `HEARTBEAT_OK` ，这个消息 **不会被投递给用户** ——用户完全无感知。只有确实有重要事项时才发送可见消息。

**高级（Q11-Q15）**

**Q11：OpenClaw 的 Memory Flush 机制如何工作？**

A：当会话 token 接近 `contextWindow - reserveTokensFloor - softThresholdTokens` 时，OpenClaw 发送一个 **静默 Agentic Turn** ——包含 systemPrompt（”Session nearing compaction. Store durable memories now.“）和 userPrompt（写入 memory 文件，用 NO\_REPLY 回复）。每个 compaction 周期只触发一次，工作区只读时跳过。

**Q12：OpenClaw 的向量搜索支持哪些 Embedding 提供商？自动选择顺序是什么？**

A：自动选择顺序：(1) `local` （如果配置了本地 GGUF 模型路径）；(2) `openai` （如果有 OpenAI Key）；(3) `gemini` ；(4) `voyage` ；(5) `mistral` 。还支持 `ollama` 但不自动选择。如果都没有，memory search 保持禁用。

**Q13：Heartbeat 和 Cron 分别适合什么场景？**

A： **Heartbeat** 适合多项定期检查的批量处理（收件箱+日历+通知合并一次处理）、需要对话上下文的智能判断。 **Cron** 适合精确定时（每周一 9 点周报）、独立任务（不需要上下文）、不同模型/算力需求、一次性提醒（ `--at "20m"` ）。

**Q14：OpenClaw 的 QMD 后端是什么？它如何增强 Memory Search？**

A：QMD 是一个实验性的本地搜索 sidecar，结合 **BM25 + 向量 + 重排序** 。通过 `memory.backend = "qmd"` 启用。QMD 使用 Bun + node-llama-cpp 完全本地运行，自动从 HuggingFace 下载 GGUF 模型。状态存储在 `~/.openclaw/agents/<agentId>/qmd/` 下，搜索失败时自动回退到内置 SQLite 管理器。

**Q15：Gateway 的 Wire Protocol 有什么安全机制？**

A：(1) 设置 `OPENCLAW_GATEWAY_TOKEN` 后， `connect.params.auth.token` 必须匹配；(2) 所有连接必须签名 `connect.challenge` nonce；(3) v3 签名绑定 `platform` + `deviceFamily` ，重连时 Gateway 校验元数据一致性；(4) 副作用方法（ `send` 、 `agent` ）需要幂等键， [服务端](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E6%9C%8D%E5%8A%A1%E7%AB%AF&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLmnI3liqHnq68iLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.duvZAZWvVdAEnmRCWkZLVV5Hs5DtpAvF_repMjzihbs&zhida_source=entity) 保持短期去重缓存。

**源码级（Q16-Q20）**

**Q16：OpenClaw 的 Agent Loop 完整执行流程是怎样的？**

A：根据 `docs/concepts/agent-loop.md` ：

(1) `agent` RPC 验证参数、解析 session、 [持久化](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E6%8C%81%E4%B9%85%E5%8C%96&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLmjIHkuYXljJYiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.rRgewafQfysCldHdOvLW7V8VNIdLhYGL8Cp639UyV98&zhida_source=entity) session 元数据，立即返回 `{ runId, acceptedAt }` ；(2) `agentCommand` 解析模型和默认值、加载 Skills 快照、调用 `runEmbeddedPiAgent` ；

(3) `runEmbeddedPiAgent` 通过 per-session + global 队列 [序列化](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E5%BA%8F%E5%88%97%E5%8C%96&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLluo_liJfljJYiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.XiG61K4Aw872yVHd2Vo-raSbVit3SveJQNThSTJGCfc&zhida_source=entity) 运行、解析 auth profile、构建 pi session、订阅事件并流式输出、超时时 abort；

(4) `subscribeEmbeddedPiSession` 将 pi-agent-core 事件桥接为 OpenClaw 的 tool/assistant/lifecycle 流。

**Q17：OpenClaw 的 Plugin Hook 系统有哪些关键 Hook 点？**

A：关键 Hook 包括： `before_model_resolve` （模型解析前覆盖 provider）、 `before_prompt_build` （注入 prependContext/systemPrompt）、 `before_tool_call` / `after_tool_call` （拦截工具参数/结果）、 `tool_result_persist` （工具结果写入前变换）、 `before_compaction` / `after_compaction` （压缩周期）、 `message_received` / `message_sending` / `message_sent` （消息钩子）、 `session_start` / `session_end` 、 `gateway_start` / `gateway_stop` 。

**Q18：OpenClaw 的 Queue Mode 有哪些？streaming 时如何处理新消息？**

A：三种模式：

- (1) `steer` — 在每次 tool call 后检查队列，有新消息时跳过剩余 tool calls（返回 “Skipped due to queued user message.” 错误），注入新消息；
- (2) `followup` — 当前 turn 结束后才处理队列消息；
- (3) `collect` — 收集所有队列消息后一次性处理。

**Q19：OpenClaw Multi-Agent 路由中，”一个 Agent” 的完整隔离范围是什么？**

A：一个 Agent 拥有独立的：

- (1) Workspace（ [文件系统](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLmlofku7bns7vnu58iLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.N8NbFpeMKfTgVSj7j1rZ14DMnbgIAhmkElNmH866GBU&zhida_source=entity) 、AGENTS.md/SOUL.md）；
- (2) Agent Dir（ `~/.openclaw/agents/<agentId>/agent` ，含 auth-profiles.json）；
- (3) Session Store（ `~/.openclaw/agents/<agentId>/sessions/` ）。Auth profile 是 per-agent 的，main agent 凭证 **不自动共享** 。Skills 通过 workspace `skills/` 隔离，共享 skills 在 `~/.openclaw/skills` 。

**Q20：OpenClaw 的 Block Streaming 和 Coalesce 机制如何工作？**

A：Block Streaming 默认关闭（ `blockStreamingDefault: "off"` ）。

启用后，完成的 assistant block 立即发送。断裂边界通过 `blockStreamingBreak` 控制（ `text_end` vs `message_end` ，默认 text\_end）。

软块分块通过 `blockStreamingChunk` 控制（默认 800-1200 字符，优先段落断裂，其次换行，最后句子）。 `blockStreamingCoalesce` 基于空闲时间合并流式 chunk，减少单行刷屏。

非 Telegram 通道需要显式 `*.blockStreaming: true` 才能启用。

---

### 三、ReAct 框架：面试必考第一题

![](https://pic4.zhimg.com/v2-55f371f8b049fb55f780ae066f3cb04f_1440w.jpg)

> 面试官：”请解释一下 ReAct 框架。”

**ReAct = Reasoning + Acting** ，即推理与行动的交替循环。这是目前 Agent 最主流的执行模式。

### 核心循环

```
Thought（推理）-> Action（行动）-> Observation（观察）-> 重复，直到任务完成
```
- **Thought** ：LLM 生成推理过程，分析当前状态，决定下一步
- **Action** ：根据推理结果执行具体操作（调用工具、查询 API 等）
- **Observation** ：收集执行结果，作为下一轮推理的输入

### 和 CoT 的区别（高频追问）

| 维度 | CoT（链式思维） | ReAct |
| --- | --- | --- |
| 核心能力 | 纯推理，逐步分解问题 | 推理 + 行动，与外部环境交互 |
| 信息来源 | 仅依赖模型内部知识 | 可调用外部工具获取实时数据 |
| 幻觉风险 | 高（无法验证事实） | 低（通过工具调用获取真实数据） |
| 适用场景 | 数学推理、逻辑分析 | 需要执行操作的复杂任务 |

> 面试金句：”CoT 是让模型’想清楚’，ReAct 是让模型’想清楚然后动手干’。ReAct 的核心优势在于推理能跟踪和更新行动计划，行动能从环境中获取新信息来纠正推理。”

### 第三章 Q&A（20 题，难度递增）

**基础级（Q1-Q5）**

**Q1：ReAct 是什么的缩写？核心思想是什么？**

A：Reasoning + Acting。核心思想是让 LLM 在推理（Thought）和行动（Action）之间交替循环，通过观察（Observation）行动结果来不断调整策略，直到完成任务。

**Q2：ReAct 循环的三个步骤分别是什么？**

A：(1) **Thought** — LLM 分析当前状态并推理下一步；(2) **Action** — 执行具体操作（调工具、查 API）；(3) **Observation** — 收集执行结果，作为下一轮推理的输入。

**Q3：ReAct 和纯 CoT 的最大区别是什么？**

A：CoT 只在模型内部推理，无法与外部环境交互，容易产生幻觉；ReAct 可以通过 Action 步骤调用外部工具获取真实数据，然后基于观察结果继续推理。 **Q4：ReAct 循环在什么条件下终止？** A：三种情况：(1) Agent 找到了最终答案；(2) 达到预设的最大迭代次数；(3) 遇到无法继续的错误。

**Q5：为什么说 ReAct 能减少幻觉？**

A：因为 ReAct 通过 Action 步骤获取 **真实的 [外部数据](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E5%A4%96%E9%83%A8%E6%95%B0%E6%8D%AE&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLlpJbpg6jmlbDmja4iLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.fLeMDd58HJ8eixTiIrr6GSJV31CRjtusM_I8Ic_CeeM&zhida_source=entity)** ，通过 Observation 步骤 **验证推理结果** ，形成了事实-推理-验证的闭环，不完全依赖模型的内部知识。

**进阶级（Q6-Q10）**

**Q6：CoT、ToT、ReAct、Reflexion 分别是什么？它们的关系是什么？**

A： **CoT** （Chain of Thought）= 逐步推理； **ToT** （Tree of Thought）= 树状搜索多条推理路径； **ReAct** = 推理+行动交替； **Reflexion** = 自我反思优化。它们不是互斥的——ReAct 可以在 Thought 步骤中使用 CoT，Reflexion 可以在 ReAct 循环失败后触发自我反思。

**Q7：OpenClaw 中的 Brain 组件如何实现 ReAct 循环？**

A：Brain 组装系统提示词（含可用工具列表）-> 发送给 LLM -> LLM 输出推理和工具调用请求 -> Brain 解析并执行工具调用 -> 将结果返回 LLM -> 循环直到 LLM 输出最终回复。

**Q8：ReAct 的推理过程和行动过程，哪个更消耗 token？如何优化？**

A：Action + Observation 通常更消耗 token（因为包含工具调用结果）。 [优化方法](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E4%BC%98%E5%8C%96%E6%96%B9%E6%B3%95&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLkvJjljJbmlrnms5UiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.fSwib6uVYXuaA_DO5rjPobhp0Ennk4BLZyBBVBQWKGE&zhida_source=entity) ：(1) 限制工具返回结果的长度；(2) 设置最大迭代次数；(3) 使用 compaction 压缩上下文；(4) 对大结果做摘要后再返回。

**Q9：Plan-and-Solve 和 ReAct 有什么区别？**

A：Plan-and-Solve 先生成完整计划再逐步执行，适合可预见的任务；ReAct 边想边做，每步根据观察动态调整，适合不确定性高的任务。Plan-and-Solve 效率更高但灵活性差，ReAct 灵活但可能走弯路。

**Q10：如果 ReAct 循环中某个 Action 失败了，Agent 应该怎么处理？**

A：好的 Agent 设计应该：(1) 将错误作为 Observation 反馈给 LLM；(2) LLM 在下一个 Thought 中分析失败原因；(3) 尝试替代方案或调整参数重试；(4) 如果多次失败，升级为向用户请求帮助。这种”自愈”能力是 Agent 区别于脚本的关键。

**高级（Q11-Q15）**

**Q11：OpenClaw 的 Agent Loop 中，tool event 的生命周期事件有哪些？**

A：根据源码，工具事件在 `tool` stream 上发射： `tool start` （开始执行）、 `tool update` （执行中更新）、 `tool end` （执行完成）。工具结果在日志记录/发射前会进行大小和图片 payload 的清理（sanitize）。

**Q12：OpenClaw 中 Reply Shaping 和 Suppression 机制是如何工作的？**

A：最终 payload 由 assistant text、reasoning（可选）、inline tool summaries（verbose 模式）、error text 组装。 `NO_REPLY` 被视为静默 token 并从外发 payload 中过滤。消息工具的重复被移除。如果没有可渲染的 payload 且工具出错，会发射 fallback 工具错误回复（除非消息工具已经发送了用户可见的回复）。

**Q13：ReAct 在多步推理中的”错误传播”问题是什么？如何缓解？**

A：如果某一步推理出错，后续步骤基于错误的 Observation 继续推理，错误会逐步放大。缓解方法：(1) 使用 Reflexion 让 Agent 定期自检；(2) 设置 confidence threshold；(3) 关键步骤加入人工审批；(4) OpenClaw 的 Lobster workflow 支持审批门控。

**Q14：OpenClaw 的 Compaction 机制与 ReAct 循环有什么关系？**

A：当 ReAct 循环消耗大量 token 导致上下文接近窗口限制时，OpenClaw 触发 auto-compaction。Compaction 会发射 `compaction` stream 事件，并可以触发 retry。Retry 时会重置 in-memory buffer 和 tool summaries 以避免重复输出。

**Q15：什么是 Agent 的 “Steering while streaming”？OpenClaw 如何实现？**

A：当 Agent 正在流式推理时，用户发送新消息来”转向”Agent 的注意力。OpenClaw 在 `steer` 模式下，每次 tool call 后检查队列。如果有新消息，跳过当前 assistant message 的剩余 tool calls，注入新用户消息，然后继续下一轮推理。

**源码级（Q16-Q20）**

**Q16：OpenClaw Agent Loop 中 `runEmbeddedPiAgent` 的序列化策略是什么？**

A：Runs 通过 **per-session lane + global lane** 进行序列化。这防止了 tool/session [竞争条件](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E7%AB%9E%E4%BA%89%E6%9D%A1%E4%BB%B6&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLnq57kuonmnaHku7YiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.B-ZkGXDZgGmS4u6NC56iCvgJ2pqFhZDcyjYbNTM2LPg&zhida_source=entity) ，保证 session history 的一致性。消息通道可以选择 queue modes（collect/steer/followup）来 feed 这个 lane 系统。

**Q17：OpenClaw 的 System Prompt 由哪些部分组装？**

A：根据源码：(1) OpenClaw 基础 prompt；(2) Skills prompt（从 Skills 快照注入）；(3) Bootstrap context（AGENTS.md、SOUL.md 等文件内容）；(4) Per-run overrides。同时强制执行 model-specific limits 和 compaction reserve tokens。

**Q18：OpenClaw 中 `agent.wait` 和 Agent timeout 分别是什么？默认值是多少？**

A： `agent.wait` 是等待 Agent 完成的 RPC，默认超时 30 秒（仅等待，不停止 Agent），通过 `timeoutMs` 参数覆盖。Agent runtime timeout 由 `agents.defaults.timeoutSeconds` 控制，默认 600 秒（10 分钟），通过 `runEmbeddedPiAgent` 的 abort timer 强制执行。

**Q19：OpenClaw 中 Messaging tool 的 “duplicate suppression” 是什么？**

A：当 Agent 通过消息工具（如 send\_whatsapp）已经发送了回复给用户后，最终的 assistant text 中可能还包含类似的确认文本。OpenClaw 会追踪消息工具的发送记录，从最终 payload 中移除重复内容，避免用户看到同一条消息两次。

**Q20：OpenClaw 的 Agent Loop 可以在哪些节点提前结束？分别是什么原因？**

A：四种提前结束：(1) **Agent timeout** — 超过 `timeoutSeconds` ，触发 abort；(2) **AbortSignal** — 外部取消信号；(3) **Gateway disconnect 或 RPC timeout** — 连接断开；(4) **`agent.wait` timeout** — 仅停止等待，不停止 Agent 本身。

---

### 四、AI Agent 四大基础组件

这是通用 Agent 架构的标准答法： **Agent = LLM（大脑）+ Planning（规划）+ Memory（记忆）+ Tool Use（工具）**

### 1\. LLM（大脑）

负责理解意图、生成文本、进行逻辑判断。是 Agent 的决策核心。

### 2\. Planning（规划）

将复杂目标拆解为可执行的子任务。主要方法：

- **CoT** （Chain of Thought）：逐步推理
- **ToT** （Tree of Thought）：树状搜索多条推理路径
- **Reflexion** ：通过自我反思优化决策
- **Plan-and-Solve** ：先生成整体计划，再逐步执行

### 3\. Memory（记忆）

- **[短期记忆](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E7%9F%AD%E6%9C%9F%E8%AE%B0%E5%BF%86&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLnn63mnJ_orrDlv4YiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.Fzla5sQ5Wgg1f5tBb94pt7oepJL2UhliPPskp7ep0is&zhida_source=entity)** ：对话历史、当前步骤状态（利用上下文窗口）
- **长期记忆** ：向量数据库存储的持久知识，支持 [语义检索](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E8%AF%AD%E4%B9%89%E6%A3%80%E7%B4%A2&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLor63kuYnmo4DntKIiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.loyC_BRO-Xm5TnevoeWOklsYuPs0aK63MMGT3yUROuA&zhida_source=entity)

### 4\. Tool Use（工具调用）

调用外部 API 获取模型训练数据中缺失的信息。下一节详细展开。

### 第四章 Q&A（20 题，难度递增）

**基础级（Q1-Q5）**

**Q1：AI Agent 的标准公式是什么？**

A：Agent = LLM（大脑）+ Planning（规划）+ Memory（记忆）+ Tool Use（工具）。

**Q2：AI Agent 和传统 Chatbot 有什么区别？**

A：Chatbot 只做对话（单轮或多轮），Agent 有自主规划、 [长短期记忆](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E9%95%BF%E7%9F%AD%E6%9C%9F%E8%AE%B0%E5%BF%86&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLplb_nn63mnJ_orrDlv4YiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.jf6TRm_Sn9PHCx6-GLkYiCG7PVmAI7jFEaAIJEMR5G0&zhida_source=entity) 和工具调用能力，能 **自主完成多步骤目标导向的任务** 。

**Q3：Agent 的”自主性”体现在哪里？**

A：五个方面：(1) 无需逐步指导，独立运作；(2) 感知环境变化并调整（反应性）；(3) 有目标导向的主动行为；(4) 与人类自然交互（社交能力）；(5) 从历史中学习改进。

**Q4：短期记忆和长期记忆的区别是什么？**

A： **短期记忆** = 上下文窗口中的对话历史和当前任务状态，随会话结束消失。 **长期记忆** = 持久化存储的知识（向量数据库、Markdown 文件等），跨会话保留。

**Q5：为什么 Agent 需要工具调用能力？**

A：LLM 的训练数据有截止日期，无法获取实时信息；LLM 不擅长精确计算和数据库操作。工具调用弥补了这些不足，让 Agent 能搜索网页、执行代码、访问 API。

**进阶级（Q6-Q10）**

**Q6：Planning 的主要方法有哪些？各自适合什么场景？**

A：(1) **CoT** — 线性逐步推理，适合逻辑清晰的简单任务；(2) **ToT** — 探索多条路径，适合有多种可能解的复杂问题；(3) **Reflexion** — 自我反思优化，适合需要迭代改进的任务；(4) **Plan-and-Solve** — 先规划后执行，适合步骤可预见的多步任务。

**Q7：Agent 的记忆系统设计有哪些常见方案？**

A：(1) **上下文窗口** — 直接放在 prompt 中，简单但受窗口限制；(2) **向量数据库** — 语义检索，适合大量非结构化知识；(3) **关系型数据库** — 结构化查询，适合事实性数据；(4) **Markdown 文件** — OpenClaw 方案，人类可读可编辑；(5) **混合方案** — 向量 + 关键词 + [图数据库](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E5%9B%BE%E6%95%B0%E6%8D%AE%E5%BA%93&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLlm77mlbDmja7lupMiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.G-3-OAbm6hSBEbzwEjJrmizRn1wF3v490QGr56_X2xw&zhida_source=entity) 。

**Q8：什么是 Agentic AI？它有哪些核心特征？**

A：Agentic AI 是具备自主性的 AI 系统，核心从”回答问题”升级为”完成目标”。五大特征：自主性（独立运作）、反应性（感知环境）、主动性（目标导向）、社交能力（自然交互）、学习能力（持续改进）。

**Q9：Agent 的 Planning 模块如何处理失败？**

A：好的 Planning 应支持：(1) **任务分解失败时回退** — 换更 [细粒度](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E7%BB%86%E7%B2%92%E5%BA%A6&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLnu4bnspLluqYiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.UmKtCrIWbl3yEp-HH5OSwKgMHiHelWBnmSZL37VYupg&zhida_source=entity) 的分解策略；(2) **执行失败时重规划** — 根据错误信息调整计划；(3) **Reflexion** — 分析失败原因并在下次避免同类错误；(4) **Human-in-the-loop** — 关键 [决策点](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E5%86%B3%E7%AD%96%E7%82%B9&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLlhrPnrZbngrkiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.xmIdE0_RuqJkJ10ae44eP3PipIm72XPbvxfGn6mHiwM&zhida_source=entity) 请求人类介入。

**Q10：如何评估一个 Agent 系统的好坏？**

A：关键指标：(1) **任务完成率** — 能否成功完成给定任务；(2) **步骤效率** — 完成任务所需的 ReAct 循环次数；(3) **token 消耗** — 成本效率；(4) **幻觉率** — 错误输出比例；(5) **鲁棒性** — 面对异常输入的 [容错能力](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E5%AE%B9%E9%94%99%E8%83%BD%E5%8A%9B&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLlrrnplJnog73lipsiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.7deHbcE6itKM42vB7Z7oT2lPHAruPnReUaotQYKOSjc&zhida_source=entity) ；(6) **延迟** — 端到端响应时间。

**高级（Q11-Q15）**

**Q11：OpenClaw 的 Workspace 文件如何塑造 Agent 的”人格”？**

A：通过 Bootstrap 文件： `SOUL.md` 定义人格、语气和边界； `AGENTS.md` 定义操作指令和行为规则； `USER.md` 定义用户信息和称呼方式； `IDENTITY.md` 定义 Agent 名称和风格。每个新会话开始时注入这些文件内容到上下文。

**Q12：Agent 的上下文管理面临什么核心挑战？如何解决？**

A：核心挑战是 **上下文窗口有限但任务需要的信息量可能超过窗口** 。解决方案：(1) Compaction — 压缩历史对话；(2) Memory Flush — 压缩前自动保存重要信息；(3) RAG — 按需从长期记忆检索相关信息；(4) 摘要 — 对长结果做总结；(5) 分层记忆 — 只加载需要的记忆层。

**Q13：什么是 Agent 的”幻觉-行动放大”问题？**

A：当 Agent 基于幻觉做出错误推理，然后通过工具调用 **实际执行** 了错误操作（如发送错误邮件、删除文件），后果比纯文本幻觉严重得多。这是自主 Agent 的核心风险—— **幻觉从”说错话”升级为”做错事”** 。

**Q14：Agent 中的 Human-in-the-loop 有哪些设计模式？**

A：(1) **审批门控** — 关键操作前暂停等待人类确认（OpenClaw 的 Lobster workflow）；(2) **主动询问** — 信息不足时主动向用户提问；(3) **异常升级** — 遇到无法处理的错误时通知人类；(4) **定期检查点** — 长任务中定期汇报进度和中间结果。

**Q15：如何设计 Agent 的 Tool Policy？**

A：分层策略：(1) **白名单/黑名单** — 明确允许和禁止的工具；(2) **权限等级** — 只读工具自动执行，写入工具需确认；(3) **沙箱隔离** — 危险操作在隔离环境中运行；(4) **[速率限制](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E9%80%9F%E7%8E%87%E9%99%90%E5%88%B6&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLpgJ_njofpmZDliLYiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.2EAdhTKmDyDkw8wG9iAOJS5zCcrHOWxEG6o90iyRdn0&zhida_source=entity)** — 防止工具被过度调用；(5) **审计日志** — 记录所有工具调用历史。

**源码级（Q16-Q20）**

**Q16：OpenClaw 的 Tool Policy 在源码中如何实现？**

A：Core tools（read/exec/edit/write 等系统工具）始终可用但受 tool policy 约束。 `apply_patch` 是可选的，通过 `tools.exec.applyPatch` 门控。 `TOOLS.md` **不控制** 哪些工具存在——它只是给 Agent 的使用指南。额外工具通过 `tools.alsoAllow` 添加（如 `["lobster"]` ）。

**Q17：OpenClaw 的 Session Manager 在 Agent Loop 中起什么作用？**

A：在 Agent Loop 中，SessionManager 负责：(1) 解析和创建 Workspace（沙箱模式下可能重定向到沙箱 workspace root）；(2) 加载 Skills（或复用快照）并注入环境和 prompt；(3) 解析 Bootstrap/context 文件并注入 system prompt；(4) 获取 session 写锁；(5) 在 streaming 前完成准备。

**Q18：OpenClaw 的 `before_prompt_build` hook 能注入哪些内容？**

A：可以注入四种内容：(1) `prependContext` — 每轮动态文本（如当前时间、环境信息）；(2) `systemPrompt` — 替换系统提示；(3) `prependSystemContext` — 在系统提示前追加稳定指导；(4) `appendSystemContext` — 在系统提示后追加稳定指导。推荐用 `prependContext` 做动态内容，用 system-context 字段做稳定指导。 **Q19：OpenClaw 中 Exec 行为的 [信任模型](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E4%BF%A1%E4%BB%BB%E6%A8%A1%E5%9E%8B&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLkv6Hku7vmqKHlnosiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.zF7TUM3PSIbDKWYR59C8CVrsc8m4rj_hSnmQuUCQOCc&zhida_source=entity) 是怎样的？** A：默认情况下，exec 行为是 **host-first** ： `agents.defaults.sandbox.mode` 默认 `off` 。 `tools.exec.host` 默认 `sandbox` 作为路由偏好，但如果 sandbox runtime 未激活，exec 会回退到 Gateway 宿主上运行。隐式 exec 调用（工具调用中不指定 host）遵循相同行为。

**Q20：OpenClaw 的 `tool_result_persist` hook 有什么作用？为什么需要它？**

A： `tool_result_persist` hook 在工具结果 **写入 session transcript 之前** 同步变换结果。应用场景包括：(1) 脱敏 — 移除工具返回的敏感信息（API keys、密码）后再持久化；(2) 压缩 — 截断过长的工具结果以节省 session 存储空间；(3) 结构化 — 将非结构化结果转换为标准格式便于后续检索。五、Function Calling / Tool Calling：让 Agent 真正”动手”

> 面试官：”解释一下 Agent 的工具调用机制。”

**Function Calling（函数调用）** 是 LLM 与外部系统交互的桥梁。它让模型不只输出文本，还能返回 **结构化的调用指令** 。

### 四步流程

**Step 1: 工具注册** — 定义可用工具的名称、描述、参数 schema

**Step 2: LLM 判断** — 根据用户请求和工具描述，模型决定是否需要调用工具

**Step 3: 结构化输出** — LLM 输出 JSON 格式的调用指令：

```
{
  "tool": "send_email",
  "args": {
    "recipient": "bob@example.com",
    "subject": "周报",
    "body": "本周完成了..."
  }
}
```

**Step 4: 执行与反馈** — **LLM 自身不执行函数** ，而是由运行时环境解析 JSON 并执行，结果返回给 LLM 作为后续推理的输入

> 关键理解：”LLM 像是一个’指挥官’，它告诉系统’调用什么工具、传什么参数’，但自己不动手执行。执行由程序运行时负责。”

### 第五章 Q&A（20 题，难度递增）

**基础级（Q1-Q5）**

**Q1：什么是 Function Calling / Tool Calling？**

A：让 LLM 不只输出文本，还能返回 **结构化的工具调用指令** （通常是 JSON），由运行时环境执行后将结果返回给模型，形成闭环。

**Q2：Function Calling 的四个步骤是什么？**

A：(1) 工具注册（定义 name/description/schema）；(2) LLM 判断是否需要调用；(3) 输出结构化 JSON 调用指令；(4) 运行时执行并反馈结果。

**Q3：LLM 自己执行函数吗？**

A：不。LLM 只负责决定”调用什么工具、传什么参数”，实际执行由程序运行时（runtime）负责。LLM 是”指挥官”而非”执行者”。

**Q4：为什么 Agent 需要 Tool Calling 能力？** A：LLM 的训练数据有截止日期，不能获取实时信息；不擅长精确计算；无法直接操作外部系统。Tool Calling 弥补这些不足。

**Q5：Tool 的 schema 描述通常包含哪些字段？**

A：(1) `name` — 工具名称；(2) `description` — 功能描述；(3) `parameters` — 参数的 JSON Schema（含参数名、类型、描述、是否必填）。

**进阶级（Q6-Q10）**

**Q6：Parallel Tool Calling 是什么？什么时候使用？**

A：LLM 在单次回复中返回多个工具调用请求，运行时并行执行。适合多个 **相互独立** 的工具调用（如同时查天气和查日历）。不适合有依赖关系的调用（如先搜索再分析搜索结果）。

**Q7：如何设计好的 Tool Description 来提高调用准确率？** A：(1) 描述要明确具体，说清工具做什么和不做什么；(2) 参数描述要包含类型、格式、示例；(3) 说明 [边界条件](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E8%BE%B9%E7%95%8C%E6%9D%A1%E4%BB%B6&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLovrnnlYzmnaHku7YiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.H0JzUgSd3a00fdapTBiuj-Xs2qF5CbOGnnuZqTAMoG4&zhida_source=entity) 和错误场景；(4) 避免模棱两可的词语。Description 质量直接影响 LLM 选对工具的概率。

**Q8：Tool Calling 和 RAG 的关系是什么？** A：RAG 本质上是一种特殊的 Tool Calling——”检索”就是一个工具。Agent 可以通过 Tool Calling 触发 RAG 检索，获取相关文档，然后基于检索结果生成回答。

**Q9：OpenClaw 中的 Built-in Tools 有哪些？** A：根据源码，Core tools 包括 `read` （读文件）、 `exec` （执行命令）、 `edit` （编辑文件）、 `write` （写文件）等系统工具，始终可用但受 tool policy 约束。 `apply_patch` 是可选的。

**Q10：什么是 MCP（Model Context Protocol）？它如何标准化 Tool Calling？** A：MCP 由 Anthropic 提出，定义了 Agent 与工具/数据源之间的标准化连接协议。每个工具提供商实现 MCP Server，Agent 通过统一的 MCP Client 接口连接——类似 USB 接口的即插即用。

**高级（Q11-Q15）**

**Q11：Tool Calling 中的”幻觉调用”问题是什么？如何防范？** A：LLM 可能调用不存在的工具、传递错误的参数类型、或在不该调用时调用。防范：(1) 严格的 schema 验证；(2) 运行时检查工具名是否在注册列表中；(3) 参数类型强校验；(4) 设置调用频率限制。

**Q12：OpenClaw 的 Tool 结果如何被清理（sanitize）？** A：工具结果在日志记录和事件发射前会进行清理：(1) 大小限制 — 过长的结果被截断；(2) 图片 payload 处理 — 大图片被压缩或替换为引用；(3) 敏感信息脱敏（通过 `tool_result_persist` hook）。

**Q13：什么是 Structured Output？它和 Function Calling 的关系是什么？** A：Structured Output 是让 LLM 按指定 JSON Schema 输出 [结构化数据](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E7%BB%93%E6%9E%84%E5%8C%96%E6%95%B0%E6%8D%AE&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLnu5PmnoTljJbmlbDmja4iLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.hxhqO7FxE5ZpPZfnEVkSXkPDEwZdBk_2FoQ6H-Gg288&zhida_source=entity) 的能力。Function Calling 是 Structured Output 的一种特殊应用——输出的结构化数据恰好是工具调用指令。

**Q14：OpenClaw 的 Extensions 系统如何扩展工具能力？** A：Extensions 是 TypeScript 插件模块（ `extensions/` 目录），每个 extension 实现特定通道或功能。例如 `extensions/feishu/` 实现飞书集成（含文档操作、表格操作、通讯录查询等）， `extensions/diffs/` 实现代码差异查看。Extensions 通过 plugin hooks 注册到 Gateway 生命周期中。

**Q15：Tool Calling 的错误处理最佳实践是什么？** A：(1) **分类错误** — 区分可重试（网络超时）和不可重试（参数错误）；(2) **错误信息反馈** — 将错误详情作为 Observation 返回给 LLM；(3) **重试策略** — 指数退避；(4) **降级方案** — 主工具失败时尝试替代工具；(5) **超时控制** — 设置每个工具的执行超时。

**源码级（Q16-Q20）**

**Q16：OpenClaw 的 `before_tool_call` 和 `after_tool_call` hook 有什么用途？** A： `before_tool_call` 可以在工具执行前拦截和修改参数（如添加认证信息、日志记录、参数校验）。 `after_tool_call` 可以在结果返回前拦截和修改（如 [数据转换](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E8%BD%AC%E6%8D%A2&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLmlbDmja7ovazmjaIiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.xZ45Pl9nzhEiuiOzysnWu9129eecWJ_s4Dimxolwfvs&zhida_source=entity) 、敏感信息脱敏、性能指标收集）。

**Q17：OpenClaw 中 Messaging Tool 的 duplicate suppression 如何影响 Tool Calling？** A：当 Agent 通过消息工具（如 send\_whatsapp）已发送消息后，OpenClaw 会追踪发送记录。如果最终 assistant text 包含类似内容，会自动移除重复部分。这是为了避免用户收到”Agent 发了一条消息”+“我已经帮你发了消息”这种重复。

**Q18：OpenClaw 的 Lobster workflow runtime 如何与 Tool Calling 交互？** A：Lobster 作为工具模式运行——Agent 通过 Tool Calling 调用 `lobster` 工具，Lobster 以 JSON envelope 返回结果。如果返回 `needs_approval` ，Agent 需要用 `resumeToken` + `approve` 标志恢复执行。Lobster 需要通过 `tools.alsoAllow: ["lobster"]` 启用。

**Q19：OpenClaw 的 Gateway 如何验证入站帧中的工具调用？** A：Gateway 使用 **TypeBox schemas** 定义协议，入站帧通过 **JSON Schema 验证** 。从这些 schemas 还会生成 Swift models（用于 macOS/iOS 客户端）。任何不符合 schema 的帧都会被拒绝。

**Q20：OpenClaw 中 `tools.exec.host` 的路由逻辑是怎样的？** A： `tools.exec.host` 默认值为 `sandbox` ，这是一个 **路由偏好** 而非硬要求。实际行为：如果当前 session 的 sandbox runtime 已激活，exec 在沙箱中运行；如果 sandbox 未激活（ `sandbox.mode = off` ），exec 回退到 Gateway 宿主上直接运行。隐式 exec（工具调用中不指定 host）遵循相同逻辑。

---

### 六、Multi-Agent 与协议标准化

2026 年面试新热点： **MCP 和 A2A 协议** 。

### \- MCP（Model Context Protocol）

![](https://picx.zhimg.com/v2-f611b4d2a7a4099dfb92967110f65f21_1440w.jpg)

由 Anthropic 提出的 **通用适配器协议** ，标准化 Agent 与工具/数据源的连接方式。

核心价值：以前每接一个新工具都要写定制连接器，有了 MCP 就像 USB 接口——即插即用。

### \- A2A（Agent-to-Agent Protocol）

![](https://pic2.zhimg.com/v2-3cea73206119cd56b8b3301f9c64a68f_1440w.jpg)

由 Google 发起、Linux [基金会](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E5%9F%BA%E9%87%91%E4%BC%9A&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLln7rph5HkvJoiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.zrF4ONTnstXVfxW-4TSf70tvYe3-347sSQqqlRDC9pY&zhida_source=entity) 托管的 **Agent 间通信协议** ，让不同 Agent 能安全、高效地协作。

### 两者的关系

| 协议 | 解决什么问题 | 类比 |
| --- | --- | --- |
| MCP | Agent 怎么连接工具和数据 | USB 接口 |
| A2A | Agent 之间怎么协作 | HTTP 协议 |

> 面试话术：”MCP 管的是 Agent 和外部世界的交互，A2A 管的是 Agent 之间的团队协作。一个对外，一个对内，两者互补而非替代。”

### 第六章 Q&A（20 题，难度递增）

**基础级（Q1-Q5）**

**Q1：MCP 和 A2A 分别是什么？** A： **MCP** （Model Context Protocol）由 Anthropic 提出，标准化 Agent 与工具/数据源的连接。 **A2A** （Agent-to-Agent Protocol）由 Google 发起、Linux 基金会托管，标准化 Agent 之间的协作通信。

**Q2：MCP 和 A2A 是替代关系还是互补关系？** A：互补关系。MCP 解决 Agent 如何连接外部工具（对外），A2A 解决 Agent 之间如何协作（对内）。生产级系统通常两者都用。

**Q3：什么是 Multi-Agent 系统？** A：多个独立的 Agent 协作完成任务的系统。每个 Agent 有自己的专长（如一个负责搜索、一个负责写作、一个负责代码），通过协议通信和协调。

**Q4：Gartner 对 Multi-Agent 系统有什么预测？** A：预测到 2026 年，几乎每个商业应用都会有 AI 助手，其中 40% 会在次年集成任务特定的 Agent。

**Q5：用一个类比解释 MCP。** A：MCP 就像 USB 接口——以前每个外设（键盘、鼠标、打印机）都有自己的专用接口，USB 统一了它们。MCP 让每个工具提供商只需实现一个标准接口，所有 Agent 都能即插即用。

**进阶级（Q6-Q10）**

**Q6：OpenClaw 如何实现 Multi-Agent？** A：OpenClaw 支持在 **一个 Gateway 进程中运行多个隔离的 Agent** 。每个 Agent 有独立的 Workspace、Agent Dir、Session Store 和 Auth Profile。通过 `bindings` 配置将入站消息路由到特定 Agent。

**Q7：OpenClaw Multi-Agent 中，Agent 之间如何隔离？** A：完全隔离：(1) 独立 Workspace（文件系统、AGENTS.md/SOUL.md）；(2) 独立 Auth Profile（ `~/.openclaw/agents//agent/auth-profiles.json` ）；(3) 独立 Session Store；(4) 独立 Skills（workspace `skills/` ）。Main agent 凭证不自动共享。

**Q8：OpenClaw 能否让一个 WhatsApp 号码服务多个人？** A：可以。通过 DM split — 匹配发送者的 E.164 号码（如 `+15551234567` ）和 `peer.kind: "direct"` 将不同用户的私信路由到不同 Agent。但回复仍从同一个 WhatsApp 号码发出。

**Q9：2026 年有哪些主要的 AI Agent 协议？** A：五大协议：(1) **MCP** — Agent-Tool 连接；(2) **A2A** — Agent-Agent 协作；(3) **ACP** （Agent Communication Protocol）— 另一种 Agent 通信标准；(4) **WebMCP** — Web 环境下的 MCP 扩展；(5) **OpenAPI/Swagger** — 传统 API 描述标准。

**Q10：Multi-Agent 系统的常见 [架构模式](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E6%9E%B6%E6%9E%84%E6%A8%A1%E5%BC%8F&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLmnrbmnoTmqKHlvI8iLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.Sl-lL_4Ssm9j78wyfNt-Y5NV-TeOXFzh1Rd8BP0lZmo&zhida_source=entity) 有哪些？** A：(1) **Supervisor** — 中央调度器分配任务给 worker agents；(2) **Peer-to-peer** — Agent 之间平等协作；(3) **Hierarchical** — 多层级的 supervisor 树；(4) **Swarm** — 动态组队，按需加入和退出。

**高级（Q11-Q15）**

**Q11：OpenClaw Multi-Agent 路由的 `bindings` 配置如何工作？** A：Bindings 定义入站消息的路由规则——匹配条件（channel、account、peer 等）映射到 `agentId` 。支持按发送者号码、群组 ID、通道类型等条件路由。使用 `openclaw agents add` 创建 Agent， `openclaw agents list --bindings` 查看 [路由表](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E8%B7%AF%E7%94%B1%E8%A1%A8&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLot6_nlLHooagiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.ab4dz1p5GHsybrdpaN5vLrEo0r-ruB-dwxhEWeuspOo&zhida_source=entity) 。

**Q12：MCP 的 Server/Client 模型是怎样的？** A： **MCP Server** 由工具提供商实现，暴露工具定义（name/description/schema）和执行端点。 **MCP Client** 集成在 Agent 中，负责发现可用 Server、发送调用请求、接收结果。通信通过标准化的 JSON-RPC 协议。

**Q13：Multi-Agent 系统面临哪些核心挑战？** A：(1) **协调开销** — Agent 间通信消耗时间和 token；(2) **一致性** — 多 Agent 共享状态时的冲突；(3) **故障传播** — 一个 Agent 故障影响整体；(4) **安全边界** — Agent 间的信任和权限管理；(5) **[可观测性](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E5%8F%AF%E8%A7%82%E6%B5%8B%E6%80%A7&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLlj6_op4LmtYvmgKciLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.sy1LZn4peX7SX4b2_slrB0nOJxC_Vhmz16YFONjO68s&zhida_source=entity)** — 调试分布式 Agent 行为困难。

**Q14：OpenClaw 的 ACP（Agent Communication Protocol）集成是什么？** A：根据仓库中的 `docs.acp.md` 和 `extensions/acpx/` ，OpenClaw 实现了 ACP 扩展——允许 OpenClaw Agent 与外部 ACP 兼容的 Agent 进行标准化通信。代码包含 config、runtime、service、JSON-RPC 和事件处理等模块。

**Q15：如何选择 Supervisor 模式还是 Peer-to-peer 模式？** A： **Supervisor** 适合：任务分工明确、需要中央协调、结果需要汇总的场景。 **Peer-to-peer** 适合：Agent 能力对等、需要灵活协商、去中心化容错的场景。实际上，很多系统混合使用——高层用 Supervisor 分配，底层 worker 之间 Peer-to-peer 协作。

**源码级（Q16-Q20）**

**Q16：OpenClaw 中创建新 Agent 的完整流程是什么？** A：(1) `openclaw agents add` — 创建独立 workspace 和 agent dir；(2) 在配置文件 `agents.list` 中添加 agent 定义；(3) 创建通道账号（每个 Agent 独立的 Discord bot / Telegram bot）；(4) 在 `bindings` 中配置路由规则；(5) `openclaw gateway restart` 重启；(6) `openclaw agents list --bindings` 和 `openclaw channels status --probe` 验证。

**Q17：OpenClaw Multi-Agent 中，Agent Dir 存储什么？为什么不能跨 Agent 共享？** A：Agent Dir（ `~/.openclaw/agents//agent` ）存储 auth profiles（API 密钥和凭证）、model registry 和 per-agent 配置。不能共享因为会导致 **auth/session 冲突** ——多个 Agent 使用同一份凭证会互相覆盖会话状态。

**Q18：OpenClaw 的 `acpx` extension 包含哪些核心模块？** A：根据仓库 `extensions/acpx/` 目录： `config.ts` （ [配置管理](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E9%85%8D%E7%BD%AE%E7%AE%A1%E7%90%86&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLphY3nva7nrqHnkIYiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.edFrzz3ksKEPGlsRus_wsfD-mCUoZOL7ax2d8jQGo58&zhida_source=entity) ）、 `ensure.ts` （依赖检查）、 `runtime.ts` （运行时）、 `service.ts` （服务注册）。 `runtime-internals/` 下有 `control-errors.ts` （错误控制）、 `events.ts` （事件系统）、 `jsonrpc.ts` （JSON-RPC 通信）、 `process.ts` （进程管理）、 `shared.ts` （共享工具）。

**Q19：OpenClaw 的 Pairing 认证在 Multi-Agent 场景中如何工作？** A：每个 WS 客户端（operators + nodes）在 `connect` 时包含 **device identity** 。新设备 ID 需要 pairing approval，Gateway 签发 **device token** 供后续连接使用。Local connects（loopback 或 Gateway 本机 tailnet 地址）可自动 approve。Non-local connects 仍需显式 approval。Gateway auth 适用于所有连接，无论 local 还是 remote。

**Q20：OpenClaw 的 Operator Trust Model 如何影响 Multi-Agent 安全？** A：OpenClaw **不将** 一个 Gateway 建模为 [多租户](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E5%A4%9A%E7%A7%9F%E6%88%B7&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLlpJrnp5_miLciLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.hTv2XH8nUzVgq8d1nGQSv28sKZqTCUyXmVZiIGRsQwc&zhida_source=entity) 的对抗性用户边界。认证过的 Gateway 调用者被视为该 Gateway 实例的 **可信操作者** 。Session ID 是路由控制而非用户级授权边界。推荐模式：一个用户一台机器/VPS，一个 Gateway，多个 Agent。多用户需求应使用独立的 VPS 或 OS 用户边界隔离。

---

### 七、OpenClaw vs 其他框架：面试对比题

| 维度 | OpenClaw | LangChain | AutoGPT |
| --- | --- | --- | --- |
| 定位 | 开箱即用的 Agent 应用 | AI 应用开发积木 | 自主 Agent 实验项目 |
| 上手难度 | 低（消息平台直接用） | 中（需要编程） | 高（配置复杂） |
| 灵活性 | 中（预设架构） | 高（高度可定制） | 低（固定流程） |
| 多平台支持 | 原生支持 20+ 平台 | 需自行构建界面 | 无内置界面 |
| 适合场景 | 个人 AI 助手、快速原型 | 企业级 RAG、复杂流水线 | [概念验证](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E6%A6%82%E5%BF%B5%E9%AA%8C%E8%AF%81&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLmpoLlv7Xpqozor4EiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.TBZI20Go9f2xF45-EJtfnkuejDvldLobzijLJaiupro&zhida_source=entity) 、学术研究 |

> 高分回答：”选框架看需求——个人用选 OpenClaw，企业开发选 LangChain/LangGraph，验证想法选 AutoGPT。OpenClaw 的差异化在于’执行优先’——它不是让你搭积木，而是直接给你一个能干活的数字员工。”

### 第七章 Q&A（20 题，难度递增）

**基础级（Q1-Q5）**

**Q1：OpenClaw、LangChain、AutoGPT 三者的定位有什么区别？** A：OpenClaw = 开箱即用的 Agent 应用；LangChain = AI 应用的开发框架/积木；AutoGPT = 自主 Agent 的实验性概念验证。

**Q2：什么场景选 OpenClaw？什么场景选 LangChain？** A： **OpenClaw** ：个人 AI 助手、快速原型、消息平台集成、不想写太多代码。 **LangChain/LangGraph** ：企业级 RAG 系统、复杂 AI 流水线、需要高度定制的生产应用。

**Q3：OpenClaw 相比 LangChain 的最大优势是什么？** A： **开箱即用的多平台消息集成** ——LangChain 需要自己构建 UI（Streamlit、React），OpenClaw 原生支持 20+ 消息平台。

**Q4：AutoGPT 为什么更适合概念验证而非生产环境？** A：AutoGPT 的问题：(1) 推理成本高；(2) 稳定性不足；(3) 缺乏生产级的错误处理和监控；(4) 固定的执行流程缺少灵活性。

**Q5：OpenClaw 的上手门槛有多低？** A：最低只需：安装 Node.js 22 -> `npm install -g openclaw` -> `openclaw onboard` -> 用消息平台和它对话。不需要写代码。

**进阶级（Q6-Q10）**

**Q6：LangGraph 和 OpenClaw 的架构理念有什么本质区别？** A： **LangGraph** 是 [状态机](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E7%8A%B6%E6%80%81%E6%9C%BA&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLnirbmgIHmnLoiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.L_JdH6UiX13fXCXhrBJnt6a25udhb162SFxV2BWLuQc&zhida_source=entity) 驱动——开发者定义 nodes 和 edges 构成有向图，精确控制执行流。 **OpenClaw** 是 Agent 运行时驱动——预设了 Gateway/Brain/Memory/Skills 架构，开发者通过配置和 Skills 定制行为。LangGraph 更灵活但需要更多编程，OpenClaw 更易用但架构较固定。

**Q7：在选型中，”本地优先”和”云优先”各有什么利弊？** A： **本地优先** （OpenClaw）：数据隐私强、无云依赖、离线可用；但需自己维护基础设施、水平扩展困难。 **云优先** （许多 LangChain 部署）：易扩展、自动运维；但数据隐私风险、依赖网络、持续成本。

**Q8：OpenClaw 的 Skills 系统和 LangChain 的 Tools 有什么区别？** A：OpenClaw Skills 是 **自然语言提示词模板** （Markdown），教 Agent “怎么做某事”；LangChain Tools 是 **代码级接口定义** （Python 函数 + schema），定义”能做什么”。Skills 更像”SOP 手册”，Tools 更像”API 文档”。

**Q9：CrewAI 和 OpenClaw 在 Multi-Agent 方面有什么区别？** A： **CrewAI** 专注于多 Agent 编排——定义 agents、tasks、crew 来协调复杂工作流。 **OpenClaw** 的 Multi-Agent 更偏向基础设施——多个隔离的 Agent 实例共享一个 Gateway，通过 bindings 路由。CrewAI 更适合复杂协作编排，OpenClaw 更适合多人格/多身份的个人助手。

**Q10：2026 年 Agent 框架的发展趋势是什么？** A：三大趋势：(1) **协议标准化** — MCP/A2A 成为基础设施层；(2) **执行优先** — 从”会说话的 AI”到”会干活的 AI”；(3) **本地+云混合** — 敏感数据本地处理，计算密集任务上云。

**高级（Q11-Q15）**

**Q11：如果要为一个企业构建 Agent 系统，你会选择什么技术栈？为什么？** A：推荐分层方案： **基础设施层** — MCP/A2A 协议； **开发框架** — LangGraph（状态管理、复杂流程）； **记忆层** — 向量数据库（Milvus/Pinecone）+ 关系型数据库； **[接入层](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E6%8E%A5%E5%85%A5%E5%B1%82&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLmjqXlhaXlsYIiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.FRpsBUxKGBSN2aXteNu_w5y15kpaRC8Tr9IgNqbORBE&zhida_source=entity)** — 如果需要消息平台集成可考虑 OpenClaw 的 Gateway 架构设计； **监控层** — LangSmith / Langfuse。选择理由：企业需要可控的执行流、 [审计能力](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E5%AE%A1%E8%AE%A1%E8%83%BD%E5%8A%9B&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLlrqHorqHog73lipsiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.OEgffHR19ke9V4TEU-prg3z_fmklw-GCVgvI9j22Iwc&zhida_source=entity) 和水平扩展。

**Q12：OpenClaw 的 Companion App 策略和其他框架有什么区别？** A：OpenClaw 是唯一提供 **原生 macOS/iOS/Android App** 的开源 Agent 框架。这些 App 作为 Node 角色连接 Gateway，提供设备级能力（摄像头、位置、屏幕录制）。其他框架（LangChain、AutoGPT）通常只有 Web UI 或 CLI。

**Q13：OpenClaw 的 Plugin 系统和 LangChain 的 Extension 生态有什么区别？** A：OpenClaw 的核心 [设计理念](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E8%AE%BE%E8%AE%A1%E7%90%86%E5%BF%B5&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLorr7orqHnkIblv7UiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.ZOQkoI3KYxEDD0uHKhXZTwbqMaoM9yGnvvT23354SzI&zhida_source=entity) 是”Core stays lean”——核心精简，能力通过 npm package 形式的 plugin 扩展，plugin 进入核心的门槛刻意设得很高。LangChain 则是”batteries included”——提供大量内置集成。OpenClaw 更类似 Unix 哲学，LangChain 更类似全家桶。

**Q14：如何评估 Agent 框架的”生产就绪度”？** A：六个维度：(1) **错误处理** — 异常恢复和降级策略；(2) **可观测性** — 日志、指标、追踪；(3) **安全性** — 沙箱、权限控制、审计；(4) **可扩展性** — 水平扩展能力；(5) **成本控制** — token 用量监控和优化；(6) **社区活跃度** — Issue 响应速度、贡献者数量。

**Q15：OpenClaw 的 Canvas/A2UI 是什么？其他框架有类似功能吗？** A：Canvas 是 OpenClaw 的 **Agent 驱动的 [可视化](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E5%8F%AF%E8%A7%86%E5%8C%96&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLlj6_op4bljJYiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.Z-SOesFg8rW8CTPAtAlD28Hc8nudbNWzeHGZ7hkfJkQ&zhida_source=entity) 工作区** ——Agent 可以生成和编辑 HTML/CSS/JS 页面，通过 Gateway HTTP 服务器提供服务。A2UI 是 Agent-to-UI 的 [交互模式](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E4%BA%A4%E4%BA%92%E6%A8%A1%E5%BC%8F&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLkuqTkupLmqKHlvI8iLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.IC9qmD2WcYRMrH6uXLQEO-agWjVqKSCGnSWbx2p57CU&zhida_source=entity) 。这在开源 Agent 框架中比较独特，Claude Artifacts 有类似概念但不开源。

**源码级（Q16-Q20）**

**Q16：OpenClaw 的 Extensions 目录中有哪些消息通道实现？** A：根据仓库 `extensions/` 目录： `discord/` （Discord bot）、 `feishu/` （飞书，含文档/表格/通讯录操作）、 `bluebubbles/` （iMessage 集成）、 `slack/` （Slack Bot）。每个 extension 包含 `index.ts` （入口）、 `src/channel.ts` （通道逻辑）、 `src/runtime.ts` （运行时）等模块。

**Q17：OpenClaw 的飞书 Extension 提供了哪些能力？** A：根据 `extensions/feishu/src/` 的 [文件结构](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E6%96%87%E4%BB%B6%E7%BB%93%E6%9E%84&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLmlofku7bnu5PmnoQiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.NIUMKAFP0OQztWXiwi_8kPBQ2SnpYh0_pCOXSV6CSEs&zhida_source=entity) ，能力包括： `docx.ts` （文档操作，含批量插入、表格、彩色文本）、 `drive.ts` （网盘操作）、 `bitable.ts` （多维表格）、 `directory.ts` （通讯录）、 `chat.ts` （群聊管理）、 `card-action.ts` （卡片交互）、 `dynamic-agent.ts` （动态 Agent）。

**Q18：OpenClaw 的 Swabble 模块是什么？用 Swift 写有什么原因？** A：Swabble 是 OpenClaw 的 **语音唤醒和语音输入** 模块，用 Swift 编写。原因：(1) 需要直接调用 macOS/iOS 的系统语音 API（SFSpeechRecognizer）；(2) 需要低延迟的音频处理；(3) Swift 是 Apple 生态的一等公民。包含 WakeWordGate（唤醒词检测）、SpeechPipeline（语音管道）等组件。

**Q19：OpenClaw 的 CI/CD 流水线包含哪些检查？** A：根据 `.github/workflows/` ： `ci.yml` （主 CI 检查）、 `docker-release.yml` （Docker 镜像发布）、 `install-smoke.yml` （安装冒烟测试）、 `sandbox-common-smoke.yml` （沙箱冒烟测试）、 `stale.yml` （过期 Issue 清理）、 `labeler.yml` （自动标签）、 `auto-response.yml` （自动回复）、 `workflow-sanity.yml` （工作流健康检查）。

**Q20：OpenClaw 的 CONTRIBUTING.md 有哪些关键规则？** A：(1) 一个 PR = 一个 Issue/话题，不捆绑不相关的修改；(2) 超过约 5000 行改动的 PR 仅在特殊情况下审查；(3) 不要同时开大量小 PR（每个 PR 有审查成本）；(4) 很小的相关修复可以合并到一个 PR 中。

---

### 八、安全与 Guardrails：容易被忽略的加分项

OpenClaw 这类自主 Agent 的安全问题，是 2026 年面试的 **新考点** 。

### 核心风险

1. **Prompt Injection（提示注入）** ：攻击者在邮件、网页中嵌入恶意指令，Agent 可能被”劫持”
2. **权限过大** ：Agent 拥有 shell、文件系统、甚至 root 权限，一旦被利用，爆炸半径极大
3. **[数据泄露](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E6%B3%84%E9%9C%B2&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLmlbDmja7ms4TpnLIiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.rU5fX5VZbxu3_PwfiwbXXUjtqyl3e80TGM-nBXcc_QI&zhida_source=entity)** ：Agent 跨平台读取信息，可能被诱导将敏感数据发到公开渠道

CrowdStrike 的安全报告指出：OpenClaw 的自主执行能力将 prompt injection 从 **数据泄露风险** 升级为 **全面入侵风险** ——”爆炸半径延伸到 Agent 能触达的每一个系统”。

### 防御措施

- **权限最小化** ：限制 Agent 的文件系统和网络访问范围
- **Pairing 认证** ：OpenClaw 默认要求未知发送者提供配对码
- **Guardrails（护栏）** ：输入输出过滤、幻觉检测、Groundedness 检查
- **CoVe（Chain of Verification）** ：让模型自验证答案，减少幻觉

### 第八章 Q&A（20 题，难度递增）

**基础级（Q1-Q5）**

**Q1：Agent 面临的三大核心安全风险是什么？** A：(1) **Prompt Injection** — 恶意指令注入劫持 Agent；(2) **权限过大** — Agent 拥有的系统权限被滥用；(3) **数据泄露** — 敏感信息被诱导发送到不安全的渠道。

**Q2：什么是 Prompt Injection？为什么对 Agent 特别危险？** A：Prompt Injection 是在输入中嵌入恶意指令来操纵 LLM 行为。对 Agent 特别危险因为 Agent 不仅能”说”还能”做”——被注入后可能执行恶意命令、发送数据、修改文件。

**Q3：直接注入和间接注入有什么区别？** A： **直接注入** — 攻击者直接向 Agent 发送恶意 prompt。 **间接注入** — 攻击者在邮件、网页等数据源中嵌入恶意指令，Agent 在处理这些数据时被”感染”。间接注入更隐蔽更危险。

**Q4：什么是 Guardrails（护栏）？** A：Guardrails 是对 AI 系统输入和输出的 [安全控制](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E5%AE%89%E5%85%A8%E6%8E%A7%E5%88%B6&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLlronlhajmjqfliLYiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.sUVMMxv5P1S3QHY8woV3NGzfewR8GoGslbAIUFXimQk&zhida_source=entity) 机制，包括内容过滤、幻觉检测、行为边界限制等，目的是确保 Agent 在安全范围内运行。

**Q5：什么是 Groundedness 检查？** A：将模型输出与可信数据源进行对比，验证回答是否有事实依据。如果回答不被可信来源支持，则标记为 “ungrounded”，由 [应用层](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E5%BA%94%E7%94%A8%E5%B1%82&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLlupTnlKjlsYIiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.-Ps1Jhc2smeRGH3oM6T94QDj7Am2rQeM6zBPd6wXi50&zhida_source=entity) 决定是否阻止或修正。

**进阶级（Q6-Q10）**

**Q6：OpenClaw 有哪些内置安全机制？** A：(1) **Pairing 认证** — 未知发送者需要配对码；(2) **设备身份绑定** — v3 签名绑定 platform + deviceFamily；(3) **Gateway Token** — 可选的连接认证；(4) **沙箱模式** — 隔离执行环境；(5) **工具权限策略** — tool policy 控制工具可用性。

**Q7：OpenClaw 的 Pairing 机制如何工作？** A：所有 WS 客户端在 connect 时提供 device identity。新设备需要 pairing approval，Gateway 签发 device token。Local 连接（loopback）可自动 approve，非 local 连接需要显式 approval。connect 帧必须签名 challenge nonce。

**Q8：什么是 Chain of Verification (CoVe)？** A：让模型在输出答案后， **自己生成验证问题来检查答案的正确性** 。如果自验证发现不一致，则修正答案。这是一种减少幻觉的自检机制。

**Q9：Agent 安全中的”爆炸半径”概念是什么？** A：指一次安全事件能影响的最大范围。对于 OpenClaw 这类拥有 shell 权限和多平台连接的 Agent，一次成功的 prompt injection 的爆炸半径可以延伸到 Agent 能触达的 **所有系统和数据** 。

**Q10：如何实现 Agent 的权限最小化？** A：(1) 按任务分配最小必要权限；(2) 使用沙箱隔离高风险操作；(3) 对写操作和副作用操作要求确认；(4) 限制文件系统和网络访问范围；(5) 使用只读 workspace 运行非信任任务。

**高级（Q11-Q15）**

**Q11：OpenClaw 的 Sandbox 模式如何工作？** A：通过 `agents.defaults.sandbox` 配置启用。启用后，非主会话的 exec 操作在沙箱 workspace（ `~/.openclaw/sandboxes` ）中运行，而非宿主 workspace。Workspace 的 `workspaceAccess` 控制读写权限（ `rw` / `ro` / `none` ）。 `ro` 或 `none` 时 Memory Flush 也会被跳过。

**Q12：OpenClaw SECURITY.md 中定义的 Operator Trust Model 是什么？** A：核心原则：(1) 一个 Gateway 不被建模为多租户对抗性边界；(2) 认证的 Gateway 调用者是可信操作者；(3) Session ID 是路由控制，非授权边界；(4) 同一 Gateway 上不同操作者的数据可见性是预期行为；(5) 推荐一个用户一个 VPS/Gateway。

**Q13：OpenClaw 的安全报告需要包含哪些内容才能被快速处理？** A：根据 SECURITY.md 的 “Report Acceptance Gate”：(1) 精确的漏洞文件、函数和行号范围；(2) 测试版本信息；(3) 可复现的 PoC；(4) 影响证明（tied to 文档化的信任边界）；(5) 证明不依赖共享 Gateway 的对抗性操作者假设；(6) 范围说明。

**Q14：OpenClaw 列出的 “Common False-Positive Patterns” 有哪些？** A：(1) 仅 prompt injection 链但无边界突破；(2) 本地特性（TUI shell）被报告为远程注入；(3) 授权用户的本地操作被报告为提权；(4) 可信操作者安装的恶意 plugin 执行特权操作；(5) 假设共享 Gateway 上的多租户授权；(6) 仅检测差异但无实际绕过的 parity 报告。

**Q15：Red Teaming 在 Agent 安全中的作用是什么？** A：Red Teaming 是让安全专家模拟真实攻击来发现 Agent 的漏洞。NIST AI [风险管理](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E9%A3%8E%E9%99%A9%E7%AE%A1%E7%90%86&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLpo47pmannrqHnkIYiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.gxrcm8IjW0OiLULGZrV8RwPRr-6BRJopu5ASOMv692s&zhida_source=entity) 框架推荐这种方式：通过模拟真实世界的攻击 prompt 来测试系统防御，帮助改进 guardrails 并减少不安全或幻觉输出。

**源码级（Q16-Q20）**

**Q16：OpenClaw 的 Gateway 签名机制具体如何工作？** A：所有连接必须签名 `connect.challenge` nonce。v3 签名 payload 绑定 `platform` + `deviceFamily` 。Gateway 在 paired 设备重连时 pin 这些元数据，如果元数据变更则要求 repair pairing。这防止了设备身份冒充攻击。

**Q17：OpenClaw 的 DM 安全策略是什么？** A：默认 “pairing” 策略——未知发送者需要提供 approval code。可切换为 “open” 模式但需要 allowlist 配置。 `channels.whatsapp.allowFrom` 是强烈推荐设置的配置项，限制可交互的号码范围。

**Q18：OpenClaw 对 Archive/Install Extraction 攻击的安全态度是什么？** A：根据 SECURITY.md，如果攻击依赖在可信状态下 **预先配置** 本地文件系统（如在目标目录下植入 symlink/hardlink），但无法展示 **不可信路径来创建/控制该原语** ，则被视为 false positive 关闭。安全报告必须证明存在不可信的写入路径。

**Q19：OpenClaw 的 Exec 安全边界在哪里？** A：Exec 默认是 host-first（ `sandbox.mode = off` ）。即使 `tools.exec.host` 设为 `sandbox` ，如果 sandbox runtime 未激活，exec 仍在宿主上运行。这意味着默认情况下，Agent 的 exec 操作 **直接运行在宿主系统上** ——这是一个需要明确理解的信任决策。OpenClaw 的态度是”强默认不杀能力”，高权限路径要求操作者显式配置。

**Q20：OpenClaw 的安全报告处理中，什么是”boundary bypass”要求？** A：对于 command-risk/parity 类报告（如一条执行路径有混淆检测但另一条没有），OpenClaw 要求提供 **具体的边界绕过路径** ——必须证明能绕过 auth、approval、allowlist 或 sandbox 中的至少一个。仅展示检测差异（parity-only findings）被视为加固建议而非漏洞。

---

### 九、综合高频面试 Q&A 速记卡

**Q：AI Agent 和传统 Chatbot 的区别？** A：Chatbot 只做对话，Agent 有规划、记忆和工具调用能力，能 **自主完成多步骤任务** 。

**Q：什么是 Agentic AI？** A：具备自主性、反应性、主动性、社交能力和学习能力的 AI 系统。核心是从”回答问题”升级为”完成目标”。

**Q：OpenClaw 的记忆为什么用 Markdown 而不是数据库？** A：本地优先、人类可读、版本可控、无需额外基础设施。用户可以像维护文档一样维护 AI 的记忆。

**Q：ReAct 怎么减少幻觉？** A：通过 Action 步骤调用外部工具获取真实数据，Observation 步骤验证推理结果，形成 **事实-推理-验证** 的闭环。

**Q：如何处理 Agent 中竞争性目标？** A：使用 **层次化规划** （Hierarchical Planning），通过 Supervisor 或 Router [架构分析](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E6%9E%B6%E6%9E%84%E5%88%86%E6%9E%90&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLmnrbmnoTliIbmnpAiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.gGCaL_HklWMY6b3emL81GuMhOi1zIV-mpq4vvkGk6Z8&zhida_source=entity) 请求、拆解子目标、分配优先级。

**Q：2026 年 Agent 岗位的关键技能？** A：ReAct/CoT 等推理模式、MCP/A2A 协议、LangGraph 状态机、RAG 系统设计、 [云原生](https://zhida.zhihu.com/search?content_id=271099459&content_type=Article&match_order=1&q=%E4%BA%91%E5%8E%9F%E7%94%9F&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzY0MjMzNDUsInEiOiLkupHljp_nlJ8iLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzEwOTk0NTksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.uYBKpB-XxBUUHvfkUiRT4sZWKzUWFUkNn9WINfT2xVA&zhida_source=entity) 部署（K8s/Docker）、OpenClaw 部署和 Skills 开发。

**Q：Heartbeat 和 Cron 怎么选？** A：需要精确定时用 Cron，需要上下文感知的批量检查用 Heartbeat。最高效的方案是两者结合。

**Q：OpenClaw 的安全第一原则是什么？** A：根据 VISION.md：”Security is a deliberate tradeoff: strong defaults without killing capability”——在不损失能力的前提下，提供强安全默认值，高权限路径需操作者显式配置。

---

![](https://pic3.zhimg.com/v2-e23a95d2c10dc148a2f667f53994179e_1440w.jpg)

## 结语

AI Agent 这个赛道才刚刚开始。OpenClaw 用 270K Stars 证明了一件事： **人们不只想和 AI 聊天，更想让 AI 替自己干活** 。

这篇文章覆盖了 **8 大章节 x 20 道面试题 = 160+ 道** 从入门到源码级的面试 Q&A。理解了五组件架构、ReAct 循环、Function Calling、MCP/A2A 协议、安全防护——你就已经拿到了 Agent 面试的入场券。

但八股终究是八股。剩下的，是去 `git clone` OpenClaw 的仓库，读读 `docs/concepts/agent-loop.md` ，写几个 Skill，部署一个自己的 Agent——把八股文变成真本事。

关于 AI Agent，你最想深入了解哪个方向？评论区聊聊。

---

### 参考来源

1. [OpenClaw GitHub 仓库](https://link.zhihu.com/?target=https%3A//github.com/openclaw/openclaw) - GitHub
2. [OpenClaw: Complete Guide to the Open-Source AI Agent](https://link.zhihu.com/?target=https%3A//milvus.io/blog/openclaw-formerly-clawdbot-moltbot-explained-a-complete-guide-to-the-autonomous-ai-agent.md) - Milvus Blog
3. [OpenClaw Wikipedia](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/OpenClaw) - Wikipedia
4. [OpenClaw: Deploying an Open-Source AI Agent Framework](https://link.zhihu.com/?target=https%3A//medium.com/%40viplav.fauzdar/clawdbot-building-a-real-open-source-ai-agent-that-actually-acts-f5333f657284) - Medium
5. [How OpenClaw Works: Understanding AI Agents Through a Real Architecture](https://link.zhihu.com/?target=https%3A//bibek-poudel.medium.com/how-openclaw-works-understanding-ai-agents-through-a-real-architecture-5d59cc7a4764) - Medium
6. [OpenClaw Explained: How the Hottest Agent Framework Works](https://link.zhihu.com/?target=https%3A//medium.com/%40cenrunzhe/openclaw-explained-how-the-hottest-agent-framework-works-and-why-data-teams-should-pay-attention-69b41a033ca6) - Medium
7. [What Security Teams Need to Know About OpenClaw](https://link.zhihu.com/?target=https%3A//www.crowdstrike.com/en-us/blog/what-security-teams-need-to-know-about-openclaw-ai-super-agent/) - CrowdStrike
8. [OpenClaw AI Agent Masterclass](https://link.zhihu.com/?target=https%3A//hellopm.co/openclaw-ai-agent-masterclass/) - HelloPM
9. [OpenClaw: Ultimate Guide to AI Agent Workforce 2026](https://link.zhihu.com/?target=https%3A//o-mega.ai/articles/openclaw-creating-the-ai-agent-workforce-ultimate-guide-2026) - o-mega
10. [大模型-Agent 面试八股文，简单背一背 (入门级)](https://zhuanlan.zhihu.com/p/30772276091) - 知乎
11. [OpenClaw 智能体](https://zhuanlan.zhihu.com/p/2004854211494560631) - 知乎
12. [OpenClaw 最强军火库：精选 2868 个 skills](https://zhuanlan.zhihu.com/p/2010926090475045346) - 知乎
13. [2026年做 Agents 应该看这篇全面的技术综述](https://link.zhihu.com/?target=https%3A//blog.csdn.net/fogdragon/article/details/158177156) - CSDN
14. [2026 AI Agent 工程化圣经](https://link.zhihu.com/?target=https%3A//blog.csdn.net/u013970991/article/details/158128253) - CSDN
15. [OpenClaw 2026 终极指南](https://link.zhihu.com/?target=https%3A//blog.csdn.net/gongjisuanli/article/details/158617411) - CSDN
16. [AI Agent 简介](https://link.zhihu.com/?target=https%3A//www.runoob.com/ai-agent/ai-agent-intro.html) - 菜鸟教程
17. [AI Agent万字长文总结：规划, 工具, 执行, 记忆](https://link.zhihu.com/?target=https%3A//www.53ai.com/news/qianyanjishu/1092.html) - 53AI
18. [开发者欢呼，普通人迷茫：OpenClaw之后](https://link.zhihu.com/?target=https%3A//www.infoq.cn/article/Br5brKyveOf15uEgOzvX) - InfoQ
19. [上海一群青年，造了个学术版OpenClaw](https://link.zhihu.com/?target=https%3A//www.qbitai.com/2026/03/383249.html) - 量子位
20. [OpenClaw 平替产品全景对比](https://link.zhihu.com/?target=https%3A//www.53ai.com/news/Openclaw/2026030306512.html) - 53AI
21. [25 Advanced Agentic AI Interview Questions for 2026](https://link.zhihu.com/?target=https%3A//aemonline.net/blog/25-advanced-agentic-ai-interview-questions-for-2026-with-answer-updated-february-2026/) - AEM Institute
22. [30 Agentic AI Interview Questions and Answers](https://link.zhihu.com/?target=https%3A//www.analyticsvidhya.com/blog/2026/02/agentic-ai-interview-questions-and-answers/) - Analytics Vidhya
23. [Top Agentic AI Interview Questions and Answers](https://link.zhihu.com/?target=https%3A//www.geeksforgeeks.org/artificial-intelligence/top-agentic-ai-interview-questions-and-answers/) - GeeksforGeeks
24. [10 Essential Agentic AI Interview Questions](https://link.zhihu.com/?target=https%3A//www.kdnuggets.com/10-essential-agentic-ai-interview-questions-for-ai-engineers) - KDnuggets
25. [Top 30 Agentic AI Interview Questions](https://link.zhihu.com/?target=https%3A//www.datacamp.com/blog/agentic-ai-interview-questions) - DataCamp
26. [Function Calling with LLMs](https://link.zhihu.com/?target=https%3A//www.promptingguide.ai/applications/function_calling) - Prompt Engineering Guide
27. [Tool Calling Explained: The Core of AI Agents](https://link.zhihu.com/?target=https%3A//composio.dev/blog/ai-agent-tool-calling-guide) - Composio
28. [ReAct 框架](https://link.zhihu.com/?target=https%3A//www.promptingguide.ai/zh/techniques/react) - Prompt Engineering Guide
29. [大模型Agent之ReAct核心原理解析](https://zhuanlan.zhihu.com/p/690358498) - 知乎
30. [Agent 的九种设计模式](https://link.zhihu.com/?target=https%3A//www.53ai.com/news/qianyanjishu/913.html) - 53AI
31. [MCP vs A2A: Protocols for Multi-Agent Collaboration 2026](https://link.zhihu.com/?target=https%3A//onereach.ai/blog/guide-choosing-mcp-vs-a2a-protocols/) - OneReach
32. [What Is Agent2Agent (A2A) Protocol?](https://link.zhihu.com/?target=https%3A//www.ibm.com/think/topics/agent2agent-protocol) - IBM
33. [Top AI Agent Protocols in 2026](https://link.zhihu.com/?target=https%3A//getstream.io/blog/ai-agent-protocols/) - GetStream
34. [OpenClaw vs LangChain: 2026 Agent Framework Comparison](https://link.zhihu.com/?target=https%3A//fast.io/resources/openclaw-vs-langchain/) - Fast.io
35. [Memory - OpenClaw](https://link.zhihu.com/?target=https%3A//docs.openclaw.ai/concepts/memory) - OpenClaw Docs
36. [OpenClaw Permanent Memory System](https://link.zhihu.com/?target=https%3A//openclawapi.org/en/blog/2026-02-22-openclaw-permanent-memory-system) - OpenClaw API
37. [What are OpenClaw Skills? A 2026 Developer’s Guide](https://link.zhihu.com/?target=https%3A//www.digitalocean.com/resources/articles/what-are-openclaw-skills) - DigitalOcean
38. [Gateway Architecture - OpenClaw](https://link.zhihu.com/?target=https%3A//docs.openclaw.ai/concepts/architecture) - OpenClaw Docs
39. [AI Agent Architecture with Diagrams](https://link.zhihu.com/?target=https%3A//www.designveloper.com/blog/ai-agent-architecture-diagram/) - Designveloper
40. [OpenClaw Deconstructed: A Visual Architecture Guide](https://link.zhihu.com/?target=https%3A//www.globalbuilders.club/blog/openclaw-architecture-visual-guide) - Global Builders Club

---

如果你觉得本文对你有帮助，记得点赞👍收藏、一键三连🙏。你的肯定是我持续创作最大的动力～

更多问题，请评论区讨论！

（文章结束）

编辑于 2026-03-07 09:25・美国[OpenClaw](https://www.zhihu.com/topic/1999063153082913027)[面试八股文](https://www.zhihu.com/topic/27801935)[AI-Agent](https://www.zhihu.com/topic/30639237)