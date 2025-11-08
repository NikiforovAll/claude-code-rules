# Handbook Sounds

Audio feedback for Claude Code events on Windows using PowerShell sounds.

## Features

- Plays system sound when Claude finishes responding (Stop hook)
- Plays system sound on notifications (permission requests, idle timeout)
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

**Customize sounds:**

Stop hook (when Claude finishes responding):
```bash
export CC_HANDBOOK_STOP_SOUNDS_FILE="C:/Windows/Media/notify.wav"
```

Notification hook (permission requests, idle timeout):
```bash
export CC_HANDBOOK_NOTIFICATION_SOUNDS_FILE="C:/Windows/Media/Windows Exclamation.wav"
```

Available Windows system sounds:
- `C:/Windows/Media/notify.wav` (default for Stop)
- `C:/Windows/Media/Windows Exclamation.wav` (default for Notification)
- `C:/Windows/Media/Windows Notify System Generic.wav`
- `C:/Windows/Media/Windows Ding.wav`
- `C:/Windows/Media/Windows Error.wav`
