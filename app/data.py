import json

def get_words_data():
    """Return list of words from project's words.json file."""
    with open('words.json', 'r', encoding='utf-8') as f:
        return json.load(f)
