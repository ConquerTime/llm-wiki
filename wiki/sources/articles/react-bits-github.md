---
title: React Bits — React 模式、反模式与技巧合集
type: source
subtype: article
tags: [programming, react, antipatterns]
created: 2026-04-28
updated: 2026-04-28
author: Vasa (vasanthk)
url: https://github.com/vasanthk/react-bits
date: 2017
sources:
  - "[[../../raw/articles/react-bits/README.md|React Bits README]]"
  - "[[../../raw/articles/react-bits/anti-patterns/01.props-in-initial-state.md|Props in Initial State]]"
  - "[[../../raw/articles/react-bits/anti-patterns/02.findDOMNode.md|findDOMNode]]"
  - "[[../../raw/articles/react-bits/anti-patterns/03.mixins.md|Mixins]]"
  - "[[../../raw/articles/react-bits/anti-patterns/04.setState-in-componentWillMount.md|setState in componentWillMount]]"
  - "[[../../raw/articles/react-bits/anti-patterns/05.mutating-state.md|Mutating State]]"
  - "[[../../raw/articles/react-bits/anti-patterns/06.using-indexes-as-key.md|Using Indexes as Key]]"
  - "[[../../raw/articles/react-bits/anti-patterns/07.spreading-props-dom.md|Spreading Props on DOM]]"
  - "[[../../raw/articles/react-bits/gotchas/01.pure-render-checks.md|Pure Render Checks]]"
---

# React Bits — React 模式、反模式与技巧合集

> GitHub 17k+ 星的社区合集，用**给反模式起名字**的方式把 React 组件层的常见坑整理成词典。成书于 2017 Class 组件时代，部分条目已过时，但"反模式 → 好代码"的对照范式与**本 wiki 的反模式笔记方法论同源**。

## 核心论点

react-bits 不提供统一架构主张，而是一本**词典式的坑点手册**。它回答：

- 什么样的 React 代码是"坏味道"？
- 对应的"好味道"长什么样？
- 为什么这是坏的（原理层面）？

把反模式命名并配对重构示例，使 code review 有了可指认的词汇：不用说"这里看着不对劲"，可以说"这是 Props in Initial State"。

## 7 个反模式摘录

### Anti-Pattern 1: Props in Initial State

> Using props to generate state in getInitialState often leads to duplication of "source of truth".
> Because getInitialState is only invoked when the component is first created, the new prop value will never be displayed if props change.

**坏**：
```javascript
constructor(props) {
  super(props);
  this.state = { inputVal: props.inputValue };
}
render() { return <div>{this.state.inputVal && <AnotherComponent/>}</div>; }
```

**好**：直接用 `this.props.inputValue`，不要把 prop 镜像到 state。

**Hooks 时代对等形态**：`const [value, setValue] = useState(props.value)` —— props 变化时 `useState` 初始值不会重跑。常见于 form 和"受控/非受控混用"。React 官方 "You Might Not Need an Effect" 文档把这类问题称为 **derived state**。

---

### Anti-Pattern 2: findDOMNode()

Class 组件访问 DOM 的废弃 API。React 18 deprecated，React 19 移除。

**修复方向**：callback refs → 现代 `useRef` + `forwardRef`。

---

### Anti-Pattern 3: Mixins

旧 `React.createClass({mixins: [...]})` 的逻辑复用机制。Hooks 出现后这个模式已死，用自定义 Hook 替代。

