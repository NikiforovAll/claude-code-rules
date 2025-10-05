---
title: "Use ccusage"
sidebar_position: 17
---

# Use ccusage

[ccusage](https://github.com/ryoppippi/ccusage) - Track your Claude Code usage and costs.

## The Problem
Claude Code's Max plan offers unlimited usage, which is fantastic! But many users are curious:

- How much am I actually using Claude Code?
- Which conversations are the most expensive?
- What would I be paying on a pay-per-use plan?
- Am I getting good value from my subscription?

## The Solution
ccusage analyzes the local JSONL files that Claude Code automatically generates and provides:

- Detailed Usage Reports - Daily, monthly, and session-based breakdowns
- Cost Analysis - Estimated costs based on token usage and model pricing
- Live Monitoring - Real-time tracking of active sessions
- Multiple Formats - Beautiful tables or JSON for further analysis

## How It Works
- Claude Code generates JSONL files containing usage data
- ccusage reads these files from your local machine
- Analyzes and aggregates the data by date, session, or time blocks
- Calculates estimated costs using model pricing information
- Presents results in beautiful tables or JSON format