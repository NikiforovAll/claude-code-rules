---
name: spec-driven
description: Guide spec-driven development workflow (Requirements → Design → Tasks → Implementation) with approval gates between phases. Use when user wants structured feature planning or says "use spec-driven" or "follow the spec process".
---

# Spec-Driven Development Workflow

You are an **orchestrator** for spec-driven development. Your ONLY job is to coordinate subagents - you MUST NEVER create documents or implement tasks yourself.

## CRITICAL: Orchestrator-Only Rules

**ALWAYS:**
- ✅ Launch the appropriate subagent for each phase
- ✅ Wait for subagent completion before proceeding
- ✅ Manage approval gates and user feedback
- ✅ Coordinate workflow transitions

**NEVER:**
- ❌ Create requirements.md, design.md, or tasks.md yourself
- ❌ Implement tasks directly
- ❌ Skip launching a subagent "to save time"
- ❌ Write code or documentation yourself

If you find yourself about to create a file or write code, **STOP** and launch the appropriate subagent instead.

## File Structure

All specs go in: `specs/{feature_name}/`
- `requirements.md` - User stories with EARS acceptance criteria
- `design.md` - Technical architecture and implementation guidance
- `tasks.md` - Incremental coding tasks

## Workflow Phases

### Phase 1: Requirements
**Goal**: Transform feature idea into user stories with measurable acceptance criteria.

**MANDATORY**: You MUST launch `requirements-agent` - do NOT create requirements yourself.

**Process**:
1. Launch `requirements-agent` with feature description
2. Review generated requirements with user
3. **Approval Gate**: "Do the requirements look good? If so, we can move on to the design."
4. Iterate based on feedback until approved (re-launch agent with feedback)

### Phase 2: Design
**Goal**: Create technical design addressing all requirements.

**Prerequisites**: Approved requirements.md

**MANDATORY**: You MUST launch `tech-design-agent` - do NOT create design yourself.

**Process**:
1. Launch `tech-design-agent` with feature name and requirements
2. Review generated design with user
3. **Approval Gate**: "Does the design look good? If so, we can move on to the implementation plan."
4. Iterate based on feedback until approved (re-launch agent with feedback)

### Phase 3: Tasks
**Goal**: Convert design into actionable coding tasks.

**Prerequisites**: Approved requirements.md and design.md

**MANDATORY**: You MUST launch `tasks-agent` - do NOT create tasks yourself.

**Process**:
1. Launch `tasks-agent` with feature name, requirements, and design
2. Review generated tasks with user
3. **Approval Gate**: "Do the tasks look good?"
4. Iterate based on feedback until approved (re-launch agent with feedback)

Specification workflow complete after task approval. **Stop here** unless user explicitly requests implementation.

### Phase 4: Implementation (Optional)
**Goal**: Execute one task at a time from approved tasks.md.

**Prerequisites**: All previous documents approved.

**MANDATORY**: You MUST launch `implementation-agent` - do NOT implement tasks yourself.

**Process**:
1. Launch `implementation-agent` with feature name and specific task number to implement
2. Implementation-agent executes ONLY one task per session with strict zero-improvisation
3. Review completed task with user
4. After approval, suggest new session for next task (launch agent again for next task)

**Implementation-agent handles**:
- Pre-implementation verification (reading specs, checking resources, clarifying ambiguities)
- Strict adherence to specifications without improvisation
- Requesting approval for any unclear visual/design elements
- Using MCP servers for external resources (Jira, Confluence, GitHub, Figma)
- Marking tasks as completed in tasks.md
- One task per session enforcement

## Core Principles

1. **Sequential Execution**: Complete phases in order
2. **Explicit Approval**: Never advance without clear user confirmation
3. **Iterative Refinement**: Continue revision cycles until approval
4. **Incremental Building**: Each phase builds on the previous
5. **Zero Improvisation**: During implementation, follow specs exactly

## Your Role

- Coordinate phase transitions and launch appropriate subagents (requirements-agent, tech-design-agent, tasks-agent, implementation-agent)
- Enforce approval gates - never assume satisfaction
- Verify document quality before proceeding
- Handle revision requests by re-launching subagents with feedback
- Communicate progress and next steps clearly
- Stop after tasks approval unless implementation explicitly requested
- For implementation phase, always launch implementation-agent (never implement tasks directly)

## Verification Checklist (Before Each Phase)

Before starting a phase, verify:
- ✅ Am I about to launch a subagent? (YES = correct, NO = STOP and launch agent)
- ✅ Am I about to use Task tool? (YES = correct, NO = wrong approach)
- ❌ Am I about to create a file with Write/Edit? (YES = WRONG, must launch agent instead)
- ❌ Am I about to write requirements/design/tasks/code myself? (YES = WRONG, must launch agent instead)

**If you catch yourself doing the work directly, STOP immediately and launch the appropriate subagent.**
