---
project: 2026-04-aitutor-arch
status: active
created: 2026-04-29
updated: 2026-04-30
---

# 支柱 B：实时 AI 语音对话链路

> 学生说完一句话，AI 家教要在多快的时间内开口回答？这篇文章沿着"一轮对话"的时间线，拆解从语音输入到音频播放的每一段延迟，以及三个关键设计：**如何打断、如何预测、如何同步字幕**。

**代码位置**
- 运行时：`aitutor-classroom-legacy/src/main/java/.../rtc/`
- 原文档：[[notes/reference-docs/LLM响应处理流程文档.md|LLM 响应处理流程文档]]

---

## 1. 一秒钟发生了什么

先建立时间感。学生说完一句"我不太懂这个"，到耳机里听到老师开口，中间要经历：

```
学生说话结束
  → ASR 识别完成            （100–500ms，取决于 ASR 引擎）
  → 服务端决定开始回答       （< 10ms，纯内存操作）
  → LLM 产出第一句文字      （500ms–2s，最大瓶颈）
  → TTS 生成第一段音频       （200ms–1s，并行压缩）
  → WebSocket 推送到客户端   （20–100ms）
  → 客户端缓冲后开始播放     （50–200ms）
```

**乐观端到端延迟**（预测命中时）：约 400ms，学生几乎感知不到停顿。  
**悲观端到端延迟**（正常路径，慢思考）：2–4 秒。

LLM 阶段是压倒性的瓶颈。后文的三个设计都在围绕它做文章。

---

## 2. 链路全景

完整的数据流经过四个角色：

```
RoundStart               ← 轮次状态机，整场对话的指挥官
  │ ASR 事件
  ↓
RoundStart.onAsrMessage  ← 处理 ASR 状态变化（VAD、打断、识别完成）
  │ AsrComplete → submitLLM
  ↓
DefaultAgentMainGraph    ← Agent 图执行，产出句子 Flowable
  │ 逐句 LLMConversationData
  ↓
LlmResponseHandlerImpl   ← 每句话并行启动 TTS + 板书生成
  │ 合并后发 TeacherMessageEvent
  ↓
RoundStart.handlerThisRoundEvent
  │ 检查打断标志 → buildAudioMessage → sendAudioMessage
  ↓
WebSocket → 客户端播放
```

每一句 LLM 输出都独立走一遍"TTS + 板书生成"，不等全部回答完成。这保证了**第一句话的延迟**和后续句子的延迟相互独立，实现流式体验。

---

## 3. 打断：双保险设计

学生随时可能开口打断老师。这是实时语音场景最难处理的问题之一：当老师的第二句话正在 TTS 生成、第三句话正在 LLM 输出时，学生打断了——系统怎么处理？

**朴素做法**的问题：
- 只停止"最上游的 LLM 请求"：下游已经在生成的 TTS 还会发给学生
- 只停止"发送"：LLM 和 TTS 还在继续花费计算资源

aitutor 的方案是**两道独立的保险**：

**保险 A：订阅层 dispose**

当 ASR 检测到学生开口（`AsrBreak` 或更激进的 `AsrStartBreak`）：

```java
teacherLLMMessageDisposable.dispose();
```

这一行停止从 LLM Flowable 拉取新元素。RxJava 的 dispose 会向上传导，最终断开 HTTP 连接（停止花 token）。

**保险 B：发送层标志位**

dispose 是异步的。在 dispose 执行的瞬间，可能已经有一条"在途"的 TeacherMessage（LLM 返回了、TTS 也完成了、事件正在总线上排队）。只靠保险 A，这条在途消息还是会发出去——学生会听到半截老师说话，体验极差。

保险 B 的做法：设一个 `teacherInterrupted = true` 标志位，在最终发送前检查：

```java
if (!roundAudioStatus.isTeacherInterrupted()) {
    downwardMessageSender.sendAudioMessage(bundle);
}
```

两道保险互补。保险 A 尽早停止资源消耗，保险 B 兜底防止老师声音"出逃"。

---

## 4. 输入预测：把 LLM 延迟消灭在等待期间

LLM 的延迟（500ms–2s）是我们没法直接压缩的。但有一段时间完全被浪费了：**老师在说话的时候，学生在干嘛？等着。**

这段等待时间完全可以用来"预热"下一轮 LLM。

**机制**：老师说完最后一句话时（`isLastRoundAudio = true`），系统启动 `UserInputPredictedTask`：

1. 根据当前对话上下文，用 `PREDICTED_BOT` 预测"学生下一句最可能说什么"
2. 基于这个预测，立刻发起一次完整的 LLM 对话请求
3. 把请求结果的 Flowable 做 `replay().connect()`——不管有没有人订阅，HTTP 连接建立，数据开始流入缓冲

**下一轮学生真正说话时**：`predicted_match` 节点把学生的真实输入和预测结果做匹配。命中时，直接复用那个已经在流动的 Flowable——LLM 延迟几乎为 0。

```
老师最后一句 ──────────────────────────────────────────→
                          ↓                            ↓
                   预热 LLM 开始                    学生说话
                   （数据开始流入缓冲）              （命中预测！复用热流）
```

