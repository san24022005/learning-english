import json
from pathlib import Path


def get_words_data():
    """Return list of words from project's words.json file."""
    data_file = Path(__file__).resolve().parent.parent / "words.json"
    with data_file.open('r', encoding='utf-8') as f:
        return json.load(f)
