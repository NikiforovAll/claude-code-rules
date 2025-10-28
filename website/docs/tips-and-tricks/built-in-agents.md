---
title: "Use Built-in Agents"
sidebar_position: 15
---

# Use Built-in Agents

Claude Code includes built-in specialized agents that can autonomously handle complex, multi-step tasks. These agents are more efficient than running individual commands because they can explore, analyze, and make decisions independently.

## Available Built-in Agents

### 1. **general-purpose** (Sonnet)
**Purpose:** General-purpose research, code search, and multi-step tasks

**Tools Available:** All tools (*)

**Use Cases:**
- Complex questions requiring multiple approaches
- Searching for keywords across large codebases
- Multi-step tasks that don't fit other specialized agents
- When you're unsure which specific agent to use

**Example:**
```
Use the general-purpose agent to find all authentication-related code and summarize the approach
```

---

### 2. **Explore** (Haiku - Fast)
**Purpose:** Fast codebase exploration and file discovery

**Tools Available:** Glob, Grep, Read, Bash

**Use Cases:**
- Finding files by patterns (e.g., `src/components/**/*.tsx`)
- Searching code for keywords (e.g., "API endpoints")
- Understanding architecture (e.g., "how does authentication work?")
- Discovering patterns across multiple files


**Example:**
```
Use Explore agent to find error handling code
```

---

### 3. **Plan**
**Purpose:** Fast codebase exploration with thoroughness control

**Tools Available:** Glob, Grep, Read, Bash

**Use Cases:**
- Finding files by patterns with adjustable depth
- Understanding codebase before implementation
- Planning implementation steps for coding tasks

---

### 4. **statusline-setup**
**Purpose:** Configure Claude Code status line settings

**Tools Available:** Read, Edit

**Use Cases:**
- Customizing status line display
- Configuring status line behavior

---

### 5. **output-style-setup**
**Purpose:** Create and configure custom output styles

**Use Cases:**
- Creating custom output formatting
- Configuring response styles

---

**Important:** Agents are stateless - you can't send follow-up messages to an agent. Make sure your initial task description is complete and detailed.

---

## Related

- [Subagents](../fundamentals/subagents.md) - Creating custom agents
- [Tools List](./tools-list.md) - Available Claude Code tools
- [Agent Skills](../fundamentals/agent-skills.md) - Advanced agent capabilities
