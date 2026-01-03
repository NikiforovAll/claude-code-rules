# Changelog

## [1.19.3] - 2026-01-03

### Changed
- handbook: Updated `/review` command to use three-dot diff syntax for clearer branch comparison

## [1.19.2] - 2025-12-29

### Changed
- handbook-dotnet: Enhanced `dotnet-dependency` skill with package search, add/remove packages, and dotnet tools management commands

## [1.19.1] - 2025-12-25

### Added
- New `handbook-csharp-lsp` plugin for C# Language Server Protocol support using csharp-ls for code intelligence features (go to definition, find references, hover, document symbols, workspace symbols, call hierarchy)

## [1.19.0] - 2025-12-20

### Added
- New `dotnet-dependency` skill in handbook-dotnet plugin for investigating dependencies and security auditing

## [1.18.0] - 2025-12-20

### Added
- New `dotnet-test` skill in handbook-dotnet plugin for selective unit testing with xUnit focus

## [1.17.0] - 2025-12-17

### Added
- New `handbook-glab` plugin for GitLab CLI (glab) integration with expertise in managing merge requests, issues, CI/CD pipelines, and repositories

## [1.16.0] - 2025-12-17

### Added
- New `handbook-microsoft-docs` plugin for Microsoft Learn documentation access via MCP server

## [1.15.0] - 2025-12-13

### Added
- New `handbook-nano-banana` plugin for Python scripting and Gemini image generation using uv

## [1.14.0] - 2025-12-04

### Added
- New `/save-prompt` command in handbook-extras for generalizing discussions into reusable prompts

## [1.13.0] - 2025-12-04

### Added
- New `dotnet-run-file` skill in handbook-dotnet plugin for C# scripting with `dotnet run file.cs`
- Stdin execution patterns for Claude Code friendly one-liners

### Changed
- Updated `update-component-reference` skill with correct badge format (`badge--{plugin-name}`)

## [1.12.0] - 2025-11-25

### Added
- New `/reflect` command in handbook-extras for creating reflective session analyses focusing on techniques, patterns, and lessons learned

## [1.11.0] - 2025-01-19

### Added
- New `handbook-agent-spec-kit` plugin for spec-driven development workflow

## [1.10.1] - 2025-01-08

### Changed
- Updated `handbook-sounds` plugin with stop and notification support

## [1.10.0] - 2025-01-08

### Added
- New `handbook-structured-plan-mode` plugin for systematic planning and tracking of complex feature implementations
- Task execution discipline with explicit user confirmation before moving between tasks
- Task lifecycle documentation with step-by-step guidance for task management
- Mermaid diagrams removed from skill documentation (replaced with text explanations)

### Changed
- Improved structured-plan-mode skill with one-task-at-a-time execution discipline
- Enhanced task management documentation with clear lifecycle steps and dual-tracking examples
- Added emphasis on reading task-planning-guide.md throughout Phase 4 and Phase 5
- Removed skills array from handbook-extras plugin.json (structured-plan-mode moved to dedicated plugin)
- Updated component reference documentation and website plugins page for new plugin

## [1.9.0] - 2025-01-08

### Added
- New `handbook-git-worktree` plugin for Git worktree management

### Changed
- Enhanced documentation navigation with improved plugin badges and sidebar organization
- Simplified plugin README files for better readability

## [1.8.0] - 2025-11-08

### Added
- New `cc-handbook-sounds` plugin with audio feedback for Windows
- Environment variable support for custom sound files (`CC_HANDBOOK_SOUNDS_FILE`)

## [1.7.0] - 2025-01-05

### Changed
- Moved Context7 plugin to dedicated `cc-handbook-context7` plugin

## [1.6.3] - 2025-11-05

### Changed
- Moved Context7 MCP server from `cc-handbook` to new dedicated plugin `cc-handbook-context7`

### Added
- New `cc-handbook-context7` plugin for Context7 MCP server integration
- Dedicated plugin structure for better modularity and separation of concerns

### Removed
- `.mcp.json` file from `cc-handbook` plugin (Context7 now in separate plugin)

