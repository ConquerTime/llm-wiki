# ada-sale-activity · 仓库地图

> M1 扫描快照（2026-04-29）。只记事实，不做结论。后续每份技术方案从这里取路标。

---

## 1. 基本信息

| 项目 | 值 |
|------|-----|
| 工程类型 | uni-app（Vue 2 + TypeScript），多端 H5 / 微信小程序 / 头条小程序 |
| 仓库路径 | `/Users/zhouyangdong/Documents/projects/ada-sale-activity` |
| 提交总数 | 1,548 commits（活跃度很高） |
| 分支总数 | 214 条（feature-* 命名，典型特性分支工作流） |
| 时间跨度 | 2021—2026（主力期 2022–2025，每年约 330–385 commits） |
| 页面数量 | 33 个页面注册（`src/pages.json`） |
| 源码规模 | 112 .vue · 62 .ts · 12 .js · 8 .scss |

---

## 2. 顶层目录速览

```
ada-sale-activity/
├── src/
│   ├── api/             # 接口层（11 个业务模块 + mp/tt 子目录）
│   ├── common/          # 全局公共资源（css 变量/mixin）
│   ├── components/      # 通用 UI 组件（29 个，带独立目录）
│   ├── config/          # 全局配置
│   ├── kitController/   # Kit 系统控制层（注册/加载/查找）
│   ├── kitTemplate/     # Kit 系统模板层（34 个 kit 组件）
│   ├── mixins/          # 业务 mixin（13 个，核心业务逻辑载体）
│   ├── pages/           # 路由页面（21 个页面目录）
│   ├── static/          # 静态资源
│   ├── store/           # Vuex 全局状态
│   ├── ttcomponents/    # 头条小程序专属组件（DyPayButton）
│   ├── types/           # TypeScript 类型定义
│   └── utils/           # 工具函数（22 个，覆盖支付/设备/上报/请求）
├── replaceManifest.js   # 构建前 manifest 动态替换（env/appid/publicPath）
├── upload.js            # 微信小程序 CI 上传脚本
├── vue.config.js        # webpack 扩展（CSS 后处理/头条小程序打包插件）
├── saber.yml            # CI/CD 流水线（Saber 平台，4 个 stage）
└── package.json         # 14 条 npm scripts，涵盖 3 端 × dev/test/staging/prod
```

---

## 3. Kit 系统（最核心的可复用资产）

### 3.1 架构原理

活动落地页的核心机制是一套"配置驱动 + 组件注册"的 Kit 系统，分两层：

```
kitController/            kitTemplate/
├── client.js    ←────── ├── kit-xxx/
│   (注册/查找)           │   ├── config.json   (元数据)
├── loader/               │   ├── view.vue      (渲染组件)
│   ├── conf.js           │   └── content.vue   (内容组件，部分有)
│   └── view.js           └── ...（34 个模板）
└── config/
    ├── owner.json
    └── category.json
```

**工作流**：
1. `client.js` 在首次调用时执行 `loadClientKitList()`，用 `folderKey` 将 `conf.js` 的 config.json 与 `view.js` 的 view.vue **对齐注册**成 `KitClient` 实例列表
2. 活动页通过 `client.getVM(name)` 拿到 Vue 组件选项，动态渲染
3. 每个 kit 有独立 `config.json` 声明元数据（`name`/`cnName`/`category`/`condition`）

### 3.2 Kit 目录清单（34 个）

| 类别 | Kit 名称 |
|------|---------|
| **按钮** | kit-button-activity · kit-button-image · kit-button-lesson · kit-button-pay · kit-button-pay-text · kit-button-price · kit-button-switch-image · kit-button-text |
| **图片/媒体** | kit-image-home · kit-image-swiper · kit-video-home · kit-audio |
| **倒计时** | kit-count-down · kit-home-count-down |
| **弹窗/留存** | kit-alert-home-retain · kit-alert-retain · kit-home-popup · kit-questionnaire-popup |
| **表单/选择** | kit-age-input · kit-choose-grade · kit-choose-grade-colorful · kit-choose-grade-popup · kit-student-info · kit-select-address · kit-payment-type |
| **信息展示** | kit-discount · kit-hint-text · kit-introduction · kit-order-info · kit-title · kit-tab-image |
| **登录** | kit-login |
| **工具** | kit-drop-placeholder · utils/ |

### 3.3 Kit 单元结构（以 kit-button-pay 为例）

