# 业务知识 #1：多端 × 多环境参数矩阵

> ada-sale-activity 中三个平台（H5 / 微信小程序 / 头条小程序）× 五个环境（development / test / staging-test / staging / production）下的关键参数映射。

---

## 1. H5 publicPath 矩阵

| env | VUE_APP_ENV | publicPath |
|-----|------------|-----------|
| `development` | test | `/ada-sale-activity`（devServer 相对路径）|
| `test` | test | `https://static-nginx-test.fbcontent.cn/ada-sale-activity` |
| `staging-test` | test | `https://static-nginx-test.fbcontent.cn/ada-sale-activity/build/h5` |
| `staging` | production | `https://static-common.fbcontent.cn/ada-sale-activity/build/h5` |
| `production` | production | `https://static-common.fbcontent.cn/ada-sale-activity` |

**注意**：staging 和 production 的路径差一段 `/build/h5`。production 的 AfterEmitPlugin 会把 `dist/build/h5/` 复制到 `dist/`，所以 publicPath 更短；staging 不做这步复制，所以 publicPath 保留完整子路径。

---

## 2. 小程序 appid 矩阵

| platform | production 环境 | 其余所有环境（test / staging / dev）|
|----------|---------------|----------------------------------|
| **微信小程序**（mp-weixin）| `wxaffa2c82823c1b0f` | `wx151572c499e056c2` |
| **头条小程序**（mp-toutiao）| `tt551f23a2ca20ce4b01` | `ttedec9b5172d372a201` |

规则简单：**production 用正式 appid，其余所有环境用测试 appid**（无论是 test / staging-test / staging / development）。

---

## 3. OSS Bucket × CDN 域名对应

| 环境 | OSS Bucket | CDN 域名 | 路径 |
|------|-----------|---------|------|
| test | `static-nginx-test` | `static-nginx-test.fbcontent.cn` | `/ada-sale-activity/build/h5/` |
| staging-test | `static-nginx-test` | `static-nginx-test.fbcontent.cn` | `/ada-sale-activity/build/h5/` |
| staging | `static-nginx-online` | `static-common.fbcontent.cn` | `/ada-sale-activity/build/h5/` |
| production | `static-nginx-online` | `static-common.fbcontent.cn` | `/ada-sale-activity/` |

CI 发布命令（stage 4）：
```bash
ossutil64 cp dist/build/h5/ oss://static-nginx-online/ada-sale-activity/build/h5/ -r -f
```

---

## 4. npm scripts 全矩阵（14 条）

| script | env 参数 | platform 参数 | NODE_ENV | 用途 |
|--------|---------|-------------|----------|------|
| `dev:h5` | development | h5 | development | 本地 H5 开发（HMR）|
| `dev:mp-weixin` | development | mp | development | 本地微信小程序开发（--watch）|
| `dev:mp-toutiao` | development | dy-mp | development | 本地头条小程序开发（--watch）|
| `build:test:h5` | test | h5 | production | 测试环境 H5 构建（CI Stage 1）|
| `build:test:staging:h5` | staging-test | h5 | production | staging-test H5 构建 |
| `build:test:mp-weixin` | test | mp | production | 测试微信小程序（CI Stage 2）|
| `build:test:mp-toutiao` | test | dy-mp | production | 测试头条小程序（手动）|
| `build:h5` | production | h5 | production | 正式 H5 构建（CI Stage 3）|
| `build:staging:h5` | staging | h5 | production | staging 正式 H5（CI Stage 3 同时产出）|
| `build:mp-weixin` | production | mp | production | 正式微信小程序（手动）|
| `build:mp-toutiao` | production | dy-mp | production | 正式头条小程序（手动）|
| `upload` | — | — | — | miniprogram-ci 上传微信小程序 |
| `dev:server` | — | — | — | 本地 mock 服务 |
| `lint` | — | — | — | ESLint 检查 |

---

## 5. Saber CI 四个 Stage

| Stage | 触发分支 | 触发条件 | 主要操作 |
|-------|---------|---------|---------|
| `test-build-job` | master | 任意 push | H5 测试构建，产物上传 CI artifacts |
| `test-mp-build-job` | master | 有文件变更 | 微信小程序构建 + miniprogram-ci 上传 |
| `online-build-job` | online | 任意 push | 正式 H5 + staging H5 双份构建 |
| `online-publish-job` | online | 依赖 Stage 3 | ossutil64 推送 H5 产物到 OSS |

**已知缺口**：
- `test-publish-job`（测试 H5 推 OSS）被注释掉，测试 H5 仅构建不发布
- 正式微信小程序无自动上传 stage（手动）
- 头条小程序无任何 CI 自动化（完全手动）
