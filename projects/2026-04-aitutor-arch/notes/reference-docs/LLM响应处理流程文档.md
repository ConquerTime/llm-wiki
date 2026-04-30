# LLM 响应处理流程文档

## 一、整体架构概览

```
+-------------------------------------------------------------------------+
|                           LLM 响应处理流程                                |
+-------------------------------------------------------------------------+
|                                                                         |
|  用户语音输入 (ASR)                                                       |
|       |                                                                 |
|       v                                                                 |
|  AsrComplete (语音识别完成)                                               |
|       |                                                                 |
|       v                                                                 |
|  StudentActivityManager.checkActivity() --> 触发 LLM 请求                |
|       |                                                                 |
|       v                                                                 |
|  RoundStart.submitLLM() --> llmConversationService.chatWithLLm()        |
|       |                                                                 |
|       v                                                                 |
|  LlmResponseHandlerImpl.onEvent() <-- LLM 流式响应 (逐句返回)             |
|       |                                                                 |
|       v                                                                 |
|  eventBus.publish(TeacherMessageEvent)                                  |
|       |                                                                 |
|       v                                                                 |
|  RoundStart.handlerThisRoundEvent()                                     |
|       |                                                                 |
|       v                                                                 |
|  DownwardMessageSender.sendAudioMessage() --> WebSocket 发送给客户端     |
|                                                                         |
+-------------------------------------------------------------------------+
```

---

## 二、核心类职责

| 类名 | 职责 |
|------|------|
| RoundStart | 一轮对话的状态管理，负责发起 LLM 请求和处理响应事件 |
| LlmResponseHandlerImpl | LLM 响应处理器，解析 LLM 输出、生成 TTS、构建 TeacherMessage |
| TeacherMessageService | 生成 TTS 音频和板书指令 |
| DownwardMessageSender | 构建并发送消息给客户端 |
| ClassRoomEventBus | 事件总线，用于组件间通信 |

---

## 三、详细处理流程

### 3.1 发起 LLM 请求

**入口**: `RoundStart.submitLLM()`

```java
private void submitLLM() {
    // 1. 构建 LLM 上下文（历史对话 + 当前用户输入 + Section 配置）
    LLMConversationContext context = getLlmConversationContext(classLLMContext, sectionState);

    // 2. 构建响应处理器
    LlmResponseHandler handler = new LlmResponseHandlerImpl(
        roomContext, roundIndex, studentMessage, clock, sectionState,
        teacherMessageService, roomEventRecorder, eventBus, ...);

    // 3. 发起异步流式调用
    teacherLLMMessageDisposable = llmConversationService.chatWithLLm(context)
        .subscribeOn(Schedulers.from(ClassRoomExecutors.getLLMExecutor()))
        .subscribe(handler::onEvent, handler::onError, handler::onComplete);
}
```

**LLMConversationContext 包含**:

- 历史对话上下文 (LLMSectionHistoryContext)
- 当前用户输入 (StudentMessage)
- Section 配置 (提示词、板书配置等)

---

### 3.2 处理 LLM 流式响应

**入口**: `LlmResponseHandlerImpl.onEvent()`

LLM 以流式方式返回响应，每返回一句话触发一次 onEvent：

```java
public void onEvent(LLMConversationData llmConversationData) {
    RoundLlmSentence roundLlmSentence = (RoundLlmSentence) llmConversationData.getLlmResponseData();
    LLMSentence llmSentence = roundLlmSentence.getLlmSentence();

    // Step 1: 检查 Section 是否结束
    if (llmSentence.getXmlTagElements("end").isNotEmpty()) {
        isSectionOver = true;
    }

    // Step 2: 异步生成 TTS 音频
    CompletableFuture<TtsResult> ttsResultFuture =
        teacherMessageService.asyncGenerateTts(llmSentence.getTalkSentence(), ...);

    // Step 3: 异步生成板书指令
    CompletableFuture<List<LLMResponseBoardCommand>> boardCommandsFuture =
        teacherMessageService.asyncGeneratePostPptBoardCommands(...);

    // Step 4: 等待异步任务完成，构建 TeacherMessage
    TeacherMessage teacherMessage = ttsResultFuture
        .thenCombine(boardCommandsFuture, this::buildTeacherMessage)
        .join();

    // Step 5: 发布事件到事件总线
    eventBus.publish(new TeacherMessageEvent(roundIndex, teacherMessage));
}
```

---

### 3.3 构建 TeacherMessage

**方法**: `LlmResponseHandlerImpl.buildTeacherMessage()`

从 LLM 响应中解析各类指令：

