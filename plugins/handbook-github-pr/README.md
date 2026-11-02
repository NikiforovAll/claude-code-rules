# handbook-github-pr

A Claude Code mod that shows the GitHub pull request of the session's current branch in a band above the prompt, right-aligned: `PR #42 open → main`. The PR number links to the PR. When the branch has no PR, the band shows `PR none for <branch> · create`, where `create` opens a new PR for the branch. Outside a GitHub repository the band shows nothing.

It finds PRs whose head branch is in the repository itself, not in a fork.

## Prerequisites

The [GitHub CLI](https://cli.github.com/) (`gh`), signed in:

```bash
gh auth login
```

The mod calls `gh` and never sees your token.

## Commands

- `/gh-pr`: the PR's title, state, merge state, link, and a count of its check runs by result.
- `/gh-pr web`: opens the PR in the browser.

## When it refreshes

- When the session starts, and every 5 minutes while it runs interactively.
- When the directory changes, through `/cd` or a Bash `cd`.
- When you submit a prompt, if the directory changed or the last check is more than 60 seconds old.
- After a Bash command that can change the branch or the PR: `git checkout`, `switch`, `push`, `pull`, `merge`, `rebase`, `reset`, `commit`, `worktree`, or `gh pr`. After `git remote`, `init` or `clone`, it also reads the remote again.

## Which folders it checks

The mod checks a folder only when its `origin` remote is on a GitHub host: a host in gh's `hosts.yml`, `GH_HOST`, `github.com`, or any host whose name contains `github`. GitHub Enterprise Server counts once you sign in to it with `gh auth login`.

It reads the remote once per folder with `git remote get-url origin`, and gh's hosts file once per session. In any other folder it starts no process after that first read, so it costs nothing in a GitLab repository or outside git. Only `origin` counts, so a repository with remotes on both GitLab and GitHub shows one band.

## Request budget

Each check runs `git branch --show-current` and one REST call to list the branch's PRs. `gh api --cache` keeps that answer on disk for 60 seconds, so sessions on the same branch share it. The repository's owner and URL are read once per folder and cached for an hour. A check after a git or `gh pr` command skips the cache, so a new push or PR shows at once.

An active session spends at most about one request a minute; an idle one about 12 an hour, against GitHub's 5,000 an hour. `/gh-pr` adds two uncached calls: the PR itself and its check runs.

## Install

```
/plugin install handbook-github-pr --marketplace NikiforovAll/claude-code-rules
```
