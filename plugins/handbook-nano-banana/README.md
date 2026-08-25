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

Atlas Cloud is also available as an optional provider. Export `ATLASCLOUD_API_KEY` and use the bundled `skills/nano-banana/scripts/generate_atlas.py` helper when Atlas is explicitly selected; the Gemini workflow remains the default.

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

### Atlas Cloud (optional)

```bash
export ATLASCLOUD_API_KEY="your-api-key"
uv run skills/nano-banana/scripts/generate_atlas.py \
  --prompt "A cute banana character" \
  --output tmp/output.png
```

The helper uses Atlas Cloud's asynchronous image API and defaults to `openai/gpt-image-2/text-to-image`. Generation submissions are sent once; only prediction checks use bounded retries.

## Installation

```bash
claude plugins add cc-handbook/handbook-nano-banana
```

## Resources
- [Official Prompting Guide](https://blog.google/products/gemini/prompting-tips-nano-banana-pro/) - Learn how to structure your prompts effectively.
- [How to prompt Nano Banana Pro](https://www.fofr.ai/nano-banana-pro-guide)
