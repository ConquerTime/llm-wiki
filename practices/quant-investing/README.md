---
practice: quant-investing
status: active
cadence: monthly
created: 2026-05-09
updated: 2026-05-09
---

# 量化投资实践

> 个人 A 股量化投资的长期实践容器：策略迭代、实盘追踪、月度复盘。当前处于**预热阶段**——等 [[projects/2026-05-a-share-quant/README|2026-05-a-share-quant]] 项目交付后正式进入节奏。

## 为什么做这件事

量化投资不是"做完就交付"的任务，而是长期的市场参与与方法论迭代：

- 市场在变，策略必须持续 review，不存在"最终答案"
- 真正的经验来自连续多轮牛熊 / 风格切换的实盘观察
- 因子有效性、回测陷阱、执行细节只有在持续实践中才能沉淀

单次"搭好数据管道 + 跑通首个策略"是 project；**持续追踪、定期 review、策略演化**是 practice。

## 节奏

- **月度**（`reviews/YYYY-MM.md`）：
  - 当月策略表现（净值、回撤、归因）
  - 因子 / 信号层面的异常点
  - 下个月调整意图
- **季度**（`reviews/YYYY-Q{1..4}.md`）：
  - 策略组合层面的再评估
  - 是否要启动新的 project（比如"Q3 研究事件驱动"）
- **年度**（`reviews/YYYY.md`）：
  - 整体收益 / 夏普 / 最大回撤总结
  - 方法论回流：把稳定下来的认知抽到 `wiki/concepts/` 或 `wiki/synthesis/`

高频的日志先不强求——A 股日频策略不值得天天记。有触发事件（比如调参、加因子、换标的池）时在 `journal/YYYY-MM.md` 追加一条即可。

## 当前状态

**预热阶段（2026-05）**：

- 策略容器暂空。待 [[projects/2026-05-a-share-quant/README|a-share-quant]] project 交付首个可运行策略后，搬到本 practice 开始月度追踪
- 还没有实盘账户，review 先以"模拟盘 / 回测滚动"口径进行
- `journal/` `reviews/` `resources/` 空目录按"§5 空目录规则"首次使用时再建

## 导航

- **关联 Project**：[[projects/2026-05-a-share-quant/README|2026-05-a-share-quant]]（当前 active）
- **关联 Wiki**：暂无（等首次 review 产出第一批回流知识）
- **关联 Writing**：暂无

## 维护约定

- 规范以项目根 CLAUDE.md §8 为准
- 本 practice 内部的决策变化写在 `journal/`，不改历史 `reviews/`
- 状态变更（active → dormant / retired）在 README frontmatter 改，并同步更新 wiki/index.md「活跃 Practices」表格
