---
title: "Prompt Engineering Techniques"
sidebar_position: 12
description: "Practical prompting techniques to get better results from Claude Code — from structural frameworks to advanced reasoning methods"
keywords: ["prompt engineering", "prompting", "4 W's", "meta prompting", "verbalized sampling", "Q&A prompting", "few-shot", "chain of thought"]
---

# Prompt Engineering Techniques

Effective prompting is a core skill for getting the most out of Claude Code. This guide covers techniques ranging from simple structural frameworks to advanced methods for increasing AI reasoning quality and creativity.

## The 4 W's (What, How, Why, When)

A framework for building detailed, well-scoped prompts by stacking four layers of context:

| Layer | Purpose | Example |
|-------|---------|---------|
| **What** | The specific task or goal | "Add pagination to the /users API endpoint" |
| **How** | Style, format, or constraints | "Use cursor-based pagination, follow existing patterns in orders.ts" |
| **Why** | Context or purpose | "The current endpoint returns all users at once, causing timeouts on large datasets" |
| **When** | Timeframe or scope limits | "Only modify the users service — don't touch the frontend yet" |

**Example prompt using 4 W's:**

```markdown
<!-- What: the task -->
Add cursor-based pagination to the /users API endpoint.

<!-- How: style and patterns -->
Follow the same pattern used in src/services/orders.ts.

<!-- Why: the problem -->
The current endpoint returns all records at once, which causes
timeouts when the user table exceeds 10k rows.

<!-- When: scope -->
Scope this to the backend service only — frontend changes come later.
```

The 4 W's help ensure your prompt isn't missing crucial context that leads to off-target results.

### Iterative Refinement

A systematic approach to building up prompts through progressive layers:

1. **Start basic** — Write the core instruction
2. **Add examples** — Show expected input/output
3. **Add constraints** — Specify boundaries and edge cases
4. **Specify format** — Define output structure
5. **Add reasoning** — Request step-by-step thinking

Each iteration refines based on where the previous output fell short.

## Advanced Techniques

### Meta Prompting

Use Claude to help you design better prompts. Instead of crafting the perfect prompt yourself, ask Claude to generate one.

```text
Act as a prompt engineer. I need to write a prompt that will help me
migrate our Express.js middleware to a new error-handling pattern.
Generate the best possible prompt for this task, including all the
context I should provide.
```

**Advanced usage**: In multi-agent architectures, a "conductor" model can generate specialized prompts for sub-agents, each handling a focused subtask — then synthesize results into a final output.

**When to use**: Complex tasks where you're unsure how to frame the request, or when you want to discover angles you hadn't considered.

### Q&A Prompting (Ask Before Answering)

Instruct Claude to ask clarifying questions *before* starting work. This prevents assumptions on ambiguous requests.

```text
I want to add caching to our API layer. Before you start implementing,
ask me 5 clarifying questions about our requirements and constraints.
```

Claude might then ask about cache invalidation strategy, TTL requirements, which endpoints to cache, whether you need distributed caching, etc. — leading to a much more targeted implementation.

**When to use**: Open-ended tasks, architectural decisions, or any request where missing context could lead to significant rework.

### Verbalized Sampling

A technique to overcome **mode collapse** — the tendency of AI to produce the single "safest" or most typical response.

```text
Generate 5 different approaches to implementing real-time notifications
in our app. For each approach, assign a probability score reflecting
how likely you'd normally be to suggest it, and explain the trade-offs.
```

This forces the model to reveal less-likely but potentially more creative or suitable options that it would normally filter out. The probability scores help you understand which approaches are conventional vs. unconventional.

**When to use**: Brainstorming, architecture decisions, or any situation where you want to explore the full solution space rather than getting a single "default" answer.

### Chain-of-Thought Prompting

Ask Claude to reason step-by-step before arriving at a conclusion. This improves accuracy on complex reasoning tasks.

