import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NEW_PACK = ROOT / "ai-3d-asset-pack-pipeline/scripts/new_pack.py"
VALIDATE_PACK = ROOT / "ai-3d-asset-pack-pipeline/scripts/validate_pack.py"


class PipelineScriptsTest(unittest.TestCase):
    def run_script(self, script: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), *args],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_scaffold_is_a_valid_draft(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            result = self.run_script(NEW_PACK, "Cozy Potion Shop", "--output", temp)
            self.assertEqual(result.returncode, 0, result.stderr)
            pack = Path(temp) / "cozy-potion-shop"
            result = self.run_script(VALIDATE_PACK, str(pack))
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_release_requires_real_approved_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            pack = Path(temp) / "pack"
            pack.mkdir()
            for name in ("installation.md", "usage.md", "license.md"):
                (pack / name).write_text("ok\n", encoding="utf-8")
            manifest = {
                "pack_id": "pack",
                "pack_name": "Pack",
                "version": "1.0.0",
                "status": "approved",
                "target_runtime": "Three.js",
                "supported_versions": ["tested"],
                "license_profile": "commercial-use-v1",
                "demo_entry": "demo/index.html",
                "assets": [{
                    "id": "prop-01",
                    "status": "approved",
                    "reference": "assets/prop-01/reference.png",
                    "model_source": "src/prop-01.ts",
                    "preview": "previews/prop-01.png",
                    "review": "assets/prop-01/review.md",
                    "provenance": "assets/prop-01/provenance.md",
                }],
                "provenance": [{"asset_id": "prop-01"}],
            }
            (pack / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            result = self.run_script(VALIDATE_PACK, "--release", str(pack))
            self.assertNotEqual(result.returncode, 0)
            (pack / "demo").mkdir()
            (pack / "demo/index.html").write_text("fixture\n", encoding="utf-8")
            for path in manifest["assets"][0].values():
                if isinstance(path, str) and "/" in path:
                    target = pack / path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text("fixture\n", encoding="utf-8")
            result = self.run_script(VALIDATE_PACK, "--release", str(pack))
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_release_rejects_unsafe_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            pack = Path(temp) / "pack"
            pack.mkdir()
            for name in ("installation.md", "usage.md", "license.md"):
                (pack / name).write_text("ok\n", encoding="utf-8")
            manifest = {
                "pack_id": "pack", "pack_name": "Pack", "version": "1.0.0",
                "status": "approved", "target_runtime": "Three.js", "supported_versions": ["tested"],
                "license_profile": "commercial-use-v1", "demo_entry": "demo/index.html", "assets": [{
                    "id": "prop-01", "status": "approved", "reference": "../outside.png",
                    "model_source": "src/model.ts", "preview": "preview.png",
                    "review": "review.md", "provenance": "provenance.md",
                }], "provenance": [{"asset_id": "prop-01"}],
            }
            (pack / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            result = self.run_script(VALIDATE_PACK, "--release", str(pack))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unsafe path", result.stdout)


if __name__ == "__main__":
    unittest.main()