```json
// config.json
{
  "name": "kit-button-pay",
  "cnName": "支付按钮",
  "thumbUrl": "https://...",
  "category": "button",
  "condition": { "max": "1" }   // 每个活动页最多出现 1 个
}
```

- `view.vue` — 渲染视图（C 端可见）
- `content.vue` — 内容组件（部分 kit 有，用于编辑态/配置态）

---

## 4. 页面体系（21 个页面目录，33 个注册页面）

| 页面目录 | 描述 | 多端条件 |
|---------|------|---------|
| `pages/detail` | **活动落地页主页**（核心，变更最频繁） | H5 + 微信 + 头条 |
| `pages/home` | 首页（头条小程序入口） | 仅 MP-TOUTIAO |
| `pages/order` | 订单列表/详情 | 微信 + 头条有差异页 |
| `pages/pay` | 支付结果页（tt-result/wx-result） | 分端独立实现 |
| `pages/school` | 进校小程序中间页 | 微信 |
| `pages/store` | 商城/middle-pay（iframe） | H5 为主 |
| `pages/middle-page` | 中间跳转页 | 全端 |
| `pages/login` | 登录页 | 仅 MP-WEIXIN |
| `pages/pc` | PC 端落地页 | H5 |
| `pages/activity` | 活动页（与 detail 协作） | |
| `pages/preview` | 预览页 | |
| `pages/webview` | Webview 容器页 | 小程序 |
| `pages/address-*` | 地址编辑/列表 | |
| `pages/literacy` | 识字相关 | |
| `pages/unqualified` | 不符合资格页 | |

**关键**：`pages/detail/detail.vue` 是整个仓库的主战场，最近 500 次提交里变更 40 次，也是 Kit 系统的消费者（活动内容在此动态组装）。

---

## 5. 业务核心：Mixin 层

Mixin 是业务逻辑的主要载体（Vue 2 时代的组合模式），13 个文件：

| Mixin | 职责 | 热度 |
|-------|------|------|
| `order.ts` | 下单流程（最核心） | ⚠️ 53 次变更，最热 |
| `login.ts` | 登录状态管理 | 15 次 |
| `detail.ts` | 落地页详情逻辑 | |
| `init.ts` | 页面初始化 | |
| `jump.js` | 页面跳转 | |
| `ybcTrack.ts` | 猿编程业务埋点 | |
| `observer.ts` | 曝光监听（IntersectionObserver） | |
| `order-common.ts` | 下单公共逻辑 | |
| `order-custom.ts` | 定制下单逻辑 | |
| `order-school.ts` | 进校下单逻辑 | |
| `literacy.ts` | 识字课程逻辑 | |
| `checkLogin.ts` | 登录校验 | |

---

## 6. 迭代热区（最近 500 commits 变更频次 Top 10）

| 排名 | 文件 | 变更次数 | 说明 |
|------|------|---------|------|
| 1 | `src/mixins/order.ts` | 53 | 下单核心，业务迭代频繁 |
| 2 | `src/pages/detail/detail.vue` | 40 | 落地页主页，活动内容变 |
| 3 | `src/manifest.json` | 28 | 环境/appid 替换（replaceManifest） |
| 4 | `src/utils/ybcUtils.ts` | 19 | 猿编程工具函数 |
| 5 | `src/api/login.ts` | 19 | 登录接口 |
| 6 | `src/pages/order/order.vue` | 18 | 订单页 |
| 7 | `src/utils/device.ts` | 16 | 设备检测 |
| 8 | `src/mixins/login.ts` | 15 | 登录 mixin |
| 9 | `src/utils/pay.ts` | 14 | 支付工具 |
| 10 | `src/components/_element.vue` | 12 | Kit 渲染器组件（推测）|

---

## 7. 构建与发布体系

### 7.1 环境矩阵（5 个环境 × 3 端）

| 环境 | H5 publicPath | 小程序 appid |
|------|--------------|-------------|
| development | `/ada-sale-activity` | test appid |
| test | `https://static-nginx-test.fbcontent.cn/ada-sale-activity` | test appid |
| staging-test | `.../ada-sale-activity/build/h5` | — |
| staging | `https://static-common.fbcontent.cn/ada-sale-activity/build/h5` | — |
| production | `https://static-common.fbcontent.cn/ada-sale-activity` | 正式 appid |

**关键机制**：`replaceManifest.js` 在构建前逐行正则替换 `src/manifest.json`，将 `h5.publicPath` / `mp-weixin.appid` / `mp-toutiao.appid` 写入正确值，再触发 uni-app 构建。

