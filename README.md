# 🤖 Claude Code Rules

A collection of [Claude Code AI rules](https://docs.anthropic.com/en/docs/claude-code/overview) for development best practices.

## Practical Recommendations

Explore common use cases for Claude Code: [claude-code/common-tasks](https://docs.anthropic.com/en/docs/claude-code/common-tasks).

⭐ Learn best practices for Claude Code: [engineering/claude-code-best-practices](https://www.anthropic.com/engineering/claude-code-best-practices).

Here is my list of practical recommendations for using Claude Code:

### Planning

- Ask “think hard” to trigger deep thinking:
    - "think" < "think hard" < "think harder" < "ultrathink."
- Ask Claude to brainstorm ideas and iterate on them. Later, these ideas can be used as grounding context for your prompts.
- Write a plan to an external source (e.g., file - plan.md) and use it as a checklist.
- `plan.prompt.md` - use an external file as memory for task management and planning.
- `plan mode` vs `auto-accept mode` vs `edit mode`:
    - Verify what is about to be performed using `plan mode`.
    - Once verified, proceed with `auto-accept mode`.
    - Step-by-step mode is the default mode with no auto-accept.
- Workflows:
    - a. Explore, plan, code, commit.
    - b. Write tests, commit; code, iterate, commit.
    - c. Write code, screenshot results, iterate.

### Knowledge Mining / Grounding

- Use the `/init` command to initialize the `CLAUDE.md` file. There’s no required format for `CLAUDE.md` files. I recommend keeping it concise and human-readable. You can use it to store important information about your project, such as architecture, design decisions, and other relevant details that can help Claude understand your codebase better.
- `CLAUDE.md` can open other files like this: `@path/to/import`. Be careful, as this file is attached every time you submit a prompt.
- You can use `# <text>` to add particular memory to the `CLAUDE.md` file.
- There are two different types:
  - Project memory `./CLAUDE.md` - share it with your team.
  - User memory `~/.claude/CLAUDE.md` - personal preferences.
- `# <text>` - short-term memory, which is cleared after the session ends.
- Use `/memory` to edit the memory file directly. It will open the file in your default editor.

- Codebase Q&A: Use Claude Code to ask questions about your codebase. It can help during onboarding or when you need to understand how something works.
- Use hints, reference files, provide examples, mention documentation, and provide links.

### Miscellaneous
- Use in “pipe” mode, as Unix philosophy utils: `claude -p ""` or `echo '' | claude -p ""`.
- 🗑️ `/clear` and `/compact <specific prompt for aggregation>` can be very helpful.
- 🧠 If you don’t know something about Claude Code, ask it! It’s self-aware.
    - E.g., What kind of tools do you have? Can you perform a web search?

## MCP Servers

You can use MCP servers. See [claude-code/mcps](https://docs.anthropic.com/en/docs/claude-code/mcps).

## Vibe Coding Workflow: AI Task-Based Development

- Use `/create-prd` to create a Product Requirements Document (PRD) based on user input.
- Use `/generate-tasks` to create a task list from the PRD.
- Use `/process-task-list` to manage and track task progress.

## Useful Links

* General Prompt Engineering with Claude Models - <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview>
* Interactive Tutorial for Prompt Engineering - <https://github.com/anthropics/prompt-eng-interactive-tutorial>
* CLI Usage - <https://docs.anthropic.com/en/docs/claude-code/cli-usage>
* ⭐ Tutorials - <https://docs.anthropic.com/en/docs/claude-code/tutorials>
* Claude Code Memory - <https://docs.anthropic.com/en/docs/claude-code/memory>

## 💳 Credits

Inspired by:
- <https://github.com/NikiforovAll/dotnet-copilot-rules>
- <https://github.com/snarktank/ai-dev-tasks>
