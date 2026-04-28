---
title: React 经典反模式（组件层）
type: concept
subtype: programming
tags: [programming, react, antipatterns]
created: 2026-04-28
updated: 2026-04-28
sources:
  - "[[wiki/sources/articles/react-bits-github.md|React Bits]]"
---

# React 经典反模式（组件层）

> 发生在**单个组件内部**的七类经典 React 反模式词典（props 镜像到 state / 直接 mutate / index 作 key / DOM 属性污染 / render 里新建引用等），来自 Class 组件时代但多数在 Hooks 时代仍然成立。与[[react-page-state-antipatterns|页面层反模式]]互补——一个看组件、一个看页面。

## 是什么

React 社区早期（2016–2018）积累了一批**组件编写层面**的反模式。它们都发生在"写一个 React 组件"的尺度，而不是"组织一个页面/应用"的尺度。每一条的结构都是：

1. **坏代码**（Bad）——容易写出来的直觉写法
2. **好代码**（Good）——应该的写法
3. **原理**——为什么坏的那个坏

本页把这七条（加一条性能 gotcha）整理为一个词典，并注明在 **Hooks 时代的对等形态**：部分反模式已随 API 废弃消失，部分只是换了壳继续存在。

## 为什么重要

- **给 code review 提供词汇**：不用泛泛说"这里不对"，可以直指 "index as key" / "derived state" / "mutated state"
- **AI 辅助编码会放大这些反模式**：LLM 倾向"照着 props 建 state"、"用 map index 当 key"——有命名的词典才能在 review 时一眼指出
- **跨 Class/Hooks 的稳定内核**：即使语法更新，背后的模型原理不变（引用比较、快照语义、不可变性）

## 反模式词典

| # | 反模式 | Hooks 时代 | 核心原理 |
|---|-------|-----------|---------|
| 1 | Props in Initial State | ✅ 仍普遍 | state 初始值只算一次，props 后续变化被忽略 |
| 2 | findDOMNode() | ❌ React 19 移除 | — |
| 3 | Mixins | ❌ 已死 | 被 Hooks 替代 |
| 4 | setState in componentWillMount | ❌ API 废弃 | — |
| 5 | Mutating State | ✅ 仍普遍 | 引用不变 → 浅比较为 true → 不触发 re-render |
| 6 | Using Indexes as Key | ✅ 仍普遍 | key 要与数据绑定而非位置绑定，否则 React reconciler 会复用错节点 |
| 7 | Spreading Props on DOM | ✅ 仍普遍 | 非 DOM 属性会被渲染到 HTML 导致警告和语义污染 |
| gotcha | Render 里新建引用（→ 浅比较失效） | ✅ 仍普遍 | `React.memo` / `useMemo` 的隐形杀手 |

### 1. Props in Initial State（Derived State）

**坏**：
```javascript
// Class
constructor(props) {
  super(props);
  this.state = { value: props.initialValue };
}

// Hooks 对等
const [value, setValue] = useState(props.initialValue);
```

**问题**：当 `props.initialValue` 变化时，state 不会更新——state 初始值只在 mount 阶段计算一次。用户以为"这是受控值"，实际上是一次性快照。

**好**：

1. 如果该值只需要读取：直接用 `props.initialValue`
2. 如果需要本地修改又需要跟随 prop 变化：
   - 用 `key` 属性强制组件重建（最干净）
   - 或用 `useEffect` 同步（下策，容易失控）
   - React 18.3+ 可用 `useState` + 比较 prev prop 的模式

**React 官方术语**：Derived State。官方文档 *You Might Not Need an Effect* 专门批驳这种写法。

### 2 / 3 / 4. 历史反模式

`findDOMNode()` / `Mixins` / `componentWillMount` 都随 API 废弃而消失，仅作历史档案保留。它们留下的教训：

- **DOM 访问要通过 ref，不要反射式获取节点**（对应 Hooks 的 `useRef` + `forwardRef`）
- **逻辑复用要组合而非继承**（Mixins 是继承思路，Hooks 是组合思路）
- **副作用要放对生命周期**（Class 的 `componentDidMount` / Hooks 的 `useEffect`）

### 5. Mutating State without setState()

**坏**：
```javascript
// Class
this.state.items.push('x');
this.setState({ items: this.state.items });

// Hooks 对等
items.push('x');
setItems(items);  // 引用没变 → React 不重渲染
```

**原理**：React 的 `setState` / `set*` 判断"是否要重渲染"用的是 `Object.is` 浅比较。数组/对象被 mutate 后引用不变，比较返回 true，组件**不重渲染**。但下次其它 state 更新触发 render 时，mutate 后的值会突然"浮现"，造成"bug 看起来是异步的"。

