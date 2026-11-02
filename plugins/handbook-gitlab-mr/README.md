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

- When the session starts, and every 5 minutes while it runs interactively.
- When the directory changes, through `/cd` or a Bash `cd`.
- When you submit a prompt, if the directory changed or the last check is more than 60 seconds old.
- After a Bash command that can change the branch or the MR: `git checkout`, `switch`, `push`, `pull`, `merge`, `rebase`, `reset`, `commit`, `worktree`, or `glab mr`. After `git remote`, `init` or `clone`, it also reads the remote again.

## Which folders it checks

The mod checks a folder only when its `origin` remote is on a GitLab host: a host in the `hosts:` list of glab's `config.yml`, `GITLAB_HOST`, `gitlab.com`, or any host whose name contains `gitlab`. Self-hosted GitLab, such as `git.epam.com`, counts once you sign in to it with `glab auth login`.

It reads the remote once per folder with `git remote get-url origin`, and glab's config file once per session. In any other folder it starts no process after that first read, so it costs nothing in a GitHub repository or outside git. Only `origin` counts, so a repository with remotes on both GitLab and GitHub shows one band.

Each check runs `git branch --show-current` and one `glab mr list` call. A branch with no MR also makes one `glab repo view` call, once per folder.

## Install

```
/plugin install handbook-gitlab-mr --marketplace NikiforovAll/claude-code-rules
```
