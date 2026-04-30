# 技术方案 #2：Kit 组件系统——配置驱动的落地页搭建机制

> ada-sale-activity 如何用 34 个 kit 模板 + kitController 实现"活动落地页内容可配置、新活动无需改页面"。

---

## 1. 问题背景

电商活动落地页有两个矛盾的特性：

- **高频变化**：每次活动的图片、按钮文案、价格、倒计时都不同
- **结构相似**：大部分活动页都是：顶图 + 说明文字 + 价格按钮 + 弹窗，差异只在内容

如果每次新活动都改代码，发布成本极高；如果把所有可能的组件都硬编码进一个大页面，代码膨胀且难以维护。

解法：**把活动页的"结构单元"抽象为 Kit 组件，后端下发配置列表，前端动态组装**。

---

## 2. 系统架构

```
后端 API
  └── 返回活动配置（pageInfo.componentList）
        每个元素：{ name: 'kit-button-pay', state: { btnText: '立即购买', ... } }

前端
  ├── detail.vue（落地页主页）
  │     ├── 从 API 拿 renderList（componentList）
  │     └── v-for renderList → <render-element :kit="kit">
  │
  ├── components/_element.vue（Kit 渲染分发器）
  │     └── v-if kit.name === 'xxx' → 渲染对应 Kit 组件，透传 kit.state 的字段为 props
  │
  └── kitController/
        ├── client.js（注册表：name → KitClient 实例）
        ├── loader/conf.js（用 require.context 批量加载所有 config.json）
        └── loader/view.js（用 require.context 批量加载所有 view.vue）

  kitTemplate/（34 个 kit 目录，每个含 config.json + view.vue）
```

**数据流**：

```
API response.componentList
  → detail.vue renderList
    → render-element (v-for)
      → v-if kit.name 分发
        → Kit view.vue (props = kit.state)
```

---

## 3. Kit 目录结构（标准单元）

每个 kit 是一个**独立目录**，包含 2~3 个文件：

```
kitTemplate/kit-button-pay/
├── config.json   ← 元数据（注册信息）
├── view.vue      ← C 端渲染视图（用户看到的）
└── content.vue   ← 编辑态组件（可选，用于后台配置界面）
```

`config.json` 的完整字段：

```json
{
  "name": "kit-button-pay",       // 唯一标识，与后端配置中的 name 对应
  "cnName": "支付按钮",            // 后台展示名
  "thumbUrl": "https://...",      // 后台预览缩略图
  "category": "button",          // 分类（用于后台筛选）
  "abstract": false,              // 抽象 kit，不直接使用
  "condition": {
    "max": "1",                  // 每个落地页最多出现 1 个
    "fixed": "bottom",           // 布局约束：固定在底部
    "type": "alert"              // 类型标记
  }
}
```

---

## 4. 注册机制（kitController）

### 4.1 两层 require.context 扫描

`client.js` 在首次调用 `loadClientKitList()` 时，通过 webpack 的 `require.context` **一次性把 kitTemplate/ 下所有 config.json 和 view.vue 批量导入**：

```js
// conf.js
const context = require.context('../../kitTemplate', true, /config.json$/)
// → 扫描 kitTemplate/ 下所有 config.json，返回 [{ name, category, condition, folderKey, ... }]

// view.js
const context = require.context('../../kitTemplate', true, /view.vue$/)
// → 扫描 kitTemplate/ 下所有 view.vue，返回 [Vue 组件选项对象，带 folderKey]
```

`folderKey` 是从文件路径里提取的目录名前缀（如 `./kit-button-pay/`），作为 **config 与 view 的对齐 key**。

### 4.2 注册与校验

```js
// _help.js: isValid()
// 对每个 config.json 做字段校验：
// name（必填+合法组件名）、cnName（必填）、thumburl、category、abstract、condition
// 不合法的 kit 被 filter 掉，不进入注册表

// client.js: loadClientKitList()
for (const conf of syncConfigs) {
  const vm = templates.find(it => it.folderKey === conf.folderKey)
  if (vm) ClientKitList.push(new KitClient(conf, vm))
}
```

### 4.3 使用方式（消费侧）

```js
// 在页面/组件里拿到 VM
import kitClient from '@/kitController/client'
const vm = kitClient.getVM('kit-button-pay')  // → Vue 组件选项对象
```

`_element.vue` 里用 `v-if kit.name === 'xxx'` 分发渲染，是一种"静态映射"方式（每个 kit 硬写一个 v-if 分支）。

---

## 5. Kit 全量清单（34 个，含 category 与 condition）

