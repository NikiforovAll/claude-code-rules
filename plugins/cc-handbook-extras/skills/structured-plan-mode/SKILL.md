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

### Phase 1: Initial Setup (TodoWrite Required)

**TodoWrite tracks ONLY phases 1-4:**
```
- [ ] Phase 1: Setup template with Phase 0 Research section
- [ ] Phase 2: Conduct research and iterate with user
- [ ] Phase 3: Finalize selected approach
- [ ] Phase 4: Create implementation tasks (T001-T00N)
```

**Note**: Phases 5-6 are tracked in the plan document itself, NOT in TodoWrite.

**Actions:**
1. Copy `assets/plan-template.md` to `tasks/[feature-name]-plan.md` (current project directory)
2. Replace `[Feature Name]` with your feature name
3. Fill in basic overview and context
4. Create Phase 0 Research section with:
   - Goal
   - Context
   - Strategy Proposals (leave empty for now)
   - **Leave "Selected Approach" EMPTY**
5. **DO NOT create T001, T002, T003 yet** - these come AFTER research

**Mark Phase 1 as completed in TodoWrite**

**Output**: Skeleton plan document with only Phase 0 Research defined

---

### Phase 2: Conduct Research and Iterate with User (AskUserQuestion Required)

**Mark Phase 2 as in_progress in TodoWrite**

**Research Process (Iterative):**
1. **Explore codebase**: Read relevant files, find similar patterns
2. **Document findings incrementally**: Add to "Key Findings" as you discover
3. **Identify 2-4 approach options**: Add to "Strategy Proposals" section
4. **ACTIVELY ITERATE with user**:
   - Use `AskUserQuestion` when finding multiple viable approaches
   - Present trade-offs clearly (pros/cons for each option)
   - Get user input on preferences
   - **User may correct assumptions** - update research based on feedback
   - Repeat questions if needed to clarify
5. **Continue until user confirms preferred approach**

**CRITICAL**:
- Do NOT fill "Selected Approach" until user explicitly confirms the strategy
- Use AskUserQuestion MULTIPLE times if needed to clarify
- This is an ITERATIVE process - expect back-and-forth, use AskUserQuestion aggressively

**Mark Phase 2 as completed in TodoWrite when user confirms approach**

**Output**: Phase 0 with Strategy Proposals filled, user has confirmed preferred approach

---

### Phase 3: Finalize Selected Approach (After User Confirmation)

**Mark Phase 3 as in_progress in TodoWrite**

