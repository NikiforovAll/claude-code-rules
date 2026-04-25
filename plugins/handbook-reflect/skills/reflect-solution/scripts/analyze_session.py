#!/usr/bin/env python3
"""Compress a Claude Code session JSONL into an agent-readable transcript.

Usage: python analyze_session.py <path-to-jsonl>

Prints a markdown transcript to stdout. The agent reads this transcript and
performs the wrong-turn analysis itself — this script does NOT classify
incidents. Its job is to strip system noise, preserve real user input,
collapse tool calls/results to one-liners, and expand compaction summaries
so embedded user quotes are not lost.

Design notes:
- User messages are preserved verbatim (truncated only if huge).
- System-reminder / command-stdout / boilerplate envelopes are stripped.
- Compaction summaries are kept but flagged; embedded user quotes surfaced.
- Assistant text kept; assistant tool_use collapsed to `→ Tool(args…)`.
- Tool results collapsed to a single line, with [ERR] / [REJECTED] markers.
- Output is grouped by turn with absolute turn numbers (T1, T2, …).
"""
import json
import re
import sys
from pathlib import Path


REJECTION_MARKERS = (
    "doesn't want to proceed",
    "tool use was rejected",
    "request interrupted by user",
    "stop what you are doing",
)

BOILERPLATE_PREFIXES = (
    "caveat: the messages below",
    "<command-name>",
    "<command-message>",
    "<command-args>",
    "<local-command-stdout>",
    "<local-command-stderr>",
)


def load_events(path):
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def squash(s, n=None):
    s = re.sub(r"\s+", " ", s).strip()
    if n and len(s) > n:
        return s[:n] + "…"
    return s


def strip_system_reminders(text):
    """Remove <system-reminder>…</system-reminder> blocks and similar wrappers."""
    text = re.sub(r"<system-reminder>.*?</system-reminder>", "", text, flags=re.S | re.I)
    text = re.sub(r"<command-name>.*?</command-name>", "", text, flags=re.S | re.I)
    text = re.sub(r"<command-message>.*?</command-message>", "", text, flags=re.S | re.I)
    text = re.sub(r"<command-args>.*?</command-args>", "", text, flags=re.S | re.I)
    text = re.sub(r"<local-command-stdout>.*?</local-command-stdout>", "", text, flags=re.S | re.I)
    text = re.sub(r"<local-command-stderr>.*?</local-command-stderr>", "", text, flags=re.S | re.I)
    text = re.sub(r"<user-prompt-submit-hook>.*?</user-prompt-submit-hook>", "", text, flags=re.S | re.I)
    return text.strip()


def is_pure_boilerplate(text):
    low = text.strip().lower()
    if not low:
        return True
    return any(low.startswith(p) for p in BOILERPLATE_PREFIXES)


def is_compaction(text):
    low = text.strip().lower()
    return (
        low.startswith("this session is being continued")
        or "summary:" in low[:500] and "previous conversation" in low[:500]
    )


def extract_compaction_quotes(text):
    """Pull embedded user-quoted strings from a compaction summary."""
    quotes = []
    for m in re.finditer(r'(?:user(?:\s+said|\s+asked|:|\s+message)?\s*[":]\s*"([^"]{5,400})")', text, re.I):
        quotes.append(m.group(1))
    for m in re.finditer(r'^\s*[-*\d.]+\s*[`"]([^"`]{5,400})[`"]\s*$', text, re.M):
        quotes.append(m.group(1))
    # Dedup, preserve order
    seen, out = set(), []
    for q in quotes:
        k = q.strip().lower()
        if k not in seen:
            seen.add(k)
            out.append(q.strip())
    return out


def summarize_tool_input(name, inp):
    """One-line summary of a tool call's salient args."""
    if not isinstance(inp, dict):
        return ""
    keys = ["file_path", "path", "command", "pattern", "url", "prompt", "description", "query"]
    parts = []
    for k in keys:
        if k in inp and inp[k]:
            v = str(inp[k])
            parts.append(f"{k}={squash(v, 120)}")
            if len(parts) >= 2:
                break
    if not parts:
        # Fallback: dump first ~120 chars of the whole input
        try:
            parts.append(squash(json.dumps(inp, ensure_ascii=False), 120))
        except Exception:
            parts.append("?")
    return ", ".join(parts)


def render_tool_result(tr):
    body = tr.get("content", "")
    if isinstance(body, list):
        body = " ".join(
            x.get("text", "") if isinstance(x, dict) else str(x) for x in body
        )
    body = str(body)
    low = body.lower()
    if any(m in low for m in REJECTION_MARKERS):
        return f"  ← [REJECTED] {squash(body, 160)}"
    if tr.get("is_error"):
        return f"  ← [ERR] {squash(body, 160)}"
    return f"  ← {squash(body, 120)}"