**好**：永远返回新引用：
```javascript
setItems(prev => [...prev, 'x']);
setUser(prev => ({ ...prev, name: 'new' }));
```

或用 [Immer](https://immerjs.github.io/immer/) 把"看似 mutate 的写法"自动转 immutable：
```javascript
import produce from 'immer';
setState(produce(draft => { draft.items.push('x'); }));
```

### 6. Using Indexes as Keys

**坏**：
```javascript
{todos.map((todo, index) => <Todo {...todo} key={index}/>)}
```

**问题**：当列表插入/删除/重排时，第 N 个位置的 key 不变但对应的数据变了——React reconciler 会**复用错节点**，导致：
- 表单内部 state 错乱（前一行的 input 值跑到下一行）
- 动画从错误起点开始
- 组件 state 跟不上数据（依赖变了但 didMount 没重跑）

**好**：用数据自身的稳定 id：
```javascript
{todos.map(todo => <Todo {...todo} key={todo.id}/>)}
```

**什么情况下 index 是安全的**：列表**只追加、从不重排或从中间删除**，且每项组件**无内部 state**。但这种条件很脆，默认不要用。

### 7. Spreading Props on DOM Elements

**坏**：
```javascript
const Sample = () => <Spread flag={true} className="content"/>;
const Spread = (props) => <div {...props}>Test</div>;
// → <div flag="true" class="content"> 渲染出无效 HTML 属性
```

**好**：用 rest 解构剔除非 DOM props：
```javascript
const Spread = ({ flag, ...domProps }) => <div {...domProps}>Test</div>;
```

**TS 时代加强**：用 `React.ComponentProps<'div'>` 静态约束 DOM 属性集合：
```typescript
type Props = { flag: boolean } & React.ComponentProps<'div'>;
```

### Gotcha: Render 里新建引用

这不算"反模式"而是"优化失效"，但后果常被误诊为"memo 不生效"。

**问题**：`React.memo` / `PureComponent` 用浅比较决定是否重渲染。任何在 render body 里新建的数组 / 对象 / 函数都会让比较恒 false。

```javascript
// 坏
function Parent() {
  return <Child options={props.opts || []} onClick={e => doThing(e)}/>;
  //                              ^^            ^^^^^^^^^^^^^^^^^^^^^
  //                    每次 render 新数组       每次 render 新函数
}

// 好
const DEFAULT_OPTS = [];  // 模块级常量

function Parent() {
  const handleClick = useCallback(e => doThing(e), []);
  const opts = props.opts ?? DEFAULT_OPTS;
  return <Child options={opts} onClick={handleClick}/>;
}
```

**进阶**：现代 React Compiler（React Forget，2024+）会自动 memo 化这些，但在它普及前，`useMemo` / `useCallback` + 模块级常量仍是基础功。

## 与页面层反模式的边界

本页 vs [[react-page-state-antipatterns|页面状态反模式]]：

| 维度 | 本页（经典反模式） | 页面层反模式 |
|------|------------------|------------|
| 尺度 | 单组件内部（10–50 行） | 整页面（200+ 行） |
| 典型病灶 | props/state/render/key | URL/state/session 合并、状态机散布 |
| 触发时机 | 写组件时 | 页面长期演化后 |
| 治理工具 | 语法级纪律 | 架构级重构 |

两套反模式可以**叠加存在**：一个页面可能同时有"字段级三源合并"（页面层）和"render 里新建对象导致 memo 失效"（组件层）。

## 开放问题

- **React Compiler 普及后，gotcha 中的 `useMemo`/`useCallback` 还有必要吗？** 目前（2026）React Compiler 的覆盖率和稳定性还在爬坡，**手写 memoization 仍是兜底**。
- **Immer 是否应该成为默认工具？** 社区分歧：喜欢显式的人认为 spread 足够清晰，Immer 是隐式魔法；喜欢工效的人认为深层更新的 spread 嵌套比 Immer 更危险。本 wiki 倾向：**有深层更新就上 Immer**，浅结构用 spread。

## 相关概念

- [[react-page-state-antipatterns|React 页面状态管理反模式]] — 互补的页面级视角
- [[feature-based-architecture|Feature-Based 架构]] — 组件之上的组织层
- [[refactoring|重构]] — 通用方法论
- [[clean-code|整洁代码]] — SOLID / DRY / YAGNI 上位原则

## 来源

- [[wiki/sources/articles/react-bits-github.md|React Bits]]（2017 年汇编，反模式命名的经典源头）
