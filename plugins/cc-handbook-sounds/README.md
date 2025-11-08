# handbook-sounds

Audio feedback plugin for Claude Code that plays system sounds on Windows when Claude finishes responding.

## Overview

This plugin provides audio feedback when Claude finishes responding using Windows system sounds via PowerShell. Get auditory confirmation when Claude completes a response.

## Features

- **Completion Notification**: Plays a sound when Claude finishes responding
- **Windows Native**: Uses Windows Media system sounds via PowerShell
- **Git Bash Compatible**: Works in git bash environment by using PowerShell `-NoProfile` flag
- **Non-blocking**: Sounds play in the background without interrupting your workflow

## Requirements

- Windows OS
- PowerShell (included with Windows)
- Git Bash (for git bash environment support)

## Installation

Install via Claude Code marketplace:

```bash
# Install from marketplace
claude code plugin install handbook-sounds
```

Or manually by cloning the repository and linking the plugin.

## Configuration

### Disabling Sounds

To disable sounds without uninstalling the plugin:

```bash
export CC_HANDBOOK_SOUNDS_DISABLE_HOOKS=true
```

Add to your `.bashrc` or `.zshrc` to make it permanent.

### Customizing Sounds

By default, the plugin uses `C:/Windows/Media/Windows Notify System Generic.wav`.

To customize, set the `CC_HANDBOOK_SOUNDS_FILE` environment variable:

```bash
# Use a different Windows system sound
export CC_HANDBOOK_SOUNDS_FILE="C:/Windows/Media/Windows Ding.wav"

# Or use a custom WAV file
export CC_HANDBOOK_SOUNDS_FILE="C:/path/to/your/custom-sound.wav"
```

Add to your `.bashrc` or `.zshrc` to make it permanent.

Available Windows system sounds include:
- `C:/Windows/Media/Windows Notify System Generic.wav` - Generic notification (default)
- `C:/Windows/Media/Windows Notify Messaging.wav` - Message notification
- `C:/Windows/Media/Windows Error.wav` - Error sound
- `C:/Windows/Media/Windows Ding.wav` - Simple ding
- `C:/Windows/Media/notify.wav` - Simple notification

## How It Works

The plugin uses a `Stop` hook that:

1. Triggers when Claude finishes generating a response
2. Plays a notification sound using PowerShell's `Media.SoundPlayer` class
3. Runs in the background to avoid blocking your workflow

The PowerShell command used:
```bash
powershell -NoProfile -NonInteractive -Command "(New-Object Media.SoundPlayer '<sound-file>').PlaySync();"
```

The `-NoProfile` flag ensures compatibility with git bash by skipping PowerShell profile loading (avoiding oh-my-posh conflicts).

## Troubleshooting

### No sound plays

1. Check that your Windows volume is not muted
2. Verify the sound files exist at the specified paths
3. Ensure PowerShell is available in your PATH

### "oh-my-posh" errors

This plugin uses `-NoProfile` flag to prevent PowerShell profile conflicts. If you still see errors, the hook may be running with a cached PowerShell session.

### Sounds are too loud/quiet

Adjust your Windows system volume or notification volume in Windows Settings > System > Sound.

## License

MIT
