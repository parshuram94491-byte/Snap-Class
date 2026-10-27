import unittest
from unittest.mock import patch

from src.pipelines import voice_pipeline


class VoicePipelineDependencyTests(unittest.TestCase):
    def test_missing_librosa_has_install_instructions(self):
        with patch(
            "src.pipelines.voice_pipeline.importlib.import_module",
            side_effect=ImportError("librosa is not installed"),
        ):
            with self.assertRaisesRegex(
                RuntimeError, "requires librosa.*pip install -r requirements.txt"
            ):
                voice_pipeline._load_librosa()

    def test_bulk_audio_processing_reports_missing_librosa(self):
        with patch(
            "src.pipelines.voice_pipeline.importlib.import_module",
            side_effect=ImportError("librosa is not installed"),
        ):
            with self.assertRaisesRegex(RuntimeError, "requires librosa"):
                voice_pipeline.process_bulk_audio(b"audio", {1: [0.1]})


if __name__ == "__main__":
    unittest.main()
