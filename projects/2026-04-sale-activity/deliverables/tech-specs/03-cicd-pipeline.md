# 技术方案 #3：CI/CD 发布流水线

> ada-sale-activity 的自动化构建发布机制：Saber CI + OSS 静态部署 + miniprogram-ci 小程序上传。

---

## 1. 整体架构

```
Git 推送
  ├── master 分支 ──→ [test-build] H5 测试构建
  │                   [test-mp-build] 微信小程序构建 + CI 上传
  │
  └── online 分支 ──→ [online-build] H5 正式 + staging 构建
                       [online-publish] H5 产物上传 OSS
```

CI 平台：**Saber**（公司内部 CI 系统，语法类似 GitLab CI），配置在 `saber.yml`。

---

## 2. 四个 Stage 详解

### Stage 1：test-build-job（H5 测试构建）

```yaml
触发：master 分支任意 push
镜像：node:14.15.4
脚本：
  npm install --registry=http://npm.zhenguanyu.com
  npm run build:test:h5
产物：dist/**（上传到 CI 存储，供后续 stage 使用）
```

`build:test:h5` 展开：
```
node replaceManifest.js test h5
  → manifest.json 写入 test 环境 publicPath
cross-env VUE_APP_ENV=test NODE_ENV=production UNI_PLATFORM=h5
  vue-cli-service uni-build
  → 产出 dist/build/h5/
AfterEmitPlugin（vue.config.js）：
  → CSS 加版本号 ?t=xxxx
  → 清理 dcloud CDN 残留
  → 复制 dist/build/h5/ → dist/（非 staging 模式）
```

**注意**：test-build-job 只构建不发布，产物暂存 CI artifacts；test-publish-job（被注释掉了）原本负责推 OSS，现在测试环境 H5 的 OSS 发布已从流水线移除（手动或其他方式触发）。

---

### Stage 2：test-mp-build-job（微信小程序测试构建 + 上传）

```yaml
触发：master 分支，且有文件变更（changes: ['.*']）
镜像：node:14.15.4
脚本：
  npm run build:test:mp-weixin
  npm run upload -- --version=1.0.0
产物：不上传到 CI（upload: false）
```

**关键**：这里 `upload -- --version=1.0.0` 调用的是 `upload.js`（miniprogram-ci），**直接将构建产物上传到微信开发者平台**，跳过了 OSS，形成了"构建即发布"的短路径。

`upload.js` 的描述字段自动从 git 取信息：
```js
desc: `【${currentBranch}】（${latestAuthor}）${latestLog}`
// 示例：【master】（张三）ADD:支持小猿编程萌萌班小程序
```

---

### Stage 3：online-build-job（正式 H5 构建）

```yaml
触发：online 分支 push
镜像：node:14.15.4
脚本：
  npm install --registry=http://npm.zhenguanyu.com
  npm run build:h5        → 正式 H5（publicPath: static-common.fbcontent.cn/ada-sale-activity）
  npm run build:staging:h5 → staging H5（publicPath: .../ada-sale-activity/build/h5）
产物：dist/**（tagged: online，供 online-publish-job 使用）
```

**注意**：一次构建同时产出 production 和 staging 两份 H5 产物（都在 dist/ 下，路径不同）。

---

### Stage 4：online-publish-job（正式 H5 发布到 OSS）

```yaml
触发：online 分支 push（接 online-build-job）
镜像：registry.cn-beijing.aliyuncs.com/yuanfd/yfd_ossutil64:latest（阿里云 ossutil）
脚本：
  ossutil64 cp dist/build/h5/ oss://static-nginx-online/ada-sale-activity/build/h5/ -r -f
依赖：online-build-job（需要 artifacts）
```

**OSS 路径映射**：
```
本地 dist/build/h5/  →  OSS: static-nginx-online/ada-sale-activity/build/h5/
                              ↓（CDN 映射）
                         https://static-common.fbcontent.cn/ada-sale-activity/
```

---

## 3. 分支策略

| 分支 | 用途 | 触发的 CI |
|------|------|---------|
| `feature-*` | 功能开发 | 无（仅本地构建） |
| `master` | 测试主干 | test-build + test-mp-build |
| `online` | 正式发布 | online-build + online-publish |
| `bugfix-*` | 线上 bugfix | 无（合并到 online 后触发）|

从 git 历史可以看出，绝大多数工作在 feature-* 分支上（214 条远端分支），合并到 master 测试，再合并到 online 发布。

