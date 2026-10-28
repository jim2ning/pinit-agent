import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import settings

class SettingsTests(unittest.TestCase):
    def test_file_load_does_not_override_existing_value(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "settings.py"
            (Path(directory) / ".env").write_text("OPENAI_MODEL=from_file\n", encoding="utf-8")
            with patch.object(settings, "__file__", str(source)), patch.dict(os.environ, {"OPENAI_MODEL":"existing"}):
                settings.load_settings()
                self.assertEqual(os.environ["OPENAI_MODEL"], "existing")
    def test_file_loaded_when_missing(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "settings.py"
            (Path(directory) / ".env").write_text("OPENAI_MODEL=from_file\n", encoding="utf-8")
            with patch.object(settings, "__file__", str(source)), patch.dict(os.environ, {}, clear=True):
                settings.load_settings()
                self.assertEqual(os.environ["OPENAI_MODEL"], "from_file")

if __name__ == "__main__": unittest.main()
