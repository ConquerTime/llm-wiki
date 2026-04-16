# 软件工程知识资料

> 来源：AI 助手整理 | 更新时间：2026-04-16

---

## 📚 经典书籍

### 必读经典

| 书名 | 作者 | 核心理念 |
|------|------|----------|
| 《代码大全》 | Steve McConnell | 软件构建百科全书 |
| 《重构》 | Martin Fowler | 代码坏味道+重构手法 |
| 《代码整洁之道》 | Robert C. Martin | SOLID原则+编码规范 |
| 《人月神话》 | Frederick Brooks | 软件项目管理经典 |
| 《架构整洁之道》 | Robert C. Martin | Clean Architecture |
| 《设计模式》 | GoF | 23种经典设计模式 |
| 《Effective Java》 | Joshua Bloch | Java高效实践 |

---

## 🛠️ 优质工具

### 代码质量分析

- **SonarQube** - 静态代码分析平台
- **ESLint / Prettier** - JS/TS 规范+格式化
- **DeepSource** - 自动化代码审查
- **Codacy** - 云端代码质量分析
- **pre-commit** - 多语言 pre-commit 钩子框架

### 重构工具

- **ast-grep** - Rust 写的代码结构搜索/Lint/重写
- **rectorphp/rector** - PHP 自动升级和重构
- **Refactoring.Guru** - 设计模式+重构可视化

---

## 🌐 开源学习资源

### Clean Code 系列（多语言适配）

