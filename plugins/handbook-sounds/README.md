# Handbook Sounds

Audio feedback for Claude Code events on Windows using PowerShell sounds.

## Features

- Plays system sound when Claude finishes responding
- Windows native via PowerShell
- Git Bash compatible (uses `-NoProfile` flag)
- Non-blocking background playback

## Requirements

- Windows OS with PowerShell

## Installation

```bash
/plugin marketplace add nikiforovall/claude-code-rules
/plugin install handbook-sounds
```

## Configuration

**Disable sounds:**
```bash
export CC_HANDBOOK_SOUNDS_DISABLE_HOOKS=true
```

**Customize sound:**
```bash
export CC_HANDBOOK_SOUNDS_FILE="C:/Windows/Media/Windows Ding.wav"
```

Available Windows system sounds:
- `C:/Windows/Media/Windows Notify System Generic.wav` (default)
- `C:/Windows/Media/Windows Ding.wav`
- `C:/Windows/Media/Windows Error.wav`
