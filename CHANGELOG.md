# Changelog

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
