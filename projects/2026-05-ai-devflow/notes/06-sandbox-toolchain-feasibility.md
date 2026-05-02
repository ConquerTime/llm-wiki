# v6: Ephemeral Sandbox + 工具链实现与可行性

> **触发问题**: 迭代场景下 Sandbox 怎么不腐化? 工具链怎么实现? 可行性如何?
> **结论信心度**: 中 — 技术路径清晰,但三个前置条件苛刻,真实团队多数不满足
> **后续**: 这一版是目前阶段最新的结论。需要真实试点验证。

## 腐化问题的根源: Sandbox 的定位错了

v4-v5 把 Sandbox 定位为"**持久的探索仓库**"——隐含假设"每个功能只探索一次"。现实中产品持续迭代,这个假设会崩。

**正确的定位**: Sandbox 是**生产环境在某个时间点的"可分叉镜像"**——探索时从生产 fork 出来,探索完销毁,结果回流生产。

| 错误类比 | 正确类比 |
|---|---|
| Sandbox 像"开发分支" | Sandbox 像"React DevTools 里的 time-travel 快照" |
| 长期存在、持续维护 | 按需创建、用完即焚 |
| 有自己的生命 | 是生产的临时镜像 |

## 新架构: Ephemeral Sandbox + Fork-from-Production

```
生产代码库 (main)
     │
     │  产品发起迭代
     ▼
Sandbox 自动 fork (从 main 最新状态)
├─ 完整复制生产 UI 组件和 design system
├─ 自动把真实 API 替换为 mock（基于生产契约生成）
├─ 保留生产的路由、auth、交互范式
└─ 开启产品的自由探索区：只能改指定范围
     │
     │  产品探索（天/周级）
     │  自动捕获 L0-L6 brief
     ▼
Promotion: diff 回生产
     │
     ▼
Sandbox 销毁 / 归档
```

**两种迭代场景**：

- **场景 A：改进现有功能** — fork 当前生产状态,只允许改该功能对应的 writable paths
- **场景 B：探索全新功能** — 继承生产 shell/auth/design system,新功能在独立路由挂载

两场景的共同点：**Sandbox 始终以当前生产为基底**，不会漂移。

## 整体工具链架构分层

```
L4: Brief 自动汇总（锦上添花）
    trace → E2E 转换、AI 摘要生成

L3: 运行时捕获（Brief 主要来源）
    DevRecorder、snapshot、decision commit hook

L2: Rebase + 归档（长期健康度）
    sandbox:rebase、expiration、archive

L1: Fork + Manifest + CI Guard（核心护栏）
    sandbox:fork、manifest 校验、mock 生成
```

**L1 是必做，其他都是可选**。只要 L1 能跑，架构骨架就立起来了。

## L1: Fork + Manifest + CI Guard（MVP 核心）

### 用户体验

```bash
$ pnpm sandbox:fork --feature notify-pref

✓ Reading production contracts from contracts/openapi.yaml
✓ Generating mocks at apps/sandbox/mocks/notify-pref/
✓ Creating manifest at apps/sandbox/current.yaml
✓ Creating branch: sandbox/notify-pref-2026-05-01
✓ Sandbox ready at: http://localhost:3001/notify-pref
```

### 实现选型

**形态**: monorepo 子目录（推荐），能直接 import 生产组件。

```
apps/
├── web/              # 生产应用
├── api/              # 生产后端
└── sandbox/          # Sandbox 应用
    ├── src/
    │   ├── shell/    # readonly: 从 web 软链或复制
    │   ├── features/ # writable: 产品探索区
    │   └── mocks/    # 自动生成
    └── current.yaml  # manifest
```

**Mock 生成选型**：

| 契约格式 | 推荐工具 |
|---|---|
| OpenAPI | Prism + openapi-typescript |
| tRPC | 手写 mock，类型从 router 推导 |
| GraphQL | MSW + graphql-codegen |

**MSW 是核心选型**——service worker 层拦截请求，不需改应用代码。

### Manifest 机制

```yaml
# apps/sandbox/current.yaml
forked_from: main@abc123
forked_at: 2026-05-01
expires: 2026-05-29
feature: notify-pref

writable_paths:
  - "apps/sandbox/src/features/notify-pref/**"
  - "apps/sandbox/mocks/notify-pref/**"
  - "apps/sandbox/e2e/notify-pref/**"

readonly_paths:
  - "apps/sandbox/src/shell/**"
  - "apps/sandbox/src/design-system/**"
```

### CI Guard

```yaml
# .github/workflows/sandbox-guard.yml
on: { pull_request: { branches: [main] } }
jobs:
  guard:
    if: startsWith(github.head_ref, 'sandbox/')
    steps:
      - name: Check writable paths
        run: node scripts/sandbox-guard.js
```

```javascript
// 核心逻辑 ~30 行
const changed = execSync('git diff --name-only origin/main...HEAD').toString().split('\n')
const violations = changed.filter(path => {
  const writable = manifest.writable_paths.some(p => minimatch(path, p))
  return !writable
})
if (violations.length) process.exit(1)
```

**工程量**：核心脚本 2-3 天，调试 + 集成 1 周。

## L2: Rebase + 归档

```bash
$ pnpm sandbox:rebase
✓ Fetching main
✓ Regenerating mocks from latest contracts
✓ Merging main into sandbox/notify-pref-2026-05-01
  ⚠ Conflict in: Sheet.tsx (组件 API 变了)
```

归档机制：Sandbox 过期后不删,归档到 `archives/` + 打 git tag。下次迭代同功能时能提示历史 Brief。

