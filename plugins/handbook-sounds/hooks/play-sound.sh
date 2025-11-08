#!/usr/bin/env bash
# shellcheck shell=bash
set -euo pipefail

# Check if hook is disabled via environment variable
if [ "${CC_HANDBOOK_SOUNDS_DISABLE_HOOKS:-false}" = "true" ]; then
    exit 0
fi

# Parse hook type argument
hook_type="${1:-stop}"

# Select sound file based on hook type
if [ "$hook_type" = "--stop" ]; then
    sound_file="${CC_HANDBOOK_STOP_SOUNDS_FILE:-C:/Windows/Media/notify.wav}"
elif [ "$hook_type" = "--notification" ]; then
    sound_file="${CC_HANDBOOK_NOTIFICATION_SOUNDS_FILE:-C:/Windows/Media/Windows Exclamation.wav}"
else
    # Fallback for backward compatibility
    sound_file="${CC_HANDBOOK_SOUNDS_FILE:-C:/Windows/Media/notify.wav}"
fi

# Play sound using PowerShell with -NoProfile to avoid oh-my-posh conflicts
# Use -NonInteractive to prevent any prompts
# Run in background to not block Claude
powershell -NoProfile -NonInteractive -Command "(New-Object Media.SoundPlayer '$sound_file').PlaySync();" &

exit 0
