

# 🎯 Claude Code Best Practices

A guide to effective development patterns and techniques using Claude Code.

<!-- vscode-markdown-toc -->
* 1. [📃 Planning & Problem Solving](#PlanningProblemSolving)
	* 1.1. [Explore → Plan → Code → Commit](#ExplorePlanCodeCommit)
	* 1.2. [Test-Driven Development](#Test-DrivenDevelopment)
	* 1.3. [Spec-Driven Development](#Spec-DrivenDevelopment)
	* 1.4. [Brainstorming & Ideation](#BrainstormingIdeation)
* 2. [🧠 Context Engineering](#ContextEngineering)
	* 2.1. [Context Grounding](#ContextGrounding)
	* 2.2. [Project Memory (`./CLAUDE.md`)](#ProjectMemory.CLAUDE.md)
	* 2.3. [Session Management](#SessionManagement)
* 3. [Extras. Tips & Tricks](#Extras.TipsTricks)
	* 3.1. [Self-Discovery & Capabilities](#Self-DiscoveryCapabilities)
	* 3.2. [Deep Thinking Nudges](#DeepThinkingNudges)
	* 3.3. [Command Line Integration](#CommandLineIntegration)
* 4. [Known How to Customize Claude](#KnownHowtoCustomizeClaude)
* 5. [🎯 Tips for Success](#TipsforSuccess)
	* 5.1. [Communication](#Communication)
	* 5.2. [Iteration](#Iteration)
	* 5.3. [Learning](#Learning)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

##  1. <a name='PlanningProblemSolving'></a>📃 Planning & Problem Solving

###  1.1. <a name='ExplorePlanCodeCommit'></a>Explore → Plan → Code → Commit

- Research and understand the problem space
- Create a detailed implementation plan using Claude's **Plan Mode**
- Write the code following the plan
- Commit with descriptive messages

**When to use:** New features, bug fixes, refactoring tasks. This is your daily driver for structured development.

💡 Use commits as checkpoints, commit frequently, use the `/commit` ([git commit](./.claude/commands/dev-workflow/commit.md)) command to automate commit creation.

💡 Use `git worktree` for parallel development

###  1.2. <a name='Test-DrivenDevelopment'></a>Test-Driven Development

- Write tests first, commit
- Implement code iteratively
- Refactor and commit improvements

**When to use:** AI-assisted development thrives when you have robust and comprehensive test suites.

💡 Make sure generated tests are meaningful and not just boilerplate. Keep the code quality as high as that of your production code.

###  1.3. <a name='Spec-DrivenDevelopment'></a>Spec-Driven Development

- Use `/create-prd` ([create project requirement document](/.claude/commands/spec/create-prd.md)) to create a Product Requirements Document (PRD) based on user input.
- Use `/generate-tasks` ([generate tasks from PRD](/.claude/commands/spec/generate-tasks.md)) to create a task list from the PRD.
- Use `/process-task-list` ([process task list](/.claude/commands/spec/process-task-list.md)) to manage and track task progress.

Or use spec-kit, <https://github.com/github/spec-kit> for more details.

**When to use:** Greenfield projects, PoC development, pet projects

💡 This is a new methodology and might not give you best results with complex production code bases. Be careful with your time and feel free to throw away code that you don't like and iterate. Also, since much work is delegated to LLM the result and applicability heavily depends on LLM at use.

###  1.4. <a name='BrainstormingIdeation'></a>Brainstorming & Ideation

- Ask Claude to brainstorm multiple approaches and iterate on ideas
- Use generated ideas as grounding context for subsequent prompts
- Build on previous suggestions rather than starting from scratch

**When to use:** Early stages of feature design, architectural decisions, or when stuck on a problem.

💡 Be very direct and explicit with the way you want to interact with LLM. E.g.: "give me 3 results and compare pros and cons for each result using markdown tables"

💡 For common tasks, you can create re-usable slash commands to help you to describe your problem solving approach, e.g.: `/five` command - [Use the "Five Whys" root cause analysis technique](./.claude/commands/five.md)

##  2. <a name='ContextEngineering'></a>🧠 Context Engineering

###  2.1. <a name='ContextGrounding'></a>Context Grounding

- Provide relevant files and examples
- Perform prior code base / feature exploration and ask Claude to focus on relevant parts
- Use web search and MCPs to gather additional context and information

💡 Hint Claude in the right direction. E.g.: "Hint: you might want to check relevant tests for this functionality"

💡 Use MCP servers for latest/authoritative information. E.g.: ([Microsoft Docs MCP](https://learn.microsoft.com/en-us/training/support/mcp), [Context7](https://context7.com/))

###  2.2. <a name='ProjectMemory.CLAUDE.md'></a>Project Memory (`./CLAUDE.md`)
- **Purpose:** Team-shared context and project knowledge
- **Content:** Architecture decisions, design patterns, coding standards
- **Import syntax:** Use `@path/to/import` to reference other files
- **Best practice:** Keep it concise but comprehensive and high-level

💡 Use `# <text>` to add specific memories to CLAUDE.md

###  2.3. <a name='SessionManagement'></a>Session Management
- **`/clear`** - Reset conversation context when needed
- **`/compact <prompt>`** - Aggregate and summarize conversation history
- **Context Control:** Manage conversation length for optimal performance
- **/context** - Review current context and adjust as necessary

💡 Be aware of context limits and how it may impact the quality of responses. It is better to keep your context short and focused.

##  3. <a name='Extras.TipsTricks'></a>✨Extras. Tips & Tricks

> 🤩 See more at [TIPS-AND-TRICKS.md](./TIPS-AND-TRICKS.md)

###  3.1. <a name='Self-DiscoveryCapabilities'></a>Self-Discovery & Capabilities

Claude Code is self-aware and driven by human language. So many discrete capabilities can be discovered and triggered through conversation.

- **Ask Claude directly** about its capabilities: "What tools do you have?" (<https://docs.anthropic.com/en/docs/claude-code/settings#tools-available-to-claude>)
- **Explore features** through conversation:
   - "Can you run tasks in the background?"
   - "Please search the web for..."
   - "Extract the content of this website and summarize it"
- **Understand limitations** by testing boundaries

💡 In this context of MCP/Tools discovery, it is very important to nudge the model to use tools explicitly to get the consistent results, especially as your LLM customizations grows. The bigger context, the less LLM can concentrate on details to give you a good result.

###  3.2. <a name='DeepThinkingNudges'></a>Deep Thinking Nudges

**Use progressive thinking levels to solve complex problems:** [claude-code/common-workflows#use-extended-thinking](https://docs.anthropic.com/en/docs/claude-code/common-workflows#use-extended-thinking)

- **"think"** - Basic analysis
- **"think hard"** - Deeper investigation
- **"think harder"** - Comprehensive analysis
- **"ultrathink"** - Maximum depth analysis

**When to use:** Complex architectural decisions, debugging difficult issues, or when initial solutions seem insufficient.

###  3.3. <a name='CommandLineIntegration'></a>Command Line Integration
- **Pipe Mode:** Use Claude as a Unix utility: `claude -p ""` or `echo '' | claude -p ""`
- **Integration:** Combine with existing development tools and scripts
- **Automation:** Chain Claude commands for repeated workflows

**When to use:** When you want to integrate Claude into your CI/CD pipelines or automate repetitive tasks. For example, you can do some decision making as part of your CI/CD workflow based on structured output from Claude.

##  4. <a name='KnownHowtoCustomizeClaude'></a>Known How to Customize Claude

* Permissions: <https://docs.anthropic.com/en/docs/claude-code/settings#permission-settings>
* Available Tools: <https://docs.anthropic.com/en/docs/claude-code/settings#tools-available-to-claude>
* Custom Slash Commands: <https://docs.anthropic.com/en/docs/claude-code/slash-commands>
* Sub-Agents: <https://docs.anthropic.com/en/docs/claude-code/sub-agents>

##  5. <a name='TipsforSuccess'></a>🎯 Tips for Success

###  5.1. <a name='Communication'></a>Communication
- Be specific about requirements and constraints
- Provide context about your development environment
- Ask for explanations when solutions aren't clear

###  5.2. <a name='Iteration'></a>Iteration
- Start with working solutions, then optimize
- Use feedback loops to refine approaches
- Don't hesitate to backtrack and try different methods

###  5.3. <a name='Learning'></a>Learning
- Experiment with different prompt styles
- Learn from Claude's reasoning and explanations
- Build a personal knowledge base of effective patterns
