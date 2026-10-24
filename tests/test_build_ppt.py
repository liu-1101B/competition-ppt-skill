"""Smoke tests for the bundled PowerPoint example generator."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from pptx import Presentation


ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "examples" / "build-ppt.py"


class BuildPptSmokeTests(unittest.TestCase):
    def test_build_saves_a_readable_20_slide_deck_to_requested_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            temp = Path(tmp)
            output = temp / "nested" / "demo.pptx"
            image_dir = temp / "project-images"
            background_dir = temp / "backgrounds"
            # Intentionally leave the asset directories absent. Missing images
            # should be skipped while the script still creates a readable deck.
            completed = subprocess.run(
                [
                    sys.executable,
                    str(BUILD_SCRIPT),
                    "--image-dir", str(image_dir),
                    "--background-dir", str(background_dir),
                    "--output", str(output),
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertTrue(output.exists(), completed.stdout)
            self.assertGreater(output.stat().st_size, 0)
            deck = Presentation(str(output))
            self.assertEqual(len(deck.slides), 20)
            self.assertIn("PPTX saved:", completed.stdout)

    def test_cli_help_is_available(self):
        completed = subprocess.run(
            [sys.executable, str(BUILD_SCRIPT), "--help"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("--image-dir", completed.stdout)
        self.assertIn("--background-dir", completed.stdout)
        self.assertIn("--output", completed.stdout)


if __name__ == "__main__":
    unittest.main()
