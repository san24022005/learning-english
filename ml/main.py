import os
import pandas as pd
import random

# Utility: determine difficulty by simple heuristics
def predict_difficulty(word: str) -> str:
    s = (word or '').strip()
    l = len(s)
    if l == 0:
        return 'unknown'
    if l <= 5:
        return 'easy'
    if l >= 10:
        return 'hard'
    return 'medium'


def recommend_word(words: list, level: str):
    """Return a recommended word dict from a list based on desired level.

    `words` is expected to be a list of dicts with a `word` key.
    """
    if not words:
        return None
    level = (level or '').strip().lower()
    candidates = [w for w in words if predict_difficulty(w.get('word', '')) == level]
    if candidates:
        return random.choice(candidates)
    return random.choice(words)


# Optional spaCy helper (lazy import to avoid heavy imports at module import time)
_nlp = None
def get_root_word_spacy(word: str) -> str:
    global _nlp
    try:
        if _nlp is None:
            import spacy
            _nlp = spacy.load('en_core_web_sm')
        doc = _nlp((word or '').strip())
        return doc[0].lemma_ if doc and len(doc) > 0 else ''
    except Exception:
        return ''


if __name__ == '__main__':
    # When run as script, optionally inspect the CSV and print simple results.
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, 'vocab.csv')
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        mismatches = []
        for _, row in df.iterrows():
            if row.get('Word') != row.get('Root_Word'):
                mismatches.append((row.get('Word'), row.get('Root_Word')))
        for w, r in mismatches:
            print(f"Word: {w}, Root_Word: {r}")
        print(f"Total mismatches found: {len(mismatches)}")
    else:
        print('vocab.csv not found in ml/ (skipping CSV checks)')