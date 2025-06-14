# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Repository Overview

This is a Claude Code Rules repository - a collection of best practices, configurations, and custom commands for using Claude Code effectively. This is NOT a traditional software project with source code, but rather a documentation and configuration repository.

## Architecture & Structure

The repository contains:
- Custom Claude commands in `.claude/commands/` for task-based development workflows
- MCP server configurations for enhanced documentation access (Microsoft Docs and Context7)
- Best practices documentation in README.md
- Claude-specific settings and permissions configuration

## Key Workflows

### Vibe Coding Workflow (Task-Based Development)
1. `/create-prd` - Creates Product Requirements Documents from user input
2. `/generate-tasks` - Generates task lists from PRDs
3. `/process-task-list` - Manages and tracks task progress

When using these commands:
- PRDs are saved as `prd-[feature-name].md` in `/tasks` directory
- Always ask clarifying questions before generating PRDs
- Target junior developers in documentation clarity

### Planning Strategies
- Use "think hard" variants for deeper analysis: "think" < "think hard" < "think harder" < "ultrathink"
- Write plans to external files (e.g., plan.md) as checklists
- Use `plan.prompt.md` as external memory for task management
- Switch between modes: `plan mode` → verify, then `auto-accept mode` → execute

## MCP Integration

Two MCP servers are configured:
- **Microsoft Docs MCP**: Access Microsoft/Azure documentation via `mcp__microsoft_docs_mcp__microsoft_docs_search`
- **Context7**: Library documentation retrieval via `mcp__context7__resolve-library-id` and `mcp__context7__get-library-docs`

## Memory Management Guidelines

- Project memory: `./CLAUDE.md` (team-shared)
- User memory: `~/.claude/CLAUDE.md` (personal preferences)
- Keep memories concise and relevant to avoid context bloat