### 7.2 CI/CD（saber.yml，Saber 平台，4 个 stage）

```
master  → test-build-job (H5) + test-mp-build-job (微信小程序 CI upload)
online  → online-build-job (H5 + staging:H5) → online-publish-job (OSS 发布)
```

- H5 产物上传到阿里云 OSS（ossutil64）
- 微信小程序通过 `miniprogram-ci` 自动上传（`upload.js`）
- 头条小程序暂无 CI 自动上传（手动）

### 7.3 webpack 扩展（vue.config.js）

| 扩展点 | 用途 |
|--------|------|
| `scss.prependData` | 全局注入 `src/common/css/index.scss`（变量/mixin 无需手动 import） |
| `AfterEmitPlugin` | H5 构建后：① CSS 加随机版本号；② 删 uni-app CDN 残留资源；③ 复制 `dist/build/h5` 到 `dist/`  |
| `uniapp-to-group` | 头条小程序打包：注入 `microapp-trade-plugin`（字节跳动交易插件，含提单/退款页） |
| `resolve.alias` | `static` / `common` / `components` / `api` 路径别名 |

---

## 8. 关键依赖（业务集成层）

| 包 | 用途 | 复用价值 |
|----|------|---------|
| `@fenbi/webview` | 粉笔系 Webview 桥接 | 公司内部 |
| `@tutor/box-bridge-ts` | App 内 JS Bridge（与客户端通信） | 公司内部 |
| `@yuanfudao/frog` / `infra-frog` | 猿辅导埋点 SDK | 公司内部 |
| `@yuanfudao/webview` | 猿辅导 Webview SDK | 公司内部 |
| `@ybc/client-api` | 猿编程客户端 API | 公司内部 |
| `@tutor/network-miniprogram` | 小程序网络请求封装 | 公司内部 |
| `@sentry/vue` + `sentry-mina` | H5 + 小程序双端错误监控 | 可通用 |
| `miniprogram-ci` | 微信小程序 CI 上传 | 可通用 |
| `flyio` | 多端 HTTP 请求库 | 可通用 |
| `pidcrypt` | 加密（登录/支付场景）| 可通用 |
| `uniapp-to-group` | 头条小程序打包为群组包 | 可通用 |
| `postcss-pxtorpx-pro` | px → rpx 自动转换 | 可通用 |

---

## 9. 萃取优先级（基于变更频次 + 可通用性）

| 优先级 | 方向 | 理由 | 对应 M2/M3 交付物 |
|--------|------|------|-----------------|
| ★★★ | **多端构建与 manifest 替换机制** | 3 端×5 环境矩阵，replaceManifest 是独特工程决策，可通用于任何 uni-app 项目 | 技术方案 #1 |
| ★★★ | **Kit 组件系统（配置驱动落地页）** | 34 个 kit 模板 + kitController，是活动页高效迭代的核心基建，设计思路可复用 | 技术方案 #2 |
| ★★ | **CI/CD 发布流水线** | saber.yml + upload.js + OSS 发布，覆盖 H5 + 微信 CI，头条手动的 gap 值得记录 | 技术方案 #3 |
| ★★ | **下单 / 支付 mixin 体系** | order.ts 是热度最高的文件（53次），其演化路径可提炼为"多端下单业务复杂度管理"经验 | 技术方案 #4（追加）|
| ★ | **业务知识：活动页玩法 + Kit 使用模式** | Kit 的 34 个模板覆盖了哪些活动类型？哪些 condition 配置控制业务规则？ | 业务知识卡片 |
| ★ | **Sentry 双端监控接入方案** | H5 + 小程序分别用 @sentry/vue 和 sentry-mina，初始化逻辑可复用 | 落地页经验规范 |

---

## 10. 待深挖的未知区

- [ ] `src/mixins/order.ts` 的完整调用链（下单流程最复杂，需单独读）
- [ ] `kitTemplate/kit-choose-grade-popup` 和 `kit-student-info` 变更频繁，背后的业务规则是什么？
- [ ] `pages/store/middle-pay.vue` 的 iframe 方案：为何使用 iframe 而不是原生页面？
- [ ] `ttcomponents/DyPayButton` — 头条小程序专有支付按钮，与微信支付方案的差异在哪？
- [ ] `src/config/` 目录内容（全局配置内容未读）
- [ ] `api/landing.ts` — 落地页专属接口，决定了活动数据的加载模式