## [1.6.2] - 2025-11-05

### Added
- CSharpier hook now supports `.CS` (uppercase) and `.csx` (C# script) files
- `CC_HANDBOOK_DOTNET_DISABLE_HOOKS` environment variable to disable formatter
- Automated test suite for CSharpier hook

## [1.6.1] - 2025-11-05

### Changed
- Renamed `handbook-qa` plugin folder to `cc-handbook-qa` for consistent naming convention

## [1.6.0] - 2025-10-31

### Added
- New `/review` command for systematic code review with structured feedback

- New `@code-reviewer` agent that invokes `/review` command in separate context

## [1.5.1] - 2025-10-30

### Changed
- Moved `codebase-analyzer`, `pair-programmer`, and `deep-research-agent` agents from `cc-handbook` to `cc-handbook-extras`

## [1.5.0] - 2025-10-30

### Added
- New `handbook-qa` plugin with Playwright MCP integration for browser automation and QA testing

### Changed
- Moved Playwright MCP from `cc-handbook` to dedicated `handbook-qa` plugin
- Moved `backend-architect` and `system-architect` agents from `cc-handbook` to `cc-handbook-extras`

## [1.4.0] - 2025-10-29

### Added
- New `git-worktree` skill for managing Git worktrees in handbook-extras plugin

## [1.3.3] - 2025-10-25

### Added
- Component reference documentation for `/tools` command

## [1.3.2] - 2025-10-25

### Added
- Task template file (`task-template.md`) for creating individual task documents in structured-plan-mode skill
- Step-by-step task creation guidance with 5-step checklist in SKILL.md and usage guide

### Changed
- Improved plan-template.md clarity with comments for placeholders and updated timestamp format
- Renamed `task-planning-guide.md` to `usage-guide.md` for better naming consistency

## [1.3.1] - 2025-10-24

### Fixed
- Corrected template and documentation for structured-plan-mode skill

## [1.3.0] - 2025-10-24

### Added
- New `structured-plan-mode` skill in `cc-handbook-extras` plugin for systematic planning of complex feature implementations

## [1.2.0] - 2025-10-23

### Added
- New `@git-diff-analyzer` agent in `cc-handbook-extras` plugin for analyzing git branch differences
- Agent generates concise, one-page summaries with file statistics and high-level change descriptions
- Component reference documentation for the git-diff-analyzer agent
- Uses Haiku model for fast, cost-efficient branch comparisons

## [1.1.0] - 2025-10-20

### Added
- New `cc-handbook-dotnet` plugin with automatic CSharpier formatting for C# files
- PostToolUse hook for automatic code formatting on file writes and edits
- Dynamic CSharpier executable detection (local and global installations)
- Comprehensive documentation for the dotnet plugin and hooks
- Website documentation for hooks in Component Reference section

### Changed
- Modernized version-bump skill to support dynamic plugin discovery
- Updated version-bump script to use new marketplace location (`.claude-plugin/marketplace.json`)
- Version management now automatically discovers all plugins from marketplace manifest
- Improved scalability for adding future plugins

## [1.0.1] - 2025-10-19

### Added
- Version bump skill for automated release version management
- Python scripts for atomic version updates across the monorepo
- Version consistency validation tooling

## [1.0.0] - 2025-10-18

### Added
- Initial plugin release as Claude Code Handbook
- 5 custom slash commands: `/tools`, `/prompt-generator`, `/five`, `/explain`, `/commit`
- 2 specialized agents: Codebase Analyzer and Pair Programmer
- 4 integrated MCP servers: Microsoft Docs, Context7, Playwright, Chrome DevTools
- Plugin manifest and directory structure following Claude Code plugin specifications
- Comprehensive best practices documentation
- Tips and tricks guide for Claude Code workflows

### Changed
- Reorganized `.claude/` directory structure into plugin-compliant layout
- Updated README with plugin installation and usage instructions
- Migrated commands to `commands/` directory
- Migrated agents to `agents/` directory

### Note
This is the first release of the plugin format. Previous versions were distributed as configuration files within user projects.
