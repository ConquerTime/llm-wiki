---
project: 2026-04-sale-activity
status: active
created: 2026-04-29
updated: 2026-04-29
---

# ada-sale-activity 知识萃取 · 简报

## 背景

`ada-sale-activity` 是一个基于 uni-app（Vue 2 + TS）的电商落地页 / 促销活动多端工程，同时支持 H5、微信小程序、头条小程序三端。仓库中沉淀了大量项目迭代中形成的**工程实践、业务规则、踩坑经验**，但它们当前只存在于代码、配置和作者记忆里，无法被其他项目或未来的自己复用。

本项目不是修改该仓库，而是**把其中可复用的东西提炼出来，沉淀到 wiki**。

外部仓库路径：`/Users/zhouyangdong/Documents/projects/ada-sale-activity`（只读参考，不修改）。

## 目标

针对 `ada-sale-activity` 仓库做一次系统性的知识萃取，产出：

- 至少 3 份独立成篇的**技术方案文档**（多端架构、发布流程、模块化等方向）
- 一份**电商落地页经验规范**（从代码和历史中归纳出的最佳实践 / 反模式）
- **业务知识**卡片（活动类型、玩法模式、关键业务流程）
- 一套可复用的**工作 skill**（做电商落地页项目时的标准工作流）

每份产出都要能脱离 `ada-sale-activity` 独立使用（"离开这个项目仍然有用"原则）。

## 非目标

- ❌ 不修改 `ada-sale-activity` 仓库任何代码
- ❌ 不为本项目写新的活动页面 / 新功能
- ❌ 不做通用的 uni-app / Vue 教学（只萃取仓库里真实出现过的模式）
- ❌ 不做一次性的、只在这次活动里成立的结论

## 范围

**会覆盖的方向**（初步，随摄入细化）：

1. **多端适配工程** — H5 / 微信小程序 / 头条小程序 的构建流程、条件编译、manifest 替换（`replaceManifest.js`）
2. **模块化与组件库** — `kitTemplate/` 组件模板机制、活动页搭建模式
3. **发布与环境管理** — dev / test / staging / production 多环境切换，`upload.js` 上传流程
4. **业务集成** — `@fenbi/webview`、`@tutor/box-bridge-ts`、网络层、监控（Sentry）
5. **活动业务知识** — 活动页常见玩法（砍价 / 拼团 / 秒杀 / 优惠券），与课程体系的对接模式
6. **复用工作 skill** — "接到一个电商活动落地页需求时的标准工作流"

范围边界会随仓库实际摄入情况动态调整，在 log.md 中追加记录。

## 交付物

- [ ] **技术方案 × 3+**（进 `deliverables/tech-specs/`）
  - [ ] 多端条件编译与构建流水线（uni-app + manifest 替换）
  - [ ] 活动页模块化与组件复用机制（kitTemplate）
  - [ ] 多环境发布与上传流程（VUE_APP_ENV / BUILD_ENV / upload.js）
- [ ] **电商落地页经验规范**（进 `deliverables/playbook/ecommerce-landing-playbook.md`）
- [ ] **业务知识卡片集**（进 `deliverables/business/`，覆盖活动类型 / 关键业务流程）
- [ ] **复盘回流到 wiki**（`retro.md` 驱动，最终进 `wiki/concepts`、`wiki/synthesis`、`wiki/entities`）
  - 可复用方法 → `wiki/concepts/programming/` 或 `wiki/concepts/business/`
  - 通用经验 → `wiki/synthesis/`
  - 相关工具 / 产品 → `wiki/entities/products/`

## 里程碑

- [ ] **M1 仓库探索与地图绘制** — 摸清仓库结构、关键目录、历史演进线索 — 预计 2026-05 第 1 周
- [ ] **M2 技术方案 3 篇成稿** — 多端构建 / 组件模板 / 发布流程 — 预计 2026-05 第 2–3 周
- [ ] **M3 业务知识 + 落地页经验规范** — 预计 2026-05 第 4 周
- [ ] **M4 知识回流到 wiki** — retro.md + 对应 wiki 页面落地 — 预计 2026-06 第 1 周

## 风险 / 未知

- **信息不对称**：当前只扫过 `README.md` 和 `package.json`，对业务逻辑、历史决策、踩坑经验的了解有限 — 需要通过源码阅读 + 与用户对话补齐
- **边界识别**：该仓库哪些是"ada 特有"、哪些是"电商落地页通用"，需要在萃取过程中判断，容易把特有决策误当作通用规范
- **深度与广度的权衡**：仓库较大，面面俱到会稀释，需要在 M1 阶段画出优先级图
- **耦合到在职公司资产**：`@fenbi`、`@tutor`、`@yuanfudao` 等内部包不方便公开讨论，萃取时要判断哪些能回流到 wiki，哪些只能留在 `deliverables/` 项目内
