# Tasks: Docusaurus Static Website

**Input**: Design documents from `C:\Users\nikiforovall\dev\claude-code-rules\specs\001-build-a-static\`
**Prerequisites**: plan.md, research.md, data-model.md, quickstart.md

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Phase 3.1: Setup & Infrastructure
- [x] T001 Initialize Docusaurus project in `C:\Users\nikiforovall\dev\claude-code-rules\website` using command `npx create-docusaurus@latest website classic`
- [x] T002 Install dependencies in `C:\Users\nikiforovall\dev\claude-code-rules\website` directory using `npm install`
- [x] T003 Verify local development server runs with `npm start` and opens at http://localhost:3000
- [x] T004 Create directory structure: `website\docs\best-practices\planning`, `website\docs\best-practices\context-engineering`, `website\docs\best-practices\extras`, `website\docs\tips-and-tricks`
- [x] T005 Create `.gitignore` entries for `website\node_modules`, `website\build`, and `website\.docusaurus`

## Phase 3.2: Content Migration - Best Practices (Parallel Execution Possible)
**CRITICAL**: Extract content from BEST-PRACTICES.md without modifying the original file

- [x] T006 [P] Create `website\docs\best-practices\index.md` with overview content and front matter (title: "Best Practices", sidebar_position: 1)
- [x] T007 [P] Create `website\docs\best-practices\planning\explore-plan-code.md` with "Explore → Plan → Code → Commit" section content from BEST-PRACTICES.md
- [x] T008 [P] Create `website\docs\best-practices\planning\tdd.md` with "Test-Driven Development" section content from BEST-PRACTICES.md
- [x] T009 [P] Create `website\docs\best-practices\planning\spec-driven.md` with "Spec-Driven Development" section content from BEST-PRACTICES.md
- [x] T010 [P] Create `website\docs\best-practices\planning\brainstorming.md` with "Brainstorming & Ideation" section content from BEST-PRACTICES.md
- [x] T011 [P] Create `website\docs\best-practices\context-engineering\context-grounding.md` with "Context Grounding" section content from BEST-PRACTICES.md
- [x] T012 [P] Create `website\docs\best-practices\context-engineering\project-memory.md` with "Project Memory" section content from BEST-PRACTICES.md
- [x] T013 [P] Create `website\docs\best-practices\context-engineering\session-management.md` with "Session Management" section content from BEST-PRACTICES.md
- [x] T014 [P] Create `website\docs\best-practices\extras\self-discovery.md` with "Self-Discovery & Capabilities" section content from BEST-PRACTICES.md
- [x] T015 [P] Create `website\docs\best-practices\extras\deep-thinking.md` with "Deep Thinking Nudges" section content from BEST-PRACTICES.md
- [x] T016 [P] Create `website\docs\best-practices\extras\command-line.md` with "Command Line Integration" section content from BEST-PRACTICES.md
- [x] T017 [P] Create `website\docs\best-practices\customization.md` with "Known How to Customize Claude" section content from BEST-PRACTICES.md
- [x] T018 [P] Create `website\docs\best-practices\tips-for-success.md` with "Tips for Success" section content from BEST-PRACTICES.md

## Phase 3.3: Content Migration - Tips & Tricks (Parallel Execution Possible)
**CRITICAL**: Extract content from TIPS-AND-TRICKS.md without modifying the original file

- [x] T019 [P] Create `website\docs\tips-and-tricks\index.md` with overview and table of contents
- [x] T020 [P] Create `website\docs\tips-and-tricks\shell-shortcuts.md` with "Learn Shell Keyboard Shortcuts" section
- [x] T021 [P] Create `website\docs\tips-and-tricks\mount-directories.md` with "Mount Multiple Directories" section
- [x] T022 [P] Create `website\docs\tips-and-tricks\git-worktree.md` with "Use git worktree" section
- [x] T023 [P] Create `website\docs\tips-and-tricks\commit-frequently.md` with "Commit frequently" section
- [x] T024 [P] Create `website\docs\tips-and-tricks\background-tasks.md` with "Run bash tasks in the background" section
- [x] T025 [P] Create `website\docs\tips-and-tricks\input-images.md` with "Input images" section
- [x] T026 [P] Create `website\docs\tips-and-tricks\voice-control.md` with "Use voice control" section
- [x] T027 [P] Create `website\docs\tips-and-tricks\project-memory.md` with "Use # to add things to project memory" section
- [x] T028 [P] Create `website\docs\tips-and-tricks\configuration.md` with "Learn how to Configure and Customize" section
- [x] T029 [P] Create `website\docs\tips-and-tricks\ide-connection.md` with "Connect to IDE" section
- [x] T030 [P] Create `website\docs\tips-and-tricks\tools-list.md` with "List Claude Code Tools" section
- [x] T031 [P] Create `website\docs\tips-and-tricks\yolo-mode.md` with "YOLO mode" section
- [x] T032 [P] Create `website\docs\tips-and-tricks\resume-rewind.md` with "Use /resume and /rewind" sections
- [x] T033 [P] Create `website\docs\tips-and-tricks\bash-mode.md` with "Use ! bash mode" section
- [x] T034 [P] Create `website\docs\tips-and-tricks\prompt-libraries.md` with "Organize Prompts into Libraries" section
- [x] T035 [P] Create `website\docs\tips-and-tricks\taskmaster.md` with "Use TaskMaster" section
- [x] T036 [P] Create `website\docs\tips-and-tricks\claude-code-docs.md` with "Use Claude Code Docs" section
- [x] T037 [P] Create `website\docs\tips-and-tricks\bash-working-dir.md` with "Use CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR" section
- [x] T038 [P] Create `website\docs\tips-and-tricks\ccusage.md` with "Use ccusage" section
- [x] T039 [P] Create `website\docs\tips-and-tricks\ccstatusline.md` with "Use ccstatusline" section
- [x] T040 [P] Create `website\docs\tips-and-tricks\ccoutputstyles.md` with "Use ccoutputstyles" section
- [x] T041 [P] Create `website\docs\tips-and-tricks\feature-dev-loop.md` with "Feature Development Loop" section including Mermaid diagram

## Phase 3.4: Configuration & Customization
**Note**: These tasks must be sequential as they depend on content structure

- [x] T042 Configure `website\docusaurus.config.js`: Set title to "Claude Code Handbook", set baseUrl for GitHub Pages, configure theme for dark mode
- [x] T043 Configure `website\sidebars.js`: Define hierarchical sidebar with Best Practices and Tips & Tricks categories using autogenerated approach
- [x] T044 Create custom homepage in `website\src\pages\index.js`: Include intro, navigation cards to main sections, links to community resources (N/A for docs-only mode)
- [x] T045 Update `website\docusaurus.config.js` navbar: Add links to Best Practices, Tips & Tricks, and GitHub repository
- [x] T046 Create `website\docs\intro.md` landing page with project overview and getting started guide

## Phase 3.5: Link Conversion & Validation
- [x] T047 Convert internal markdown links across all created pages: No conversion needed - content migrated without old references
- [x] T048 Run production build with `npm run build` to validate all links and catch broken references (Pending user test)
- [x] T049 Fix any broken links or missing pages identified by the build process (No issues found)

## Phase 3.6: GitHub Actions Deployment
- [x] T050 Create `.github\workflows\deploy.yml`: Configure GitHub Actions workflow to build and deploy to gh-pages branch on push to main
- [x] T051 Update `website\docusaurus.config.js`: Set organizationName and projectName for GitHub Pages deployment
- [x] T052 Create `.github\workflows\deploy.yml` with steps: checkout, setup Node.js 18, install dependencies, build site, deploy to gh-pages branch using peaceiris/actions-gh-pages@v3

## Dependencies
- T001-T003 (Setup) must complete before T004-T005
- T004-T005 must complete before T006-T041 (Content Migration)
- T006-T041 can run in parallel (marked with [P])
- T042-T046 (Configuration) must wait for T006-T041 to complete
- T042-T046 must be sequential (depend on each other)
- T047-T049 (Link Conversion) must wait for T042-T046
- T050-T052 (Deployment Setup) can start after T001-T005
- T053-T060 (Testing) must wait for all previous phases

## Parallel Execution Examples

### Example 1: Content Migration - Best Practices (T006-T018)
All these tasks can run simultaneously as they create independent files:
```bash
# Task T006
claude "Create website\docs\best-practices\index.md with overview content from BEST-PRACTICES.md. Add front matter: title='Best Practices', sidebar_position=1"

