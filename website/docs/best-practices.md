---
title: "🎯 Best Practices"
sidebar_position: 1
description: "A guide to effective development patterns and techniques using Claude Code"
keywords: [best practices, claude code, development]
---

# 🎯 Claude Code Best Practices

A guide to effective development patterns and techniques using Claude Code.

---

## 🧘 Claude Code Is Self-Aware

Claude Code is self-aware and driven by human language. So many discrete capabilities can be discovered and triggered through conversation.

- **Ask Claude directly** about its capabilities: "What tools do you have?"
- **Explore features** through conversation:
   - "Can you run tasks in the background?"
   - "Please search the web for..."
   - "Extract the content of this website and summarize it"
- **Understand limitations** by testing boundaries

> 💡 You can go even further and setup [Claude Code Docs](/extras/claude-code-docs) to enhance Claude Code with `/docs` and work with most recent documentation directly from Claude Code.

---

## 🔎Explore → 📃Plan → 🤖Implement → 🧪Evaluate

This is a structured multi-stage approach for implementing features with Claude Code based on Plan Mode and Context Priming (aka Context Grounding).

**When to use:** New features, bug fixes, refactoring tasks. This is your daily driver for structured development.

**Stage 1: Context Priming**
- Research and understand the problem space
- Provide Claude with proper context about the codebase
- Share requirements and implementation details
- Help Claude understand existing patterns and architecture

**Stage 2: Planning**
- Use Claude Code's **Plan Mode** to create an implementation plan
- Review the plan thoroughly before proceeding
- Ensure all edge cases and requirements are covered

**Stage 3: Implementation**
- Let Claude Code follow the plan autonomously
- Monitor progress and inspect changes as they happen
- Provide additional context or course-correct if needed

**Stage 4: Evaluation**
- Enable Claude Code to evaluate the task outcome
- Use unit tests and integration tests for validation
- For frontend changes, use Playwright or similar tools to verify visual results
- Find a way to somehow close the feedback loop and give feedback to Claude

> 💡 Act as a supervisor during implementation - stay engaged but let Claude work through the plan independently.

> 💡 The evaluation stage is crucial - having automated tests or visual verification tools ready before starting saves time and ensures quality.

More at [Extended Plan Mode](/tips-and-tricks/extended-plan-mode).

---

## 📝 Prompt Engineering

The best practices of working with Anthropic's Claude models are covered in the [docs/build-with-claude/prompt-engineering/claude-4-best-practices](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices).

But it is good idea to have a good understanding of general prompt engineering principles:

* Be precise and specific
* Provide context (one or few short learning by examples)
* Break things down (simplification)
* Use clear language (use proper terminology, avoid ambiguity)
* Set expectations and limitations
* Experiment (tune the prompt to have better answer)
* Role play scenarios (set roles to you, to somebody who respond, to the chat, etc.)
* Explanation using Analogies
* Debate-style questions (ask argument for and against to have more understanding)

> 💡 In Claude Code you can apply your knowledge of prompt engineering when you create [Custom Slash Commands](./tips-and-tricks/custom-slash-commands) and [Subagents](./tips-and-tricks/subagents)

More guides at [Prompt Engineering Guide](https://www.promptingguide.ai/), [Learn Prompting](https://learnprompting.org/docs/introduction)

---

## ⚖️ Context Engineering

> 🗣️ “Context engineering is the delicate art and science of filling the context window with just the right information for the next step.” — Andrej Karpathy


- Provide relevant files and examples
- Perform prior code base/feature exploration and ask Claude to focus on relevant parts
- Use web search and MCPs to gather additional context and information

> 💡 Be aware of context limits and how it may impact the quality of responses. It is better to keep your context short and focused.

> 💡 Use MCP servers for latest/authoritative information. E.g.: [Microsoft Docs MCP](https://learn.microsoft.com/en-us/training/support/mcp), [Context7](https://context7.com/)

> 💡 Explicitly mention relevant tools and resources that could assist Claude in understanding the context better.

> 💡 Hint Claude in the right direction. E.g.: "Hint: you might want to check relevant tests for this functionality"

See [Manage Context](/tips-and-tricks/manage-context) for more information about context window and strategies for effective context management.

---

## 🧠 Brainstorming & Ideation

Use Claude Code to brainstorm and generate ideas for complex problems. Treat it as a peer developer that can provide multiple perspectives, give you fresh ideas and provide constructive feedback.

- Ask Claude to brainstorm multiple approaches and iterate on ideas
- Use generated ideas as grounding context for subsequent prompts
- Build on previous suggestions rather than starting from scratch

> 💡 Be direct in a way you interact with LLM. E.g.: "give me 3 results and compare pros and cons for each result using markdown tables"

> 💡 For common tasks, you can create re-usable slash commands to help you to describe your problem solving approach, e.g.: `/five` command - Use the "Five Whys" root cause analysis technique

---
## ⚙️ Know How to Customize Claude

> “Claude Code is intentionally low-level and unopinionated, providing close to raw model access without forcing specific workflows. This design philosophy creates a flexible, customizable, scriptable, and safe power tool. While powerful, this flexibility presents a learning curve for engineers new to agentic coding tools—at least until they develop their own best practices.”

By design, Claude Code is a flexible and customizable tool that can be adapted to various workflows and preferences. To get the most out of Claude Code, it's important to understand how to configure its settings and capabilities.

Claude Code offers a variety of settings to configure its behavior to meet your needs. You can configure Claude Code by running the `/config` command when using the interactive REPL, which opens a tabbed Settings interface where you can view status information and modify configuration options.

Configure Claude Code with **global** and **project-level** settings, and environment variables.

* [Permissions](https://docs.anthropic.com/en/docs/claude-code/settings#permission-settings)
* [Available Tools](https://docs.anthropic.com/en/docs/claude-code/settings#tools-available-to-claude)
* [Custom Slash Commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands)
* [Sub-Agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)

## 🎯 Tips for Success

### Communication
- Learn the basics of Prompt Engineering
- Be specific about requirements and constraints
- Provide context about your development environment
- Ask for explanations when solutions aren't clear

### Iteration
- Start with working solutions, then optimize
- Use feedback loops to refine approaches
- Don't hesitate to backtrack and try different methods

### Learning
- Experiment with different prompt styles
- Learn from Claude's reasoning and explanations
- Build a personal knowledge base of effective patterns
