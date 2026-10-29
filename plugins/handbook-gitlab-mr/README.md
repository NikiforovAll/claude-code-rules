# handbook-gitlab-mr

A Claude Code mod that shows the GitLab merge request of the session's current branch in a band above the prompt, right-aligned: `MR !1436 opened → develop`. The MR number links to the MR. When an open MR cannot merge yet, the band adds the reason, for example `· need rebase`. When the branch has no MR, the band shows `MR none for <branch> · create`, where `create` opens a new MR for the branch. Outside a GitLab repository the band shows nothing.

## Prerequisites

The [GitLab CLI](https://gitlab.com/gitlab-org/cli#installation) (`glab`), signed in to your GitLab host:

```bash
glab auth login --hostname <your GitLab host>
```

The mod calls `glab` and never sees your token.

## Commands

- `/mr`: the MR's title, state, merge status, link, and the link of its latest pipeline.
- `/mr web`: opens the MR in the browser.

## When it refreshes

- When the session starts, and every 60 seconds while it runs interactively.
- After `/cd`.
- After a Bash command that can change the branch or the MR: `git checkout`, `switch`, `push`, `pull`, `merge`, `rebase`, `reset`, `commit`, `worktree`, or `glab mr`.

In a folder that `glab` does not know, the timer stops checking until one of the other events happens.

Each check runs `git branch --show-current` and one `glab mr list` call. A branch with no MR also makes one `glab repo view` call, once per folder.

## Install

```
/plugin install handbook-gitlab-mr --marketplace NikiforovAll/claude-code-rules
```
