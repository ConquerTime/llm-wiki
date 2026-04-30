---
project: 2026-04-aitutor-arch
status: active
created: 2026-04-29
updated: 2026-04-30
---

# 支柱 C：状态管理与可回归迁移测试

> 如果你的系统需要在更新代码后，仍然能正确恢复六个月前的线上数据——你会怎么做？这篇文章拆解 StateStore 的版本化存储设计，以及更重要的：**一套把"状态演进"变成可回归测试的方法论**。

**代码位置**
- 运行时：`aitutor-classroom-java/src/main/java/.../store/`
- 迁移引擎：`.../store/migration/`
- 测试框架：`aitutor-classroom-java/src/test/java/.../store/migration/integration/`
- 原文档：[[notes/reference-docs/StateStore迁移集成测试框架—开发者手册.md|StateStore 迁移集成测试框架—开发者手册]]

---

## 1. 问题：每次改字段都是冒险

AI 家教的一节课会产生大量运行时状态：教学模块的进度、课件页码、对话历史、板书内容……这些状态需要持久化，因为：

- **服务重启后要恢复**（容灾）
- **需要支持回放调试**（线上问题复现）
- **代码会持续迭代**（每次发版都可能改字段）

最简单的做法是把所有状态序列化成一个大 JSON 存起来。这在前两个需求上没问题——但第三个需求会把它彻底击垮。

想象一下：线上有一批用半年前的代码序列化的快照。半年里字段加了删了改了类型。今天发了新版本，一个学生的课中途重启服务——拿着新代码去读半年前的快照，能正确恢复吗？

这就是为什么需要 StateStore。

---

## 2. StateStore 的核心设计：强类型 + 版本化

StateStore 的解法不是"魔法式兼容"，而是**把版本演进变成一等公民**。

**每个字段显式声明**：用 `StateDescriptor<K, V>` 声明每个字段的键类型和值类型，状态不再是一个 any 类型的大对象。

```java
// 读写 API 是强类型的
stateStore.getValue(AGENT_STATE_DESCRIPTOR)   // 返回 Optional<AgentState>
stateStore.setValue(AGENT_STATE_DESCRIPTOR, agentState)
```

**快照带版本号**：每个持久化的快照里都记录了它是用第几版代码写的。

**版本链**：目前是 v1 → v2 → v3 → v4 → v5，每一步都有明确的"从这版到下一版需要做什么"。

---

## 3. 迁移链：从旧快照到新版本

当系统加载一个旧快照时，`StateStoreMigrationEngine` 会沿版本链一步步把它升级到当前版本：

```
读入 v3 快照
  → v3→v4 迁移（AgentState 引入）
  → v4→v5 迁移（TeachingToolState 引入）
  → 得到 v5 快照，交给当前代码使用
```

关键约束：**只允许相邻版本迁移**。没有直接的 v3→v5 迁移，只有 v3→v4 和 v4→v5。

为什么？假设允许跨版本迁移，5 个版本之间就有 5²=25 种迁移需要维护（且测试）。只允许相邻迁移，只需要 4 条迁移链。版本数越多，收益越大。更重要的是，每条相邻迁移的逻辑简单清晰——"上一版是什么样，新版加了什么"，而不是"三个版本前是什么样"。

**自动处理同名同类型字段**：迁移时，框架会自动把旧版本中名字和类型都一样的字段复制到新版本（`copyFrom`）。业务代码的 `migrate()` 方法只需要处理"真正需要特殊处理"的字段：新字段的默认值、字段类型的变更、从其他来源回填数据。

典型的 migrate() 很简洁：

```java
public void migrate(MigrationContext ctx) {
    // 大多数字段：copyFrom 已经自动复制，不用管

    // 新字段从旧数据回填
    LegacyField old = ctx.classRoomSnapshot.getLegacyField();
    ctx.currentStore.setValue(NEW_DESCRIPTOR, transform(old));
}
```

---

## 4. 版本定义的接入方式

每个新版本是一个实现了 `StateStoreVersionDefinition` 接口的类：

```java
public interface StateStoreVersionDefinition {
    int version();
    List<StateDescriptor<?, ?>> descriptors();    // 这版新加了哪些字段
    default void migrate(MigrationContext context) {}  // 迁移逻辑（默认空操作）
}
```

这些类加上 `@Component` 注解，Spring 启动时自动扫描收集，**不需要修改任何中心化的配置代码**。加一个新版本只需要：写一个新的 `XxxVersionDefinition` 类，加 `@Component`，完成。

同样，迁移链在**应用启动时**会做完整性校验：如果 v3→v4 的迁移类没有注册，启动直接失败。问题在开发期暴露，而不是在用户上课时暴露。

---

## 5. 测试策略：用真实快照做回归

这是整套方案最有方法论价值的部分。

**为什么不用假数据测试？**

假数据的问题在于：它只覆盖"你想到的情况"。线上真实数据中有大量历史遗产——某个六个月前的版本里有一个 bug，导致某个字段被写成了 null；某次迁移时用了特殊的逻辑，留下了一批格式怪异的快照。这些"历史怪癖"是迁移逻辑出错的高风险区，但假数据永远模拟不出来。

**核心主张：用线上真实快照做回归，把历史数据导入 CI。**

### 语义断言 Spec

每次引入新版本时，除了写迁移代码，还必须写一个配套的测试：`ResourceSnapshotSemanticSpec`。

