<!-- vscode-markdown-toc -->
* 1. [Mount Multiple Directories](#MountMultipleDirectories)
* 2. [Use `git worktree` for parallel development](#Usegitworktreeforparalleldevelopment)
* 3. [Use `git commit` as checkpoints, commit frequently](#Usegitcommitascheckpointscommitfrequently)
* 4. [Run bash tasks in the background](#Runbashtasksinthebackground)
* 5. [Input images](#Inputimages)
* 6. [Use voice control to interact with Claude Code](#UsevoicecontroltointeractwithClaudeCode)
* 7. [Use `#` to add things to the project memory](#Usetoaddthingstotheprojectmemory)
* 8. [Learn how to Configure and Customize](#LearnhowtoConfigureandCustomize)
* 9. [Connect to IDE](#ConnecttoIDE)
* 10. [List Claude Code Tools](#ListClaudeCodeTools)
* 11. [You can use YOLO mode `--dangerously-skip-permissions`](#YoucanuseYOLOmode--dangerously-skip-permissions)
* 12. [Use `/resume` to resume a conversation](#Useresumetoresumeaconversation)
* 13. [Use `! bash` mode to run bash commands without leaving Claude Code](#UsebashmodetorunbashcommandswithoutleavingClaudeCode)
* 14. [Organize your Prompts into Prompt Libraries (Personal, Project, Organization levels)](#OrganizeyourPromptsintoPromptLibrariesPersonalProjectOrganizationlevels)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=false
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

# Tips & Tricks 

This is a collection of tips and tricks for using Claude Code.

##  1. <a name='MountMultipleDirectories'></a>Mount Multiple Directories

**Why**: Assume you want to be able to read external project to get context, instead of copying information manually from one agent to another. You can just mount multiple directories.

##  2. <a name='Usegitworktreeforparalleldevelopment'></a>Use `git worktree` for parallel development

You can use `git worktree` to create multiple working directories for the same repository. This is useful for parallel development, e.g., working on multiple features or bug fixes simultaneously without needing to switch branches in a single working directory.

##  3. <a name='Usegitcommitascheckpointscommitfrequently'></a>Use `git commit` as checkpoints, commit frequently

Git Commits are free 😅 so please commit often and use meaningful commit messages. This will help you keep track of changes and make it easier to revert back if needed.
You can use the `/commit` ([git commit](./.claude/commands/dev-workflow/commit.md)) command to automate commit creation. This command will do a commit for you.

##  4. <a name='Runbashtasksinthebackground'></a>Run bash tasks in the background

You can nudge Claude to run bash tasks in the background. For example, you have some long-running tasks and you want claude to see the tasks's output.

##  5. <a name='Inputimages'></a>Input images

Claude is multi-modal and you can input images by pressing `alt + v`

##  6. <a name='UsevoicecontroltointeractwithClaudeCode'></a>Use voice control to interact with Claude Code

You can use voice control to interact with Claude Code. Especially useful for ideation and brainstorming sessions.

##  7. <a name='Usetoaddthingstotheprojectmemory'></a>Use `#` to add things to the project memory

This is just a shortcut to now leave the conversation and edit the `./CLAUDE.md` file manually. You can just use `#` to add things to the project memory.

##  8. <a name='LearnhowtoConfigureandCustomize'></a>Learn how to Configure and Customize

* Settings
* Permissions
* MCP Configuration
* Custom Slash Commands
* Sub-Agents
* Output Prompts
* Hooks

##  9. <a name='ConnecttoIDE'></a>Connect to IDE

You can connect to VSCode or JetBrains IDEs to get context for files and diagnostics.

##  10. <a name='ListClaudeCodeTools'></a>List Claude Code Tools

Claude Code in a way is self-aware of its capabilities. You can ask it to list available tools. See [`/tools`](./.claude/commands/tools.md) command.

##  11. <a name='YoucanuseYOLOmode--dangerously-skip-permissions'></a>You can use YOLO mode `--dangerously-skip-permissions`

##  12. <a name='Useresumetoresumeaconversation'></a>Use `/resume` to resume a conversation

Also `/export` conversation to a file or clipboard.

##  13. <a name='UsebashmodetorunbashcommandswithoutleavingClaudeCode'></a>Use `! bash` mode to run bash commands without leaving Claude Code

The benefit of this approach is that Claude Code is actually aware of what you are doing in bash and can adjust its behavior accordingly.

##  14. <a name='OrganizeyourPromptsintoPromptLibrariesPersonalProjectOrganizationlevels'></a>Organize your Prompts into Prompt Libraries (Personal, Project, Organization levels)

You can create prompt libraries to organize your prompts. You can have personal, project, and organization level prompt libraries. 