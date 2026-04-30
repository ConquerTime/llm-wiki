---
epoch: 1777467154682
modelKey: "MiniMax-M2.7|anthropic"
topic: "LLM Providers Overview"



tags:
  - copilot-conversation
---

**user**: | Provider | 说明 |
|----------|------|
| OpenaiLLM | 标准 OpenAI SSE 流式 |
| GeminiLLM | Google Gemini |
| DeepseekLLM | DeepSeek |
| TongyiLLM | 阿里通义 |
| VLLM | 自托管 vLLM 推理服务 |
| KanyunLLM | 内部模型服务 |
| AnthropicClaudeLLM | Anthropic Claude |
| AudioChatLlamaLLM | 语音原生 LLM：直接接收 PCM/URL 音频，audio_hex 或 audio_url 格式，支持 system_id 短系统提示 |

这段 md 的表格为什么无法渲染
[Context: Notes: projects/2026-04-aitutor-arch/brief.md]
[Timestamp: 2026/04/29 20:52:34]

**ai**: 
<think>The user is asking why the table in their markdown note is not rendering. Let me look at the table they provided:

```
| Provider | 说明 |
|----------|------|
| OpenaiLLM | 标准 OpenAI SSE 流式 |
| GeminiLLM | Google Gemini |
| DeepseekLLM | DeepSeek |
| TongyiLLM | 阿里通义 |
| VLLM | 自托管 vLLM 推理服务 |
| KanyunLLM | 内部模型服务 |
| AnthropicClaudeLLM | Anthropic Claude |
| AudioChatLlamaLLM | 语音原生 LLM：直接接收 PCM/URL 音频，audio_hex 或 audio_url 格式，支持 system_id 短系统提示 |


```

I'm noticing the table has inconsistent pipe spacing and formatting issues that could be preventing proper rendering. The real culprit is probably the HTML comment at the top of the file—Obsidian's Live Preview mode might be choking on that tag, especially if there's an unclosed or malformed comment interfering with the parser.
</think>

可能是文件开头那段 HTML 注释（`<active_note>...</active_note>`）没有闭合，被当成了未结束的 HTML 标签处理，导致后面的 markdown 内容解析异常。

**解决方案：删除这段注释**（这是系统内部元数据，Obsidian 会自动管理，不需要写在文档里）。

如果只是想保留项目标记，可以改用纯 markdown 格式：

```markdown
---
project: 2026-04-aitutor-arch
status: active
created: 2026-04-29
updated: 2026-04-29
---

# AI 家教技术架构萃取 · 简报
```

或者干脆从文件开头去掉那段注释即可。
[Timestamp: 2026/04/29 20:52:47]