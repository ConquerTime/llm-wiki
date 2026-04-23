# Work Summary: 2026-04-14 to 2026-04-17

> Personal work log generated from Claude Code session analysis (50 sessions analyzed across 16-day window, focused on last 3 days).

---

## Horizon Web Commerce — 正价课 & 落地页功能链路

### 公共支付页（Unified Payment Page）

- 设计并实现了 WeChat H5 commerce app 的统一支付页，合并了原本分散的多条支付路径
- 完成 Bolt 支付集成：修复了 Alipay redirect 处理逻辑，包括用户重入未支付订单时参数传递问题
- 完整归档 `unified-payment-page` change，通过 opsx:archive 工作流完成 spec sync 与 commit

**关键 commit：**
```
6ef80f9 2026-04-17  feat: [HORIZON-8347] 正价课完整购课链路 + 公共支付页
```

### 落地页管理重写（Landing Page Management Rewrite）

- 完整重写落地页管理功能，支持体验课/正价课双类型 + 投放方案管理
- 修复落地页布局：全宽图片、产品卡悬浮定位、移除背景色与标语、SVG 改用 img
- 修复购买状态检测与已登录直接建单逻辑
- 修复 landing 缓存 pageId 校验，对齐 spec

**关键 commits：**
```
3f0f25d 2026-04-17  style: [HORIZON-8347] 落地页布局调整
775bece 2026-04-16  feat: 落地页管理完整重写（体验课/正价课双类型 + 投放方案管理）
0e08768 2026-04-14  feat: [HORIZON-8347] 落地页购买状态检测与已登录直接建单
```

### 渠道管理重写（Channel Management Rewrite）

- 按新 PRD 重写渠道管理页，从 UTM-based 模型切换为小红书/社群来源模型
- 引入枚举类型，重构渠道/线索/落地页数据模型，与后端 API 对齐

**关键 commits：**
```
802f17a 2026-04-16  feat: channel API 对齐 —— 引入枚举类型并重构渠道/线索/落地页数据模型
139881e 2026-04-15  feat: 渠道管理页完整重写（小红书/社群来源模型）
```

### 线索管理重写（Lead Management Rewrite）

- 完成线索管理完整重写：线索列表/详情/导入/推送管道
- 验证并归档 lead-management-rewrite change

**关键 commit：**
```
264b7a7 2026-04-16  feat: leads 管理完整重写（线索列表/详情/导入/推送管道）
```

### Admin Growth 后台

- 新建增长管理后台 admin-growth
- 验证实现，调试了登录状态认证问题

**关键 commit：**
```
0fcccc7 2026-04-15  feat: [HORIZON-XXXX] 新建增长管理后台 admin-growth
```

---

## Horizon Web Commerce — Auth & Course Landing

- 修复了课程落地页认证 bug：用户被意外重定向到 login 的问题
- 归档了 `fix-course-auth-user-field` change
- 解决了 git worktree 清理问题，修复了 MR#13 的 rebase 问题（feature-course 分支）
- 验证了 logout 可纯前端实现（清 session），无需后端 API

---

## Horizon Web AiTutor

- 调研了 JSBridge/WebView 通信模式，评估如何在 aitutor 复用该模式
- 调研了 WeChat OAuth 集成流程
- 配置了 Alibaba Cloud ECS SSH 免密登录 + GitLab 密钥

**关键 commits（aitutor，近3天）：**
```
9ff021e34 2026-04-16  Merge branch 'feature-cocos-layout' into 'deploy-test'
257a17a18 2026-04-16  feat: [HORIZON-8673] 透传2dx气泡状态
797327e5e 2026-04-16  fix: [HORIZON-8624] 修复行程图教具宽度适配
160ac1a13 2026-04-17  fixup: 优化页面滚动
```

---

## Kaigao — Promptfoo Evaluation System

- 从零重新设计评测系统架构（Script Provider 方案），删除旧 eval sets
- 将 promptfoo view 改为展示真实 prompt（而非模板），eval 结果与 prompt 版本关联
- 重构为 adapter 架构，覆盖 7 个 prompt 函数
- 修复 SQLite `FOREIGN KEY constraint failed` 错误（`--no-write` 绕过 promptfoo bug）
- 修复 hook feedback loop bug，修复 prettier 格式化和 education-levels test
- 运行 baseline evaluations，固化基准结果