> See [Mixins are dead - Long live higher order components](https://medium.com/@dan_abramov/mixins-are-dead-long-live-higher-order-components-94a0d2f9e750)

---

### Anti-Pattern 4: setState() in componentWillMount()

> componentWillMount is invoked immediately before mounting. It is called before render(), therefore setting state in this method will not trigger a re-render.

`componentWillMount` 已废弃，该反模式实际失效。但其"不该在错误的生命周期做异步初始化"的内核映射到 Hooks：**不要在 render body 里做 side effect**，应该放 `useEffect`。

---

### Anti-Pattern 5: Mutating State without setState()

> Causes state changes without making component re-render. Whenever setState gets called in future, the mutated state gets applied.

**坏**：
```javascript
this.state.items.push('lorem');
this.setState({ items: this.state.items });
```

**好**：
```javascript
this.setState(prevState => ({
  items: prevState.items.concat('lorem')
}));
```

**Hooks 时代仍适用**：`useState` 下直接 mutate 数组/对象不会触发 re-render（引用没变，`Object.is` 相等）。Immer 的使命就是让"看起来像 mutate 的写法"在底层变成 immutable 更新。

---

### Anti-Pattern 6: Using Indexes as Keys

> Keys should be stable, predictable, and unique so that React can keep track of elements.

**坏**：`<Todo key={index}/>` —— 插入/删除/重排时 key 和内容错配，导致 React 复用错节点
**好**：`<Todo key={todo.id}/>` —— 用数据本身的稳定 id

**100% 跨时代适用**。Hooks 没改变这一点，反而因为函数组件写法更短，更多人不假思索用 index。

---

### Anti-Pattern 7: Spreading Props on DOM Elements

> When we spread props we run into the risk of adding unknown HTML attributes.

**坏**：
```javascript
const Spread = (props) => (<div {...props}>Test</div>);
// 调用 <Spread flag={true} className="content"/> → flag 会被渲染为 DOM 属性
```

**好**：用 `...rest` 解构剔除非 DOM prop：
```javascript
const Spread = ({ flag, ...domProps }) => (<div {...domProps}>Test</div>);
```

**Hooks / TS 时代加强**：TypeScript 能把非 DOM props 静态筛掉（`ComponentProps<'div'>`），但 runtime 仍需配合 rest 解构。

## Gotcha: Pure Render Checks

`shouldComponentUpdate` / `PureComponent` 的陷阱：**在 render 里创建新引用**会让浅比较恒为 false，优化失效。

### 问题 1：`||` 默认值

```javascript
// 坏：每次 render 都创建新数组
<Cell options={this.props.options || []}/>

// 好：把默认值常量化
const defaultval = [];
<Cell options={this.props.options || defaultval}/>
```

### 问题 2：render 里新建函数

```javascript
// 坏：每次 render 都创建新函数
<MyInput onChange={e => this.props.update(e.target.value)}/>
<MyInput onChange={this.update.bind(this)}/>

// 好：构造器里绑定一次
constructor() { this.update = this.update.bind(this); }
<MyInput onChange={this.update}/>
```

### 问题 3：render 里新建对象

```javascript
// 坏
const options = this.props.options || {test: 1};
// 好：类字段
options = {test: 1};
render() { const options = this.props.options || this.options; }
```

**Hooks 时代对等形态**：这些陷阱在 `React.memo` + `useCallback` / `useMemo` 下依然存在。所有 "child 被 `React.memo` 包了但仍在重渲染"的问题，十有八九是父组件在 render 里传了新引用。

## 提到的实体

- **Dan Abramov** — 在链接的 "Mixins are dead" 博客和 React 官方 "Mixins considered harmful" 中多次出现
- **Kent C. Dodds** — 在 spread props 讨论中被引用（"children are just props"）

（两人在 React 社区都是顶级权威，但本次仓库仅为引用关系，不值得新建实体页；如果之后有专题资料再建）

## 提到的概念

- [[react-classic-antipatterns|React 经典反模式]] — 本资料的主要贡献（在本 wiki 中提炼的版本）
- [[react-page-state-antipatterns|React 页面状态管理反模式]] — 互补的"页面层"反模式视角
- [[feature-based-architecture|Feature-Based 架构]] — 更高层的组织模式

## 时代背景说明

- 仓库最后实质性更新在 2017–2018 年
- 示例全部用 Class 组件 / `React.createClass`
- 但"给反模式命名 + 配对 Good/Bad 代码"的**方法论至今不过时**
- 部分条目（findDOMNode / Mixins / componentWillMount）读作**历史档案**即可；其余在 Hooks 时代仍高度相关
