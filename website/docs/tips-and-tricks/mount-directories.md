---
title: "Mount Directories"
sidebar_position: 16
---

# Mount Directories

**Why**:

If you want to read external projects to get more context, instead of copying information manually from one agent to another, you can just mount multiple directories. 

Use `/add-dir` inside Claude Code or `--add-dir` when starting the agent.

```bash
claude --add-dir /path/to/project
```

> 💡 For example, let's say, you want to use some open-source project and it has recent code examples that you want to reference. By mounting the project directory, Claude Code can access the code directly and provide more relevant suggestions based on cloned project.

> 💡 Or, let's say you have an existing project template that you want to reuse. By mounting the template directory, Claude Code can help you adapt the code to your new project more easily.