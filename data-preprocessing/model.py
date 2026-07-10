import pandas as pd
import re
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer


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

df = pd.read_csv("data.csv")

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

# Tải dữ liệu từ điển nếu chưa có
nltk.download("wordnet")

# 2. Khởi tạo Lemmatizer
lemmatizer = WordNetLemmatizer()

# 3. Tạo bản đồ ánh xạ 
POS_MAP = {
    "n": [wordnet.NOUN],
    "noun": [wordnet.NOUN],
    "v": [wordnet.VERB],
    "verb": [wordnet.VERB],
    "vauxiliary": [wordnet.VERB],
    "modal": [wordnet.VERB],
    "modal verb": [wordnet.VERB],
    "to": [wordnet.VERB],
    "adj": [wordnet.ADJ, wordnet.VERB],
    "adjective": [wordnet.ADJ, wordnet.VERB],
    "adv": [wordnet.ADV],
    "adverb": [wordnet.ADV],
}

COMPACT_POS_MAP = {
    "adjv": ["adj", "v"],
    "detpron": ["det", "pron"],
    "nprep": ["n", "prep"],
    "ndet": ["n", "det"],
    "nv": ["n", "v"],
    "vconj": ["v", "conj"],
}

def normalize_pos(pos):
    if not isinstance(pos, str):
        return []

    tokens = []
    for part in pos.split(","):
        for token in part.strip().lower().rstrip(".").split():
            if token in COMPACT_POS_MAP:
                tokens.extend(COMPACT_POS_MAP[token])
            elif token:
                tokens.append(token)

    return tokens

def get_wordnet_pos_candidates(pos):
    candidates = []
    for token in normalize_pos(pos):
        if token in POS_MAP:
            for candidate in POS_MAP[token]:
                if candidate not in candidates:
                    candidates.append(candidate)

    return candidates

# 4. Hàm xử lý NHẬN VÀO MỘT DÒNG (ROW) thay vì một từ
def lemmatize_row(row):
    word = str(row.get("Word", "")).strip().lower()
    
    if not word:
        return word

    if re.search(r"\s", word):
        return word

    candidates = get_wordnet_pos_candidates(row.get("POS", ""))

    if not candidates:
        return word

    lemmas = [lemmatizer.lemmatize(word, pos) for pos in candidates]

    for lemma in lemmas:
        if lemma != word:
            return lemma

    return lemmas[0]

# 5. Duyệt toàn bộ DataFrame (axis=1) để tạo cột mới 'Root_Word'
# Lưu ý: df.apply thay vì df['Word'].apply
df["Root_Word"] = df.apply(lemmatize_row, axis=1)

df.to_csv("../ml/vocab.csv", index=False)