| Kit 名称 | cnName（推测） | category | condition 要点 |
|---------|------------|---------|--------------|
| kit-image-home | 首图 | image | 无限制 |
| kit-image-swiper | 轮播图 | image | 无限制 |
| kit-video-home | 视频 | video | 无限制 |
| kit-audio | 音频 | audio | 无限制 |
| kit-title | 标题文字 | text | 无限制 |
| kit-hint-text | 提示文字 | text | 无限制 |
| kit-button-pay | 支付按钮 | button | max:1 |
| kit-button-pay-text | 支付文字按钮 | button | max:1 |
| kit-button-price | 价格按钮 | purchase-button | max:1，fixed:bottom |
| kit-button-text | 文字按钮 | purchase-button | max:1，fixed:bottom |
| kit-button-image | 图片按钮 | button | 无限制 |
| kit-button-lesson | 课节按钮 | button | 无限制 |
| kit-button-activity | 活动按钮 | button | 无限制 |
| kit-button-switch-image | 切换图片按钮 | button | 无限制 |
| kit-choose-grade | 年级选择 | button | 无限制 |
| kit-choose-grade-colorful | 彩色年级选择 | button | 无限制 |
| kit-introduction | 介绍组件 | button | 无限制 |
| kit-tab-image | Tab 图片 | button | 无限制 |
| kit-choose-grade-popup | 年级选择弹窗 | purchase-alert | max:1，fixed:center |
| kit-age-input | 年龄输入弹窗 | purchase-alert | max:1，fixed:center，type:alert |
| kit-alert-retain | 留存弹窗 | retain-alert | max:1，fixed:center，type:alert |
| kit-alert-home-retain | 首页留存弹窗 | retain-alert | max:1，fixed:center |
| kit-home-popup | 首页弹窗 | alert | max:1，fixed:center，type:alert |
| kit-questionnaire-popup | 问卷弹窗 | purchase-alert | max:1，fixed:center |
| kit-count-down | 倒计时 | other | 无限制 |
| kit-home-count-down | 首页倒计时 | other | 无限制 |
| kit-discount | 折扣信息 | other | max:1 |
| kit-order-info | 订单信息 | other | 无限制 |
| kit-login | 登录组件 | form | 无限制 |
| kit-student-info | 学生信息 | form | 无限制 |
| kit-select-address | 地址选择 | — | 无限制 |
| kit-payment-type | 支付方式 | — | 无限制 |
| kit-drop-placeholder | 拖拽占位符 | — | 无限制（comp-drop-placeholder） |
| utils/ | — | — | 工具目录（非 kit） |

**分类体系**（category.json 定义的 7 个官方分类）：
`image` · `purchase-info` · `purchase-button` · `alert` · `video` · `comment` · `audio`

**落地页类型**（owner.json 定义的 2 种）：
- `purchase-landing`：售卖落地页（含价格按钮、年龄选择、弹窗）
- `basic-activity`：纯图活动页（图片+视频+评论+音频）

---

## 6. 关键设计决策与权衡

### 6.1 require.context 批量注册（优）
- 新增 kit 只需在 `kitTemplate/` 下建目录，**不需要改任何注册代码**
- webpack 在编译时静态分析，所有 kit 都被打进 bundle（不存在运行时动态加载的问题）
- 代价：bundle 体积随 kit 数量线性增长，34 个 kit 全部进主包

### 6.2 _element.vue 的 v-if 分发（弱点）
- 当前实现是**手写每个 kit 的 v-if 分支**（_element.vue 里可以看到一长串 v-if）
- 问题：新增 kit 需要改 _element.vue，与"注册自动化"理念矛盾
- 更好的实现：用 `<component :is="vm">` 动态组件，直接从 kitClient.getVM(kit.name) 拿 vm

### 6.3 condition 约束（编辑态逻辑）
- `max`：限制单个落地页可放置的上限数量
- `fixed`：布局约束（center / bottom）
- `type: alert`：弹窗类型，触发特殊渲染逻辑

这些约束**在后台编辑态生效**，C 端渲染不依赖 condition（服务端下发的已经是合法配置）。

### 6.4 view.vue 的 `preview` prop
所有 kit view.vue 都接受 `preview` prop（Boolean），区分**预览态**和**生产态**，同一组件可在后台预览和 C 端复用。

---

## 7. 可复用的设计模式

> 以下内容脱离 ada-sale-activity 后仍然成立，适合回流到 wiki。

**"配置驱动落地页"模式**的核心要素：
1. **标准化 Kit 单元**：每个 UI 模块 = config.json（元数据）+ view.vue（渲染）
2. **批量自动注册**：require.context 扫描目录，folderKey 对齐 config 与 view，无需手动维护注册表
3. **后端下发渲染列表**：`[{ name, state }]`，前端按 name 取组件、按 state 传 props
4. **condition 约束**：在编辑态做合法性校验，C 端无需感知

**适用场景**：
- 需要运营/产品自助配置页面内容的活动/营销页
- 多个活动页结构相似但内容不同，希望复用组件池
- 前后端分离，后端控制"放什么组件"，前端控制"组件长什么样"

**与低代码平台的区别**：这套机制是"轻量配置驱动"，没有可视化拖拽编辑器，编辑态逻辑由后台系统维护；低代码平台则把编辑器也内置进来。
