import pandas as pd

INPUT_FILE = 'words.csv'
OUTPUT_FILE = '../words.json'

df_from_csv = pd.read_csv(INPUT_FILE)
df_from_csv.to_json(OUTPUT_FILE, orient='records', force_ascii=False, indent=4)