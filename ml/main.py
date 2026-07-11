import pandas as pd

df = pd.read_csv("vocab.csv")

i = 0;

for index, row in df.iterrows():
    if row["Word"] != row["Root_Word"]:
        print(f"Word: {row['Word']}, Root_Word: {row['Root_Word']}")
        i += 1

print(f"Total mismatches found: {i}")

import spacy

# Tải mô hình ngôn ngữ tiếng Anh nhỏ gọn
nlp = spacy.load("en_core_web_sm")

def get_root_word_spacy(word: str) -> str:
    """
    Trả về từ gốc (lemma) của một từ bằng spaCy
    """
    doc = nlp(word.strip())
    # Trả về lemma của từ đầu tiên tìm thấy
    return doc[0].lemma_

# --- Thử nghiệm ---
words = ["running", "flies", "better", "development", "happiness", "discussion"]

print("--- Kết quả từ spaCy ---")
for w in words:
    print(f"{w} -> {get_root_word_spacy(w)}")