**命中率和成本**：教学场景的学生回答高度模式化（"听懂了"/"再讲一遍"/"举个例子"），命中率有望超过 30%。命中率 > 30% 时，额外花费的 token 成本已经被体验提升所抵消。不命中时，就走正常路径——唯一的代价是那次"白发"的预测请求。

---

## 5. 字幕同步：把对齐成本放到服务端

字幕同步是个经典难题：TTS 输出的是一段完整音频，客户端怎么知道"每个字对应音频的第几毫秒"？

客户端方案（ASR 回对齐）：让客户端在播放时再做一次语音识别来对齐文字。准确率低、计算重、中英混合时经常出错。

aitutor 的做法：**TTS 服务在生成音频时，同时返回时间轴元数据**。每个字/词都带一个 `(text, startMs, endMs)` 三元组，打包进 `StandardAudioMessage.textAudioIntervalsList`，随音频一起推给客户端。

客户端播放时，只需要根据当前播放进度查表找到对应的字，触发高亮。对齐计算全在服务端完成，客户端只做渲染。

---

## 6. TTS 和板书的并行生成

每当 LLM 流出一句话，`LlmResponseHandlerImpl` 同时启动两个异步任务：

```java
CompletableFuture<TtsResult> ttsFuture = asyncGenerateTts(sentence);
CompletableFuture<List<BoardCommand>> boardFuture = asyncGeneratePostPptBoardCommands(sentence);

TeacherMessage message = ttsFuture
    .thenCombine(boardFuture, this::buildTeacherMessage)
    .join();
```

TTS 和板书指令生成是独立的——分别请求不同的服务，`thenCombine` 等两者都完成再合并。两者的等待时间重叠，总延迟是 `max(TTS时间, 板书时间)` 而不是两者之和。

同时，生图（`onGenImage`）是纯异步的——`TeacherMessage` 里有生图指令时，发出后不等结果，图片好了再单独推给客户端。不会阻塞主线的语音播放。

---

## 7. 消息下发结构

每句话最终打包成一个 `StandardAudioMessageBundle`：

```
StandardAudioMessageBundle
├── StandardAudioMessage        ← 音频本体 + 字幕时间轴
├── StandardBoardCommandMessage ← 板书指令（可能为空）
├── StandardEmotionMessage      ← 表情指令（可能为空）
├── StandardClassBreakMessage   ← 课间消息（可能为空）
└── StandardTeacherMediaOverMessage ← 本轮最后一帧标记
```

几个协议约定值得注意：
- **`isLastRoundAudio`**：本轮最后一句的标记。客户端据此切换状态，服务端据此触发下一轮预测
- **`isLastTeacherAudioFrame`**：整个响应流程的结束信号
- **`id`**：消息 ID，客户端用来做重复判定（WebSocket 不保证幂等）

---

## 8. 延迟预算总览

| 阶段 | 乐观 | 悲观 | 压缩手段 |
|------|------|------|---------|
| 学生说话 → ASR 完成 | 100ms | 500ms | 取决于 ASR 引擎 |
| ASR → submitLLM | < 10ms | < 10ms | 纯内存事件，不可再优化 |
| submitLLM → LLM 首句 | **预测命中：≈0**<br>不命中：500ms–2s | 3s+ | **预测机制**（最大杠杆） |
| LLM 首句 → TTS 首帧 | 200ms | 1s | TTS/板书并行 |
| TTS 首帧 → 客户端接收 | 20ms | 300ms | WebSocket 直推 |
| 客户端缓冲 → 播放 | 50ms | 500ms | jitter buffer 调优 |

端到端乐观（预测命中）：**~400ms**  
端到端悲观（慢思考，无预测）：**~4s**

预测机制的命中率是影响平均体验的最关键单一变量。

---

## 9. 小结

这套实时语音链路的核心思路：**把等待时间转化为有效工作**。

- 老师说话的时候，预热下一轮 LLM（消灭最大瓶颈）
- LLM 流式产出句子，每句立刻并行 TTS + 板书（不等全文）
- TTS 和板书并行生成，`thenCombine` 合流（互不等待）
- 字幕对齐在 TTS 生成时完成（成本下沉到服务端）
- 打断双保险（dispose + 标志位），防止体验灾难

这些设计的出发点都不是"更快的硬件"，而是"让同样的时间做更多事"——经典的延迟优化思路。

---

## 附：代码地图

| 主题 | 文件 |
|------|------|
| 轮次主状态机 | `rtc/classstate/RoundStart.java` |
| LLM 响应处理 | `rtc/service/LlmResponseHandlerImpl.java` |
| TTS + 板书生成 | `rtc/service/TeacherMessageService.java` |
| 下行消息构建与发送 | `rtc/service/DownwardMessageSender.java` |
| 输入预测任务 | `rtc/service/UserInputPredictedTask.java` |
| 事件总线 | `rtc/eventbus/ClassRoomEventBus.java` |
| **架构文档** | [[notes/reference-docs/LLM响应处理流程文档.md|LLM 响应处理流程文档]] |
