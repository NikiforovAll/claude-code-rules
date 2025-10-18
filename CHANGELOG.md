# Changelog

All notable changes to the Claude Code Handbook plugin are documented in this file.

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
