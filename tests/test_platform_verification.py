import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch


class JsonResponse:
    def __init__(self, value: object) -> None:
        self.stream = BytesIO(json.dumps(value).encode("utf-8"))

    def __enter__(self) -> BytesIO:
        return self.stream

    def __exit__(self, *args: object) -> None:
        self.stream.close()


class PlatformVerificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(__file__).resolve().parent.parent

    def load_electron_doctor(self) -> object:
        path = self.root / "skills" / "verify-electron-apps" / "scripts" / "electron_cdp_doctor.py"
        specification = importlib.util.spec_from_file_location("electron_cdp_doctor", path)
        assert specification and specification.loader
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
        return module

    def test_apple_doctor_returns_machine_readable_readiness(self) -> None:
        script = self.root / "skills" / "verify-apple-apps" / "scripts" / "apple_verification_doctor.py"
        result = subprocess.run(
            [sys.executable, str(script), "--platform", "macos"],
            check=False,
            capture_output=True,
            text=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(report["platform"], "macos")
        self.assertIn("xcodebuild", report["tools"])
        self.assertIsInstance(report["ready"], bool)
        self.assertIn(result.returncode, (0, 1))

    def test_apple_doctor_requires_simulator_service(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tools = Path(directory)
            xcodebuild = tools / "xcodebuild"
            xcrun = tools / "xcrun"
            xcodebuild.write_text("#!/bin/sh\nprintf 'Xcode test\\n'\n", encoding="utf-8")
            xcrun.write_text("#!/bin/sh\nprintf 'simulator unavailable\\n' >&2\nexit 1\n", encoding="utf-8")
            xcodebuild.chmod(0o755)
            xcrun.chmod(0o755)
            environment = os.environ.copy()
            environment["PATH"] = str(tools)
            script = self.root / "skills" / "verify-apple-apps" / "scripts" / "apple_verification_doctor.py"
            result = subprocess.run(
                [sys.executable, str(script), "--platform", "ios"],
                check=False,
                capture_output=True,
                text=True,
                env=environment,
            )
            report = json.loads(result.stdout)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(report["ready"])
            self.assertEqual(report["simulator"]["query"]["exit_code"], 1)

    def test_electron_doctor_verifies_renderer_and_main_targets(self) -> None:
        module = self.load_electron_doctor()
        responses = [
            JsonResponse({"Browser": "MockElectron/1.0"}),
            JsonResponse(
                [
                    {
                        "id": "renderer-1",
                        "title": "Mock App",
                        "type": "page",
                        "url": "app://index.html",
                        "webSocketDebuggerUrl": "ws://127.0.0.1/devtools/page/renderer-1",
                    }
                ]
            ),
        ]
        with patch.object(module.urllib.request, "urlopen", side_effect=responses):
            report = module.inspect_endpoint("127.0.0.1", 9222)
        self.assertTrue(report["reachable"])
        self.assertEqual(report["targets"][0]["title"], "Mock App")
        self.assertEqual(module.match_targets(report["targets"], "Mock", "app://"), report["targets"])
        self.assertEqual(module.match_targets(report["targets"], "Other", None), [])

    def test_electron_doctor_rejects_non_loopback_debugging(self) -> None:
        script = self.root / "skills" / "verify-electron-apps" / "scripts" / "electron_cdp_doctor.py"
        result = subprocess.run(
            [sys.executable, str(script), "--host", "192.0.2.1", "--renderer-port", "9222"],
            check=False,
            capture_output=True,
            text=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(report["ready"])
        self.assertIn("loopback", report["error"])

    def test_electron_doctor_rejects_non_ip_hostnames(self) -> None:
        script = self.root / "skills" / "verify-electron-apps" / "scripts" / "electron_cdp_doctor.py"
        result = subprocess.run(
            [sys.executable, str(script), "--host", "example.test", "--renderer-port", "9222"],
            check=False,
            capture_output=True,
            text=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(report["ready"])


if __name__ == "__main__":
    unittest.main()