def render_assistant_text(text):
    text = strip_system_reminders(text).strip()
    if not text:
        return ""
    # Collapse internal whitespace lightly but keep paragraph structure for readability.
    lines = [l.rstrip() for l in text.splitlines()]
    lines = [l for l in lines if l.strip()]
    joined = "\n".join(lines)
    return squash(joined, 600)


def compress(events):
    # Meta
    cwd = ""
    session_id = ""
    for ev in events:
        if not cwd and ev.get("cwd"):
            cwd = ev.get("cwd", "")
        if not session_id and ev.get("sessionId"):
            session_id = ev.get("sessionId", "")
        if cwd and session_id:
            break

    lines = []
    lines.append(f"# Session transcript (compressed)")
    lines.append(f"")
    lines.append(f"- session: `{session_id}`")
    lines.append(f"- cwd: `{cwd}`")
    lines.append(f"- events: {len(events)}")
    lines.append(f"")
    lines.append(f"Legend: `→` assistant tool call · `←` tool result · `[ERR]` failed · `[REJECTED]` user blocked it · `[COMPACTED]` auto-summary block · `[INTERRUPT]` user interrupted")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    turn = 0
    first_user_goal = None
    user_count = 0
    rejection_count = 0
    interrupt_count = 0
    compaction_count = 0

    for ev in events:
        t = ev.get("type")
        msg = ev.get("message", {}) or {}
        content = msg.get("content")

        if t == "user":
            turn += 1
            # Distinguish: tool_result-only message vs real user text
            if isinstance(content, list) and content and all(
                isinstance(b, dict) and b.get("type") == "tool_result" for b in content
            ):
                for tr in content:
                    line = render_tool_result(tr)
                    if "[REJECTED]" in line:
                        rejection_count += 1
                    if "[INTERRUPT" in line.upper() or "interrupted by user" in line.lower():
                        interrupt_count += 1
                    lines.append(line)
                continue

            # Real user message (string or list with text blocks)
            if isinstance(content, str):
                raw = content
            elif isinstance(content, list):
                raw = "\n".join(
                    b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"
                )
            else:
                raw = ""

            cleaned = strip_system_reminders(raw)

            if not cleaned or is_pure_boilerplate(cleaned):
                continue

            if is_compaction(cleaned):
                compaction_count += 1
                quotes = extract_compaction_quotes(cleaned)
                lines.append(f"## T{turn} · USER [COMPACTED]")
                lines.append(f"")
                lines.append(f"_(auto-summary block — embedded user quotes extracted below)_")
                if quotes:
                    lines.append(f"")
                    for q in quotes[:25]:
                        lines.append(f"- > {squash(q, 280)}")
                lines.append(f"")
                continue

            user_count += 1
            if first_user_goal is None:
                first_user_goal = squash(cleaned, 300)

            lines.append(f"## T{turn} · USER")
            lines.append(f"")
            lines.append(squash(cleaned, 1200))
            lines.append(f"")

        elif t == "assistant":
            turn += 1
            if not isinstance(content, list):
                continue
            text_blocks = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
            tool_uses = [b for b in content if isinstance(b, dict) and b.get("type") == "tool_use"]

            text = "\n".join(text_blocks).strip()
            rendered_text = render_assistant_text(text) if text else ""

            if not rendered_text and not tool_uses:
                continue

            header = f"## T{turn} · ASSISTANT"
            lines.append(header)
            if rendered_text:
                lines.append(f"")
                lines.append(rendered_text)
            for tu in tool_uses:
                name = tu.get("name", "?")
                args = summarize_tool_input(name, tu.get("input", {}))
                lines.append(f"")
                lines.append(f"→ {name}({args})")
            lines.append(f"")

    # Trailer with cheap structural summary (no classification — just counts)
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Structural summary")
    lines.append(f"")
    lines.append(f"- real user turns (after stripping system reminders): {user_count}")
    lines.append(f"- compaction blocks: {compaction_count}")
    lines.append(f"- tool rejections: {rejection_count}")
    lines.append(f"- explicit interrupts: {interrupt_count}")
    if first_user_goal:
        lines.append(f"- first user goal: {first_user_goal}")
    lines.append(f"")
    lines.append(f"_Analyze this transcript yourself: identify wrong-turn moments (corrections, retries, reversals, dead-ends, drift) by reading the user/assistant flow. Do not rely on counts alone._")
    lines.append(f"")
    lines.append(f"_This transcript is **lossy by design** — tool args, results, and long user messages are truncated. When an incident hinges on detail not visible here (exact rejected input, full error body, diff content), read the source JSONL directly with `Read` (scoped via `offset`/`limit`). The compressed view is an index; the JSONL is the source of truth._")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("usage: analyze_session.py <jsonl>", file=sys.stderr)
        sys.exit(2)
    path = Path(sys.argv[1])
    events = load_events(path)
    sys.stdout.write(compress(events))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
