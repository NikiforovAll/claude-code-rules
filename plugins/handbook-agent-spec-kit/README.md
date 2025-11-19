# Agent Spec Kit

Spec-driven development workflow system with structured phases: Requirements → Design → Tasks → Implementation.

Created by [Vitalii Matviichuk](https://github.com/vmatviichuk).

## Overview

This plugin provides a systematic approach to feature development through four distinct phases, each handled by a specialized agent. The workflow ensures comprehensive planning, clear technical designs, actionable task lists, and strict implementation adherence.

## Workflow Phases

### 1. Requirements (requirements-agent)
Transform feature ideas into structured requirements documents with user stories and EARS-format acceptance criteria.

**Output:** `specs/{feature_name}/requirements.md`

### 2. Design (tech-design-agent)
Create comprehensive technical design documents addressing all requirements with clear implementation guidance.

**Output:** `specs/{feature_name}/design.md`

### 3. Tasks (tasks-agent)
Convert technical designs into actionable, incremental coding tasks for implementation.

**Output:** `specs/{feature_name}/tasks.md`

### 4. Implementation (implementation-agent)
Execute individual coding tasks following requirements exactly without improvisation, asking for clarification when needed.

**Approach:** One task per session with strict zero-improvisation policy

## Features

**Skill:**
- `spec-driven` - Orchestrator that coordinates the entire workflow, manages approval gates, and ensures sequential execution

**Agents:**
- `requirements-agent` - Expert business analyst that creates requirements with EARS acceptance criteria
- `tech-design-agent` - Expert software architect that creates technical design documents
- `tasks-agent` - Expert development lead that converts designs into actionable coding tasks
- `implementation-agent` - Strict implementation agent that executes tasks following specifications exactly

## Quick Start

### Using the Spec-Driven Workflow

Trigger the orchestrator skill with any of these phrases:

```
"Let's use spec-driven development for this feature"
"Follow the spec process"
"Use spec-driven approach"
```

The orchestrator will:
1. Launch `requirements-agent` to create requirements
2. Wait for approval before proceeding
3. Launch `tech-design-agent` to create design
4. Wait for approval before proceeding
5. Launch `tasks-agent` to create implementation tasks
6. Wait for approval before proceeding
7. Optionally launch `implementation-agent` for task execution (one task per session)

### Direct Agent Usage

You can also invoke agents directly:

```
"Use requirements-agent to create requirements for user authentication"
"Use tech-design-agent to design the architecture"
"Use tasks-agent to break down the design into tasks"
"Use implementation-agent to implement task 2.1"
```

## File Structure

All specifications are created in the `specs/{feature_name}/` directory:

```
specs/user-authentication/
├── requirements.md    - User stories with EARS acceptance criteria
├── design.md         - Technical architecture and implementation guidance
└── tasks.md          - Incremental coding tasks with progress tracking
```

## Key Principles

1. **Sequential Execution** - Complete phases in order with explicit approval gates
2. **Zero Improvisation** - During implementation, follow specs exactly without assumptions
3. **Incremental Building** - Each phase builds on the previous
4. **One Task Focus** - Implementation agent completes only one task per session
5. **Strict Adherence** - Follow specifications exactly, ask for clarification when unclear

## Implementation Details

### Requirements Agent
- Creates structured requirements with EARS syntax (WHEN/IF/WHERE/WHILE + THEN)
- Generates 4-8 requirements covering complete feature scope
- Each requirement includes 3-7 specific acceptance criteria
- Focuses on WHAT needs to be built, not HOW

### Tech Design Agent
- Creates comprehensive technical designs addressing all requirements
- Includes architecture diagrams, component specifications, data models
- Defines error handling, testing strategy, and integration points
- Focuses on architecture, not specific code implementation

### Tasks Agent
- Converts design into discrete, manageable coding tasks (1-4 hours each)
- Tasks are coding activities only (no manual testing, deployment, etc.)
- Includes Progress Summary, Completed Tasks, and Pending Tasks sections
- Every task references specific requirements for traceability

### Implementation Agent
- Executes ONE task at a time with strict zero-improvisation
- Completes pre-implementation checklist before coding
- Requests approval for unclear visual/design elements
- Marks tasks as completed in tasks.md after implementation
- Suggests new session for next task

## Installation

```bash
/plugin marketplace add nikiforovall/claude-code-rules
/plugin install handbook-agent-spec-kit
```

## Example Usage

```
User: "I want to build a user authentication system"

Claude: "Let's use the spec-driven approach. I'll launch the requirements-agent to create the requirements document."

[requirements-agent creates requirements.md]

Claude: "Do the requirements look good? If so, we can move on to the design."

User: "Yes, looks good"

[tech-design-agent creates design.md]

Claude: "Does the design look good? If so, we can move on to the implementation plan."

User: "Approved"

[tasks-agent creates tasks.md]

Claude: "Do the tasks look good?"

User: "Yes, let's start implementing"

Claude: "I'll launch the implementation-agent to work on task 1."

[implementation-agent implements task 1, updates tasks.md]

Claude: "Task 1 is complete. Please review. Once approved, start a new session for task 2."
```

## License

MIT