- [ryanmcdermott/clean-code-javascript](https://github.com/ryanmcdermott/clean-code-javascript) - JS版整洁代码 ⭐94k
- [labs42io/clean-code-typescript](https://github.com/labs42io/clean-code-typescript) - TS版整洁代码
- [zedr/clean-code-python](https://github.com/zedr/clean-code-python) - Python版整洁代码
- [piotrplenik/clean-code-php](https://github.com/piotrplenik/clean-code-php) - PHP版整洁代码
- [thangchung/clean-code-dotnet](https://github.com/thangchung/clean-code-dotnet) - .NET版整洁代码

### 技术债务

- [labcodes/awesome-technical-debt](https://github.com/labcodes/awesome-technical-debt) - 技术债务文章合集
- [lucidarch/lucid](https://github.com/lucidarch/lucid) - Laravel最小化技术债务架构

### 静态分析工具合集

- [analysis-tools-dev/static-analysis](https://github.com/analysis-tools-dev/static-analysis) - 各语言静态分析工具

---

## 🎓 学习路线

```
1. 入门：读《代码整洁之道》 + clean-code-javascript
                ↓
2. 实践：用 ESLint + Prettier 规范团队代码
                ↓
3. 进阶：学 SonarQube + 理解《重构》23种坏味道
                ↓
4. 体系化：掌握 SOLID / DRY / KISS 原则 + DDD
```

---

## 🔗 实用链接

- [Refactoring.Guru](https://refactoringguru.cn/) - 重构与设计模式可视化
- [Sourcemaking](https://sourcemaking.com/) - 设计模式与重构
- [Teach Yourself CS](https://teachyourselfcs.com/) - 自学计算机科学
- [System Design Primer](https://github.com/donnemartin/system-design-primer) - 系统设计 ⭐150k

---

# 设计模式深入

> 更新时间：2026-04-16

---

## 📖 GoF 23种设计模式

### 创建型模式 (5种)

| 模式 | 目的 | 示例仓库 |
|------|------|----------|
| **Singleton** | 单例 | [fbeline/design-patterns-JS](https://github.com/fbeline/design-patterns-JS) |
| **Factory Method** | 工厂方法 | [iluwatar/java-design-patterns](https://github.com/iluwatar/java-design-patterns) |
| **Abstract Factory** | 抽象工厂 | 同上 |
| **Builder** | 构建器 | 同上 |
| **Prototype** | 原型 | 同上 |

### 结构型模式 (7种)

| 模式 | 目的 | 示例仓库 |
|------|------|----------|
| **Adapter** | 适配器 | 同上 |
| **Bridge** | 桥接 | 同上 |
| **Composite** | 组合 | 同上 |
| **Decorator** | 装饰器 | 同上 |
| **Facade** | 门面 | 同上 |
| **Flyweight** | 享元 | 同上 |
| **Proxy** | 代理 | 同上 |

### 行为型模式 (11种)

| 模式 | 目的 | 示例仓库 |
|------|------|----------|
| **Chain of Responsibility** | 责任链 | 同上 |
| **Command** | 命令 | 同上 |
| **Iterator** | 迭代器 | 同上 |
| **Mediator** | 中介者 | 同上 |
| **Memento** | 备忘录 | 同上 |
| **Observer** | 观察者 | 同上 |
| **State** | 状态 | 同上 |
| **Strategy** | 策略 | 同上 |
| **Template Method** | 模板方法 | 同上 |
| **Visitor** | 访问者 | 同上 |

---

## 🌐 多语言设计模式实现

| 仓库 | 语言 | 特点 | ⭐ |
|------|------|------|-----|
| [iluwatar/java-design-patterns](https://github.com/iluwatar/java-design-patterns) | Java | 最全 Java 实现 | 🔥 |
| [faif/python-patterns](https://github.com/faif/python-patterns) | Python | Python 版设计模式 | 🔥 |
| [tmrts/go-patterns](https://github.com/tmrts/go-patterns) | Go | Go 语言惯用模式 | 🔥 |
| [ochococo/Design-Patterns-In-Swift](https://github.com/ochococo/Design-Patterns-In-Swift) | Swift | Swift 5.0 实现 | 🔥 |
| [DesignPatternsPHP/DesignPatternsPHP](https://github.com/DesignPatternsPHP/DesignPatternsPHP) | PHP | PHP 8.x 实现 | 🔥 |
| [torokmark/design_patterns_in_typescript](https://github.com/torokmark/design_patterns_in_typescript) | TypeScript | TS 版实现 | 🔥 |
| [rust-unofficial/patterns](https://github.com/rust-unofficial/patterns) | Rust | Rust 模式+反模式 | 🔥 |
| [fbeline/design-patterns-JS](https://github.com/fbeline/design-patterns-JS) | JavaScript | JS 实现全部23种 | 🔥 |
| [dbcfox/DesignPatternsInKotlin](https://github.com/dbacinski/Design-Patterns-In-Kotlin) | Kotlin | Kotlin 实现 | 🔥 |
| [fadeevab/design-patterns-rust](https://github.com/fadeevab/design-patterns-rust) | Rust | Rust 版 GoF + 更多 | 🔥 |

---

## 🎯 SOLID 原则深入

### 五大原则

| 原则 | 全称 | 核心理念 |
|------|------|----------|
| **S** | Single Responsibility | 单一职责：一个类只做一件事 |
| **O** | Open/Closed | 开闭原则：对扩展开放，对修改封闭 |
| **L** | Liskov Substitution | 里氏替换：子类必须能替换基类 |
| **I** | Interface Segregation | 接口隔离：接口要小而专 |
| **D** | Dependency Inversion | 依赖倒置：依赖抽象而非具体 |

### SOLID 学习资源

| 仓库 | 描述 | ⭐ |
|------|------|-----|
| [heykarimoff/solid.python](https://github.com/heykarimoff/solid.python) | Python 理解 SOLID | 🔥 |
| [bespoyasov/solidbook](https://github.com/bespoyasov/solidbook) | SOLID 原则书籍 | 🔥 |
| [jafari-dev/oop-expert-with-typescript](https://github.com/jafari-dev/oop-expert-with-typescript) | TS 面向对象+SOLID | 🔥 |

---

## 🏛️ 架构模式

### Clean Architecture

| 仓库 | 描述 | ⭐ |
|------|------|-----|
| [rmanguinho/clean-ts-api](https://github.com/rmanguinho/clean-ts-api) | Node.js+TDD+Clean+SOLID | 🔥 |
| [rmanguinho/clean-react](https://github.com/rmanguinho/clean-react) | React+Clean Architecture | 🔥 |
| [rmanguinho/clean-flutter-app](https://github.com/rmanguinho/clean-flutter-app) | Flutter+Clean Architecture | 🔥 |
| [Sairyss/domain-driven-hexagon](https://github.com/Sairyss/domain-driven-hexagon) | DDD+六边形架构 | 🔥 |

### DDD (领域驱动设计)

| 仓库 | 描述 | ⭐ |
|------|------|-----|
| [heynickc/awesome-ddd](https://github.com/heynickc/awesome-ddd) | DDD+CQRS+Event Sourcing 资源合集 | 🔥 |
| [bitloops/ddd-hexagonal-cqrs-es-eda](https://github.com/bitloops/ddd-hexagonal-cqrs-es-eda) | TypeScript+NestJS 完整示例 | 🔥 |
| [qu3vipon/python-ddd](https://github.com/qu3vipon/python-ddd) | Python DDD 示例 | 🔥 |

### 微服务架构

| 仓库 | 描述 | ⭐ |
|------|------|-----|
| [EdwinVW/pitstop](https://github.com/EdwinVW/pitstop) | Microservices+CQRS+EventSourcing+DDD | 🔥 |

---

## ⚠️ 反模式 (Anti-Patterns)

| 仓库 | 描述 | 语言 |
|------|------|------|
| [rust-unofficial/patterns](https://github.com/rust-unofficial/patterns) | Rust 反模式+惯用写法 | Rust |
| [quantifiedcode/python-anti-patterns](https://github.com/quantifiedcode/python-anti-patterns) | Python 反模式集合 | Python |
| [tcorral/Refactoring_Patterns](https://github.com/tcorral/Refactoring_Patterns) | 31种重构模式 | JavaScript |
| [jarulraj/sqlcheck](https://github.com/jarulraj/sqlcheck) | SQL 反模式自动检测 | 多语言 |
| [doyensec/electronegativity](https://github.com/doyensec/electronegativity) | Electron 安全反模式 | JavaScript |

---

## 📚 经典书籍（设计模式专项）

| 书名 | 作者 | 特点 |
|------|------|------|
| 《设计模式》 | GoF | 23种模式开山之作 |
| 《Head First 设计模式》 | Freeman 等 | 图解入门首选 |
| 《重构》 | Martin Fowler | 模式+重构结合 |
| 《企业应用架构模式》 | Martin Fowler | 架构级别模式 |
| 《领域驱动设计》 | Eric Evans | DDD 奠基之作 |
| 《实现领域驱动设计》 | Vernon Vaughn | DDD 实践指南 |

---

## 🔗 实用链接

- [Refactoring.Guru](https://refactoringguru.cn/) - 设计模式+重构可视化
- [Sourcemaking](https://sourcemaking.com/) - 设计模式与重构
- [Kamran Ahmed - Design Patterns for Humans](https://github.com/kamranahmedse/design-patterns-for-humans) - 极简版设计模式解释 ⭐70k
- [DovAmir/awesome-design-patterns](https://github.com/DovAmir/awesome-design-patterns) - 软件+架构设计模式合集 ⭐

---

## 🗺️ 学习路线建议

```
阶段1：GoF 23种设计模式
  → java-design-patterns / python-patterns 多语言对照学习

阶段2：SOLID 原则
  → solid.python + solidbook 理论+实践

阶段3：架构模式
  → Clean Architecture → DDD → CQRS/EventSourcing

阶段4：反模式识别
  → 理解常见 anti-patterns，避免重蹈覆辙

日常：结合 Refactoring.Guru + Sourcemaking 复习
```
