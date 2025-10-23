# Task Planning Guide

> This guide explains how to effectively plan and track complex feature implementations using the task template approach.

## Overview

The task template approach is designed to help you systematically break down complex features into manageable, well-documented tasks. This guide explains the methodology behind the template and how to use it effectively.

## Core Philosophy

### 1. Research Before Implementation
Always start with a **Phase 0: Research** phase:
- Understand existing patterns in the codebase
- Evaluate multiple approaches before committing
- Document findings and rationale for decisions
- Create a clear implementation plan

**Why**: Prevents false starts, reduces rework, and ensures consistency with existing patterns.

### 2. Iterative Documentation
Update task documentation throughout implementation:
- Mark tasks as completed when finished
- Document actual implementation details (not just plans)
- Record lessons learned and unexpected challenges
- Keep success criteria current

**Why**: Creates valuable reference material for future similar features.

### 3. Interactive Clarification
Ask clarifying questions proactively when planning or implementing:
- When multiple valid approaches exist
- When requirements are ambiguous or unclear
- When design decisions affect architecture
- When user preferences matter for implementation

**Why**: Prevents wasted effort on wrong assumptions and ensures alignment with user needs.

**Tool**: Use the **AskUserQuestion** tool to gather decisions during execution.

### 4. Phased Approach
Break features into logical phases:
- **Phase 1**: Foundation (core functionality)
- **Phase 2**: Integration (connecting to existing systems)
- **Phase 3**: Advanced features (nice-to-haves)

**Why**: Enables early delivery of core value while deferring optional features.

## Template Structure Explained

### Task Metadata
```markdown
**Status**: 🟡 **Planned**
**Priority**: High
**Effort**: Medium
```

**Purpose**: Quick visibility into task state and scope.

**Best Practices**:
- Update status in real-time as work progresses
- Use actual effort estimates from similar past work
- Adjust priority based on dependencies and business value

### Goal Section
```markdown
### Goal
[Clear, one-sentence objective]
```

**Purpose**: Ensures everyone understands what success looks like.

**Best Practices**:
- Make it specific and measurable
- Focus on outcomes, not activities
- Example: "Implement citation-based linking between DI and SPO using driveId/itemId matching"

### Context Section
```markdown
### Context
[Why this task exists and how it fits into the larger feature]
```

**Purpose**: Provides background and motivation.

**Best Practices**:
- Explain dependencies on other tasks
- Reference related features or patterns
- Highlight any constraints or assumptions

### Requirements Section
```markdown
### Requirements
#### 1. [Requirement Category]
[Detailed description with code examples]
```

**Purpose**: Breaks down the work into concrete, actionable pieces.

**Best Practices**:
- Use numbered categories for organization
- Include code snippets showing intended design
- Specify integration points with existing code
- Address non-functional requirements (performance, security, etc.)

### Action Items
```markdown
### Action Items
- [ ] [Specific, actionable task]
- [ ] [Another task]
```

**Purpose**: Creates a checklist for implementation.

**Best Practices**:
- Make items specific and testable
- Include cross-cutting concerns (error handling, logging, tests)
- Check off items as you complete them
- Add new items as they're discovered

### Test Scenarios
```markdown
### Test Scenarios
- [ ] Happy path: [Description]
- [ ] Error case: [Description]
```

**Purpose**: Ensures comprehensive testing coverage.

**Best Practices**:
- Cover happy path, error cases, and edge cases
- Include performance/load testing scenarios
- Reference specific test files once written

### Dependencies
```markdown
### Dependencies
- [External dependency or blocking task]
```

**Purpose**: Makes blocking relationships explicit.

**Best Practices**:
- List both internal (other tasks) and external dependencies
- Link to related tasks using markdown
- Update when dependencies are resolved

### Related Files
```markdown
### Related Files
- `path/to/file.cs` - Description of relevance
```

**Purpose**: Creates navigable links to relevant code.

**Best Practices**:
- Include both files to read and files to modify
- Add brief descriptions of relevance
- Update as implementation progresses

## How to Use the Template

### Step 1: Copy the Template
```bash
cp docs/plan-template.md tasks/[feature-name]-plan.md (current project directory)
```

### Step 2: Fill in the Overview
- Replace `[Feature Name]` throughout
- Write a brief feature overview
- Identify the main phases of work

