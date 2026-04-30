# AI 家教技术架构萃取 · 活动日志

> 追加式时间线，记录讨论、决策、产出、阻塞。

---

## [2026-04-29] 启动
- 项目创建，目录初始化
- 与用户对齐：萃取 aitutor-backend 的 Agent 图设计（StateGraphLite / DefaultAgentMainGraph）、实时语音对话架构（ASR→LLM→TTS 流水线）、性能表现与评估策略（StateStore 迁移测试框架）
- 外部仓库：`/Users/zhouyangdong/Documents/projects/horizon/aitutor-backend`
- 已读取 docs/ 下两份文档（LLM响应处理流程、StateStore迁移集成测试框架）及核心 Java 源码

## [2026-04-29] 第一份 deliverable
- 产出：[[projects/2026-04-aitutor-arch/deliverables/arch-overview.md|arch-overview.md]]
- 补读：WaitbotSubgraph（WAIT_BOT shouldWait 判断）、GetLlmFlowableSubgraph（fastSlow/simple 路由分叉）、DefaultAgentGraphContext（context 继承链）、CompiledStateGraphLite.ExecutionSession（token 驱动 fan-in + ReentrantLock 并发模型）、AssistantType 9 种 bot 枚举
- 覆盖内容：模块拓扑、三大支柱、完整图拓扑（主图 + 3 个子图）、延迟优化清单、LLM 抽象层速览、后续 deliverable 路线
- 填补 brief 中的"风险/未知"：WaitbotSubgraph 的 shouldWait 逻辑（WAIT_BOT 返回 "true" 字符串）、StateGraphLite 并发模型（token 驱动 + ReentrantLock + 同 executor 回调）
- 剩余空白：TTS 供应商延迟数字、监控 p50/p99、COMPRESSION_BOT 挂载点

## [2026-04-29] 三大支柱深度文档
- 复制原文档到 notes/reference-docs/：LLM响应处理流程文档.md、LLM响应处理流程文档_confluence.txt、StateStore迁移集成测试框架—开发者手册.md
- 产出三份 deliverable：
  - [[projects/2026-04-aitutor-arch/deliverables/agent-graph-design.md|agent-graph-design.md]]（支柱 A：StateGraphLite 深度分析 + DefaultAgentMainGraph 完整图）
  - [[projects/2026-04-aitutor-arch/deliverables/voice-pipeline.md|voice-pipeline.md]]（支柱 B：ASR→LLM→TTS 全链路 + 打断/预测/字幕）
  - [[projects/2026-04-aitutor-arch/deliverables/evaluation-strategy.md|evaluation-strategy.md]]（支柱 C：StateStore 版本迁移 + 可回归测试框架）
- 补读：StateGraphLite（完整 API 含样本值校验）、CompiledStateGraphLite.ExecutionSession（完整并发实现）、RoundStart.submitLLM/onAsrMessage/predictedUserInput（打断 + 预测完整实现）、StateStoreMigrationEngine/VersionDefinition/AdjacentMigration（完整迁移引擎）
- 每份 deliverable 末尾列出"可复用方法论候选"，为后续知识回流到 wiki 做准备