**Actions to finalize proposal:**
1. **Fill "Selected Approach" section** with:
   - **Decision**: Which approach was selected (must match user's confirmed preference)
   - **Rationale**: Why this approach was chosen over alternatives
   - **Key Findings**: Summarize important discoveries from research
   - **Implementation Plan**: High-level steps (5-7 bullet points)
2. Mark all Phase 0 action items as [x] completed
3. Change Phase 0 status to ✅ **Completed**
4. Update Progress Summary to show Phase 0 complete

**Mark Phase 3 as completed in TodoWrite**

**Output**: Phase 0 fully documented with clear decision and rationale

---

### Phase 4: Create Implementation Tasks (ONLY AFTER Phase 0 Complete)

**Mark Phase 4 as in_progress in TodoWrite**

**Actions:**
1. **NOW create T001, T002, T003, ...T00N** based on selected approach
   - Number of tasks depends on complexity (simple: 1-2, medium: 3-5, complex: 5+)
   - Break down into manageable chunks (2-5 days each)
2. Each task should:
   - Define clear, measurable goal
   - List concrete requirements
   - Identify integration points
   - Specify action items and test scenarios
   - Document dependencies
3. Update Progress Summary at top to include all tasks

**Mark Phase 4 as completed in TodoWrite**

**Output**: Complete task breakdown (T001-T00N) aligned with selected approach

---

### Phase 5: Track Throughout Implementation

**Note**: Phase 5 is NOT tracked in TodoWrite. Track progress directly in the plan document.

As you implement tasks (T001, T002, etc.):
- Check off action items as completed in the plan document
- Update task status (🟡 Planned → 🟢 In Progress → ✅ Completed)
- Add newly discovered tasks/requirements
- Fill in "Execution Summary" after each task
- Note lessons learned

---

### Phase 6: Post-Implementation Review

**Note**: Phase 6 is NOT tracked in TodoWrite. Update the plan document directly.

After feature completion:
- Fill in "Lessons Learned" section
- Verify all task statuses are accurate
- Document any technical debt or future work
- Review what went well and what could improve

## Key Patterns from Successful Use

### Pattern 1: Follow Existing Patterns
Research existing similar features (Phase 0) and match their architecture exactly.
**Benefit**: Consistent codebase, faster implementation, reduced bugs.

### Pattern 2: Simplify When Possible
During research, look for ways to simplify (e.g., avoid unnecessary API calls).
**Benefit**: Reduced dependencies, better performance, easier maintenance.

### Pattern 3: Discover Existing Implementations
Research phase may reveal the work is already done - mark task complete.
**Benefit**: Avoids duplicate work, leverages tested code.

### Pattern 4: Document Design Decisions
In Phase 0, use the **"Selected Approach"** section to document WHY you chose one approach over alternatives.
Include: decision, rationale, key findings, and implementation plan.
**Benefit**: Future developers understand rationale, prevents second-guessing, provides clear starting point.

### Pattern 5: Keep Tasks Focused
Break large tasks into smaller chunks that are independently testable.
**Benefit**: Steady progress, clear milestones, easier to parallelize.

## Workflow Summary

**TodoWrite tracks ONLY phases 1-4 (not subtasks):**
```
- [ ] Phase 1: Setup template with Phase 0 Research section
- [ ] Phase 2: Conduct research and iterate with user
- [ ] Phase 3: Finalize selected approach
- [ ] Phase 4: Create implementation tasks (T001-T00N)
```

**Phase-by-Phase Workflow:**

1. **Phase 1 - Setup**:
   - Copy template skeleton
   - Create Phase 0 Research section ONLY
   - DO NOT create T001, T002, T003 yet
   - Mark Phase 1 complete in TodoWrite

2. **Phase 2 - Research & Iterate** (AskUserQuestion REQUIRED):
   - Mark Phase 2 as in_progress
   - Explore codebase, document findings
   - Present 2-4 approach options
   - **Actively iterate with user** via AskUserQuestion
   - User may correct assumptions - update research
   - Mark Phase 2 complete when user confirms approach

3. **Phase 3 - Finalize**:
   - Mark Phase 3 as in_progress
   - Fill "Selected Approach" section with confirmed decision
   - Mark Phase 0 as ✅ Completed in plan document
   - Mark Phase 3 complete in TodoWrite

4. **Phase 4 - Create Tasks**:
   - Mark Phase 4 as in_progress
   - NOW create T001, T002, T003, ...T00N based on selected approach
   - Number of tasks depends on complexity
   - Update Progress Summary
   - Mark Phase 4 complete in TodoWrite

5. **Phase 5 - Implementation** (NOT in TodoWrite):
   - Track progress in plan document as tasks complete
   - Update task statuses directly in the markdown file

6. **Phase 6 - Review** (NOT in TodoWrite):
   - Document lessons learned in plan document

## Reference Materials

For detailed guidance on template sections and best practices, refer to `references/task-planning-guide.md` when needed.

## Success Indicators

Good task planning exhibits:
- ✅ **TodoWrite tracks PHASES**: Creates phase-level todos, not subtasks
- ✅ **Phase 1 completed first**: Phase 0 Research created, T001/T002/T003 NOT created yet
- ✅ **Phase 2 is iterative**: AskUserQuestion used multiple times to clarify with user
- ✅ **User confirmation obtained**: Phase 2 complete only when user confirms approach
- ✅ **Selected Approach filled in Phase 3**: AFTER user confirmation, not before
- ✅ **T001-T00N created in Phase 4**: AFTER Phase 0 complete, aligned with selected approach
- ✅ **Appropriate task count**: Matches complexity (simple: 1-2, medium: 3-5, complex: 5+)
- ✅ **Research includes rationale**: Clear documentation of WHY this approach
- ✅ **Tasks sized appropriately**: 2-5 days each
- ✅ **Progress visible**: TodoWrite shows phase progress clearly

---

**Remember**:
1. **TodoWrite tracks PHASES**
2. **Phases are sequential** - complete Phase 1 before Phase 2, etc.
3. **Phase 2 is iterative** - use AskUserQuestion multiple times, expect back-and-forth
4. **User confirms approach** - Phase 3 only happens after user explicitly agrees
5. **No premature planning** - T001-T00N created in Phase 4
6. **Task count is flexible** - create as many as needed (T001, T002, ...T00N)
