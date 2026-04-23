# kaigao ECS 部署方案与迁移配置经验

> 来源：kaigao 项目 2026-04 ECS 迁移，从阿里云 SAE 迁移到 ECS + docker-compose 方案的完整过程记录。

---

## 背景：为什么从 SAE 迁移到 ECS

项目原部署在阿里云 SAE（Serverless 应用引擎），遇到两个核心问题：

1. **配置复杂**：SAE 控制台操作繁琐，NAT 网关 / CLB / 安全组 / 网关路由需要多处配置，每次变更都容易踩坑（见"SAE 踩坑清单"）
2. **成本偏高**：两个 SAE 应用（api + web）月费 200-400 元，对日访问量仅几万的早期项目不经济
3. **Worker 耦合**：Worker 进程通过 `child_process.spawn` 嵌在 API 进程内，无法独立重启或扩容

迁移到 ECS 后：计算成本降至约 100 元/月，Worker 独立容器，运维更简单。

---

## 项目服务结构

项目是 Monorepo，有以下服务角色：

| 角色 | 入口 | 说明 |
|------|------|------|
| web | Next.js standalone | SSR 前端 + API 代理层 |
| api | Hono (Node.js) | HTTP 业务接口 + 轻量 in-process worker |
| worker | BullMQ Worker | 全文生成（AI 长任务，并发 3）+ 订单恢复 + 分析会话 |
| reduce-worker | BullMQ Worker | 降重任务（并发 2） |

**关键发现**：前端所有 API 请求走相对路径 `/api/xxx`，由 Next.js 内置的 catch-all 代理（`app/api/[...proxy]/route.ts`）转发到后端 Hono。这意味着浏览器不直接访问后端，所有流量入口只需指向 web。

---

## 部署架构

```
Internet
  │
  ▼
ALB (:443, HTTPS 卸载)
  │ /* → ECS:3000
  ▼
ECS 2C4G（docker-compose）
  ┌────────┐  ┌──────────────────────────────────────────┐
  │  web   │  │  api  │  worker  │  reduce-worker        │
  │ :3000  │  │ :8080 │ (无端口) │  (无端口)              │
  └────────┘  └──────────────────────────────────────────┘
       │ http://api:8080 (docker 内网)
       ▼
  Hono API

  ↓ 内网
PolarDB + Redis + OSS（保持现有托管服务）
```

**核心设计决策**：

1. **ALB 只需一个服务器组**：指向 web:3000，API 流量由 Next.js 代理层处理，不需要 ALB 路径分流
2. **api 不暴露端口到宿主机**：`docker-compose.yml` 中 api 服务不写 `ports`，只在 docker 网络内可达
3. **同一镜像、不同 command**：worker 和 reduce-worker 复用 `kaigao-api` 镜像，通过 docker-compose `command` 字段指定入口

---

## docker-compose.prod.yml

```yaml
services:
  web:
    image: registry.cn-hangzhou.aliyuncs.com/zydddd/kaigao-web:latest
    ports:
      - "3000:3000"
    restart: always
    env_file: .env.prod
    environment:
      API_BASE_URL: "http://api:8080"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    depends_on:
      api:
        condition: service_healthy
    networks:
      - kaigao-net

  api:
    image: registry.cn-hangzhou.aliyuncs.com/zydddd/kaigao-api:latest
    command: ["node", "dist/server.js"]
    restart: always
    env_file: .env.prod
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    networks:
      - kaigao-net

  worker:
    image: registry.cn-hangzhou.aliyuncs.com/zydddd/kaigao-api:latest
    command: ["node", "dist/worker.js"]
    restart: always
    env_file: .env.prod
    depends_on:
      api:
        condition: service_healthy
    networks:
      - kaigao-net

  reduce-worker:
    image: registry.cn-hangzhou.aliyuncs.com/zydddd/kaigao-api:latest
    command: ["node", "dist/reduce-worker.js"]
    restart: always
    env_file: .env.prod
    depends_on:
      api:
        condition: service_healthy
    networks:
      - kaigao-net

networks:
  kaigao-net:
    driver: bridge
```

**要点**：
- `api` 没有 `ports` 字段 → 不暴露到宿主机
- `worker` / `reduce-worker` 用 `depends_on: api: condition: service_healthy` → 等 API 完成数据库迁移后才启动
- `web` 的 `API_BASE_URL` 设为 `http://api:8080` 使用 docker service name 寻址

---

## 代码层面需要做的事

### 1. 从 server.ts 移除 spawn worker

```diff
- import { spawn } from 'child_process'
- let restartCount = 0
- function startWorker() { ... spawn(...) ... }

  async function main() {
    ...
    serve(...)
-   startWorker()   // 删除，改由 docker-compose 独立容器管理
    startCreditReconcile()  // 保留：轻量 cron
  }
```

**为什么**：spawn 方式的 worker 和 API 进程耦合，崩了一个影响另一个，且无法独立重启。docker-compose 独立容器隔离更彻底，`restart: always` 自动重启。

### 2. tsup 补全 reduce-worker 入口

```diff
  entry: ['src/server.ts', 'src/worker.ts', 'src/reduce-worker.ts'],
```

### 3. API Dockerfile 安装 curl

