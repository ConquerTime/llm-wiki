---
title: 金丝雀部署（Canary Deployment）
type: concept
subtype: programming
tags: [programming, deployment, devops]
created: 2026-04-18
updated: 2026-04-18
sources: []
---

# 金丝雀部署（Canary Deployment）

> 将新版本先推给一小部分真实用户，通过监控指标决定是否扩大流量——把风险控制在可接受范围内的渐进式发布策略。

## 是什么

**金丝雀部署**得名于矿工用金丝雀检测矿洞毒气的做法：金丝雀先进去，没事了人再进。类比到软件发布，新版本先暴露给少量用户，通过观察错误率、延迟、业务指标来判断是否安全，再逐步扩大比例。

### 与其他发布策略的对比

| 策略 | 做法 | 风险 | 回滚速度 |
|---|---|---|---|
| 全量发布（Big Bang）| 直接替换所有实例 | 高，故障影响全部用户 | 慢（需重新部署） |
| 蓝绿部署（Blue-Green）| 两套完整环境，切换负载均衡 | 中，切换时全量 | 快（切回蓝环境） |
| **金丝雀部署**| 新版本承载小比例流量 | 低，故障只影响少数用户 | 快（缩流量到 0%） |
| 功能开关（Feature Flag）| 代码级别控制特性开关 | 低 | 即时（改配置） |
| 滚动更新（Rolling Update）| 逐个替换实例 | 中，过渡期新旧版本并存 | 中 |

金丝雀部署的核心优势：**用真实生产流量验证，同时把爆炸半径控制到最小**。

## 架构原理

### 基本流程

```
                        ┌─────────────────┐
                        │   负载均衡 / 网关  │
                        └────────┬────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │ 95% 流量         │                  │ 5% 流量
              ▼                  │                  ▼
    ┌──────────────────┐         │       ┌──────────────────┐
    │   稳定版 v1.0    │         │       │   金丝雀 v1.1    │
    │  (大多数实例)    │         │       │   (少量实例)     │
    └──────────────────┘         │       └──────────────────┘
                                 │                  │
                        监控系统持续观察              │
                        - 错误率                     │
                        - P99 延迟                   │
                        - 业务指标（转化率等）        │
                                 │
              ┌──────────────────┴──────────────────┐
              │ 指标正常                             │ 指标异常
              ▼                                      ▼
     继续扩大金丝雀比例                         回滚：将金丝雀
     5% → 25% → 50% → 100%                   流量缩减至 0%
```

### 流量切分方式

流量切分是金丝雀的核心机制，有几种不同粒度：

**1. 实例比例切分（最简单）**

用实例数量控制比例。10 个实例，1 个跑 v1.1，负载均衡轮询，约 10% 流量到新版本。

```
instances:
  v1.0: 9 replicas  # 90% 流量
  v1.1: 1 replica   # 10% 流量
```

缺点：粒度粗，比例不精确，同一用户可能同时命中新旧版本（体验不一致）。

**2. 负载均衡权重（精确比例）**

在负载均衡层设置流量权重，与实例数解耦：

```yaml
# Nginx upstream 权重
upstream backend {
    server v1.0:8080 weight=95;
    server v1.1:8080 weight=5;
}
```

**3. Header / Cookie 路由（精准定向）**

将特定用户群固定路由到金丝雀版本，保证单个用户体验一致：

```yaml
# Kong / Istio VirtualService
- match:
    - headers:
        x-canary:
          exact: "true"
  route:
    - destination:
        host: backend-v1.1
- route:
    - destination:
        host: backend-v1.0
      weight: 95
    - destination:
        host: backend-v1.1
      weight: 5
```

常见路由规则：
- 内部员工（通过 user_id 或特殊 Header）
- 特定地区的用户
- VIP 用户 / 测试用户群
- 随机 5% 用户（通过 Cookie 固定，同一用户每次都进金丝雀）

## 关键组件

### 1. 流量路由层

执行流量切分决策的组件：

- **服务网格（Istio / Linkerd）**：在 sidecar proxy 层拦截流量，规则灵活，支持 Header/Cookie/权重
- **API 网关（Kong / APISIX / Nginx）**：在入口处做路由，适合 HTTP 服务
- **Kubernetes Ingress**：`nginx-ingress` 支持 canary annotation
- **云平台负载均衡**：AWS ALB / GCP Load Balancer 原生支持权重路由

### 2. 监控与指标

没有监控的金丝雀是盲目的。关键指标分三层：

```
业务层：转化率、下单率、支付成功率（最能反映真实问题）
    ↑
应用层：HTTP 5xx 错误率、P99/P95 延迟、异常日志
    ↑
基础层：CPU、内存、GC 停顿、连接池饱和度
```