**工程量**: Rebase 2 天 + 归档 1-2 天 + 过期检测半天。

## L3: 运行时捕获

**交互 trace**: Rrweb（日常录制）+ Playwright codegen（正式 E2E）。

**组件树快照**: 建议 MVP 跳过,信息大部分能从 trace + 代码得到。

**Decision commit hook**: Husky + 一个脚本,30 秒记录。

## L4: Brief 自动汇总

**Trace → E2E spec**: Playwright codegen 直接产出。

**AI 摘要生成**: 调用 LLM 消费 brief/ 全部产物生成 SUMMARY.md。

## 总体工程量评估

| 层 | 工程量 | 必要性 |
|---|---|---|
| L1 Fork + Guard | 1-2 周 | 必做 |
| L2 Rebase + 归档 | 3-5 天 | 强烈建议 |
| L3 Trace + Decision hook | 2-3 周 | 建议 |
| L3 组件树快照 | 2-4 周 | 可选（跳过） |
| L4 Trace → E2E | 3-5 天 | 可选 |
| L4 AI 摘要 | 1-2 周 | 可选 |

**合计**：
- **MVP（L1 + 基础 L3）**: 3-4 周（单人 full-time）
- **完整版**: 3-4 个月

## 最大的四个坑

### 坑 1: 没有契约单一事实源（最致命）

如果生产 API 是手写 Express + 手写类型,那 Mock 生成无从下手。**必须先做契约化改造**,这可能比 Sandbox 工具本身工作量还大。

### 坑 2: 生产组件库不成熟

Sandbox 假设"产品能用生产组件快速拼原型"。若组件库残缺,产品一上来就得研发补组件,Sandbox 的速度优势没了。

### 坑 3: Rebase 冲突频繁

生产代码改动很快（月 100+ PR）时,Sandbox 存在几周就会频繁冲突。缓解:
- 缩短生命周期（默认 2 周而非 4 周）
- `sandbox:rebase` 每日自动执行
- Writable path 粒度细化

### 坑 4: 产品抵触"命令行"

整套工具链依赖命令行 + git。产品经理可能抵触。解决需要做 UI 封装（VSCode 插件或内部 web 工具）,非必需但体验巨大的投入。

## 可以白嫖的现成方案

| 工具 | 覆盖层 | 局限 |
|---|---|---|
| v0.dev / Bolt / Lovable | 生成 UI 原型 | 不集成生产契约、难迁移 |
| StackBlitz Codeflow | 浏览器 ephemeral 环境 | 需适配工作流 |
| Gitpod / Devcontainer | Ephemeral dev 环境 | 只解决环境,不解决 Brief |
| Storybook | 组件级探索 | 只到组件层 |

**现实建议**：
- 原型阶段用 v0/Bolt 做快速 UI 探索
- **配合**自建的 L1 Fork 工具（做正式 Sandbox）
- 两者互补

## 最小可行启动路径

**Week 1**: 检查/建立契约单一事实源；搭 `apps/sandbox`；写 `sandbox:fork` 脚本

**Week 2**: MSW 集成 + mock 自动生成 + Manifest + CI Guard（**MVP 可跑**）

**Week 3-4**: Rebase 命令 + Rrweb 录制 + Decision hook

**Week 5-8**: Playwright codegen 集成 + AI 摘要 + **真实跑一个功能迭代**

**Week 9+**: 根据反馈决定是否做组件树快照、UI 封装

## 当前结论

> **Sandbox 工具链是"工程难度中等，但前置条件严苛"的项目。**
>
> 技术上没有深水区——本质是"git + mock + CI + 脚本"的组合。真正决定可行性的不是工具本身，而是：
> 1. 生产代码是否已有契约单一事实源
> 2. 组件库是否足够成熟
> 3. 团队文化是否接受"产品写代码 + 研发做翻译"
>
> **投资这套工具链之前，先投资这三个前置条件**——它们独立存在也有价值。

## 时间估算

| 团队状态 | Sandbox 工具链落地时间 |
|---|---|
| 已有契约 + 成熟组件库 + 接受新协作模式 | 1-2 个月 |
| 契约不完整 / 组件库初级 | 4-6 个月（含前置改造） |
| 一切从零 | 8-12 个月（更像文化变革） |

## 演进总览（v1 → v6）

| 版本 | 核心贡献 | 被推翻/修正的 |
|---|---|---|
| v1 | 产品 vs 设计师边界初步辨析 | 缺工程细节 |
| v2 | 全栈分工 + AI 穿透能力分层 | 缺可执行机制 |
| v3 | 分支 + CI + 时序图 | 契约先行假设在探索期不成立 |
| v4 | 双空间 Sandbox | Sandbox 定位为持久仓库会腐化 |
| v5 | Brief 的 L0-L6 结构化 | 自动捕获能力的工程门槛未评估 |
| **v6（当前）** | Ephemeral Sandbox + 工具链可行性 | **需真实试点验证** |

## 下一步（项目层面）

所有推演到此。必须**找到真实试点场景**验证 L1 层，不然这套理论到此为止，不进 wiki。

试点候选（暂列）：
- 自有项目：找一个正在起步、有 greenfield 机会的内部项目
- 合作方：找一个愿意尝试的外部团队
- 最小化：只试 L1（Fork + Guard），不上全套

试点成功的标准（待定义）：
- [ ] 产品至少完成一次完整 Sandbox → Promotion → 上线循环
- [ ] CI Guard 至少挡住一次真实的越界写入
- [ ] 产品 & 研发都认为值得继续（主观评价）
