
# Implementation Plan: Docusaurus Static Website

**Branch**: `001-build-a-static` | **Date**: 2025-10-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `C:\Users\nikiforovall\dev\claude-code-rules\specs\001-build-a-static\spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from file system structure or context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on the content of the constitution document.
4. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, `GEMINI.md` for Gemini CLI, `QWEN.md` for Qwen Code, or `AGENTS.md` for all other agents).
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
Transform existing markdown documentation (BEST-PRACTICES.md and TIPS-AND-TRICKS.md) into a searchable Docusaurus static website deployed via GitHub Pages. Content will be restructured into focused, topic-based pages while preserving all existing content. Original markdown files remain untouched.

## Technical Context
**Language/Version**: Node.js 18+ (for Docusaurus build tooling), Markdown/MDX
**Primary Dependencies**: Docusaurus 3.x (classic preset), React 18+, GitHub Actions
**Storage**: N/A (static files only)
**Testing**: Manual verification against acceptance scenarios, link validation
**Target Platform**: Static web hosting (GitHub Pages)
**Project Type**: Documentation website (static site generator)
**Performance Goals**: <3s page load time, instant navigation with client-side routing
**Constraints**: Must not modify existing BEST-PRACTICES.md or TIPS-AND-TRICKS.md files
**Scale/Scope**: ~20-30 documentation pages split from 2 source markdown files

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**I. Markdown-First**: ✅ PASS
- All new documentation pages will be in markdown format
- Docusaurus natively supports markdown with MDX enhancements
- Existing .md files remain untouched

**II. Docusaurus-Compatible**: ✅ PASS
- Using Docusaurus 3.x as the static site generator
- Will follow Docusaurus conventions: front matter, directory structure, sidebars
- Enables search, versioning, responsive design out of the box

**III. Clarity & Accuracy**: ✅ PASS
- Content split into focused topic pages improves clarity
- All existing content preserved without loss
- No new content created, only restructuring

**Result**: NO VIOLATIONS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)
```
specs/001-build-a-static/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
claude-code-rules/
├── website/                    # NEW: Docusaurus root directory
│   ├── docs/                  # NEW: Documentation pages
│   │   ├── best-practices/    # NEW: From BEST-PRACTICES.md
│   │   │   ├── index.md
│   │   │   ├── planning/
│   │   │   ├── context-engineering/
│   │   │   └── tips-for-success/
│   │   └── tips-and-tricks/   # NEW: From TIPS-AND-TRICKS.md
│   │       ├── index.md
│   │       ├── shortcuts.md
│   │       ├── git-worktree.md
│   │       └── ...
│   ├── src/                   # NEW: Docusaurus source
│   │   └── pages/
│   │       └── index.js       # NEW: Homepage
│   ├── static/                # NEW: Static assets
│   │   └── img/
│   ├── docusaurus.config.js   # NEW: Docusaurus configuration
│   ├── sidebars.js            # NEW: Sidebar navigation
│   └── package.json           # NEW: Node dependencies
├── .github/
│   └── workflows/
│       └── deploy.yml         # NEW: GitHub Actions for deployment
├── BEST-PRACTICES.md          # UNCHANGED: Original file
├── TIPS-AND-TRICKS.md         # UNCHANGED: Original file
└── README.md                  # UNCHANGED
```

**Structure Decision**: Documentation website structure (static site generator). The Docusaurus site will be created in a new `website/` directory at the repository root. All new markdown files go under `website/docs/` organized by topic. Original markdown files remain untouched in the root.

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Generate contract tests** from contracts:
   - One test file per endpoint
   - Assert request/response schemas
   - Tests must fail (no implementation yet)

4. **Extract test scenarios** from user stories:
   - Each story → integration test scenario
   - Quickstart test = story validation steps

5. **Update agent file incrementally** (O(1) operation):
   - Run `.specify/scripts/bash/update-agent-context.sh claude`
     **IMPORTANT**: Execute it exactly as specified above. Do not add or remove any arguments.
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, agent-specific file

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (data model, research, quickstart)
- Infrastructure setup (Docusaurus init, configuration files)
- Content migration tasks (one per major section from source files)
- Testing and validation tasks
- Deployment configuration

**Task Categories**:
1. **Setup** (~5 tasks): Initialize Docusaurus, configure, install dependencies
2. **Content Migration** (~20 tasks): Split BEST-PRACTICES.md and TIPS-AND-TRICKS.md into individual pages
3. **Configuration** (~5 tasks): Sidebar, homepage, theme customization
4. **Deployment** (~3 tasks): GitHub Actions workflow, test deployment
5. **Validation** (~3 tasks): Link checking, content verification, manual testing

**Ordering Strategy**:
- Setup → Content Migration → Configuration → Deployment → Validation
- Content migration tasks can be parallel [P] (independent files)
- Configuration tasks sequential (depend on content structure)

**Estimated Output**: 30-35 numbered, ordered tasks in tasks.md

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [x] Complexity deviations documented (N/A - no violations)

**Artifacts Generated**:
- [x] `C:\Users\nikiforovall\dev\claude-code-rules\specs\001-build-a-static\research.md`
- [x] `C:\Users\nikiforovall\dev\claude-code-rules\specs\001-build-a-static\data-model.md`
- [x] `C:\Users\nikiforovall\dev\claude-code-rules\specs\001-build-a-static\quickstart.md`
- [x] `C:\Users\nikiforovall\dev\claude-code-rules\CLAUDE.md` (updated)

---
*Based on Constitution v1.0.0 - See `.specify/memory/constitution.md`*