金丝雀版本的这些指标必须与稳定版**实时对比**，而不是看绝对值。

### 3. 自动分析（可选）

高级金丝雀系统会自动分析指标并决策是否继续推进：

```
Kayenta（Netflix 开源）/ Argo Rollouts Analysis：
1. 定义成功标准：canary 错误率 < baseline * 1.2
2. 自动运行分析：每 N 分钟采样一次
3. 自动决策：
   - 连续 X 次分析通过 → 自动提升比例
   - 任意一次分析失败 → 自动回滚
```

## 在 Kubernetes 中的实现

### 方案 A：原生 Deployment（简单）

```yaml
# stable deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: backend
      version: stable
  template:
    metadata:
      labels:
        app: backend
        version: stable
    spec:
      containers:
        - name: backend
          image: backend:v1.0

---
# canary deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-canary
spec:
  replicas: 1          # 10% 流量（1/10 实例）
  selector:
    matchLabels:
      app: backend
      version: canary
  template:
    metadata:
      labels:
        app: backend
        version: canary
    spec:
      containers:
        - name: backend
          image: backend:v1.1

---
# Service 同时选中两个 Deployment（通过 app: backend 标签）
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  selector:
    app: backend   # 不区分 version，流量按实例数比例分配
```

### 方案 B：Argo Rollouts（推荐）

Argo Rollouts 是 Kubernetes 的渐进式交付控制器，直接内置金丝雀策略：

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: backend
spec:
  strategy:
    canary:
      steps:
        - setWeight: 5      # Step 1: 5% 流量给金丝雀
        - pause: {duration: 10m}  # 等待 10 分钟观察
        - setWeight: 25     # Step 2: 扩大到 25%
        - pause: {duration: 10m}
        - setWeight: 50
        - pause: {}         # 手动确认才继续
        - setWeight: 100    # 全量发布
      analysis:             # 自动分析（可选）
        templates:
          - templateName: error-rate
        startingStep: 1
```

**回滚只需一条命令：**

```bash
kubectl argo rollouts abort backend   # 立即将金丝雀流量缩至 0
kubectl argo rollouts undo backend    # 回滚到上一个稳定版本
```

### 方案 C：Istio VirtualService（精细流量控制）

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: backend
spec:
  hosts:
    - backend
  http:
    - match:
        - headers:
            cookie:
              regex: ".*canary=true.*"  # 有 canary cookie 的用户
      route:
        - destination:
            host: backend
            subset: v1-1
    - route:
        - destination:
            host: backend
            subset: v1-0
          weight: 95
        - destination:
            host: backend
            subset: v1-1
          weight: 5
```

## 金丝雀的执行流程（实战）

```
1. 发布前准备
   ├── 确认监控 Dashboard 和告警规则已就位
   ├── 准备回滚 runbook（出了问题怎么操作）
   └── 定义成功标准（错误率 < X%，P99 < Xms）

2. 初始投放（1%-5%）
   ├── 先放内部员工流量（dogfooding）
   ├── 观察 15-30 分钟
   └── 检查日志有无明显错误

3. 逐步扩大
   ├── 5% → 25% → 50% → 100%
   ├── 每个阶段观察 10-30 分钟
   └── 对比新旧版本各项指标

4. 全量或回滚
   ├── 指标正常 → setWeight: 100，删除旧版本
   └── 指标异常 → abort，通知团队，分析原因
```

## 常见陷阱

**陷阱 1：数据库 Schema 变更**

金丝雀期间新旧版本同时运行，如果 v1.1 做了不向后兼容的数据库变更（删列、改类型），v1.0 实例会报错。

解决：**展开式迁移（Expand-Contract 模式）**
```
Phase 1（发布前）: 添加新列（不删旧列）→ 新旧版本都能运行
Phase 2（金丝雀完成）: 删除旧列
```

**陷阱 2：Session / 有状态请求**

用户在 v1.0 建立的 session，下一个请求路由到 v1.1 可能因格式不兼容而失败。

解决：Session 序列化格式向后兼容，或用 Cookie 将用户固定到同一版本。

**陷阱 3：比例太低，样本不足**

1% 的流量样本量太小，指标波动大，难以判断是版本问题还是噪声。

解决：至少 5%，或等待足够长时间积累样本（通常 15-30 分钟）。

**陷阱 4：只看技术指标，忽略业务指标**

错误率 0%、延迟正常，但转化率下降了 10%——这是更隐蔽的问题。

解决：监控 Dashboard 必须包含核心业务指标。

## 相关概念

- [[monolith-async-worker|Monolith with Async Worker]] — 部署架构演进的起点
- [[message-queue|消息队列]] — 金丝雀期间异步任务的版本兼容问题
- [[read-after-write|写后读问题]] — 新旧版本并存时的数据一致性挑战
