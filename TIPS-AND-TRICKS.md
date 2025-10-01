<!-- vscode-markdown-toc -->
* 1. [Learn Shell Keyboard Shortcuts for Text Editing](#LearnShellKeyboardShortcutsforTextEditing)
* 2. [Navigation](#Navigation)
* 3. [Editing](#Editing)
* 4. [History](#History)
* 5. [Control](#Control)
* 6. [Mount Multiple Directories](#MountMultipleDirectories)
* 7. [Use `git worktree` for parallel development](#Usegitworktreeforparalleldevelopment)
* 8. [Use `git commit` as checkpoints, commit frequently](#Usegitcommitascheckpointscommitfrequently)
* 9. [Run bash tasks in the background](#Runbashtasksinthebackground)
* 10. [Input images](#Inputimages)
* 11. [Use voice control to interact with Claude Code](#UsevoicecontroltointeractwithClaudeCode)
* 12. [Use `#` to add things to the project memory](#Usetoaddthingstotheprojectmemory)
* 13. [Learn how to Configure and Customize](#LearnhowtoConfigureandCustomize)
* 14. [Connect to IDE](#ConnecttoIDE)
* 15. [List Claude Code Tools](#ListClaudeCodeTools)
* 16. [You can use YOLO mode `--dangerously-skip-permissions`](#YoucanuseYOLOmode--dangerously-skip-permissions)
* 17. [Use `/resume` to resume a conversation](#Useresumetoresumeaconversation)
* 18. [Use `/rewind` to rewind a conversation](#Userewindtorewindaconversation)
* 19. [Use `! bash` mode to run bash commands without leaving Claude Code](#UsebashmodetorunbashcommandswithoutleavingClaudeCode)
* 20. [Organize your Prompts into Prompt Libraries (Personal, Project, Organization levels)](#OrganizeyourPromptsintoPromptLibrariesPersonalProjectOrganizationlevels)
* 21. [Use TaskMaster](#UseTaskMaster)
* 22. [Use Claude Code Docs](#UseClaudeCodeDocs)
* 23. [Use CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR](#UseCLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR)
* 24. [Use ccusage](#Useccusage)
* 25. [Use ccstatusline](#Useccstatusline)
* 26. [Use ccoutputstyles](#Useccoutputstyles)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=false
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

# Tips & Tricks 

This is a collection of tips and tricks for using Claude Code.

##  1. <a name='LearnShellKeyboardShortcutsforTextEditing'></a>Learn Shell Keyboard Shortcuts for Text Editing

##  2. <a name='Navigation'></a>Navigation
| Key | Action |
|-----|--------|
| `Ctrl+A` | Beginning of line |
| `Ctrl+E` | End of line |

##  3. <a name='Editing'></a>Editing
| Key | Action |
|-----|--------|
| `Ctrl+W` | Delete word |
| `Ctrl+U` | Delete line |
| `Ctrl+K` | Delete to end |
| `Ctrl+_` | Undo |

##  4. <a name='History'></a>History
| Key | Action |
|-----|--------|
| `↑/↓` | Previous/Next command |

##  5. <a name='Control'></a>Control
| Key | Action |
|-----|--------|
| `Ctrl+C` | Kill process |
| `Ctrl+L` | Clear screen |
| `Tab` | Auto-complete |

##  6. <a name='MountMultipleDirectories'></a>Mount Multiple Directories

**Why**: Assume you want to be able to read external project to get context, instead of copying information manually from one agent to another. You can just mount multiple directories.

##  7. <a name='Usegitworktreeforparalleldevelopment'></a>Use `git worktree` for parallel development

You can use `git worktree` to create multiple working directories for the same repository. This is useful for parallel development, e.g., working on multiple features or bug fixes simultaneously without needing to switch branches in a single working directory.

##  8. <a name='Usegitcommitascheckpointscommitfrequently'></a>Use `git commit` as checkpoints, commit frequently

Git Commits are free 😅 so please commit often and use meaningful commit messages. This will help you keep track of changes and make it easier to revert back if needed.
You can use the `/commit` ([git commit](./.claude/commands/dev-workflow/commit.md)) command to automate commit creation. This command will do a commit for you.

##  9. <a name='Runbashtasksinthebackground'></a>Run bash tasks in the background

You can nudge Claude to run bash tasks in the background. For example, you have some long-running tasks and you want claude to see the tasks's output.

##  10. <a name='Inputimages'></a>Input images

Claude is multi-modal and you can input images by pressing `alt + v`

##  11. <a name='UsevoicecontroltointeractwithClaudeCode'></a>Use voice control to interact with Claude Code

You can use voice control to interact with Claude Code. Especially useful for ideation and brainstorming sessions.

##  12. <a name='Usetoaddthingstotheprojectmemory'></a>Use `#` to add things to the project memory

This is just a shortcut to now leave the conversation and edit the `./CLAUDE.md` file manually. You can just use `#` to add things to the project memory.

##  13. <a name='LearnhowtoConfigureandCustomize'></a>Learn how to Configure and Customize

* Settings
* Permissions
* MCP Configuration
* Custom Slash Commands
* Sub-Agents
* Output Prompts
* Hooks

##  14. <a name='ConnecttoIDE'></a>Connect to IDE

You can connect to VSCode or JetBrains IDEs to get context for files and diagnostics.

##  15. <a name='ListClaudeCodeTools'></a>List Claude Code Tools

Claude Code in a way is self-aware of its capabilities. You can ask it to list available tools. See [`/tools`](./.claude/commands/tools.md) command.

##  16. <a name='YoucanuseYOLOmode--dangerously-skip-permissions'></a>You can use YOLO mode `--dangerously-skip-permissions`

##  17. <a name='Useresumetoresumeaconversation'></a>Use `/resume` to resume a conversation

Also `/export` conversation to a file or clipboard.

##  18. <a name='Userewindtorewindaconversation'></a>Use `/rewind` to rewind a conversation

##  19. <a name='UsebashmodetorunbashcommandswithoutleavingClaudeCode'></a>Use `! bash` mode to run bash commands without leaving Claude Code

The benefit of this approach is that Claude Code is actually aware of what you are doing in bash and can adjust its behavior accordingly.

##  20. <a name='OrganizeyourPromptsintoPromptLibrariesPersonalProjectOrganizationlevels'></a>Organize your Prompts into Prompt Libraries (Personal, Project, Organization levels)

You can create prompt libraries to organize your prompts. You can have personal, project, and organization level prompt libraries. 

##  21. <a name='UseTaskMaster'></a>Use TaskMaster

https://www.task-master.dev/

##  22. <a name='UseClaudeCodeDocs'></a>Use Claude Code Docs

<https://github.com/ericbuess/claude-code-docs>

##  23. <a name='UseCLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR'></a>Use CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR

You may have noticed that Claude gets really confused about its current directory after doing that.

The problem is that cd changes the current working directory permanently (for the rest of the session). So any steps after that will also use the new CWD. Which Claude does not expect.

Anyway they recently added a flag to change this:

```bash
export CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1
```

##  24. <a name='Useccusage'></a>Use ccusage

https://ccusage.com/guide/

##  25. <a name='Useccstatusline'></a>Use ccstatusline

https://github.com/sirmalloc/ccstatusline

##  26. <a name='Useccoutputstyles'></a>Use ccoutputstyles

https://github.com/viveknair/ccoutputstyles