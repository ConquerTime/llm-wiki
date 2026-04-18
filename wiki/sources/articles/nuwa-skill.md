---
title: "nuwa-skill（女娲·Skill造人术）"
type: source
subtype: article
tags: [thinking-distillation, mind-model, ai-skill, claude-code, multi-agent]
created: 2026-04-16
updated: 2026-04-16
author: 花叔 (alchaincyf)
url: https://github.com/alchaincyf/nuwa-skill
date: 2026-04
sources:
  - ../../raw/articles/nuwa-skill-github.md
---

# nuwa-skill（女娲·Skill造人术）

> 提炼任何人的思维框架（心智模型、决策启发式、表达DNA、价值观、反模式）为可运行的 Claude Code Skill，11.3K Stars，MIT 协议。

## 核心论点

女娲系统的目标是**提炼思维框架而非复制人物**。通过结构化多源调研和三重验证，将个人/专家的认知操作系统转化为自包含、可分发的 AI Skill。其关键创新是在人物 Skill 中引入 Agentic 回答工作流（先研究、再回答），使 Skill 从「鹦鹉学舌」升级为「可靠思维顾问」。

## 关键要点

1. **五层认知提取**：表达DNA → 心智模型 → 决策启发式 → 价值观/反模式 → 诚实边界
2. **六路并行调研**：著作、对话、表达、他者评价、决策记录、时间线——6个 Agent 并行采集
3. **三重验证机制**：跨域复现（≥2领域出现）、生成力（能推断新立场）、排他性（非通用常识）
4. **Agentic 回答工作流**：问题分类 → 人物式研究（联网查事实）→ 人物式回答——不凭训练数据编造
5. **双 Agent 精炼**：验证通过后由 optimizer + creator 两个 Agent 独立评审、交叉改进
6. **自包含分发**：所有调研存储在 Skill 目录内部，Skill 可独立分发
7. **增量更新**：更新已有 Skill 时只启动 3/6 个 Agent，增量修补
8. **信息源黑名单**：永不使用知乎、微信公众号、百度百科；中文仅接受权威媒体和一手视频/播客
9. **品味守则**：长文>金句、争议>共识、变化>固定
10. **预置 13+1 个 Skill**：Paul Graham、Elon Musk、Steve Jobs、Charlie Munger、Naval Ravikant、Andrej Karpathy 等

## 技术架构

五阶段流水线：

| 阶段 | 内容 | 关键机制 |
|------|------|----------|
| Phase 0 | 入口分流与需求澄清 | 直接路径 vs 诊断路径 |
| Phase 1 | 六路并行多源采集 | 6 Agent 并行，本地语料优先 |
| Phase 2 | 框架提炼 | 三重验证筛选心智模型 |
| Phase 3 | Skill 构建 | 标准 SKILL.md 模板 + Agentic 工作流 |
| Phase 4 | 质量验证 | 已知/边缘/风格三项独立测试 |
| Phase 5 | 双 Agent 精炼 | optimizer + creator 交叉评审 |

## 质量标准

- 心智模型 3-7 个，每个有来源证据和失效条件
- 表达DNA 读 100 字能认出是谁
- 诚实边界 ≥3 条具体局限
- 至少 2 对内在矛盾
- 一手来源占比 >50%

## 核心金句

> 「写不进去的那部分，才是你真正的护城河。但写得进去的部分，已经足够强大。」

> 「绝不做的事：编造未说过的话、包装通用道理、忽略负面评价、信息不足时强行生成。」

## 提到的实体

- [[../../entities/products/nuwa-skill|nuwa-skill]] — 本项目
- 花叔 (alchaincyf) — 独立 AI 开发者，项目作者
- colleague-skill (titanwings) — 灵感来源项目

## 提到的概念

- [[../../concepts/ai/ai-skills|AI Skills 生态]] — nuwa-skill 是 Skills 生态的代表性项目
- [[../../concepts/ai/ai-agent|AI Agent]] — 六路 Agent 并行调研 + 双 Agent 精炼是 Multi-Agent 实践
