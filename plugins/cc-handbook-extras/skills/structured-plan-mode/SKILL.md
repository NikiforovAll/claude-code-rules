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
1. Copy `assets/plan-template.md` to `tasks/[feature-name]-plan.md` (current project directory)
2. Replace `[Feature Name]` with your feature name
3. Fill in basic overview and context
4. Create Research section with:
   - Goal
   - Context
   - Strategy Proposals (leave empty for now)
   - **Leave "Selected Approach" EMPTY**
5. Create a todo list by using TodoWrite based on the phases below


**TodoWrite tracks ONLY phases 1-4:**
```
- [ ] Phase 1: Setup template with Research section
- [ ] Phase 2: Conduct research and iterate with user
- [ ] Phase 3: Finalize selected approach
- [ ] Phase 4: Create implementation tasks (T001-T00N)
```

**Mark Phase 1 as completed in TodoWrite**

**Output**: Skeleton plan document with only Research defined and todo list created for phases 1-4

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

## Workflow Summary

**TodoWrite tracks ONLY phases 1-4 (not subtasks):**
```
- [ ] Phase 1: Setup template with Research section
- [ ] Phase 2: Conduct research and iterate with user
- [ ] Phase 3: Finalize selected approach
- [ ] Phase 4: Create implementation tasks (T001-T00N)
```

**Phase-by-Phase Workflow:**

1. **Phase 1 - Setup**:
   - Copy template skeleton
   - Create Research section ONLY
   - DO NOT create T001, T002, T003 yet
   - Mark Phase 1 complete in TodoWrite

2. **Phase 2 - Research & Iterate** (AskUserQuestion REQUIRED):
   - Explore codebase, document findings
   - Present 2-3 approach options
   - **Iterate on EACH proposal** via AskUserQuestion (discuss trade-offs, clarify constraints)
   - User may correct assumptions - update research
   - **If user strongly prefers one approach**, may skip detailed discussion of remaining options
   - **Proactively ask**: "Are you ready to select an approach?"
   - Mark Phase 2 complete when user confirms

3. **Phase 3 - Finalize**:
   - Present 2-3 researched approaches and ask user to select one
   - Once user confirms, fill "Selected Approach" section
   - Mark research as ✅ Completed in plan document
   - Mark Phase 3 complete once documentation is done

4. **Phase 4 - Create Tasks**:
   - NOW create T001, T002, T003, ...T00N based on selected approach
   - Number of tasks depends on complexity
   - Update Progress Summary
   - Mark Phase 4 complete in TodoWrite

5. **Phase 5 - Implementation**:
   - Track progress in plan document as tasks complete
   - Update task statuses directly in the markdown file

6. **Phase 6 - Review**:
   - Document lessons learned in plan document


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

For detailed guidance on template sections and best practices, refer to `references/task-planning-guide.md` when needed.

---

**Remember**:
1. **TodoWrite tracks PHASES**
2. **Phases are sequential** - complete Phase 1 before Phase 2, etc.
3. **Phase 2 is iterative** - use AskUserQuestion multiple times, expect back-and-forth
4. **User confirms approach** - do NOT fill "Selected Approach" until user confirms
5. **No premature planning** - T001-T00N created in Phase 4
6. **Task count is flexible** - create as many as needed (T001, T002, ...T00N)
