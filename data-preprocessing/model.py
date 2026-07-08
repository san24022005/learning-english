import pandas as pd
import re

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

df = pd.read_csv("vocab.csv")

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

df.to_csv("../ml/processed_vocab.csv", index=False)