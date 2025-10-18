# Marketplace Configuration

This document describes the Claude Code Handbook Marketplace configuration.

## Marketplace File

**Location:** `.claude-plugin/marketplace.json` (Official specification location)

**Schema:** https://anthropic.com/claude-code/marketplace.schema.json

## Configuration Details

### Marketplace Metadata
- **Name:** Claude Code Handbook Marketplace
- **Version:** 1.0.0
- **Owner:** nikiforovall
- **Repository:** https://github.com/nikiforovall/claude-code-rules

### Required Fields
- `$schema` - JSON Schema reference (validates the marketplace structure)
- `name` - Marketplace name
- `owner` - Object with `name` and `email` fields
- `plugins` - Array of plugin entries

### Plugin Entries

Each plugin entry includes:
- `name` (required) - Plugin identifier
- `version` - Semantic version
- `description` - Short description
- `author` - Object with `name` and `url`
- `source` - GitHub URL or local path
- `category` - Plugin category (e.g., "productivity", "extensions")
- `tags` - Array of descriptive tags
- `homepage` - Documentation URL
- `strict` - Boolean (true = plugin.json required, false = optional)

## Adding to Claude Code

### Step 1: Add Marketplace

```bash
/plugin marketplace add https://github.com/nikiforovall/claude-code-rules
```

Claude Code will automatically look for `.claude-plugin/marketplace.json`

### Step 2: Install Plugins

```bash
# Install core plugin
/plugin install cc-handbook

# Install extras plugin
/plugin install cc-handbook-extras
```

### Step 3: Verify

```bash
/help
```

## Plugins Included

### cc-handbook
- **Type:** Core
- **Status:** Stable
- **Category:** productivity
- **Source:** `plugins/cc-handbook/`

### cc-handbook-extras
- **Type:** Experimental
- **Status:** Open for contributions
- **Category:** extensions
- **Source:** `plugins/cc-handbook-extras/`

## Official Documentation

For more information about Claude Code plugin marketplaces, visit:
https://docs.claude.com/en/docs/claude-code/plugin-marketplaces

## Marketplace JSON Schema Reference

The marketplace configuration follows the official Claude Code marketplace JSON schema with:
- Full schema validation support
- Semantic versioning for plugins
- Category and tag-based discovery
- Strict and non-strict plugin modes
- Support for local paths and remote URLs
