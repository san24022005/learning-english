import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "data-preprocessing" / "model.py"


class TestModelPaths(unittest.TestCase):
    def test_process_and_save_resolves_relative_paths_from_script_directory(self):
        spec = importlib.util.spec_from_file_location("model_script", SCRIPT_PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "processed.csv"
            module.process_and_save("vocab.csv", output_path)
            self.assertTrue(output_path.exists())

    def test_clean_meaning_with_nlp_removes_non_content_word_types(self):
        spec = importlib.util.spec_from_file_location("model_script", SCRIPT_PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        result = module.clean_meaning_with_nlp("the quick fox is running")
        self.assertNotIn("the", result.lower())
        self.assertNotIn("is", result.lower())
        self.assertIn("quick", result.lower())
        self.assertIn("fox", result.lower())


if __name__ == "__main__":
    unittest.main()
