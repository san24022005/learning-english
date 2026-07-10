import pandas as pd

df = pd.read_csv("vocab.csv")

for index, row in df.iterrows():
    if row["Word"] != row["Root_Word"]:
        print(f"Word: {row['Word']}, Root_Word: {row['Root_Word']}")