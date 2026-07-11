import unittest

from ml.main import predict_difficulty, recommend_word


class AITestCase(unittest.TestCase):
    def test_predict_difficulty_for_short_word(self):
        difficulty = predict_difficulty("apple")
        self.assertEqual(difficulty, "easy")

    def test_predict_difficulty_for_long_word(self):
        difficulty = predict_difficulty("recommendation")
        self.assertEqual(difficulty, "hard")

    def test_recommend_word_for_medium_level(self):
        recommendation = recommend_word([{"word": "apple", "meaning": "Quả táo"}, {"word": "banana", "meaning": "Quả chuối"}, {"word": "developer", "meaning": "Lập trình viên"}], "medium")
        self.assertIsNotNone(recommendation)


if __name__ == '__main__':
    unittest.main()
