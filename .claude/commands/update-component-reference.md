description: Add plugin components to the website docs, including component reference pages, plugin index entries, and plugin READMEs
argument-hint: Component or plugin to document (e.g., "skill glab", "agent code-reviewer", "plugin handbook-reflect")
allowed-tools: ["Skill(update-component-reference)", "Read", "Write", "Edit", "Glob", "Grep", "Bash"]
---

Load the "update-component-reference" skill via `Skill` tool and follow its instructions.

When documenting a new plugin, also:
- update the website plugin index in `website/docs/plugins.md`
- add or refresh the plugin's concise `README.md` so the plugin structure matches repo conventions

**Request:** $ARGUMENTS
