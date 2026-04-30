# 业务知识 #3：Kit 组件目录

> ada-sale-activity 的 34 个 Kit 组件清单，含分类、页面类型归属、使用约束，以及 Kit 系统的配置语义说明。

---

## 1. Kit 分类体系（category.json）

7 个官方分类：

| category | 含义 | 示例 Kit |
|----------|------|---------|
| `image` | 图片类展示 | kit-image-home, kit-image-swiper |
| `video` | 视频类 | kit-video-home |
| `audio` | 音频类 | kit-audio |
| `purchase-info` | 购买信息展示 | kit-discount, kit-order-info |
| `purchase-button` | 购买入口按钮（有 condition 约束）| kit-button-price, kit-button-text |
| `alert` | 弹窗类 | kit-home-popup, kit-alert-retain |
| `comment` | 评论类 | （当前无对应 Kit）|

---

## 2. 落地页类型（owner.json）

2 种落地页类型，决定哪些 Kit 可用：

| owner | 用途 | 包含 Kit 类型 |
|-------|------|-------------|
| `purchase-landing` | 售卖落地页 | 含价格按钮、年龄选择弹窗、购买弹窗，完整购买链路 |
| `basic-activity` | 纯图活动页 | 图片 + 视频 + 评论 + 音频，无购买功能 |

---

## 3. condition 字段语义

`config.json` 中 `condition` 字段由**后台编辑器**读取，C 端渲染不依赖（服务端已校验合法性）：

| condition 字段 | 类型 | 含义 |
|--------------|------|------|
| `max` | 字符串数字 | 单个落地页最多放置几个该 Kit（`"1"` = 唯一）|
| `fixed` | `"bottom"` / `"center"` | 布局约束（底部固定 / 居中弹窗）|
| `type` | `"alert"` | 弹窗类型，触发后台特殊渲染逻辑 |

---

## 4. Kit 全量清单（34 个）

### 4.1 图片 / 媒体类（image / video / audio）

| Kit 名称 | category | condition | 说明 |
|---------|---------|-----------|------|
| `kit-image-home` | image | 无 | 首图，落地页顶部大图 |
| `kit-image-swiper` | image | 无 | 轮播图 |
| `kit-video-home` | video | 无 | 视频展示（主视频）|
| `kit-audio` | audio | 无 | 音频播放 |

### 4.2 文字类（text）

| Kit 名称 | category | condition | 说明 |
|---------|---------|-----------|------|
| `kit-title` | text | 无 | 标题文字 |
| `kit-hint-text` | text | 无 | 提示性说明文字 |

### 4.3 普通按钮类（button）

| Kit 名称 | category | condition | 说明 |
|---------|---------|-----------|------|
| `kit-button-pay` | button | max:1 | 支付按钮（简化版）|
| `kit-button-pay-text` | button | max:1 | 文字版支付按钮 |
| `kit-button-image` | button | 无 | 图片样式按钮 |
| `kit-button-lesson` | button | 无 | 课节/课次选择按钮 |
| `kit-button-activity` | button | 无 | 活动入口按钮 |
| `kit-button-switch-image` | button | 无 | 切换图片按钮（多态展示）|
| `kit-choose-grade` | button | 无 | 年级选择（inline）|
| `kit-choose-grade-colorful` | button | 无 | 彩色年级选择 |
| `kit-introduction` | button | 无 | 课程/活动介绍组件 |
| `kit-tab-image` | button | 无 | Tab 图片切换 |

### 4.4 购买入口按钮类（purchase-button）

有布局约束，一般固定在页面底部：

| Kit 名称 | category | condition | 说明 |
|---------|---------|-----------|------|
| `kit-button-price` | purchase-button | max:1, fixed:bottom | 价格+购买按钮，落地页核心购买入口 |
| `kit-button-text` | purchase-button | max:1, fixed:bottom | 纯文字购买按钮（底部固定）|

### 4.5 弹窗类（alert / purchase-alert / retain-alert）

| Kit 名称 | category | condition | 说明 |
|---------|---------|-----------|------|
| `kit-choose-grade-popup` | purchase-alert | max:1, fixed:center | 年级选择弹窗（购买前）|
| `kit-age-input` | purchase-alert | max:1, fixed:center, type:alert | 年龄输入弹窗 |
| `kit-home-popup` | alert | max:1, fixed:center, type:alert | 首页进入时的弹窗（活动/留资）|
| `kit-questionnaire-popup` | purchase-alert | max:1, fixed:center | 问卷调查弹窗 |
| `kit-alert-retain` | retain-alert | max:1, fixed:center, type:alert | 用户离开时的留存弹窗 |
| `kit-alert-home-retain` | retain-alert | max:1, fixed:center | 首页留存弹窗（变体）|

### 4.6 信息展示类（other）

| Kit 名称 | category | condition | 说明 |
|---------|---------|-----------|------|
| `kit-count-down` | other | 无 | 倒计时（活动截止/限时优惠）|
| `kit-home-count-down` | other | 无 | 首页倒计时（变体）|
| `kit-discount` | other | max:1 | 折扣信息展示（如"原价299 现价99"）|
| `kit-order-info` | other | 无 | 订单信息展示 |

### 4.7 表单类（form）

| Kit 名称 | category | condition | 说明 |
|---------|---------|-----------|------|
| `kit-login` | form | 无 | 登录组件（购买链路内嵌登录）|
| `kit-student-info` | form | 无 | 学生信息填写（姓名/年级/班级/学校）|

### 4.8 功能辅助类

| Kit 名称 | category | condition | 说明 |
|---------|---------|-----------|------|
| `kit-select-address` | — | 无 | 地址选择（实体商品场景）|
| `kit-payment-type` | — | 无 | 支付方式选择（微信/支付宝/IAP）|
| `kit-drop-placeholder` | — | 无 | 后台编辑态拖拽占位符，C 端不渲染 |

---

## 5. Kit 组件被消费的方式

### detail.vue（落地页主页）

```js
// 从 API 拿 renderList
computed.renderList = pageInfo.componentList  // [{ name, state }, ...]
```

```html
<!-- 遍历渲染 -->
<render-element v-for="kit in renderList" :kit="kit" />
```

编译条件控制：`v-if="$mp.query.kitName === kit.name"`（小程序条件编译，用于单 Kit 调试）

### _element.vue（Kit 渲染分发器）

当前实现：对每个 Kit name 硬写 `v-if` 分支：
```html
<kit-button-price v-if="kit.name === 'kit-button-price'" v-bind="kit.state" />
<kit-image-home   v-if="kit.name === 'kit-image-home'"   v-bind="kit.state" />
<!-- ... 34 个 if ... -->
```

更优实现（未改）：
```html
<component :is="kitClient.getVM(kit.name)" v-bind="kit.state" />
```

---

## 6. 新增 Kit 的步骤

1. 在 `src/kitTemplate/` 下新建目录：`kit-xxx/`
2. 在目录中创建 `config.json`（必填字段：name、cnName、category）
3. 创建 `view.vue`（必须接受 `preview: Boolean` prop）
4. 可选：创建 `content.vue`（后台编辑态）
5. **必须手动**在 `_element.vue` 里加一个 `v-if kit.name === 'kit-xxx'` 分支（否则不会渲染）

注：步骤 5 是当前的已知"弱点"，理想情况下应该自动化。
