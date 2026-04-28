---
project: 2026-04-kaigao
status: active
created: 2026-04-28
updated: 2026-04-28
---

# 2026-04 KaiGao · 项目简报

> 本文件定义"这次工作做完长什么样"。启动时先填背景 / 目标 / 交付物，之后随认知变化增量更新。

## 背景

**外部代码仓**：`/Users/zhouyangdong/Documents/projects/kaigao`

从该仓库的 `CLAUDE.md` 摘取的事实：

- **产品形态**：AI 论文写作助手，帮用户生成论文大纲和全文
- **技术栈**：Next.js 15 + Hono + SQLite (Drizzle) + Redis/BullMQ + 阿里云 OSS + Turborepo + 阿里云 SAE
- **已有基础设施约束**：BullMQ 入队必须用 `enqueueWithTrace`；Drizzle migration 只能通过 `pnpm db:generate`；默认开发分支 `feature-dev`

**本 llm-wiki 项目的定位**：不是替代 kaigao 代码仓自己的文档，而是作为**"这段时间围绕 kaigao 做的工作"的知识与产出管理台**。代码在代码仓，思考/资料/复盘在这里。

## 目标

> 待用户填写。示例方向（需确认）：
>
> 1. 支持某个里程碑式功能上线（写出完整规格 + 联调记录 + 复盘）
> 2. 围绕 kaigao 做一次架构/产品/质量的整理输出
> 3. 收集用户反馈并整理需求 backlog
> 4. ……

## 非目标

> 待用户填写（明确**不做**什么，防止范围蔓延）。

## 范围

> 待用户填写（工作内容的边界，例如"仅覆盖 prompt 优化相关模块"）。

## 交付物

> 启动时列出可验证的产出清单，过程中勾选。

- [ ] （待补）
- [ ] （待补）

## 里程碑

- [ ] （待补）— 预计 {日期}

## 风险 / 未知

- 项目阶段性目标尚未与用户对齐，需在首次讨论后补齐目标 / 非目标 / 交付物三节
- 外部代码仓有自己的 `CLAUDE.md`、`AGENTS.md`、`openspec/`，避免在本 wiki 侧重复产出已在代码仓沉淀的内容（防止双份事实）
