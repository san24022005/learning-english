import random
from typing import List, Dict


def predict_difficulty(word: str) -> str:
    """Dự đoán độ khó từ vựng dựa trên độ dài và các đặc trưng đơn giản."""
    normalized = word.strip().lower()
    if len(normalized) <= 5:
        return "easy"
    if len(normalized) <= 10:
        return "medium"
    return "hard"


def recommend_word(words: List[Dict], level: str) -> Dict | None:
    """Gợi ý từ phù hợp với mức độ học viên."""
    if not words:
        return None
    candidates = [w for w in words if predict_difficulty(w.get("word", "")) == level]
    if not candidates:
        candidates = words
    return random.choice(candidates)
