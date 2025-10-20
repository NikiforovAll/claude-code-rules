---
name: add-tip
description: This skill should be used when the user wants to add a new tip, document a command, or create documentation for a feature in the tips&tricks section of the website.
---

# Add Tip Skill

Add new documentation pages to the Claude Code Handbook website's tips&tricks section.

## When to Use

Use this skill when the user requests to:
- Add a tip about a specific feature or command
- Document a command (e.g., "document the /foo command")
- Create documentation for a development technique
- Add information to the tips&tricks section

## Website Structure

The tips&tricks documentation lives in the Docusaurus website under:

```
website/docs/tips-and-tricks/
├── [root-level-tips].md           # General tips
├── miscellaneous/                  # Miscellaneous category
│   └── [specific-tips].md
└── extras/                         # External tools/resources
    └── [tool-docs].md
```

### Categories

- **Root level** (`website/docs/tips-and-tricks/`): General development practices, major features
- **Miscellaneous** (`website/docs/tips-and-tricks/miscellaneous/`): Specific commands, shortcuts, utilities
- **Extras** (`website/docs/tips-and-tricks/extras/`): Third-party tools, external resources

## Implementation Process

### 1. Determine Target Directory

Ask the user which category is appropriate, or infer from context:
- Commands, shortcuts, utilities → `miscellaneous/`
- Third-party tools → `extras/`
- General practices → root level

### 2. Determine sidebar_position

Read existing files in the target directory to find the highest `sidebar_position` number and add 1.

Example:
```bash
# Find highest sidebar_position in miscellaneous
grep -h "sidebar_position:" website/docs/tips-and-tricks/miscellaneous/*.md | sort -n
```

### 3. Understand Existing Style

Before writing, read 2-3 existing files from the target category to understand:
- Content length and detail level
- Tone (concise, developer-friendly)
- Structure (sections, code examples, links)
- Use of callouts and formatting

### 4. Create the File

**Filename convention**: Use kebab-case (lowercase with hyphens)
- Good: `release-notes.md`, `keyboard-shortcuts.md`
- Bad: `ReleaseNotes.md`, `release_notes.md`

**Required frontmatter**:
```yaml
---
title: "Page Title"
sidebar_position: N
---
```

**Content guidelines**:
- Keep it concise - developers don't need obvious explanations
- Focus on practical information and examples
- Use bullet points for clarity
- Include code examples where relevant
- Add callouts (> 💡) for important tips
- **Use Mermaid diagrams** when visualizing workflows, processes, or relationships (Docusaurus supports Mermaid natively)

### 5. Review

After creating the file:
- Verify the frontmatter is correct
- Confirm the content matches the style of other pages in that category
- Check that the sidebar_position is sequential

## Example Workflow

User: "Document the /release-notes command"

1. Identify category: `miscellaneous/` (it's a command)
2. Check existing files to determine next sidebar_position
3. Read 2-3 files in `miscellaneous/` to understand style
4. Create `website/docs/tips-and-tricks/miscellaneous/release-notes.md`
5. Write concise content following observed patterns
6. Use next available sidebar_position number

## Important Notes

- **Do NOT modify** `TIPS-AND-TRICKS.md` or `BEST-PRACTICES.md` - these are obsolete
- The website documentation in `website/docs/` is the source of truth
- Match the brevity and style of existing pages
- Avoid verbose explanations - respect developers' time