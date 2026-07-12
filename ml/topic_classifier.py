import os
import torch
import pandas as pd
from transformers import pipeline
from tqdm import tqdm

class TopicModel:
    def __init__(self, device=-1):
        print("\n[MÔ-ĐUN] Đang khởi tạo mô hình Chủ đề (BART)...")
        # ĐÃ ĐỔI: Chuyển sang mô hình chính thức của Facebook, chạy công khai không cần Token
        self.pipeline = pipeline(
            "zero-shot-classification", 
            model="facebook/bart-large-mnli", 
            device=device
        )
        self.candidate_topics = [
            # Tiếng Anh cơ bản đời sống
            "Daily Greetings / Basics", "Family / Relationships", "Weather / Seasons",
            "Food / Drinks / Dining", "Clothing / Fashion", "Home / Housing", 
            "Feelings / Emotions", "Shopping / Prices", "Time / Dates",
            
            # Công việc & Học thuật nâng cao
            "School / Education", "Information Technology / Computers", 
            "Healthcare / Medicine", "Economics / Business / Finance", 
            "Arts / Entertainment / Media", "Sports / Fitness", 
            "Transportation / Travel", "Science / Nature / Environment", 
            "Law / Government / Politics", "Crime / Safety"
        ]

    def predict(self, text):
        try:
            prediction = self.pipeline(text, candidate_labels=self.candidate_topics)
            return prediction['labels'][0], round(prediction['scores'][0], 4)
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
        
        topic_model = TopicModel(device=device)
        topics, scores = [], []
        
        print("--- Bắt đầu phân loại Chủ đề Độc lập ---")
        for item in tqdm(df["Word"], desc="Chủ đề"):
            tpc, scr = topic_model.predict(str(item).strip())
            topics.append(tpc)
            scores.append(scr)
            
        df['related_topic'], df['topic_confidence'] = topics, scores
        df.to_json(OUTPUT_FILE, orient='records', force_ascii=False, indent=4)
        print("Đã lưu kết quả Chủ đề!")