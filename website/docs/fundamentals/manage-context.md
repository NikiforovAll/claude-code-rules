---
title: "Manage Context"
sidebar_position: 1
---

The **context window** refers to the entirety of the amount of text a language model can look back on and reference when generating new text plus the new text it generates. This is different from the large corpus of data the language model was trained on, and instead represents a **working memory** for the model. It includes your messages, Claude's responses, file contents, and tool outputs. 

![](/img/context1.png)

## Why Manage Context Window

As context windows fill up, LLM performance actually decreases. Models become less precise, are more prone to error, and struggle with complex reasoning when operating near token limits. Context window awareness prevents performance degradation and ensures consistent results.

**The Problem: Context Rot**

💡 **Key Insight**: LLMs have an "attention budget" that gets depleted as context grows

- Every token attends to every other token (n² relationships)
- As context length increases, model accuracy decreases
- Models have less training experience with longer sequences
- Context must be treated as a finite resource with diminishing marginal returns



### Context Engineering vs Prompt Engineering

| Approach | Definition | Scope |
|----------|------------|-------|
| **Prompt Engineering** | Writing and organizing LLM instructions for optimal outcomes | One-time task |
| **Context Engineering** | Curating and maintaining the optimal set of tokens during inference across multiple turns | Iterative process |

![](/img/context2.png)

## System Prompts: Find the "Right Altitude"

System Prompt is a special instruction that sets the behavior of an agent/subagent. System prompts directly impact context management.

### The Goldilocks Zone

**Too Prescriptive** ❌
- Hardcoded if-else logic
- Brittle and fragile
- High maintenance complexity

**Too Vague** ❌
- High-level guidance without concrete signals
- Falsely assumes shared context
- Lacks actionable direction

**Just Right** ✅
- Specific enough to guide behavior effectively
- Flexible enough to provide strong heuristics
- Minimal set of information that fully outlines expected behavior

**Best Practices:**
- Use simple, direct language
- Organize into distinct sections (`<background_information>`, `<instructions>`, `## Tool guidance`, etc.)
- Use XML tags or Markdown headers for structure
- Start with minimal prompt, add based on failure modes

## Long-Horizon Tasks: Three Techniques

When working on tasks that require long-term context retention, consider these three techniques to manage context effectively:

### 1. Compaction
**What**: Summarize conversation nearing context limit, reinitiate with summary

**Implementation**:
- Pass message history to model for compression
- Preserve critical details (architectural decisions, bugs, implementation)
- Discard redundant outputs
- Continue with compressed context + recently accessed files

**Tuning Process**:
1. **First**: Maximize recall (capture all relevant information)
2. **Then**: Improve precision (eliminate superfluous content)

**Low-Hanging Fruit**: Clear old tool calls and results

**Best For**: Tasks requiring extensive back-and-forth

### 2. Structured Note-Taking
**What**: Agent writes notes persisted outside context window, retrieved later

**Examples**:
- To-do lists
- NOTES.md files
- Game state tracking (Pokémon example: tracking 1,234 steps of training)
- Project progress logs

**Benefits**:
- Persistent memory with minimal overhead
- Maintains critical context across tool calls
- Enables multi-hour coherent strategies

**Best For**: Iterative development with clear milestones

### 3. Sub-Agent Architectures
**What**: Specialized sub-agents handle focused tasks with clean context windows

**How It Works**:
- Main agent coordinates high-level plan
- Sub-agents perform deep technical work
- Sub-agents explore extensively (tens of thousands of tokens)
- Return condensed summaries (1,000-2,000 tokens)

**Benefits**:
- Clear separation of concerns
- Parallel exploration
- Detailed context remains isolated

**Best For**: Complex research and analysis tasks

## Tips & Tricks

> 💡 Use compaction explicitly, do not rely on auto-compaction.

> 💡 Use `/compact` and `/rewind` when it makes sense. Use `/context` to get an overview of the current context. And make a decision to start fresh `/clear` or to compact with the focus on particular subject `/compact`. See [Manage Session](../tips-and-tricks/manage-sessions) for more details on session commands.

> 💡 Break large tasks into smaller pieces that can be completed within optimal context bounds. Avoid the last fifth of the context window for memory-intensive tasks.

> 💡 Use **"structured notes taking"** approach when you need to re-use context and store it for later use. For example, you could ask Claude Code something like: "Please write a summary of this conversation to design-decision.md and focus on key decisions and findings we explored during this session". See more at [Structured Note-Taking](./structured-note-taking)

## Additional References

- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - Anthropic's comprehensive guide to context engineering techniques
- See amazing [Advanced Context Engineering for Agents](https://www.youtube.com/watch?v=IS_y40zY-hc)
- [advanced-context-engineering-for-coding-agents](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents)
- [12-factor-agents](https://github.com/humanlayer/12-factor-agents)