**关键 commits：**
```
19019c6 2026-04-16  fix(ci): prettier format promptfoo-evals adapters, fix education-levels test
a5ed223 2026-04-15  feat(promptfoo-evals): 重构评测系统为 adapter 架构，覆盖 7 个 prompt 函数
ad6f981 2026-04-15  fix(promptfoo-evals): save/compare 脚本加 --no-write 绕过 promptfoo SQLite bug
391cc49 2026-04-15  chore(hooks): stop hook 成功时静默
```

## Kaigao — References（英文文献检索）

- 将英文文献检索从第三方 API 切换为本地向量语义检索（Milvus）
- 编写了爬取 qianbixiezuo.com 学术文献的 Tampermonkey 脚本，批量导出 50 万条数据
- 尝试统一中英文文献数据库结构（部分完成）

**关键 commit：**
```
804b457 2026-04-16  feat(references): 英文文献检索从第三方 API 切换为本地向量语义检索
```

---

## LLM Wiki 知识库

### 结构建设

- 初始化了 llm-wiki 仓库，按 Karpathy 的 LLM Wiki 设计规范实现目录结构
- 添加了 Karpathy Guidelines 到 wiki 和 CLAUDE.md
- 配置了 Obsidian vault（`.obsidian/` 目录）

### 知识摄入

- Ingest `karpathy/autoresearch` GitHub 仓库 → 原文 + 源摘要页 + 概念页
- Ingest `nuwa-skill` GitHub 仓库 → raw 原文 + wiki 页面
- Ingest 「AI Agent 面试八股文」中文文章
- 新增消息队列知识文档（通过 /learn skill 触发）
- Ingest 软件工程知识资料（代码质量/重构）
- 新增设计模式 wiki 页面（GoF/SOLID/DDD/反模式深入内容）

### 技能与工具

- 创建了 `wiki-query` skill，可从任意项目目录查询 llm-wiki 知识库
- 将 `learn skill` 与 llm-wiki 集成，支持 project tags

### 维护

- 执行 daily lint，修复断链（`[[page]]` 语法示例误判、nuwa-skill raw 路径修正）
- 发布 morning brief 2026-04-15：AI Skills 生态爆发

**关键 commits：**
```
9422443 2026-04-16  fix: 修复断链
a08b29a 2026-04-16  feat: 添加软件工程知识资料及设计模式 wiki 页面
868ff8c 2026-04-16  docs: 补充设计模式深入内容 (GoF/SOLID/DDD/反模式)
9fbe6e5 2026-04-16  docs: 添加软件工程知识资料 (代码质量+重构)
1d6ef34 2026-04-15  feat: ingest morning-brief 2026-04-15
```

---

## DevOps / Infra

- 规划并部分实现了 SAE → 单 ECS 实例的部署架构迁移（kaigao 项目）
- 配置 Alibaba Cloud ECS SSH 免密认证
- 修复了多个 CI lint 失败，解决了 pre-commit hook 未能拦截的格式问题
- 创建了多个 MR（feature-dev → deploy-test, feature-dev → main），处理了 CI 失败和 merge conflicts

---

## 工具 / 效率

- 编写了 Tampermonkey 脚本，批量导出内部平台 API 文档
- 调研了 Sourcegraph MCP plugin（安装测试，部分功能未成功）
- 优化了 Claude hooks：stop hook 成功时静默，避免反馈注入对话循环

---

## 统计摘要（2026-04-02 ~ 2026-04-17，近3天重点）

| 项目 | Sessions | 主要交付 |
|------|---------|---------|
| horizon-web-commerce | 15 | 支付页、落地页、渠道、线索管理完整重写 |
| kaigao (promptfoo + references) | 11 | eval 架构重建、向量检索切换 |
| llm-wiki | 8 | wiki 初始化、5+ 知识摄入、skill 集成 |
| horizon-web-aitutor | 4 | auth 修复、JSBridge 调研 |
| DevOps/CI | 5 | ECS 迁移规划、MR 流程、CI 修复 |

总计 50 sessions analyzed · 约 470 小时 · 50 commits

---

## 工作模式观察

1. **流程化交付**：explore → propose → apply → verify → archive 的完整工作流，在 channel/lead/payment 三大功能中均完整执行
2. **知识管理**：在开发过程中并行维护 llm-wiki，将学到的技术概念即时沉淀（消息队列、设计模式、Agent 等）
3. **自动化习惯**：hooks 静默优化、skill 跨项目复用、promptfoo 评测体系建设，体现出持续投资工具效率的倾向
4. **主要摩擦点**：TypeScript 类型错误在 commit 时暴露（5+ 次），导致多轮修复循环；Claude 偶发错误路径（Docker vs bare ECS、raw/ 写摘要而非原文）
