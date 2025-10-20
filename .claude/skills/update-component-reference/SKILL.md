---
name: update-component-reference
description: This skill should be used when the user wants to add components (commands, agents, or skills) to the Component Reference section of the website.
---

# Update Component Reference Skill

Add documentation for Claude Code components (commands, agents, skills) to the website's Component Reference section.

## When to Use

Use this skill when the user requests to:
- Add a new component to the Component Reference documentation
- Document a newly created command, agent, or skill
- Update component documentation in the reference section

## Prerequisites Checklist

Before documenting a component, ensure:

1. **Component exists** in the appropriate plugin directory:
   - Commands: `plugins/cc-handbook/commands/{name}.md`
   - Agents: `plugins/cc-handbook/agents/{name}.md`
   - Skills: `plugins/cc-handbook/skills/{name}/SKILL.md`

2. **For skills only**: Component is registered in plugin.json:
   ```json
   {
     "skills": [
       "./skills/skill-creator",
       "./skills/{new-skill-name}"
     ]
   }
   ```

3. **Verify plugin name**: Check `.claude-plugin/plugin.json` for the badge (usually "cc-handbook")

## Implementation Process

### Step 1: Determine Target Directory

Component documentation goes in: `website/docs/component-reference/{type}/`

- Commands → `website/docs/component-reference/commands/`
- Agents → `website/docs/component-reference/agents/`
- Skills → `website/docs/component-reference/skills/`

All category directories and `_category_.json` files already exist for these types.

### Step 2: Determine sidebar_position

Read existing `.mdx` files in the target directory to find the highest `sidebar_position` and add 1.

Example:
```bash
grep -h "sidebar_position:" website/docs/component-reference/skills/*.mdx | sort -n
```

### Step 3: Create Component Documentation File

**Filename convention**: Use kebab-case matching the component name
- Command `/commit` → `commit.mdx`
- Agent `@backend-architect` → `backend-architect.mdx`
- Skill `skill-creator` → `skill-creator.mdx`

### Step 4: Write MDX Content

Use the appropriate template based on component type:

#### Commands Template

```mdx
---
title: "/command-name"
sidebar_position: N
---

import CommandNameSource from '!!raw-loader!../../../../plugins/cc-handbook/commands/command-name.md'
import CodeBlock from '@theme/CodeBlock';

# Use `/command-name`

<span className="badge badge--primary">cc-handbook</span>

Brief description of what this command does (1-2 sentences).

More detailed explanation of the command's purpose and benefits.

## Command Specification

<CodeBlock language="markdown">
{CommandNameSource}
</CodeBlock>

## Additional sections as needed
- Example usage
- Tips and tricks
- Related commands
```

#### Agents Template

```mdx
---
title: "@agent-name"
sidebar_position: N
---

import AgentNameSource from '!!raw-loader!../../../../plugins/cc-handbook/agents/agent-name.md'
import CodeBlock from '@theme/CodeBlock';

# Use `@agent-name` agent

<span className="badge badge--primary">cc-handbook</span>

Brief description of what this agent specializes in (1-2 sentences).

More detailed explanation of the agent's capabilities and when to use it.

## Agent Specification

<CodeBlock language="markdown">
{AgentNameSource}
</CodeBlock>

## Additional sections as needed
- Key strengths
- Example use cases
- Related agents
```

#### Skills Template

```mdx
---
title: "skill-name"
sidebar_position: N
---

import SkillNameSource from '!!raw-loader!../../../../plugins/cc-handbook/skills/skill-name/SKILL.md'
import CodeBlock from '@theme/CodeBlock';

# Use `skill-name` skill

<span className="badge badge--primary">cc-handbook</span>

Brief description of what this skill provides (1-2 sentences).

More detailed explanation of the skill's purpose and capabilities.

## When to Use This Skill

Use the `skill-name` skill when you want to:

- Primary use case
- Secondary use case
- Additional scenarios

## Skill Specification

<CodeBlock language="markdown">
{SkillNameSource}
</CodeBlock>

## Additional sections as needed
- Key concepts
- Example workflows
- Related skills
```

### Step 5: Verify Import Paths

Double-check the raw-loader import path matches the component location:

- Commands: `'!!raw-loader!../../../../plugins/cc-handbook/commands/{name}.md'`
- Agents: `'!!raw-loader!../../../../plugins/cc-handbook/agents/{name}.md'`
- Skills: `'!!raw-loader!../../../../plugins/cc-handbook/skills/{name}/SKILL.md'` ⚠️ Note the `/SKILL.md` suffix

The import path goes up 4 directories (`../../../../`) from the `.mdx` file to reach the repo root.

## Common Pitfalls

1. **Forgetting plugin.json registration for skills**
   - Skills MUST be in plugin.json or they won't be available
   - Commands and agents are auto-discovered, skills are not

2. **Incorrect import paths**
   - Skills use `/SKILL.md` suffix: `skills/{name}/SKILL.md`
   - Commands and agents use `.md` directly: `commands/{name}.md`

3. **Wrong relative path depth**
   - Always use 4 levels up: `../../../../`
   - Path starts from the `.mdx` file location

4. **Inconsistent naming**
   - File names should match component names exactly (kebab-case)
   - Title in frontmatter should include prefix (`/` for commands, `@` for agents)

## Quick Reference

### Import Variable Naming Convention
Match the component name in PascalCase + "Source":
- `commit.md` → `CommitCommandSource`
- `backend-architect.md` → `BackendArchitectAgentSource`
- `skill-creator/SKILL.md` → `SkillCreatorSource`

### Badge
Most components use: `<span className="badge badge--primary">cc-handbook</span>`

Change the text to match the plugin name if documenting a different plugin.

## Example Workflow

**User**: "Add the new @pair-programmer agent to the documentation"

1. **Verify** component exists: `plugins/cc-handbook/agents/pair-programmer.md` ✓
2. **Check** it's an agent (auto-discovered, no plugin.json needed) ✓
3. **Find** next sidebar_position in `website/docs/component-reference/agents/`
4. **Create** `website/docs/component-reference/agents/pair-programmer.mdx`
5. **Write** content using agent template
6. **Import** using: `'!!raw-loader!../../../../plugins/cc-handbook/agents/pair-programmer.md'`
7. **Verify** documentation renders correctly