---

## 4. 微信小程序发布的完整路径

```
1. 开发：feature-* 本地 dev:mp-weixin（--watch 模式）
2. 测试构建：master → test-mp-build-job
     npm run build:test:mp-weixin
       → replaceManifest.js test mp（写入测试 appid wx151572c499e056c2）
       → UNI_PLATFORM=mp-weixin uni-build --minimize
       → 产出 dist/dev/mp-weixin/
     npm run upload -- --version=1.0.0
       → miniprogram-ci 上传到微信开发者平台（测试 appid）
3. 正式发布：saber.yml 中没有 online 分支的小程序上传 stage
     → 正式小程序需要手动执行 npm run build:mp-weixin 再手动上传（或另有流程）
```

**Gap 识别**：正式小程序发布没有自动化，是已知的流程缺口。

---

## 5. 头条小程序发布现状

```yaml
saber.yml 中：无头条小程序相关 stage
package.json 中：有 build:test:mp-toutiao 和 build:mp-toutiao 脚本
```

头条小程序**完全没有 CI 自动化**，构建和上传均为手动操作。

原因推测：
- 头条小程序使用 `uniapp-to-group` 打包为"小程序群组包"（行业 SDK），上传工具链与普通小程序不同
- 字节跳动官方 tt-ide-cli 在该项目建立时可能尚未完善

---

## 6. 环境与 OSS 存储桶对应关系

| 环境 | OSS Bucket | 路径 |
|------|-----------|------|
| test | `static-nginx-test` | `/ada-sale-activity/build/h5/` |
| production | `static-nginx-online` | `/ada-sale-activity/build/h5/` |
| staging（test） | `static-nginx-test` | `/ada-sale-activity/build/h5/` |
| staging（prod） | `static-nginx-online` | `/ada-sale-activity/build/h5/` |

test 和 production 使用不同的 CDN 域名：
- test：`static-nginx-test.fbcontent.cn`
- production：`static-common.fbcontent.cn`

---

## 7. upload.js 设计要点

```js
// 三个 git 信息自动注入 desc
const latestLog    = git log -1 --pretty=format:%s   // 最新提交信息
const latestAuthor = git log -1 --pretty=format:%an  // 最新提交人
const currentBranch = git rev-parse --abbrev-ref HEAD // 当前分支

// desc 格式：【分支名】（作者）提交信息
// 上传后在微信开发者平台可直接看到来源，方便追踪
```

这个"desc 注入 git 信息"的做法**值得通用化**：任何通过 miniprogram-ci 上传的项目都可以用这套模板，不用手动填写上传备注。

---

## 8. 已知问题 / 可改进点

| 问题 | 现状 | 改进方向 |
|------|------|---------|
| test-publish-job 被注释掉 | 测试 H5 产物有 CI 构建但没有 OSS 发布 | 恢复该 stage，或改用其他发布机制 |
| 正式微信小程序手动发布 | online 分支没有小程序上传 stage | 仿 test-mp-build-job，在 online stage 加 `build:mp-weixin + upload` |
| 头条小程序无 CI | 完全手动 | 调研 tt-ide-cli 自动上传方案 |
| node:14.15.4 镜像版本旧 | Node 14 已 EOL（2023-04） | 升级到 node:18 LTS |
| 版本号硬编码 1.0.0 | `npm run upload -- --version=1.0.0` | 从 package.json version 或 git tag 自动读取 |

---

## 9. 可复用的设计模式

> 以下内容脱离 ada-sale-activity 后仍然成立，适合回流到 wiki。

**miniprogram-ci + git 信息注入**模式（通用微信小程序 CI 上传脚本）：
```js
const latestLog    = execa.commandSync('git log -1 --pretty=format:%s').stdout
const latestAuthor = execa.commandSync('git log -1 --pretty=format:%an').stdout
const currentBranch = execa.commandSync('git rev-parse --abbrev-ref HEAD').stdout
desc: `【${currentBranch}】（${latestAuthor}）${latestLog}`
```

**分支策略**（feature → master → online 三段式）：
- feature 分支开发，不触发 CI，保持灵活
- master = 测试环境（自动构建测试包 + 小程序测试上传）
- online = 正式环境（自动构建 + OSS 发布）
- 缺点：两条主干需要维护，发布时需要额外操作（cherry-pick 或 merge）；适合发布节奏明确的项目