```java
private TeacherMessage buildTeacherMessage(LLMSentence llmSentence, TtsResult ttsResult, ...) {

    // 1. 使用流式处理器解析 LLM 指令
    List<LlmCommand> allLlmCommands = commandProcessor.process(llmSentence);

    // 2. 按类型分离指令
    for (LlmCommand cmd : allLlmCommands) {
        if (cmd instanceof LLmResponseGenImage)    genImages.add(...);       // 生图
        if (cmd instanceof StandardEmotion)        emotions.add(...);        // 表情
        if (cmd instanceof StandardBoardCommand)   boardCommands.add(...);   // 板书
        if (cmd instanceof NavigatePage)           navigatePages.add(...);   // 翻页
    }

    // 3. 解析特殊标签
    StandardClassBreak classBreak = buildStandardClassBreak(llmSentence.getXmlTagElements("rest"));
    List<StandardReward> rewards = buildRewardCommands(llmSentence);

    // 4. 构建最终消息
    return TeacherMessage.builder()
        .text(ttsResult.getText())
        .ttsResult(ttsResult)
        .genImageCommands(genImages)
        .boardCommands(boardCommands)
        .standardEmotions(emotions)
        .navigatePageCommands(navigatePages)
        .standardClassBreak(classBreak)
        .standardRewards(rewards)
        .sectionOver(isSectionOver)
        .lastRoundAudio(isLastSentence)
        .build();
}
```

**TeacherMessage 数据结构**:

| 字段 | 类型 | 说明 |
|------|------|------|
| text | String | TTS 文本 |
| ttsResult | TtsResult | TTS 音频数据 + 时间轴 |
| genImageCommands | List | 生图指令 |
| boardCommands | List | 板书指令 |
| standardEmotions | List | 表情指令 |
| navigatePageCommands | List | 翻页指令 |
| standardClassBreak | Object | 课间休息 |
| standardRewards | List | 奖励指令 |
| sectionOver | boolean | Section 是否结束 |
| lastRoundAudio | boolean | 是否本轮最后一句 |

---

### 3.4 处理 TeacherMessageEvent

**入口**: `RoundStart.handlerThisRoundEvent()`

```java
private void handlerThisRoundEvent(IOEvent event) {
    if (event instanceof TeacherMessageEvent) {
        TeacherMessage teacherMessage = ((TeacherMessageEvent) event).getTeacherMessage();

        // 1. 处理翻页指令
        processNavigateCommands(teacherMessage.getNavigatePageCommands());

        // 2. 处理生图指令 (异步)
        onGenImage(teacherMessage.getGenImageCommands());

        // 3. 构建客户端消息包
        StandardAudioMessageBundle bundle = downwardMessageSender.buildAudioMessage(teacherMessage);

        // 4. 处理奖励和板书
        processRewardAndBoardCommand(teacherMessage, bundle);

        // 5. 发送给客户端 (如果没有被用户打断)
        if (!roundAudioStatus.isTeacherInterrupted()) {
            downwardMessageSender.sendAudioMessage(bundle);

            // 更新播放状态
            clientTeacherAudioPlayState.onTeacherMessage(teacherMessage, bundle);

            // 记录事件 (用于回放)
            roomEventRecorder.record(RoundTeacherAudioSentEvent...);
        }

        // 6. 预测下一轮用户输入 (如果是最后一句)
        if (teacherMessage.isLastRoundAudio()) {
            predictedUserInput(teacherMessage);
        }

        // 7. 处理 Section 结束
        if (teacherMessage.isSectionOver() && teacherMessage.isLastRoundAudio()) {
            eventBus.publish(new SectionOverLLMEvent(roundIndex));
        }
    }
}
```

---

### 3.5 发送给客户端

**方法**: `DownwardMessageSender.buildAudioMessage()` + `sendAudioMessage()`

```java
public StandardAudioMessageBundle buildAudioMessage(TeacherMessage teacherMessage) {
    // 1. 构建音频消息
    StandardAudioMessage audioMessage = StandardAudioMessage.builder()
        .id(nextId())
        .data(ttsResult.getAudioData())
        .url(ttsResult.getAudioUrl())
        .textAudioIntervalsList(textAudioIntervals)  // 文字-音频时间轴
        .isLastTeacherAudioFrame(teacherMessage.isLastRoundAudio())
        .build();

    // 2. 构建板书消息
    StandardBoardCommandMessage boardCommandMessage = ...;

    // 3. 构建表情消息
    StandardEmotionMessage emotionMessage = ...;

    // 4. 构建课间消息
    StandardClassBreakMessage classBreakMessage = ...;

    return StandardAudioMessageBundle.builder()
        .audioMessage(audioMessage)
        .boardCommandMessage(boardCommandMessage)
        .standardEmotionMessage(emotionMessage)
        .classBreakMessage(classBreakMessage)
        .build();
}

public void sendAudioMessage(StandardAudioMessageBundle bundle) {
    channel.sendAudioMessage(bundle);  // WebSocket 发送
}
```

**StandardAudioMessageBundle 结构**:

