# ada-sale-activity 知识萃取 · 活动日志

> 追加式时间线，记录讨论、决策、产出、阻塞。

---

## [2026-04-29] M4 知识回流到 wiki

- 新建 wiki 页面：
  - **concepts/programming/validation-chain.md** — 校验链模式（早退结构 + 与责任链模式的区别 + ada 下单链路实例）
  - **concepts/programming/config-driven-page.md** — 配置驱动落地页（Kit 单元 + require.context + 与低代码平台的区别 + 已知权衡）
  - **concepts/programming/uniapp-multienv-build.md** — uni-app 多端多环境构建（replaceManifest + 三层环境变量分工 + AfterEmitPlugin + 头条特殊处理）
  - **synthesis/frontend-ecommerce-antipatterns.md** — 6 类反模式：单文件过长 / env 魔法字符串 / Mixin 不透明 / 构建配置进 git / 实例变量重试 / CI 手动孤岛
- 更新 wiki 页面：
  - **concepts/programming/unified-payment-route.md** — 补充"客户端支付路由器"前端变体维度
- 所有回流页面均已建立交叉引用（validation-chain ↔ unified-payment-route ↔ antipatterns ↔ config-driven-page ↔ uniapp-multienv-build）
- M4 完成，项目全部里程碑（M1–M4）交付完毕

## [2026-04-29] M3 业务知识 + 落地页经验规范

- **deliverables/playbook/ecommerce-landing-playbook.md** — 6 个维度的最佳实践 + 反模式：架构层 / 构建层 / 发布层 / 下单支付层 / Kit 组件层 / 跨层通用原则
- **deliverables/business/01-app-env-matrix.md** — 多端 × 多环境参数矩阵（H5 publicPath / 小程序 appid / OSS bucket / CI Stage 全表）
- **deliverables/business/02-payment-params.md** — 支付参数体系（payType / bizType / env / payChannel×payFrom 矩阵 / 微信支付页路由 / 支付宝分发 / IAP / 价格计算 / extraInfos）
- **deliverables/business/03-kit-catalog.md** — Kit 全量清单（34 个，含 category / condition / 消费方式 / 新增步骤）
- M3 交付物覆盖 brief.md 中"落地页经验规范"和"业务知识"两大类

## [2026-04-29] M2 技术方案 × 4 成稿

- 完成全部 4 份技术方案，进 `deliverables/tech-specs/`
- **01-multiplatform-build.md** — 多端构建与 manifest 替换机制（replaceManifest + 3端×5环境矩阵 + AfterEmitPlugin + vue.config.js 扩展）
- **02-kit-system.md** — Kit 组件系统配置驱动落地页（34 kit + kitController require.context 注册 + owner/category 分类 + detail.vue 消费方式）
- **03-cicd-pipeline.md** — CI/CD 发布流水线（Saber 4 stage + OSS + miniprogram-ci + 分支策略 + 已知 gap：头条无 CI、正式小程序无自动上传）
- **04-order-payment-mixin.md** — 下单与支付 Mixin 体系（1643 行 order.ts 完整拆解：校验链 + 错误处理矩阵 + 支付路由器 pay.ts + 多端支付分发 + 价格计算 + extraInfos + customCreateOrder 钩子）
- 额外阅读：src/mixins/order.ts（全文）、src/utils/pay.ts（全文）、src/mixins/order-common.ts
- brief.md 预设 3 份技术方案，实际产出 4 份（发现 order.ts 萃取价值高）

## [2026-04-29] M1 仓库探索

- 完成仓库结构全面扫描（顶层、src/ 两级目录、页面、kit 体系、git 历史）
- 阅读关键配置：replaceManifest.js / vue.config.js / upload.js / saber.yml / package.json / kitController/client.js
- 分析 git 热区：最近 500 次提交，order.ts（53次）、detail.vue（40次）为最热文件
- 产出：`notes/repo-map.md`（仓库地图：基本信息 + 目录速览 + Kit 系统 + 页面体系 + 迭代热区 + 构建发布 + 萃取优先级）
- 确认萃取优先级：多端构建（★★★）> Kit 系统（★★★）> CI/CD（★★）> 下单 mixin（★★）> 业务知识/监控（★）
- 阻塞/待深挖：order.ts 调用链、middle-pay iframe 方案、DyPayButton、api/landing.ts（已在 repo-map.md 第 10 节列出）

## [2026-04-29] 启动
- 项目创建，目录初始化（README / brief / log / retro / raw / notes / deliverables）
- 与用户对齐：目标是归纳 `ada-sale-activity` 仓库的工作 skill、技术方案、业务知识，沉淀到 wiki
- 外部仓库：/Users/zhouyangdong/Documents/projects/ada-sale-activity（只读参考）
- brief.md 中"交付物"按四大类（技术方案 × 3+、落地页经验规范、业务知识、工作 skill）列出，里程碑 M1–M4 待执行中细化
