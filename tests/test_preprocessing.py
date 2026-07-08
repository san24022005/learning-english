import os
import tempfile
import unittest

from ml.preprocessing import build_vocab_dataframe, parse_vocab_line, simplify_meaning


class VocabularyPreprocessingTest(unittest.TestCase):
    def test_parse_vocab_line_with_pos_and_pronunciation(self):
        row = parse_vocab_line("abandon v. /ə’bændən/ bỏ, từ bỏ")
        self.assertEqual(row["Word"], "abandon")
        self.assertEqual(row["POS"], "v.")
        self.assertEqual(row["Pronunciation"], "ə’bændən")
        self.assertEqual(row["Meaning"], "bỏ, từ bỏ")

    def test_simplify_meaning_uses_the_first_gloss(self):
        self.assertEqual(simplify_meaning("sự thích nghi, điều tiết; điều chỉnh, sửa lại"), "sự thích nghi")

    def test_build_vocab_dataframe_from_text_file(self):
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as handle:
            handle.write("abandon v. /ə’bændən/ bỏ, từ bỏ\n")
            handle.write("by accident\n")
            path = handle.name

        try:
            df = build_vocab_dataframe(path)
            self.assertEqual(len(df), 2)
            self.assertEqual(df.loc[0, "Word"], "abandon")
            self.assertEqual(df.loc[1, "Word"], "by accident")
            self.assertEqual(df.loc[1, "Meaning"], "by accident")
        finally:
            os.unlink(path)

    def test_build_vocab_dataframe_skips_non_content_words(self):
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as handle:
            handle.write("a det. /ə/ một\n")
            handle.write("about adv. /əˈbaʊt/ khoảng\n")
            handle.write("oh interj. /oʊ/ ồ\n")
            handle.write("abandon v. /əˈbændən/ bỏ, từ bỏ\n")
            path = handle.name

        try:
            df = build_vocab_dataframe(path)
            self.assertEqual(list(df["Word"]), ["abandon"])
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
