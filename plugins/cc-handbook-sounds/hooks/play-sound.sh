#!/usr/bin/env bash
# shellcheck shell=bash
set -euo pipefail

# Check if hook is disabled via environment variable
if [ "${CC_HANDBOOK_SOUNDS_DISABLE_HOOKS:-false}" = "true" ]; then
    exit 0
fi

# Completion sound when Claude finishes responding
# Can be customized via CC_HANDBOOK_SOUNDS_FILE environment variable
sound_file="${CC_HANDBOOK_SOUNDS_FILE:-C:/Windows/Media/Windows Notify System Generic.wav}"

# Play sound using PowerShell with -NoProfile to avoid oh-my-posh conflicts
# Use -NonInteractive to prevent any prompts
# Run in background to not block Claude
powershell -NoProfile -NonInteractive -Command "(New-Object Media.SoundPlayer '$sound_file').PlaySync();" &

exit 0
