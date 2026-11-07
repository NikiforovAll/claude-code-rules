import importlib.util
import json
import unittest
import urllib.error
from io import BytesIO
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "scripts" / "generate_atlas.py"
SPEC = importlib.util.spec_from_file_location("generate_atlas", SCRIPT)
atlas = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(atlas)


class FakeResponse:
    def __init__(self, payload):
        self.body = BytesIO(json.dumps(payload).encode("utf-8"))

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.body.read()


class AtlasImageTests(unittest.TestCase):
    def test_generate_submits_once_then_polls(self):
        calls = []

        def fake_request(url, _api_key, **kwargs):
            calls.append((url, kwargs.get("method", "GET")))
            if url.endswith("/generateImage"):
                body = json.loads(kwargs["body"])
                self.assertEqual(body["model"], atlas.DEFAULT_MODEL)
                self.assertEqual(body["size"], "1024x1024")
                return {"id": "prediction/1", "status": "created"}
            return {
                "status": "completed",
                "outputs": ["https://cdn.example/image.png"],
            }

        with mock.patch.object(atlas, "request_json", side_effect=fake_request), mock.patch.object(
            atlas, "download_image", return_value=Path("tmp/output.png")
        ), mock.patch.object(atlas.time, "sleep"):
            output = atlas.generate_image("a lighthouse", "tmp/output.png", "test-key")

        self.assertEqual(output, Path("tmp/output.png"))
        self.assertEqual(
            calls,
            [
                (f"{atlas.API_BASE}/model/generateImage", "POST"),
                (f"{atlas.API_BASE}/model/prediction/prediction%2F1", "GET"),
            ],
        )

    def test_completed_submission_skips_polling(self):
        with mock.patch.object(
            atlas,
            "request_json",
            return_value={
                "status": "completed",
                "outputs": ["https://cdn.example/image.png"],
            },
        ) as request_json, mock.patch.object(
            atlas, "download_image", return_value=Path("tmp/output.png")
        ):
            atlas.generate_image("a lighthouse", "tmp/output.png", "test-key")

        self.assertEqual(request_json.call_count, 1)
        self.assertEqual(request_json.call_args.kwargs["method"], "POST")

    def test_decode_response_rejects_api_errors(self):
        with self.assertRaisesRegex(RuntimeError, "quota exceeded"):
            atlas._decode_response(
                FakeResponse({"code": 400, "message": "quota exceeded"})
            )

    def test_post_network_failure_is_not_retried(self):
        with mock.patch.object(
            atlas.urllib.request,
            "urlopen",
            side_effect=urllib.error.URLError("offline"),
        ) as urlopen, self.assertRaisesRegex(RuntimeError, "offline"):
            atlas.request_json(
                f"{atlas.API_BASE}/model/generateImage",
                "test-key",
                method="POST",
                body=b"{}",
                get_retries=2,
            )

        self.assertEqual(urlopen.call_count, 1)

    def test_prediction_get_retries_transient_network_failure(self):
        completed = FakeResponse(
            {"code": 200, "data": {"status": "completed", "outputs": []}}
        )
        with mock.patch.object(
            atlas.urllib.request,
            "urlopen",
            side_effect=[urllib.error.URLError("offline"), completed],
        ) as urlopen, mock.patch.object(atlas.time, "sleep") as sleep:
            result = atlas.request_json(
                f"{atlas.API_BASE}/model/prediction/test-id",
                "test-key",
                get_retries=2,
            )

        self.assertEqual(result["status"], "completed")
        self.assertEqual(urlopen.call_count, 2)
        sleep.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
