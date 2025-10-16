---
title: "Manage Context"
sidebar_position: 3
---

The **context window** refers to the entirety of the amount of text a language model can look back on and reference when generating new text plus the new text it generates. This is different from the large corpus of data the language model was trained on, and instead represents a **working memory** for the model. It includes your messages, Claude's responses, file contents, and tool outputs. 

![](/img/context1.png)

## Why Manage Context Window

As context windows fill up, LLM performance actually decreases. Models become less precise, are more prone to error, and struggle with complex reasoning when operating near token limits. Context window awareness prevents performance degradation and ensures consistent results.

> 💡 Use compaction explicitly, do not rely on auto-compaction.

> 💡 Use `/compact` and `/rewind` when it makes sense. Use `/context` to get an overview of the current context. And make a decision to start fresh `/clear` or to compact with the focus on particular subject `/compact`. See [Manage Session](/tips-and-tricks/manage-sessions) for more details on session commands.

> 💡 Break large tasks into smaller pieces that can be completed within optimal context bounds. Avoid the last fifth of the context window for memory-intensive tasks.

> 💡 Use **"structured notes"** taking approach when you need to re-use context and store it for later use. For example, you could ask Claude Code something like: "Please write a summary of this conversation to design-decision.md and focus on key decisions and findings we explored during this session"

![](/img/context2.png)

## Additional References

- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - Anthropic's comprehensive guide to context engineering techniques
- See amazing [Advanced Context Engineering for Agents](https://www.youtube.com/watch?v=IS_y40zY-hc)
- [advanced-context-engineering-for-coding-agents](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents)
- [12-factor-agents](https://github.com/humanlayer/12-factor-agents)