```diff
  FROM node:22-alpine AS runner
  ENV NODE_ENV=production
+ RUN apk add --no-cache curl
```

原因：docker-compose healthcheck 用 `curl -f http://localhost:8080/health`，alpine 镜像默认没有 curl。

---

## ALB 配置

只需一个监听器 + 一个服务器组：

```
HTTPS :443 → kaigao-web-sg (ECS内网IP:3000)
HTTP  :80  → 重定向到 HTTPS

健康检查: GET / (web 容器)
```

**不需要**按路径分流 `/api/*` → api，因为 Next.js 代理层已经处理了。

### 路由前缀确认

检查 Hono 路由后发现：所有后端路由都带 `/api` 前缀（在各 domain 的 `routes/index.ts` 中通过 `commerceApp.route('/api', ...)` 挂载），所以即使将来要做 ALB 路径分流，也不需要 rewrite。

---

## CI/CD 分工

| 系统 | 职责 | 触发 |
|------|------|------|
| GitHub Actions | PR 质量门禁（format / lint / type-check / test） | PR 到 main / feature/* |
| 云效 Flow | CD（构建镜像 → 推送 ACR → SSH 部署 ECS） | push to main |

**为什么保留两套**：GitHub Actions 的 PR check 已完善，没必要重建。云效 Flow 构建机在阿里云内网，推 ACR 比 GitHub runner 跨境快很多，且原生支持「主机部署」到 ECS，不用配 SSH action。

### 云效 Flow 流水线结构

```
触发: main 分支 push
  │
  ├── Stage 1 (并行)
  │   ├── docker build kaigao-api → push ACR
  │   └── docker build kaigao-web → push ACR
  │
  └── Stage 2
      └── SSH 到 ECS 执行 deploy.sh
```

### deploy.sh（ECS 上执行）

```bash
#!/bin/bash
set -euo pipefail
cd /opt/kaigao
docker compose pull
docker compose up -d
docker image prune -f
sleep 10
docker compose ps
```

幂等性：`docker compose up -d` 对已在运行且镜像未变的容器不做操作。

---

## Web-Worker 架构模式

这种「API + Background Worker」架构的正式名称：

- **Web-Worker Pattern**：HTTP 接口处理请求（producer），Worker 异步消费队列（consumer）
- **Single-image, multi-role**：同一镜像通过启动命令区分角色

这是业界主流做法，Rails/Sidekiq、Django/Celery、Node/BullMQ 都是这个模式。

**同一镜像的好处**：
- Worker 和 API 共享 schema、domain service、类型，版本一致性天然保证
- CI 只构建一次，通过不同 command 启动不同角色
- 代码在同一仓库，开发体验好

**什么时候才需要拆分镜像**：worker 有独立重依赖（ML 库、FFmpeg）、镜像超 1GB、或不同团队独立发布周期。

---

## ECS 安全组配置

| 方向 | 协议 | 端口 | 来源 |
|------|------|------|------|
| 入站 | TCP | 3000 | ALB 安全组 |
| 入站 | TCP | 22 | 运维 IP（可用云助手替代） |
| 出站 | 全部 | 全部 | 0.0.0.0/0 |

**注意**：8080 不对 ALB 开放，API 只在 docker 网络内访问。

---

## SAE 踩坑记录（迁移原因之一）

从原部署手册整理，这些问题在 ECS 方案中不存在：

| 问题 | 原因 |
|------|------|
| SAE 容器默认无公网出口 | 需要 NAT 网关 + EIP + SNAT（ECS 同样需要） |
| Web 无法访问 API | SAE 应用间需要配 CLB 内网转发（ECS 用 docker 网络直连） |
| ALB 503 | SAE 网关路由和 ALB 服务器组容易断开，需要重新保存 |
| 路由 Path `/` 只匹配根路径 | 要用 `/*` 才能匹配所有子路径 |
| SAE 和 PolarDB 不通 | 必须在同一个 vSwitch，不只是同一 VPC |
| ALB 控制台直接修改被覆盖 | SAE 网关路由会覆盖 ALB 配置，只能通过 SAE 控制台操作 |

---

## 费用对比

| 项 | SAE 方案 | ECS 方案 |
|----|---------|---------|
| 计算 | 两个 SAE 应用 ~200-400/月 | ECS 2C4G 包年 ~100/月 |
| ALB | ~10-20/月 | ~10-20/月（不变） |
| PolarDB | 不变 | 不变 |
| Redis | 不变 | 不变 |
| **计算差价** | 200-400 | **100** |

---

## 迁移顺序（关键：可回滚的切换方式）

1. 代码改动（server.ts / tsup / Dockerfile / docker-compose.prod.yml）
2. ECS 购买、安装 Docker、上传配置、手动验证容器启动
3. ALB 新建服务器组指向 ECS，不切流量
4. ALB 转发规则切换到新服务器组（此时可立即回切）
5. 验证全链路正常后，再下线 SAE
6. 建云效 Flow 流水线

**回滚**：步骤 4 之前，SAE 一直在运行。步骤 4 后出问题，ALB 切回 SAE 服务器组 < 1 分钟。步骤 5 之后不可回滚，需充分验证后再执行。
