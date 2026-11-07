#!/usr/bin/env python3
"""Generate an image with the optional Atlas Cloud provider."""

import argparse
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


API_BASE = "https://api.atlascloud.ai/api/v1"
DEFAULT_MODEL = "openai/gpt-image-2/text-to-image"
TRANSIENT_HTTP_CODES = {408, 429, 500, 502, 503, 504}


def _decode_response(response):
    payload = json.loads(response.read().decode("utf-8"))
    if payload.get("code") not in (None, 0, 200):
        message = payload.get("message") or payload.get("msg") or "unknown error"
        raise RuntimeError(f"Atlas Cloud API error: {message}")
    data = payload.get("data", payload)
    if not isinstance(data, dict):
        raise RuntimeError("Atlas Cloud returned an unexpected response")
    return data


def request_json(url, api_key, *, method="GET", body=None, get_retries=0):
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    if body is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=body, headers=headers, method=method)

    for attempt in range(get_retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return _decode_response(response)
        except urllib.error.HTTPError as exc:
            can_retry = method == "GET" and exc.code in TRANSIENT_HTTP_CODES
            if not can_retry or attempt == get_retries:
                raise RuntimeError(
                    f"Atlas Cloud request failed with HTTP {exc.code}"
                ) from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            if method != "GET" or attempt == get_retries:
                raise RuntimeError(f"Atlas Cloud request failed: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError("Atlas Cloud returned invalid JSON") from exc
        time.sleep(2**attempt)

    raise RuntimeError("Atlas Cloud request failed")


def _output_url(data):
    outputs = data.get("outputs")
    if isinstance(outputs, list) and outputs and isinstance(outputs[0], str):
        return outputs[0]
    output = data.get("output")
    return output if isinstance(output, str) else None


def download_image(url, output_path):
    if not url.startswith("https://"):
        raise RuntimeError("Atlas Cloud returned a non-HTTPS output URL")
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            destination.write_bytes(response.read())
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise RuntimeError(f"Unable to download generated image: {exc}") from exc
    return destination


def generate_image(
    prompt,
    output_path,
    api_key,
    *,
    model=DEFAULT_MODEL,
    size="1024x1024",
    quality="medium",
    output_format="png",
    poll_interval=3,
    max_polls=60,
):
    body = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "output_format": output_format,
        }
    ).encode("utf-8")

    # Generation requests may be billable, so the POST is intentionally sent once.
    submitted = request_json(
        f"{API_BASE}/model/generateImage",
        api_key,
        method="POST",
        body=body,
    )
    immediate_url = _output_url(submitted)
    if submitted.get("status") in {"completed", "succeeded"} and immediate_url:
        return download_image(immediate_url, output_path)

    prediction_id = submitted.get("id")
    if not isinstance(prediction_id, str) or not prediction_id:
        raise RuntimeError("Atlas Cloud response did not include a prediction id")

    prediction_id = urllib.parse.quote(prediction_id, safe="")
    for _ in range(max_polls):
        time.sleep(poll_interval)
        result = request_json(
            f"{API_BASE}/model/prediction/{prediction_id}",
            api_key,
            get_retries=2,
        )
        result_url = _output_url(result)
        if result.get("status") in {"completed", "succeeded"}:
            if not result_url:
                raise RuntimeError("Atlas Cloud completed without an output URL")
            return download_image(result_url, output_path)
        if result.get("status") in {"failed", "canceled", "cancelled"}:
            message = result.get("error") or result.get("message") or "unknown error"
            raise RuntimeError(f"Atlas Cloud generation failed: {message}")

    raise RuntimeError("Atlas Cloud generation timed out while polling")


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt")
    prompt_group.add_argument("--prompt-file", type=Path)
    parser.add_argument("--output", type=Path, default=Path("tmp/output.png"))
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument(
        "--size",
        default="1024x1024",
        choices=(
            "1024x1024",
            "1024x768",
            "768x1024",
            "1024x1536",
            "1536x1024",
            "2048x2048",
            "2048x1152",
            "1152x2048",
            "2560x1088",
            "1088x2560",
            "2880x2160",
            "2160x2880",
            "3840x2160",
            "2160x3840",
        ),
    )
    parser.add_argument("--quality", choices=("low", "medium", "high"), default="medium")
    parser.add_argument("--format", choices=("jpeg", "png"), default="png")
    return parser.parse_args()


def main():
    args = parse_args()
    api_key = os.environ.get("ATLASCLOUD_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("ATLASCLOUD_API_KEY is required")
    prompt = args.prompt
    if args.prompt_file:
        prompt = args.prompt_file.read_text(encoding="utf-8").strip()
    if not prompt or not prompt.strip():
        raise SystemExit("prompt must not be empty")

    output = generate_image(
        prompt.strip(),
        args.output,
        api_key,
        model=args.model,
        size=args.size,
        quality=args.quality,
        output_format=args.format,
    )
    print(output)


if __name__ == "__main__":
    main()
