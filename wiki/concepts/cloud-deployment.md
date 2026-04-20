---
title: 云服务部署
type: concept
subtype: programming
tags: [cloud, deployment, aws, azure, gcp, docker, kubernetes, iac]
created: 2026-04-16
updated: 2026-04-16
sources:
  - ../sources/articles/backend-architecture-article.md
---

# 云服务部署

> 将后端服务部署到云端的技术与最佳实践。

## 主流云平台

### AWS (Amazon Web Services)

| 服务 | 用途 |
|------|------|
| **Lambda** | 无服务器计算 |
| **API Gateway** | REST/WebSocket API |
| **ECS / EKS** | 容器编排 |
| **RDS** | 关系数据库托管 |
| **DynamoDB** | NoSQL 文档数据库 |
| **S3** | 对象存储 |
| **CloudFront** | CDN |
| **ElastiCache** | Redis 缓存 |
| **CDK** | 基础设施即代码 |

### Azure (Microsoft)

| 服务 | 用途 |
|------|------|
| **App Service** | Web 应用托管 |
| **Azure Functions** | 无服务器函数 |
| **AKS** | Azure Kubernetes Service |
| **Azure SQL** | 托管 SQL Server |
| **Cosmos DB** | 多模型 NoSQL |
| **Azure DevOps** | CI/CD |
| **Azure Bicep** | IaC |

### GCP (Google Cloud Platform)

| 服务 | 用途 |
|------|------|
| **Cloud Run** | 容器化无服务器 |
| **GKE** | 托管 Kubernetes |
| **Cloud Functions** | 无服务器函数 |
| **BigQuery** | 数据仓库 |
| **Vertex AI** | ML 平台 |
| **Spanner** | 全球分布式数据库 |

## 容器化

### Docker

将应用及其依赖打包为容器镜像，实现"一次构建，到处运行"。

关键概念：
- **Dockerfile** — 镜像构建脚本
- **Docker Compose** — 多容器编排
- **Registry** — 镜像存储（Docker Hub / ECR / ACR）

### Kubernetes (K8s)

容器编排平台，核心概念：

| 概念 | 说明 |
|------|------|
| **Pod** | 最小调度单元 |
| **Deployment** | 无状态应用部署 |
| **StatefulSet** | 有状态应用 |
| **Service** | 网络暴露 |
| **Ingress** | HTTP 路由 |
| **ConfigMap/Secret** | 配置管理 |
| **PersistentVolume** | 持久存储 |

## 基础设施即代码 (IaC)

用代码管理云资源，版本化、可重复、可测试。

| 工具 | 特点 |
|------|------|
| **Terraform** | 多云支持，HCL 语言 |
| **AWS CDK** | 代码定义 AWS 资源 |
| **Azure Bicep** | Azure 专用，简洁语法 |
| **Pulumi** | 通用编程语言 |

## CI/CD 流水线

典型流水线：

```
Code → Build → Test → Security Scan → Deploy
 ↑                              ↓
 ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

工具：GitHub Actions / GitLab CI / Jenkins / ArgoCD

## 可观测性

三层支柱：

| 类型 | 工具 |
|------|------|
| **Metrics** | Prometheus, CloudWatch |
| **Logs** | Loki, ELK, CloudWatch Logs |
| **Traces** | Jaeger, Zipkin |

统一标准：**OpenTelemetry**

## 相关资源

- [yeongseon/cloudblocks](https://github.com/yeongseon/cloudblocks) — 可视化云架构学习
- [andredesousa/devops-best-practices](https://github.com/andredesousa/devops-best-practices) — DevOps 最佳实践
- [aws-samples/aws-ecs-devops-using-aws-cdk](https://github.com/aws-samples/aws-ecs-devops-using-aws-cdk) — AWS DevOps 完整方案

## 相关概念

- [[backend-architecture|后端架构]] — 核心架构模式
- [[microservices|微服务架构]] — 服务拆分与通信模式