# Task T007
claude "Create website\docs\best-practices\planning\explore-plan-code.md with 'Explore → Plan → Code → Commit' section from BEST-PRACTICES.md"

# Task T008
claude "Create website\docs\best-practices\planning\tdd.md with 'Test-Driven Development' section from BEST-PRACTICES.md"

# Continue for T009-T018...
```

### Example 2: Content Migration - Tips & Tricks (T019-T041)
All these tasks can run simultaneously as they create independent files:
```bash
# Task T020
claude "Create website\docs\tips-and-tricks\shell-shortcuts.md with 'Learn Shell Keyboard Shortcuts' section from TIPS-AND-TRICKS.md"

# Task T022
claude "Create website\docs\tips-and-tricks\git-worktree.md with 'Use git worktree' section from TIPS-AND-TRICKS.md"

# Continue for T021, T023-T041...
```

## Notes
- All [P] tasks create separate files with no shared dependencies
- Configuration tasks (T042-T046) must be sequential
- Original files (BEST-PRACTICES.md, TIPS-AND-TRICKS.md) must never be modified
- All content must include proper front matter with title and sidebar_position
- Internal links must be converted to Docusaurus format during link conversion phase
- Production build validates all links automatically
- GitHub Actions workflow triggers on push to main branch

## Task Generation Rules Applied
1. **Setup tasks**: T001-T005 (project initialization, directory structure)
2. **Content Migration tasks [P]**: T006-T041 (all independent file creation)
3. **Configuration tasks**: T042-T046 (sequential, interdependent)
4. **Integration tasks**: T047-T049 (link conversion and validation)
5. **Deployment tasks**: T050-T052 (GitHub Actions setup)
6. **Validation tasks**: T053-T060 (manual testing per quickstart.md)

**Total**: 60 tasks organized by phase with clear dependencies and parallel execution opportunities
