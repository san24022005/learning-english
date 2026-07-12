import os
import torch
import pandas as pd
from transformers import pipeline
from tqdm import tqdm

class CEFRModel:
    def __init__(self, device=-1):
        print("\n[MÔ-ĐUN] Đang khởi tạo mô hình CEFR (DeBERTa)...")
        self.pipeline = pipeline("text-classification", model="dksysd/cefr-classifier", device=device)

    def predict(self, text):
        try:
            prediction = self.pipeline(text)[0]
            return prediction['label'], round(prediction['score'], 4)
        except Exception:
            return "Error", 0.0

# Đoạn code dưới đây chỉ chạy khi bạn bấm thực thi TRỰC TIẾP file này
if __name__ == "__main__":
    INPUT_FILE = "vocab.csv"
    OUTPUT_FILE = "../words.json"
    
    if not os.path.exists(INPUT_FILE):
        print(f"Không tìm thấy file {INPUT_FILE}")
    else:
        df = pd.read_csv(INPUT_FILE)
        device = 0 if torch.cuda.is_available() else -1
        
        cefr_model = CEFRModel(device=device)
        levels, scores = [], []
        
        print("--- Bắt đầu phân loại CEFR Độc lập ---")
        for item in tqdm(df["Word"], desc="CEFR"):
            lvl, scr = cefr_model.predict(str(item).strip())
            levels.append(lvl)
            scores.append(scr)
            
        df['cefr_level'], df['cefr_confidence'] = levels, scores
        df.to_json(OUTPUT_FILE, orient='records', force_ascii=False, indent=4)
        print("Đã lưu kết quả CEFR!")