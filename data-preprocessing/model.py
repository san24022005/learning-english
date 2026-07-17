import pandas as pd
import re
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import spacy
from nltk.stem import PorterStemmer


nonContentWords = {
    "a", "an", "as", "the", "this", "that", "these", "those", "some", "any", "each",
    "every", "either", "neither", "my", "your", "his", "her", "its", "our",
    "their", "mine", "yours", "hers", "ours", "theirs", "it", "i", "you", "he",
    "she", "we", "they", "me", "him", "her", "us", "them", "who", "whom",
    "whose", "what", "which", "where", "when", "why", "how", "there", "here",
    "one", "ones", "someone", "something", "anyone", "anything", "everyone",
    "everything", "noone", "nothing", "oh", "ah", "wow", "oops", "from", "to",
    "in", "on", "at", "by", "with", "about", "for", "of", "and",
}

df = pd.read_csv("./data.csv")

index_to_remove = []

for index, row in df.iterrows():
    
    if len(row["Word"]) < 3:
        index_to_remove.append(index)
        continue

    if row["Word"] in nonContentWords:
        index_to_remove.append(index)
        continue

    if re.search(r'[()]', row["Word"]):
        index_to_remove.append(index)
        continue
        
    if isinstance(row["Word"], str) and ' ' in row["Word"]:
        index_to_remove.append(index)
        continue

df = df.drop(index_to_remove)

def CleanMeaning(meaning):
    part = re.split(r'[.;]', meaning)[0]

    return part.strip()

df["Meaning"] = df["Meaning"].apply(CleanMeaning)

def count_syllables_from_ipa(ipa_str):
    # 1. Định nghĩa các nguyên âm đôi (Diphthongs) để đếm trước (tránh bị đếm thành 2 nguyên âm đơn)
    diphthongs = ['eɪ', 'aɪ', 'ɔɪ', 'aʊ', 'əʊ', 'ɪə', 'eə', 'ʊə']
    
    # Làm sạch chuỗi: xóa dấu trọng âm (ˈ, ˌ), dấu kéo dài (ː), dấu chấm phân cách (.)
    clean_ipa = re.sub(r'[ˈˌː.]', '', ipa_str)
    
    syllable_count = 0
    
    # 2. Tìm và đếm các nguyên âm đôi, sau đó xóa chúng khỏi chuỗi
    for d in diphthongs:
        syllable_count += clean_ipa.count(d)
        clean_ipa = clean_ipa.replace(d, '')
        
    # 3. Đếm các nguyên âm đơn (Monophthongs) còn lại
    monophthongs_pattern = r'[iɪeæɑɒɔʊuʌɜə]'
    monophthongs_found = re.findall(monophthongs_pattern, clean_ipa)
    syllable_count += len(monophthongs_found)
    
    # 4. Kiểm tra các phụ âm đóng vai trò âm tiết ở cuối từ (Syllabic Consonants như /l/, /n/, /m/)
    # Thường đứng sau một phụ âm khác ở cuối từ (Ví dụ: bɒtl, bʌtn)
    if re.search(r'[tdbpkgfvdðs zʃʒθ]l$', clean_ipa) or \
       re.search(r'[tdbpkgfvdðs zʃʒθ]n$', clean_ipa) or \
       re.search(r'[tdbpkgfvdðs zʃʒθ]m$', clean_ipa):
        syllable_count += 1
        
    return syllable_count

df["Syllables"] = df["Pronunciation"].apply(count_syllables_from_ipa)

# Tải mô hình ngôn ngữ tiếng Anh nhỏ gọn
nlp = spacy.load("en_core_web_sm")

def get_root_word_spacy(word: str) -> str:
    """
    Trả về từ gốc (lemma) của một từ bằng spaCy
    """
    doc = nlp(word.strip())
    # Trả về lemma của từ đầu tiên tìm thấy
    return doc[0].lemma_

df["Root_Word"] = df["Word"].apply(get_root_word_spacy)

df = df.reset_index(drop=True)

df.insert(0, 'id', df.index + 1)

df['Count'] = df['Word'].apply(len)

df.to_csv("../ml/vocab.csv", index=False)
