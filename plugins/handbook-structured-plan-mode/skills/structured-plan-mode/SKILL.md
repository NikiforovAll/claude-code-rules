---
name: structured-plan-mode
description: This skill should be used when planning and tracking complex feature implementations that require systematic task decomposition. Use this skill to break down large features into manageable, well-documented tasks with clear dependencies, action items, and success criteria. The skill provides a structured template and methodology for iterative planning and tracking throughout implementation.
---

# Structured Plan Mode Skill

## Purpose

This skill provides a structured approach for planning and tracking complex feature implementations through systematic task decomposition. It helps break down large, multi-component features into manageable tasks with clear goals, dependencies, and success criteria.

## When to Use This Skill

Use this skill when:
- **Complex features**: Features requiring multiple components or integration points
- **Multi-step implementations**: Work spanning several days with interdependent tasks
- **Pattern-setting work**: Features that will establish patterns for future development
- **Research required**: Work where multiple approaches need evaluation

Do NOT use this skill for:
- Simple bug fixes
- Trivial feature additions
- One-off scripts or experiments
- Work with single, clear implementation path

## How to Use the Skill

**IMPORTANT**: This is a PHASED approach. Complete each phase BEFORE moving to the next.

### Phase 1: Initial Setup

**Actions:**
1. Create `.plans/[feature-name]/` directory (in current project directory)
2. Copy `assets/plan-template.md` to `.plans/[feature-name]/plan.md`
3. Create `.plans/[feature-name]/tasks/` directory for task files
4. Replace `[Feature Name]` with your feature name in plan.md
5. Fill in basic overview and context
6. Create Research section with:
   - Goal
   - Context
   - Strategy Proposals (leave empty for now)
   - **Leave "Selected Approach" EMPTY**
7. Create a todo list by using TodoWrite based on the phases below


**TodoWrite tracks ONLY phases 1-4:**
```
- [ ] Phase 1: Setup template with Research section
- [ ] Phase 2: Conduct research and iterate with user
- [ ] Phase 3: Finalize selected approach
- [ ] Phase 4: Create implementation tasks (T01-T0N)
```

**Mark Phase 1 as completed in TodoWrite**

**Output**: Skeleton plan document with Research section defined and todo list created for phases 1-4

---

### Phase 2: Conduct Research and Iterate with User

**Research Process (Iterative):**
1. **Explore codebase**: Read relevant files, find similar patterns
2. **Document findings incrementally**: Add to "Key Findings" as you discover
3. **Identify 2-3 approach options**: Add to "Strategy Proposals" section
4. **ITERATE with user on EACH proposal**:
   - Present each proposal with trade-offs (pros/cons)
   - Use `AskUserQuestion` to clarify requirements and constraints
   - **User may correct assumptions** - update research based on feedback
   - Refine understanding through questions (typically 3-5 questions, but quality over quantity)
   - **If user strongly prefers one approach early**, you may skip detailed discussion of remaining options
5. **Proactively ask if research is complete**: Once you've explored all options and answered clarifying questions, explicitly ask: "Are you ready to select an approach?"

**CRITICAL**:
- This is an ITERATIVE process - expect back-and-forth discussion on each proposal
- Use AskUserQuestion frequently to refine understanding
- Don't wait for user to say research is done - ASK them proactively

**Mark Phase 2 as completed in TodoWrite when user confirms that research is complete**

**Output**: Research with 2-3 Strategy Proposals documented and reviewed with user

---

### Phase 3: Finalize Selected Approach

