// notes-map.js — 溢出文案 / 口播补偿
//
// 约定：键是 slide 页码（1 基），值是 speaker notes 字符串。
// 当 HTML 前景文字装不下安全区时，**不要缩字号**，把溢出内容写到这里。
// 没有溢出/补偿需求的页可以省略。

module.exports = {
  4: `【口播 · Harness 五类组件】
— Tools：bash / read / write / edit / glob / grep / browser — Claude Code 实现了 30+ 个工具方法
— Knowledge：CLAUDE.md、skill 文件、领域文档都属于这一层
— Observation：每轮 LLM 调用前注入 git diff、错误日志、浏览器状态
— Permissions：cc-haha 里有精细的 allow/deny 权限治理，默认拒绝危险操作`,

  7: `【口播 · 最小 Agent Loop 细节】
— run_tools() 对每个 tool_use block 依次执行，返回 tool_result 列表
— messages[] 持续累积：user → assistant → tool_result → assistant → ...
— cc-haha queryLoop 有 7 个以上 continue 站点，处理各种中断 / 重试 / 压缩触发
— 最小实现和生产实现的本质差异：错误处理、token 计数、权限检查；循环结构完全相同`,

  12: `【口播 · Subagent 四条 Fork 路径（cc-haha）】
— Fork 1：新 tmux 窗口（独立终端，视觉可见）
— Fork 2：新 iTerm2 tab（macOS 专用）
— Fork 3：in-process（AsyncLocalStorage 上下文隔离，最快）
— Fork 4：worktree 绑定（s12 的隔离执行模式）
— 禁止递归生成：child agent 的 TOOLS 列表里不包含 AgentTool`,

  13: `【口播 · cc-haha 5 层压缩策略细节】
— Snip：只裁剪最老的几轮，保留最近完整历史
— Micro Compact：把 3 轮前的 tool_result 替换为 [result truncated: N chars]
— Context Collapse：整段历史折叠成一个摘要 block
— Auto Compact：token 超阈值时触发 LLM 摘要
— Session Memory：跨会话提取记忆，写入 .claude/memory/
— 熔断器：压缩操作本身不得消耗超过可用 token 的 20%`,

  16: `【口播 · cc-haha 执行后端选择逻辑】
— in-process：开发测试首选，无系统开销
— tmux：生产环境首选，每个队友一个 window，可 attach 查看
— iTerm2：macOS 本地开发的视觉调试选项
— 邮箱格式：{"type":"message","from":"orchestrator","to":"coder","body":"...","request_id":"uuid"}
— drain-on-read：读完就清空文件，避免重复处理历史消息`,

  19: `【口播 · 三个最值得精读的 cc-haha 模块】
— AgentTool：子 agent 的完整生命周期，Fork 四路径，context 传递方式
— Skills：6 种来源的优先级顺序，realpath 去重原理，bundled skills 延迟解压
— Memory：5 层压缩的选择逻辑，熔断器实现，跨会话记忆的 diff 策略`,
};