```java
public interface ResourceSnapshotSemanticSpec {
    int fromSnapshotFileVersion();   // 用哪个版本的线上快照来测

    void assertMigrated(
        StateStore previousStore,     // 迁移前的数据（旧版本视角）
        ClassRoomSnapshot classRoomSnapshot,  // 原始快照（含原始格式数据）
        StateStore migratedStore      // 迁移后的数据（新版本视角）
    );
}
```

三个参数覆盖了三类断言场景：

| 场景 | 怎么断言 |
|------|---------|
| 已有字段，copyFrom 自动复制 | `previousStore` 和 `migratedStore` 里值应相等 |
| 新字段从旧数据回填 | `classRoomSnapshot` 的旧字段 = `migratedStore` 的新字段 |
| 新字段没有 migrate，应为空 | `migratedStore.getValue(...).isEmpty()` |

### 局部引擎：防止串扰

测试 v4 的迁移逻辑时，只运行"到 v4 为止"的迁移引擎——不运行 v4→v5 的迁移。这样即使 v5 的迁移代码有 bug，v4 的测试也不会因此失败，问题定位精准。

### 强制配 Spec

如果某个版本有 `VersionDefinition`（即修改了状态），且 CI 里已有更旧版本的真实快照，那**必须**配一个对应的 `SemanticSpec`——否则测试框架在构造时就报错。这个强制约束确保"每次变更都带着自己的回归测试"，不留技术债。

---

## 6. 从线上获取快照的工程化路径

**没有快照，测试就是空转。**

aitutor 提供了 Admin 工具 `SnapshotDevToolController`，一键完成：

```
线上日志里找到快照的 filePath
  → 访问 Admin 接口 /api/dev-tools/snapshots/upload-to-internal-oss?filePath=...
  → 工具自动：
      1. 从线上 OSS 下载快照 JSON
      2. 从 OSS 下载对应教室的 InRoomClass JSON（完整恢复路径需要）
      3. 上传到内网 OSS 的 statestore-snapshot/v{version}_production_{date}/
      4. 返回一行 registry 格式的配置
  → 把这一行粘贴到 src/test/resources/statestore-snapshot/registry
  → CI 自动运行时，@TestFactory 读 registry，枚举所有快照，跑匹配的 Spec
```

"内网 OSS"的细节值得一提：用的是 `oss-cn-beijing-internal.aliyuncs.com`，走内网不走公网，CI 里读这些快照几乎不产生额外成本。

---

## 7. 整体设计模式总结

| 问题 | 解法 | 收益 |
|------|------|------|
| 旧版本快照如何读？ | 每个版本保留独立 TypeRegistry | 老字段定义不丢失，老快照能反序列化 |
| 迁移代码越来越多怎么办？ | 只允许相邻版本，`copyFrom` 自动处理同名字段 | 每次只写"真正变化的部分" |
| 迁移链完整性怎么保证？ | 启动时校验，不完整就拒绝启动 | 启动时失败 > 运行时失败 |
| 怎么确保迁移逻辑是对的？ | 真实线上快照 + 语义断言 + CI 回归 | 历史怪癖被测试覆盖 |
| 多版本测试互相干扰怎么办？ | 局部引擎，每个 Spec 只跑自己那步 | 失败定位精准到单次迁移 |
| 快照怎么导入测试？ | Admin 工具一键导出到内网 OSS | 无手动操作，CI 可重复 |

---

## 8. 可复用的方法论

这套"版本化存储 + 可回归迁移测试"的模式不只适用于 AI 家教，凡是有以下特征的场景都可以直接借鉴：

- 状态有长生命周期（需要跨版本存活）
- 状态模式（schema）会随业务迭代演进
- 需要容灾恢复（服务重启后要能读回旧数据）

可以推广到：数据库 schema 演进（Flyway/Liquibase）、Event Sourcing 的事件格式演进、API/消息队列消息格式的协议升级。

核心信条四条：
1. **每次变更同时写回归测试**——不留"以后再补"的测试债
2. **真实数据胜过假数据**——真实数据里藏着你想象不到的历史
3. **多层 fail-fast**——启动时校验优于运行时校验
4. **局部测试，精准定位**——每次迁移只对自己负责

---

## 附：代码地图

| 主题 | 文件 |
|------|------|
| 状态存储接口与实现 | `store/StateStore.java`, `store/impl/InMemoryStateStore.java` |
| 字段声明 | `store/descriptor/StateDescriptor.java` |
| 版本定义接口 | `store/migration/StateStoreVersionDefinition.java` |
| 相邻迁移接口 | `store/migration/AdjacentStateStoreMigration.java` |
| 迁移引擎 | `store/migration/StateStoreMigrationEngine.java` |
| 多版本 Registry | `store/migration/TypeRegistryCatalog.java` |
| 语义断言接口 | `test/.../migration/integration/ResourceSnapshotSemanticSpec.java` |
| 版本清单入口 | `test/.../migration/integration/StateStoreMigrationTestModules.java` |
| 集成测试 | `test/.../migration/StateStoreMigrationIntegrationTest.java` |
| Admin 导出工具 | `aitutor-classroom-java-admin/.../SnapshotDevToolController.java` |
| **原文档** | [[notes/reference-docs/StateStore迁移集成测试框架—开发者手册.md|StateStore 迁移集成测试框架—开发者手册]] |
