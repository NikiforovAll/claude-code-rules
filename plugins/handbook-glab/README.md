# handbook-glab

GitLab CLI (glab) expertise for Claude Code, providing guidance for managing merge requests, issues, CI/CD pipelines, and repositories from the command line.

## Features

- **Merge Request Management**: Create, review, approve, and merge MRs
- **Issue Tracking**: Create, update, and manage GitLab issues
- **CI/CD Pipeline Operations**: Monitor, trigger, and troubleshoot pipelines
- **Repository Operations**: Clone, fork, and manage repositories
- **API Access**: Direct GitLab API access for advanced operations

## Prerequisites

Install the GitLab CLI before using this plugin:

```bash
# macOS
brew install glab

# Windows (winget)
winget install glab

# Windows (scoop)
scoop install glab

# Linux (various package managers)
# See: https://gitlab.com/gitlab-org/cli#installation
```

Authenticate with GitLab:

```bash
glab auth login
```

## Usage

The skill activates automatically when you ask about GitLab operations:

- "Create a merge request for this branch"
- "List my assigned issues"
- "Check the pipeline status"
- "How do I approve an MR?"

## Skill Structure

```
skills/
└── glab-skill/
    ├── SKILL.md                    # Main skill with core workflows
    └── references/
        ├── commands-detailed.md    # Comprehensive command reference
        ├── quick-reference.md      # Condensed cheat sheet
        └── troubleshooting.md      # Error scenarios and solutions
```

## Common Workflows

### Create a Merge Request

```bash
git push -u origin feature-branch
glab mr create --title "Add feature" --description "Implements X"
```

### Review and Approve MR

```bash
glab mr list --reviewer=@me
glab mr checkout 123
glab mr approve 123
```

### Monitor CI/CD Pipeline

```bash
glab pipeline ci view
glab ci status
glab ci trace
```

## Self-Hosted GitLab

For self-hosted GitLab instances:

```bash
glab auth login --hostname gitlab.example.org

# Or set environment variable
export GITLAB_HOST=gitlab.example.org
```

## License

MIT
