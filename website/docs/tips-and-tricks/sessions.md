---
title: "Manage Sessions"
sidebar_position: 2
---

Use `/rewind` to rewind a conversation. You will be prompted to select from recent sessions and then a point in the conversation history to rewind to. The code and context will be restored to that point.


⭐ Being able to rewind is very useful if you want to backtrack to a previous state, this is crucial feature to keep your context window clean in case something goes wrong.

* Use `/clear` to start a new session. Note, the context will be cleared and you will start a new session. Previous sessions are saved and can be resumed later.
* Use `/resume` to resume a conversation. You will be prompted to select from recent sessions.
* Use `/export` conversation to a file or clipboard.
* Use `/compact` to compact the context window.

---

From the command line, you can use `claude --resume` to resume to a session. Or `claude --continue` to continue the last session.