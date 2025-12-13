# Nano Banana Plugin

Python scripting and Gemini image generation using uv with inline script dependencies.

## Features

- **Image Generation**: Generate images using Google's Gemini models
- **Image Editing**: Edit existing images with AI
- **Python Scripting**: Run Python scripts with uv using heredocs
- **Inline Dependencies**: Self-contained scripts with `# /// script` metadata

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed
- `GOOGLE_API_KEY` environment variable set with a valid Gemini API key

## Usage

The skill activates when you ask Claude to generate images or run Python scripts. Example triggers:

- "Generate an image of..."
- "Create a picture..."
- "Draw..."
- "nano banana"

## Quick Example

```bash
uv run - << 'EOF'
# /// script
# dependencies = ["google-genai", "pillow"]
# ///
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=["A cute banana character"],
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE']
    )
)

for part in response.parts:
    if part.inline_data is not None:
        part.as_image().save("tmp/output.png")
        print("Saved: tmp/output.png")
EOF
```

## Installation

```bash
claude plugins add cc-handbook/handbook-nano-banana
```
