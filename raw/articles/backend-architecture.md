# 后端架构与云服务部署

> 来源：AI 助手使用 gh search 检索 | 更新时间：2026-04-16

---

## 📚 经典书籍

| 书名 | 作者 | 核心理念 |
|------|------|----------|
| 《系统设计》 | ByteByteGo | 大规模系统设计入门 |
| 《Designing Data-Intensive Applications》 | Martin Kleppmann | 数据密集型系统设计 |
| 《构建微服务》 | Sam Newman | 微服务设计与落地 |
| 《架构整洁之道》 | Robert C. Martin | Clean Architecture |
| 《程序员修炼之道》 | Andrew Hunt | 务实软件之道 |

---

## 🌐 开源学习资源

### 后端架构（综合）

| 仓库 | 描述 | ⭐ |
|------|------|-----|
| [afteracademy/nodejs-backend-architecture-typescript](https://github.com/afteracademy/nodejs-backend-architecture-typescript) | Node.js 后端架构完整示例 | 🔥 |
| [fastapi-practices/fastapi-best-architecture](https://github.com/fastapi-practices/fastapi-best-architecture) | FastAPI 企业级后端架构方案 | 🔥 |
| [afteracademy/wimm-apis](https://github.com/afteracademy/wimm-apis) | NestJS 模块化后端开发 | 🔥 |
| [afteracademy/goserve](https://github.com/afteracademy/goserve) | Go 后端架构，REST API | 🔥 |
| [TFdream/awesome-backend-architecture](https://github.com/TFdream/awesome-backend-architecture) | 后端技术栈/中间件/微服务合集 | 🔥 |

### 微服务架构

| 仓库 | 描述 | ⭐ |
|------|------|-----|
| [jhipster/generator-jhipster](https://github.com/jhipster/generator-jhipster) | 微服务生成+部署平台 | 🔥 |
| [sqshq/piggymetrics](https://github.com/sqshq/piggymetrics) | Spring Boot+Spring Cloud+Docker | 🔥 |
| [juicycleff/ultimate-backend](https://github.com/juicycleff/ultimate-backend) | CQRS+GraphQL+微服务+多租户 SaaS | 🔥 |
| [asc-lab/dotnetcore-microservices-poc](https://github.com/asc-lab/dotnetcore-microservices-poc) | .NET Core 微服务保险系统 | 🔥 |
| [mehdihadeli/go-food-delivery-microservices](https://github.com/mehdihadeli/go-food-delivery-microservices) | Go DDD+CQRS+EventSourcing 微服务 | 🔥 |
| [rammyblog/ecommerce-microservice](https://github.com/rammyblog/ecommerce-microservice) | 电商微服务+单体前端 | 🔥 |

### 云架构模式

| 仓库 | 描述 | ⭐ |
|------|------|-----|
| [yeongseon/cloudblocks](https://github.com/yeongseon/cloudblocks) | 可视化云架构学习工具 | 🔥 |
| [ishiharatma/aws-cdk-reference-architectures](https://github.com/ishiharatma/aws-cdk-reference-architectures) | AWS CDK 参考架构 | 🔥 |
| [tasasho/cloud-architecture-pattern](https://github.com/tasasho/cloud-architecture-pattern) | AWS/GCP 云架构模式 | 🔥 |
| [andredesousa/devops-best-practices](https://github.com/andredesousa/devops-best-practices) | DevOps 最佳实践指南 | 🔥 |

### 云原生基础设施

| 仓库 | 描述 | ⭐ |
|------|------|-----|
| [labring/sealos](https://github.com/labring/sealos) | AI 原生云操作系统，基于 K8s | 🔥 |
| [eugenekofi/microservice-infra-3tier](https://github.com/eugenekofi/microservice-infra-3tier) | 3 层云原生架构+可观测性 | 🔥 |
| [TheToriqul/k3s-aws-terraform](https://github.com/TheToriqul/k3s-aws-terraform) | AWS K3s + Terraform IaC | 🔥 |
| [hbinduni/bun-golang-react-monorepo](https://github.com/hbinduni/bun-golang-react-monorepo) | 全栈 Monorepo+Docker+K8s | 🔥 |

---

## ☁️ 云服务部署方案

### AWS

| 服务 | 用途 | 相关仓库 |
|------|------|----------|
| **Lambda** | 无服务器计算 | Serverless 架构示例 |
| **API Gateway** | API 管理 | Serverless 博客平台 |
| **ECS/EKS** | 容器编排 | AWS CDK DevOps |
| **RDS** | 关系数据库 | — |
| **DynamoDB** | NoSQL | Serverless 示例 |
| **CloudFront** | CDN | — |
| **S3** | 对象存储 | SPA+API Gateway 示例 |
| ** CDK** | 基础设施即代码 | aws-cdk-reference-architectures |

### Azure

| 服务 | 用途 |
|------|------|
| **Azure App Service** | Web 应用托管 |
| **Azure Functions** | 无服务器函数 |
| **Azure Kubernetes Service** | K8s 托管服务 |
| **Azure SQL/Cosmos DB** | 数据库 |
| **Azure DevOps** | CI/CD |
| **Azure Bicep** | IaC |

参考：[Erudinsky/Azure-Bicep-Workshop](https://github.com/erudinsky/Azure-Bicep-Workshop)

### GCP

| 服务 | 用途 |
|------|------|
| **Cloud Run** | 容器化无服务器 |
| **GKE** | 托管 K8s |
| **Cloud Functions** | 无服务器函数 |
| **BigQuery** | 数据仓库 |
| **Vertex AI** | ML 平台 |

---

## 🔧 DevOps 与 CI/CD

### CI/CD 工具

| 工具 | 特点 |
|------|------|
| **GitHub Actions** | 与 GitHub 深度集成 |
| **GitLab CI** | GitLab 内置 |
| **Jenkins** | 成熟插件生态 |
| **ArgoCD** | GitOps K8s 部署 |
| **Tekton** | K8s 原生 CI/CD |

### GitHub Actions 示例

- [cleverneves/cicd-pipeline-github-actions](https://github.com/cleverneves/cicd-pipeline-github-actions) — 完整 CI/CD 流水线
- [richardigwegbu1/cicd-pipeline-github-actions](https://github.com/richardigwegbu1/cicd-pipeline-github-actions) — Python Flask + AWS 部署
- [aws-samples/aws-ecs-devops-using-aws-cdk](https://github.com/aws-samples/aws-ecs-devops-using-aws-cdk) — MSA+IaC+CI/CD+监控

---

## 📐 架构模式

### 核心架构模式

| 模式 | 描述 | 适用场景 |
|------|------|----------|
| **分层架构** | Controller/Service/Repository | 传统 Web 应用 |
| **六边形架构** | 端口+适配器 | 业务逻辑与框架解耦 |
| **Clean Architecture** | 依赖倒置+分层 | 可测试+可维护 |
| **CQRS** | 命令查询职责分离 | 读写分离 |
| **Event Sourcing** | 用事件记录状态 | 审计+回放 |
| **API Gateway** | 统一入口 | 微服务聚合 |
| **BFF** | Backend for Frontend | 多端适配 |

### CQRS + Event Sourcing

| 仓库 | 描述 | ⭐ |
|------|------|-----|
| [EduardoPires/EquinoxProject](https://github.com/EduardoPires/EquinoxProject) | .NET Clean+DDD+CQRS+ES | 🔥 |
| [bitloops/ddd-hexagonal-cqrs-es-eda](https://github.com/bitloops/ddd-hexagonal-cqrs-es-eda) | TypeScript+NestJS DDD+CQRS+ES | 🔥 |
| [hamed-shirbandi/TaskoMask](https://github.com/hamed-shirbandi/TaskoMask) | .NET 8 DDD+CQRS+ES+Testing | 🔥 |
| [mehdihadeli/go-food-delivery-microservices](https://github.com/mehdihadeli/go-food-delivery-microservices) | Go 微服务+CQRS+EventSourcing | 🔥 |
| [ecotoneframework/ecotone](https://github.com/ecotoneframework/ecotone) | PHP DDD+CQRS+EventSourcing | 🔥 |

---

## 🛠️ 基础设施即代码 (IaC)

| 工具 | 特点 | 仓库 |
|------|------|------|
| **Terraform** | 多云支持 | IaC 模板 |
| **AWS CDK** | 代码定义 AWS 资源 | aws-cdk-reference-architectures |
| **Azure Bicep** | Azure 专用 | Azure-Bicep-Workshop |
| ** Pulumi** | 通用编程语言 | — |
| **Ansible** | 配置管理 | — |

---

## 📊 可观测性 (Observability)

### 核心工具链

| 领域 | 工具 | 仓库 |
|------|------|------|
| **指标** | Prometheus | — |
| **日志** | Loki / ELK | — |
| **链路追踪** | Jaeger / Zipkin | — |
| **可视化** | Grafana | — |
| **统一标准** | OpenTelemetry | microservice-infra-3tier |

### 相关仓库

- [api-evangelist/observability](https://github.com/api-evangelist/observability) — 可观测性工具索引
- [usefusefi/data-pipeline-observability](https://github.com/usefusefi/data-pipeline-observability) — 数据管道可观测性

---

## 🔗 实用链接

### 系统设计

- [System Design Primer](https://github.com/donnemartin/system-design-primer) — 系统设计面试 ⭐150k
- [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) — 大规模系统设计

### 微服务

- [mfornos/awesome-microservices](https://github.com/mfornos/awesome-microservices) — 微服务资源合集 ⭐

### 云原生

- [aws-samples/aws-ecs-devops-using-aws-cdk](https://github.com/aws-samples/aws-ecs-devops-using-aws-cdk) — AWS DevOps 最佳实践

---

## 🗺️ 学习路线

```
阶段1：后端基础
  → Node/Go/Python 后端框架
  → REST API 设计
  → 数据库设计与优化

阶段2：架构模式
  → 分层架构 → Clean Architecture
  → DDD + CQRS + EventSourcing

阶段3：微服务
  → 服务拆分 + API Gateway
  → 服务间通信 + 分布式事务

阶段4：云原生部署
  → Docker 容器化
  → Kubernetes 编排
  → Terraform IaC
  → CI/CD + 可观测性
```