### Step 3: Create Phase 0 (Research)
**Always start here**, even for "obvious" features:
1. List what you need to research
2. Document similar patterns in the codebase
3. Evaluate multiple approaches (list pros/cons for each - 2-4 options)
4. **Ask clarifying questions** via AskUserQuestion if approaches have different trade-offs
5. **Get user confirmation** on selected approach
6. **Document final decision** in "Selected Approach" section
7. Create high-level implementation plan (5-7 steps)

### Step 4: Break Down Implementation Tasks (AFTER Phase 0 Complete)
For each major component:
1. Create implementation tasks (T001, T002, T003, ...T00N as needed)
2. Define clear goal and requirements for each
3. Identify dependencies between tasks
4. Estimate effort based on similar past work

**Tips**:
- Number of tasks depends on complexity (simple: 1-2, medium: 3-5, complex: 5+)
- Keep tasks focused (ideally 2-5 days each)
- Tasks should be independently testable
- Consider parallelization opportunities
- ALL tasks should align with the approach selected in Phase 0

**Why**: Provides clear definition of "done" and prevents scope creep.

## Common Pitfalls to Avoid

### 1. Skipping Research (Phase 0)
❌ **Don't**: Jump straight into implementation.
✅ **Do**: Always start with research, even for "simple" features.

**Why**: Prevents rework and ensures consistency with existing patterns.

### 2. Vague Requirements
❌ **Don't**: "Add Q&A feature"
✅ **Do**: "Implement Q&A feature allowing users to post questions and receive answers, with upvote functionality and moderation tools."

**Why**: Clear requirements prevent misunderstandings and scope creep.

### 3. Ignoring Dependencies
❌ **Don't**: Start Task 2 before Task 1 is complete.
✅ **Do**: Explicitly list and track dependencies.

**Why**: Prevents blocked work and wasted effort.

### 4. Not Updating Documentation
❌ **Don't**: Leave task docs outdated after implementation.
✅ **Do**: Update tasks as you work, marking completions and adding discoveries.

**Why**: Creates accurate reference material for future work.

### 5. Over-Committing to Advanced Features
❌ **Don't**: Try to implement all tasks at once.
✅ **Do**: Focus on core functionality first, defer advanced features.

**Why**: Enables earlier delivery and reduces risk.

### 6. Assuming Instead of Asking
❌ **Don't**: Make assumptions about requirements, architecture choices, or user preferences.
✅ **Do**: Use **AskUserQuestion** tool to clarify ambiguities before committing to an approach.

**Why**: Prevents wasted effort on wrong assumptions and rework.

**Example scenarios**:
- "Should we use library A (faster) or library B (more features)?"
- "Which authentication method do you prefer: OAuth, JWT, or session-based?"
- "Do you want to support real-time updates or is polling acceptable?"

## Checklist for Good Task Planning

Use this checklist when creating or reviewing task documentation:

### Research Phase
- [ ] Identified similar features/patterns in codebase
- [ ] Evaluated multiple approaches with pros/cons
- [ ] **Asked clarifying questions** using AskUserQuestion tool as needed
- [ ] **Documented final decision** in "Selected Approach" section
- [ ] Included rationale explaining why chosen approach is best
- [ ] Listed key findings from research
- [ ] Created high-level implementation plan

### Task Definition
- [ ] Clear, measurable goal
- [ ] Context explaining why task exists
- [ ] Detailed requirements with code examples
- [ ] Specific action items
- [ ] Comprehensive test scenarios
- [ ] Dependencies explicitly listed
- [ ] Related files identified

### Planning
- [ ] Tasks are appropriately sized (2-5 days ideal)
- [ ] Dependencies are correct and up-to-date
- [ ] Sprint/phase groupings are logical
- [ ] Success criteria are measurable
- [ ] Implementation order makes sense

### Maintenance
- [ ] Task statuses reflect reality
- [ ] Completed tasks show actual implementation
- [ ] New discoveries are documented
- [ ] Lessons learned are captured

---

## Quick Start Checklist

When starting a new feature:

1. [ ] Copy `plan-template.md` to `[feature]-plan.md`
2. [ ] Fill in feature overview and goals
3. [ ] Create Phase 0 (Research) and complete it first
4. [ ] Break down implementation into 2-5 day tasks
5. [ ] Define clear success criteria
6. [ ] Plan sprints/phases
7. [ ] Update documentation throughout implementation
8. [ ] Fill in lessons learned when complete

---

**Remember**: Good planning prevents poor performance. Invest time upfront in task breakdown and research—it pays dividends throughout implementation.