```text
Analyze why our WebSocket connections drop after exactly 30 seconds.
Think through this step by step — check timeout configs, proxy settings,
load balancer configuration, and keep-alive intervals.
```

**When to use**: Debugging, root cause analysis, complex logic problems.

:::tip
Claude Code supports [extended thinking](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking) — see the [Ultrathink](/tips-and-tricks/ultrathink) tip for details on triggering deeper reasoning.
:::

## Reasoning Strategies as Prompt Building Blocks

LLMs are already trained on well-known reasoning strategies — you don't need to explain the technique, just **name it**. This makes them powerful building blocks for the **"How"** layer in your prompts.

| Strategy | Abbreviation | Key Phrase | Best For |
|----------|-------------|------------|----------|
| Chain-of-Thought | CoT | "Think through step by step" | Math, planning, debugging |
| Tree-of-Thought | ToT | "Consider multiple approaches" | Architecture, creative solutions |
| Atom-of-Thought | AoT | "Break into independent parts" | Coding, modular design |
| Chain-of-Draft | CoD | "Draft, then refine" | Long-form content, documentation |
| Reflexion | — | "Critique your solution" | Code review, quality assurance |
| Self-Consistency | — | "Try multiple ways, find consensus" | High-precision factual tasks |

**Example — just reference by name:**

```markdown
<!-- What -->
Architect the notification service for our app.

<!-- How: reasoning strategy -->
Use Tree-of-Thought reasoning — propose 3 different architectures,
evaluate trade-offs for each, then recommend the best option.
```

**Strategies compose well.** For example, a code review workflow might chain: AoT (segment code into reviewable parts) → Reflexion (critique each section) → CoT (trace logical flow).

For a detailed breakdown of each strategy with examples, see [Reasoning Strategies](https://nikiforovall.blog/github-copilot-rules/fundamentals/reasoning-strategies).

## Combining Techniques

These techniques compose well. A strong prompt for a complex task might combine several:

```markdown
<!-- Why: context and motivation -->
Our e-commerce checkout has a 12% cart abandonment rate at the payment
step. We need to fix this before the holiday sale next month.

<!-- What + How: task and constraints -->
Propose improvements to the payment flow in src/checkout/.
Follow our existing React patterns and use Stripe's latest API.

<!-- Q&A gate: clarify before acting -->
Before proposing changes, ask me 3 questions about our current
payment flow and known pain points.

<!-- Verbalized sampling: explore the solution space -->
Then generate 3 different approaches with confidence scores,
ranging from conservative to ambitious.
```

## Tips for Claude Code Specifically

- **Start specific, not generic** — Claude Code has full codebase access. Reference specific files, functions, and patterns.
- **Use context priming** — Before a complex task, ask Claude to read relevant files first: "Read src/auth/ and summarize the current authentication flow." See [Manage Context](./manage-context) for more on this.
- **Leverage [`CLAUDE.md`](./use-claude-md)** — Put recurring style/format instructions in your project's `CLAUDE.md` rather than repeating them in every prompt.
- **Break large tasks down** — Use [Extended Plan Mode](./extended-plan-mode) or [Structured Plan Mode](./structured-plan-mode) for complex multi-step work instead of trying to cram everything into one prompt.
- **Manage context** — Long conversations degrade quality. See [Manage Context](./manage-context) for techniques to keep context sharp.

## Additional References

- [Prompt Engineering Fundamentals](https://nikiforovall.blog/github-copilot-rules/fundamentals/prompt-engineering) — Zero-shot, few-shot, and prompt structure basics
- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — Official techniques for prompting Claude models
- [Verbalized Sampling: A Training-Free Prompting Technique](https://medium.com/data-science-collective/verbalized-sampling-how-one-single-prompt-can-bring-back-the-creative-potential-of-large-language-92f291519854) — Deep dive into restoring LLM diversity
- [Meta Prompting: A Complete Guide](https://www.prompthub.us/blog/a-complete-guide-to-meta-prompting) — Using AI to design better prompts