**Actions:**
1. **Ask the user to select an approach** using AskUserQuestion (present the 2-3 researched approaches as formal selection options)
2. **Once user confirms their selection**, fill "Selected Approach" section with:
   - **Decision**: Which approach was selected (must match user's confirmed preference)
   - **Rationale**: Why this approach was chosen over alternatives
   - **Key Findings**: Summarize important discoveries from research
   - **Implementation Plan**: High-level steps (5-7 bullet points)
3. Mark all research action items as [x] completed
4. Change research status to ✅ **Completed**
5. Update Progress Summary to show research complete

**Mark Phase 3 as completed in TodoWrite once Selected Approach section is fully documented**

**Output**: Research fully documented with clear decision and rationale

---

### Phase 4: Create Implementation Tasks (ONLY AFTER Phase 1-3 Complete)

**IMPORTANT**: Before creating tasks, read `references/task-planning-guide.md` to understand:
- How to break down work into appropriate task sizes
- Task file structure and required sections
- Best practices for defining clear requirements and action items
- How to set proper dependencies between tasks

**Actions:**
**NOW create T01, T02, T03, ...T0N** as separate files in `.plans/[feature-name]/tasks/` based on selected approach

- Number of tasks depends on complexity (simple: 1-2, medium: 3-5, complex: 5+)
- Break down into manageable chunks (2-5 days each)

**Step-by-Step: Creating a Task File**

For each task you need to create:

1. **Copy the template**:
   ```bash
   cp [path-to-task-template.md] .plans/[feature-name]/tasks/T01.md
   ```
2. **Update task header**: Replace `T0X` with actual task number (T01, T02, etc.)
3. **Fill in core sections**:
   - Goal: One clear, measurable objective
   - Context: How it relates to the feature and selected approach
   - Requirements: Detailed specifications with implementation steps
   - Action Items: Specific checkboxes for work to complete
4. **Update metadata**: Set Status (🟡 Planned), Effort (Small/Medium/Large), Blocked By
5. **Add to Progress Summary**: Update plan.md with link: `- [ ] [**T01**: Task Name](tasks/T01.md) - Status: 🟡 Planned`

**Mark Phase 4 as completed in TodoWrite**

**Output**: Complete task breakdown (T01.md - T0N.md files) in tasks/ folder, all linked from plan.md Progress Summary

---

### Phase 5: Working with Tasks (Implementation)

**Note**: Phase 5 is NOT tracked in TodoWrite. Track progress directly in task files and plan.md.

**IMPORTANT**: Before starting work on ANY task, read `references/task-planning-guide.md` for:
- Task structure guidance and best practices
- How to maintain task files during execution
- Examples of effective task documentation
- Common pitfalls to avoid

**When to consult task-planning-guide.md:**
- Before starting a new task (every time)
- When unclear about task file structure or what to document
- When encountering challenges during task execution
- When adding new tasks mid-implementation

#### Task Execution Discipline

**CRITICAL RULE**: Work on ONE task at a time. Do NOT start the next task until the current task is FULLY completed.

**Task Status Flow:**
1. 🟡 **Planned** → Task created but not started
2. 🟢 **In Progress** → Currently working on this task (only ONE task should be in this state)
3. ✅ **Completed** → All action items done, both locations updated, Execution Summary filled
4. 🔴 **Blocked** → Cannot proceed due to dependency or external issue (move to next task until unblocked)

#### Task Lifecycle: Step-by-Step

**Starting a Task:**
1. **Read `references/task-planning-guide.md`** - Review relevant sections before beginning work
2. Choose next task from plan.md Progress Summary (respecting dependencies)
3. Update status to 🟢 **In Progress** in TWO places:
   - Task file metadata: `**Status**: 🟢 **In Progress**`
   - plan.md Progress Summary: `- [ ] [**T01**: Task Name](tasks/T01.md) - Status: 🟢 In Progress`

**During Task Execution:**
4. Work through Action Items, checking off boxes as you complete them:
   ```markdown
   - [x] Create API endpoint
   - [x] Add request validation
   - [ ] Add error handling  ← Currently working here
   - [ ] Write tests
   ```
5. Update task file in real-time as work progresses
6. If you discover new requirements, add them to Action Items

**Completing a Task:**
7. Verify ALL action items are checked: `[x]`
8. Fill in "Execution Summary" section in task file:
   ```markdown
   ## Execution Summary
   **Completed**: 2025-01-08 14:30

   **What was implemented**:
   - Added /api/users endpoint with validation
   - Implemented error handling for edge cases

   **Challenges encountered**:
   - Had to refactor auth middleware to support new endpoint
   ```
9. Update status to ✅ **Completed** in TWO places:
   - Task file metadata: `**Status**: ✅ **Completed**`
   - plan.md Progress Summary: `- [x] [**T01**: Task Name](tasks/T01.md) - Status: ✅ Completed`
10. **Explicitly ask user**: "Task T01 is complete. Ready to move to T02?"
11. **ONLY after user confirms** proceed to next task

#### Dual-Tracking Example

When completing T01, you must update BOTH locations:

**In `tasks/T01.md`** (lines 7-9):
```markdown
**Status**: ✅ **Completed**
**Effort**: Medium
**Blocked By**: None
```

**In `plan.md` Progress Summary** (line ~18):
```markdown
- [x] [**T01**: Add API endpoint](tasks/T01.md) - Status: ✅ Completed
```

**Why dual-tracking?**
- plan.md provides high-level overview of all tasks at a glance
- Task files provide detailed implementation notes for deep dives
- Both serve different purposes and audiences

#### Handling Blocked Tasks

If you cannot complete a task:
1. Update status to 🔴 **Blocked** in both locations
2. Update "Blocked By" field in task file metadata
3. Document blocking reason in task file
4. Move to next non-blocked task
5. Return when blocker is resolved

#### Discovering New Tasks Mid-Implementation

If you discover additional work during Phase 5:
1. Create new task file (e.g., `T06.md`) in tasks/ directory
2. Fill in all sections using task-template.md
3. Add link to plan.md Progress Summary
4. Update dependent tasks if needed

---

**Remember**: ONE task at a time. Complete it FULLY (all checkboxes, both locations updated, Execution Summary filled), then ASK USER for confirmation before moving to the next.

---

### Phase 6: Post-Implementation Review

**Note**: Phase 6 is NOT tracked in TodoWrite. Update the plan document directly.

After feature completion:
- Fill in "Lessons Learned" section
- Verify all task statuses are accurate
- Document any technical debt or future work
- Review what went well and what could improve

## Workflow Summary

**TodoWrite tracks ONLY phases 1-4 (not subtasks):**
```
- [ ] Phase 1: Setup template with Research section
- [ ] Phase 2: Conduct research and iterate with user
- [ ] Phase 3: Finalize selected approach
- [ ] Phase 4: Create implementation tasks (T01-T0N)
```

**Phase-by-Phase Workflow:**

1. **Phase 1 - Setup**:
   - Create `.plans/[feature-name]/` and `.plans/[feature-name]/tasks/` directories
   - Copy plan-template.md to `.plans/[feature-name]/plan.md`
   - Create Research section ONLY in plan.md
   - DO NOT create T01, T02, T03 task files yet
   - Mark Phase 1 complete in TodoWrite

2. **Phase 2 - Research & Iterate** (AskUserQuestion REQUIRED):
   - Explore codebase, document findings in plan.md
   - Present 2-3 approach options
   - **Iterate on EACH proposal** via AskUserQuestion (discuss trade-offs, clarify constraints)
   - User may correct assumptions - update research
   - **If user strongly prefers one approach**, may skip detailed discussion of remaining options
   - **Proactively ask**: "Are you ready to select an approach?"
   - Mark Phase 2 complete when user confirms

3. **Phase 3 - Finalize**:
   - Present 2-3 researched approaches and ask user to select one
   - Once user confirms, fill "Selected Approach" section in plan.md
   - Mark research as ✅ Completed in plan.md
   - Mark Phase 3 complete once documentation is done

4. **Phase 4 - Create Tasks**:
   - **Read `references/task-planning-guide.md` before creating tasks**
   - NOW create T01.md, T02.md, T03.md, ...T0N.md files in `.plans/[feature-name]/tasks/`
   - Copy task-template.md for each task file
   - Fill in task details based on selected approach
   - Number of tasks depends on complexity
   - Update Progress Summary in plan.md with links to task files
   - Mark Phase 4 complete in TodoWrite

5. **Phase 5 - Implementation** (ONE task at a time):
   - **Read `references/task-planning-guide.md` before starting EACH task**
   - Work on ONE task until FULLY completed (all checkboxes, both locations updated, Execution Summary filled)
   - Update status in TWO places: task file metadata AND plan.md Progress Summary
   - Track progress: 🟡 Planned → 🟢 In Progress → ✅ Completed
   - Check off action items as you complete them
   - Fill Execution Summary before marking complete
   - **Explicitly ask user for confirmation** before moving to next task
   - ONLY after user confirms proceed to next task

6. **Phase 6 - Review**:
   - Document lessons learned in plan.md


## Key Patterns from Successful Use

### Pattern 1: Follow Existing Patterns
During research phase, research existing similar features and match their architecture exactly.
**Benefit**: Consistent codebase, faster implementation, reduced bugs.

### Pattern 2: Simplify When Possible
During research, look for ways to simplify (e.g., avoid unnecessary API calls).
**Benefit**: Reduced dependencies, better performance, easier maintenance.

### Pattern 3: Discover Existing Implementations
Research phase may reveal the work is already done - mark task complete.
**Benefit**: Avoids duplicate work, leverages tested code.

### Pattern 4: Document Design Decisions
During research phase, use the **"Selected Approach"** section to document WHY you chose one approach over alternatives.
Include: decision, rationale, key findings, and implementation plan.
**Benefit**: Future developers understand rationale, prevents second-guessing, provides clear starting point.

### Pattern 5: Keep Tasks Focused
Break large tasks into smaller chunks that are independently testable.
**Benefit**: Steady progress, clear milestones, easier to parallelize.

## Reference Materials

**CRITICAL**: `references/task-planning-guide.md` is NOT just for planning - read it throughout implementation.

**Read `references/task-planning-guide.md`:**
- **Phase 4**: Before creating task files (understand task structure, sizing, dependencies)
- **Phase 5**: Before starting EACH task (review best practices, avoid common pitfalls)
- **During execution**: When updating task files, adding action items, or documenting progress
- **When stuck**: Consult checklist for good task planning and common pitfalls section

---

**Remember**:
1. **TodoWrite tracks PHASES** - not individual subtasks
2. **Phases are sequential** - complete Phase 1 before Phase 2, etc.
3. **Phase 2 is iterative** - use AskUserQuestion multiple times, expect back-and-forth
4. **User confirms approach** - do NOT fill "Selected Approach" until user confirms
5. **No premature planning** - T01-T0N created in Phase 4
6. **Task count is flexible** - create as many as needed (T01, T02, ...T0N)
7. **ONE task at a time** - Complete current task FULLY (all checkboxes, both locations, Execution Summary) before starting next
8. **Dual-tracking required** - Update status in BOTH task file AND plan.md
9. **Explicit user confirmation** - Ask user for approval before moving to next task
10. **Read task-planning-guide.md** - Before Phase 4, before EACH task in Phase 5, and when stuck
