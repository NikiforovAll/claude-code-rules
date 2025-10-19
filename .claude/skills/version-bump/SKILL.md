---
name: version-bump
description: This skill automates version bumping during the release process for the Claude Code Handbook monorepo. It should be used when the user requests to bump versions, prepare a release, or increment version numbers across the repository.
---

# Version Bump Skill

This skill automates the version management process for the Claude Code Handbook monorepo, ensuring consistent version updates across all plugin files and the marketplace manifest.

## When to Use This Skill

Trigger this skill when users mention:
- "bump version" or "bump the version"
- "prepare for release" or "release process"
- "increment version" or "update version numbers"
- "new release" or "create a release"
- Any mention of "major", "minor", or "patch" version changes

## Version Management Overview

The monorepo maintains versions in 5 locations that must stay synchronized:

1. `marketplace/marketplace.json` - Marketplace version
2. `marketplace/marketplace.json` - cc-handbook plugin entry
3. `marketplace/marketplace.json` - cc-handbook-extras plugin entry
4. `plugins/cc-handbook/.claude-plugin/plugin.json`
5. `plugins/cc-handbook-extras/.claude-plugin/plugin.json`

This skill ensures all locations are updated atomically and remain consistent.

## Workflow Instructions

### Step 1: Validate Current State

Before proceeding with any version bump:

1. Check for uncommitted changes in the working directory using `git status`
2. Validate current version consistency by running the validation check:
   ```bash
   python .claude/skills/version-bump/scripts/bump_version.py patch --dry-run
   ```
   (Note: The script doesn't actually support --dry-run flag, so skip this and proceed directly to asking the user)

3. If versions are inconsistent, report the discrepancy to the user and ask whether to proceed

### Step 2: Determine Bump Type

Ask the user which type of version bump to perform using semantic versioning:

- **Major** (X.0.0): Breaking changes, incompatible API changes
- **Minor** (x.X.0): New features, backward-compatible additions
- **Patch** (x.x.X): Bug fixes, backward-compatible fixes

Use clear language: "Which version component should be bumped: major, minor, or patch?"

### Step 3: Prompt for Changelog Entry

Before executing the version bump, collect information for the CHANGELOG.md update:

1. Ask the user to provide a summary of changes for this release
2. Request specific items to include:
   - Added features (### Added)
   - Changed functionality (### Changed)
   - Deprecated features (### Deprecated)
   - Removed features (### Removed)
   - Fixed bugs (### Fixed)
   - Security updates (### Security)

Keep the summary concise but informative.

### Step 4: Execute Version Bump

Run the bundled Python script to update all version references:

```bash
python .claude/skills/version-bump/scripts/bump_version.py <bump_type>
```

Replace `<bump_type>` with the user's selection (major, minor, or patch).

The script will:
- Read current versions from all files
- Detect any version inconsistencies (with warning)
- Bump the version according to semantic versioning rules
- Update all 5 version locations atomically
- Verify consistency after the update

### Step 5: Update CHANGELOG.md

After the script succeeds, update the CHANGELOG.md file:

1. Read the current CHANGELOG.md
2. Insert a new version section at the top (after the header), following this format:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- List of new features

### Changed
- List of changes to existing functionality

### Fixed
- List of bug fixes
```

3. Use today's date in YYYY-MM-DD format
4. Include the changelog content collected in Step 3
5. Preserve all existing changelog entries below the new section

### Step 6: Report Results

After successful completion:

1. Display a summary showing:
   - Old version → New version
   - Bump type applied
   - Files modified (all 3 JSON files + CHANGELOG.md)

2. Provide next steps for the user:
   ```
   Version bump completed successfully!

   Changes made:
   - marketplace/marketplace.json
   - plugins/cc-handbook/.claude-plugin/plugin.json
   - plugins/cc-handbook-extras/.claude-plugin/plugin.json
   - CHANGELOG.md

   Next steps:
   1. Review changes: git diff
   2. Commit changes: git add . && git commit -m "chore: bump version to X.Y.Z"
   3. Create git tag (optional): git tag vX.Y.Z
   4. Push changes: git push && git push --tags
   ```

## Error Handling

Handle common error scenarios:

- **Version inconsistency detected**: Warn the user and ask whether to proceed
- **File not found**: Report which file is missing and suggest checking repository structure
- **Invalid version format**: Report the parsing error and current version string
- **Script execution failure**: Display the error message and suggest manual inspection

## Bundled Resources

### Scripts

- `scripts/bump_version.py`: Python script that performs atomic version updates across all files with validation and consistency checks

## Examples

### Example 1: Patch Release
```
User: "Bump the version for a patch release"
Claude: "I'll help you bump the version for a patch release. First, let me check the current version state..."

[Runs validation]

Claude: "Current version is 1.0.0. What changes should I include in the CHANGELOG for this patch release?"
User: "Fixed bug in commit command and updated documentation"
Claude: "Perfect. I'll now bump the patch version to 1.0.1 and update the changelog."

[Executes bump_version.py patch]
[Updates CHANGELOG.md]

Claude: "Version bump completed successfully!
- Old version: 1.0.0
- New version: 1.0.1

Files updated:
- marketplace/marketplace.json
- plugins/cc-handbook/.claude-plugin/plugin.json
- plugins/cc-handbook-extras/.claude-plugin/plugin.json
- CHANGELOG.md

Next steps:
1. Review changes: git diff
2. Commit: git add . && git commit -m 'chore: bump version to 1.0.1'
3. Tag (optional): git tag v1.0.1"
```

### Example 2: Minor Release with New Features
```
User: "I want to release a new minor version with the new agents I added"
Claude: "I'll help you prepare a minor version release. Let me validate the current version state first..."

[Runs validation]

Claude: "Current version is 1.0.1. What new features and changes should I include in the CHANGELOG?"
User: "Added two new agents: root-cause-analyst and refactoring-expert. Updated documentation for all agents."
Claude: "Great! I'll bump the minor version to 1.1.0 and update the changelog accordingly."

[Executes bump_version.py minor]
[Updates CHANGELOG.md with Added and Changed sections]

Claude: "Minor version release prepared successfully!
- Old version: 1.0.1
- New version: 1.1.0

Next steps:
1. Review changes: git diff
2. Commit and tag for release
3. Push to trigger deployment"
```

## Notes

- The script does NOT create git commits or tags - the user handles version control operations manually
- All version updates are atomic - either all files are updated or none are
- The skill validates version consistency before and after updates
- Follows semantic versioning (semver) conventions strictly
- The marketplace version is treated as the source of truth when checking consistency