```
StandardAudioMessageBundle
|-- StandardAudioMessage          // 音频数据
|   |-- id                        // 消息ID
|   |-- data / url                // 音频二进制或URL
|   |-- textAudioIntervalsList    // 文字-音频时间轴 (用于字幕)
|   +-- isLastTeacherAudioFrame   // 是否最后一帧
|-- StandardBoardCommandMessage   // 板书指令
|-- StandardEmotionMessage        // 表情指令
|-- StandardClassBreakMessage     // 课间消息
+-- StandardTeacherMediaOverMessage // 媒体结束标记
```

---

## 四、打断处理机制

当用户在教师说话时打断 (AsrBreak / AsrStartBreak)：

```java
// RoundStart.onAsrMessage()
if (asrState instanceof AsrBreak || asrState instanceof AsrStartBreak) {
    // 1. 标记被打断
    roundAudioStatus.setTeacherInterrupted(true);

    // 2. 取消 LLM 订阅 (停止接收后续响应)
    teacherLLMMessageDisposable.dispose();

    // 3. 通知客户端
    downwardMessageSender.sendStudentSpeakStateMessage(SPEAK_BREAK);
}
```

后续 handlerThisRoundEvent 中检查打断标记：

```java
if (!roundAudioStatus.isTeacherInterrupted()) {
    downwardMessageSender.sendAudioMessage(bundle);  // 只有没被打断才发送
}
```

---

## 五、流程时序图

```
+--------+    +------------+    +---------------+    +------------+    +--------+
| Client |    | RoundStart |    | LlmHandler    |    | TtsService |    |  LLM   |
+---+----+    +-----+------+    +-------+-------+    +-----+------+    +---+----+
    |               |                   |                  |               |
    | ASR完成       |                   |                  |               |
    |-------------->|                   |                  |               |
    |               |                   |                  |               |
    |               | submitLLM()       |                  |               |
    |               |------------------>|                  |               |
    |               |                   |                  |               |
    |               |                   | chatWithLLm()    |               |
    |               |                   |--------------------------------->|
    |               |                   |                  |               |
    |               |                   |     流式响应(句子1)              |
    |               |                   |<---------------------------------|
    |               |                   |                  |               |
    |               |                   | asyncGenerateTts |               |
    |               |                   |----------------->|               |
    |               |                   |                  |               |
    |               |                   |   TtsResult      |               |
    |               |                   |<-----------------|               |
    |               |                   |                  |               |
    |               | TeacherMessageEvent                  |               |
    |               |<------------------|                  |               |
    |               |                   |                  |               |
    | AudioMsg      |                   |                  |               |
    |<--------------|                   |                  |               |
    |               |                   |                  |               |
    |               |                   |     流式响应(句子2)              |
    |               |                   |<---------------------------------|
    |               |                   |                  |               |
    |    ...        |     ...           |      ...         |     ...       |
```

---

## 六、关键配置项

| 配置 | 说明 |
|------|------|
| maxSilenceDurationMilliseconds | 用户沉默超时时间，超时后触发模拟输入 |
| userInputPredictedConfig | 用户输入预测配置，用于提前发起 LLM 请求 |
| hintMessageAssistantConfig | Hint 消息配置 (口算场景使用) |

---

## 七、相关文件路径

```
aitutor-classroom-legacy/src/main/java/com/yuanfudao/aitutor/aitutorclassroomjava/rtc/
|-- classstate/
|   +-- RoundStart.java                    # 轮次状态管理
|-- service/
|   |-- LlmResponseHandlerImpl.java        # LLM 响应处理
|   |-- TeacherMessageService.java         # TTS 和板书生成
|   |-- DownwardMessageSender.java         # 下行消息发送
|   +-- StudentActivityManager.java        # 学生活动管理
+-- ClassRoom.java                         # 教室主类
```

---

## 八、附录：完整数据流转图

```
+------------------+     +----------------------+     +------------------+
|   ASR 识别完成    |     |   LLM 流式响应        |     |   客户端接收      |
|   AsrComplete    |     |   RoundLlmSentence   |     |   AudioBundle    |
+--------+---------+     +-----------+----------+     +--------+---------+
         |                           |                         ^
         v                           v                         |
+--------+---------+     +-----------+----------+     +--------+---------+
| StudentActivity  |     | LlmResponseHandler   |     | DownwardMessage  |
| Manager          |     | Impl                 |     | Sender           |
| .checkActivity() |     | .onEvent()           |     | .sendAudioMsg()  |
+--------+---------+     +-----------+----------+     +--------+---------+
         |                           |                         ^
         v                           v                         |
+--------+---------+     +-----------+----------+     +--------+---------+
| RoundStart       |     | TeacherMessage       |     | StandardAudio    |
| .handleStudent   |---->| (TTS+板书+表情+指令)  |---->| MessageBundle    |
| ClientMessage()  |     |                      |     |                  |
+------------------+     +----------------------+     +------------------+
```
