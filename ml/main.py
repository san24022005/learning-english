import os
import torch
import pandas as pd
from tqdm import tqdm

# KẾ THỪA CODE: Gọi trực tiếp các class xử lý từ 2 file mô-đun phía trên
from cefr_classifier import CEFRModel
from topic_classifier import TopicModel

# 1. Cấu hình đường dẫn
INPUT_FILE = "vocab.csv"
OUTPUT_FILE = "../words.json"
COLUMN_NAME = "Word"

if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(f"Không tìm thấy file dữ liệu đầu vào '{INPUT_FILE}'")

# 2. Đọc file CSV dữ liệu gốc
df = pd.read_csv(INPUT_FILE)
device = 0 if torch.cuda.is_available() else -1

# 3. Khởi tạo 2 mô hình bằng cách tái sử dụng code đã import
cefr_ai = CEFRModel(device=device)
topic_ai = TopicModel(device=device)

# 4. Khởi tạo các danh sách lưu kết quả
cefr_levels, cefr_scores = [], []
predicted_topics, topic_scores = [], []

print("\n--- Bắt đầu chạy tích hợp (Sử dụng code thừa kế từ 2 file mô-đun) ---")
for item in tqdm(df[COLUMN_NAME], desc="Đang xử lý song song"):
    text_input = str(item).strip()
    
    if text_input and text_input != "nan":
        # Gọi hàm xử lý của file cefr_classifier.py
        lvl, c_scr = cefr_ai.predict(text_input)
        cefr_levels.append(lvl)
        cefr_scores.append(c_scr)
        
        # Gọi hàm xử lý của file topic_classifier.py
        tpc, t_scr = topic_ai.predict(text_input)
        predicted_topics.append(tpc)
        topic_scores.append(t_scr)
    else:
        cefr_levels.append("Unknown")
        cefr_scores.append(0.0)
        predicted_topics.append("Unknown")
        topic_scores.append(0.0)

# 5. Gộp kết quả và xuất ra JSON
df['cefr_level'] = cefr_levels
df['cefr_confidence'] = cefr_scores
df['related_topic'] = predicted_topics
df['topic_confidence'] = topic_scores

df.to_json(OUTPUT_FILE, orient='records', force_ascii=False, indent=4)
print(f"\n Hoàn thành chạy file tích hợp! Kết quả lưu tại: '{OUTPUT_FILE}'")