import csv
import json
import random

# Tên file đầu vào và đầu ra
csv_file_path = 'words.csv'
json_output_path = '../lessons.json' # Xuất trực tiếp ra thư mục cha như log của bạn

# 1. Định nghĩa quy chuẩn phân bổ 126 bài học
lessons_rule = [
    { "lesson": 1, "distribution": { 3: 25, 4: 5 } },
    { "lesson": 2, "distribution": { 3: 25, 4: 5 } },
    { "lesson": 3, "distribution": { 3: 25, 4: 5 } },
    { "lesson": 4, "distribution": { 3: 25, 4: 5 } },
    { "lesson": 5, "distribution": { 3: 25, 4: 5 } },
    { "lesson": 6, "distribution": { 3: 15, 4: 15 } }, 
    { "lesson": 7, "distribution": { 3: 15, 4: 15 } },
    { "lesson": 8, "distribution": { 3: 15, 4: 15 } },
    { "lesson": 9, "distribution": { 3: 10, 4: 20 } },
    { "lesson": 10, "distribution": { 3: 10, 4: 20 } },
    { "lesson": 11, "distribution": { 3: 5, 4: 25 } },
    { "lesson": 12, "distribution": { 4: 25, 5: 5 } },
    { "lesson": 13, "distribution": { 4: 25, 5: 5 } },
    { "lesson": 14, "distribution": { 4: 25, 5: 5 } },
    { "lesson": 15, "distribution": { 4: 25, 5: 5 } },
    { "lesson": 16, "distribution": { 4: 25, 5: 5 } },
    { "lesson": 17, "distribution": { 4: 25, 5: 5 } },
    { "lesson": 18, "distribution": { 4: 25, 5: 5 } },
    { "lesson": 19, "distribution": { 4: 25, 5: 5 } },
    { "lesson": 20, "distribution": { 4: 25, 5: 5 } },
    { "lesson": 21, "distribution": { 4: 25, 5: 5 } },
    { "lesson": 22, "distribution": { 4: 25, 5: 5 } },
    { "lesson": 23, "distribution": { 4: 25, 5: 5 } },
    { "lesson": 24, "distribution": { 4: 25, 5: 5 } },
    { "lesson": 25, "distribution": { 4: 25, 5: 5 } },
    { "lesson": 26, "distribution": { 4: 15, 5: 15 } },
    { "lesson": 27, "distribution": { 4: 15, 5: 15 } },
    { "lesson": 28, "distribution": { 4: 15, 5: 15 } },
    { "lesson": 29, "distribution": { 4: 15, 5: 15 } },
    { "lesson": 30, "distribution": { 4: 15, 5: 15 } },
    { "lesson": 31, "distribution": { 4: 15, 5: 15 } },
    { "lesson": 32, "distribution": { 4: 15, 5: 15 } },
    { "lesson": 33, "distribution": { 4: 10, 5: 20 } },
    { "lesson": 34, "distribution": { 4: 10, 5: 20 } },
    { "lesson": 35, "distribution": { 4: 10, 5: 20 } },
    { "lesson": 36, "distribution": { 4: 10, 5: 20 } },
    { "lesson": 37, "distribution": { 4: 10, 5: 20 } },
    { "lesson": 38, "distribution": { 4: 12, 5: 18 } },
    { "lesson": 39, "distribution": { 5: 25, 6: 5 } },
    { "lesson": 40, "distribution": { 5: 25, 6: 5 } },
    { "lesson": 41, "distribution": { 5: 25, 6: 5 } },
    { "lesson": 42, "distribution": { 5: 25, 6: 5 } },
    { "lesson": 43, "distribution": { 5: 25, 6: 5 } },
    { "lesson": 44, "distribution": { 5: 25, 6: 5 } },
    { "lesson": 45, "distribution": { 5: 25, 6: 5 } },
    { "lesson": 46, "distribution": { 5: 25, 6: 5 } },
    { "lesson": 47, "distribution": { 5: 25, 6: 5 } },
    { "lesson": 48, "distribution": { 5: 25, 6: 5 } },
    { "lesson": 49, "distribution": { 5: 15, 6: 15 } },
    { "lesson": 50, "distribution": { 5: 15, 6: 15 } },
    { "lesson": 51, "distribution": { 5: 15, 6: 15 } },
    { "lesson": 52, "distribution": { 5: 15, 6: 15 } },
    { "lesson": 53, "distribution": { 5: 15, 6: 15 } },
    { "lesson": 54, "distribution": { 5: 15, 6: 15 } },
    { "lesson": 55, "distribution": { 5: 10, 6: 20 } },
    { "lesson": 56, "distribution": { 5: 10, 6: 20 } },
    { "lesson": 57, "distribution": { 5: 9, 6: 21 } },
    { "lesson": 58, "distribution": { 6: 25, 7: 5 } },
    { "lesson": 59, "distribution": { 6: 25, 7: 5 } },
    { "lesson": 60, "distribution": { 6: 25, 7: 5 } },
    { "lesson": 61, "distribution": { 6: 25, 7: 5 } },
    { "lesson": 62, "distribution": { 6: 25, 7: 5 } },
    { "lesson": 63, "distribution": { 6: 25, 7: 5 } },
    { "lesson": 64, "distribution": { 6: 25, 7: 5 } },
    { "lesson": 65, "distribution": { 6: 25, 7: 5 } },
    { "lesson": 66, "distribution": { 6: 25, 7: 5 } },
    { "lesson": 67, "distribution": { 6: 25, 7: 5 } },
    { "lesson": 68, "distribution": { 6: 25, 7: 5 } },
    { "lesson": 69, "distribution": { 6: 25, 7: 5 } },
    { "lesson": 70, "distribution": { 6: 15, 7: 15 } },
    { "lesson": 71, "distribution": { 6: 15, 7: 15 } },
    { "lesson": 72, "distribution": { 6: 15, 7: 15 } },
    { "lesson": 73, "distribution": { 6: 15, 7: 15 } },
    { "lesson": 74, "distribution": { 6: 15, 7: 15 } },
    { "lesson": 75, "distribution": { 6: 15, 7: 15 } },
    { "lesson": 76, "distribution": { 6: 10, 7: 20 } },
    { "lesson": 77, "distribution": { 6: 10, 7: 20 } },
    { "lesson": 78, "distribution": { 6: 10, 7: 20 } },
    { "lesson": 79, "distribution": { 7: 25, 8: 5 } },
    { "lesson": 80, "distribution": { 7: 25, 8: 5 } },
    { "lesson": 81, "distribution": { 7: 25, 8: 5 } },
    { "lesson": 82, "distribution": { 7: 25, 8: 5 } },
    { "lesson": 83, "distribution": { 7: 25, 8: 5 } },
    { "lesson": 84, "distribution": { 7: 25, 8: 5 } },
    { "lesson": 85, "distribution": { 7: 25, 8: 5 } },
    { "lesson": 86, "distribution": { 7: 25, 8: 5 } },
    { "lesson": 87, "distribution": { 7: 25, 8: 5 } },
    { "lesson": 88, "distribution": { 7: 25, 8: 5 } },
    { "lesson": 89, "distribution": { 7: 15, 8: 15 } },
    { "lesson": 90, "distribution": { 7: 15, 8: 15 } },
    { "lesson": 91, "distribution": { 7: 15, 8: 15 } },
    { "lesson": 92, "distribution": { 7: 15, 8: 15 } },
    { "lesson": 93, "distribution": { 7: 15, 8: 15 } },
    { "lesson": 94, "distribution": { 7: 10, 8: 20 } },
    { "lesson": 95, "distribution": { 7: 10, 8: 20 } },
    { "lesson": 96, "distribution": { 7: 4, 8: 26 } },
    { "lesson": 97, "distribution": { 8: 25, 9: 5 } },
    { "lesson": 98, "distribution": { 8: 25, 9: 5 } },
    { "lesson": 99, "distribution": { 8: 25, 9: 5 } },
    { "lesson": 100, "distribution": { 8: 25, 9: 5 } },
    { "lesson": 101, "distribution": { 8: 25, 9: 5 } },
    { "lesson": 102, "distribution": { 8: 15, 9: 15 } },
    { "lesson": 103, "distribution": { 8: 15, 9: 15 } },
    { "lesson": 104, "distribution": { 8: 15, 9: 15 } },
    { "lesson": 105, "distribution": { 8: 15, 9: 15 } },
    { "lesson": 106, "distribution": { 8: 10, 9: 20 } },
    { "lesson": 107, "distribution": { 8: 8, 9: 22 } },
    { "lesson": 108, "distribution": { 9: 25, 10: 5 } },
    { "lesson": 109, "distribution": { 9: 25, 10: 5 } },
    { "lesson": 110, "distribution": { 9: 25, 10: 5 } },
    { "lesson": 111, "distribution": { 9: 25, 10: 5 } },
    { "lesson": 112, "distribution": { 9: 15, 10: 15 } },
    { "lesson": 113, "distribution": { 9: 15, 10: 15 } },
    { "lesson": 114, "distribution": { 9: 10, 10: 20 } },
    { "lesson": 115, "distribution": { 9: 5, 10: 25 } },
    { "lesson": 116, "distribution": { 10: 20, 11: 10 } },
    { "lesson": 117, "distribution": { 10: 20, 11: 10 } },
    { "lesson": 118, "distribution": { 10: 20, 11: 10 } },
    { "lesson": 119, "distribution": { 10: 15, 11: 15 } },
    { "lesson": 120, "distribution": { 10: 10, 11: 20 } },
    { "lesson": 121, "distribution": { 10: 11, 11: 19 } },
    { "lesson": 122, "distribution": { 11: 20, 12: 10 } },
    { "lesson": 123, "distribution": { 11: 13, 12: 17 } },
    { "lesson": 124, "distribution": { 12: 25, 13: 5 } },
    { "lesson": 125, "distribution": { 13: 25, 14: 5 } },
    { "lesson": 126, "distribution": { 14: 2, 15: 1 } }
]

words_by_count = {}

print("Bắt đầu đọc dữ liệu từ file CSV...")

try:
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Bỏ qua dòng tiêu đề cột
        
        for row in reader:
            if not row or len(row) < 12:
                continue
            try:
                # Trích xuất dữ liệu từ các cột
                word_id = int(row[0])
                word = row[1].strip()
                pos = row[2].strip()           # POS (Cột index 2)
                pronunciation = row[3].strip() # Pronunciation (Cột index 3)
                meaning = row[4].strip()       # Meaning (Cột index 4)
                count_val = int(row[11])       # Count (Cột index 11)
                
                # Cấu trúc câu hỏi mới với đúng 5 keys: id, Word, POS, Pronunciation, Meaning
                word_item = {
                    "id": word_id,
                    "Word": word,
                    "POS": pos,
                    "Pronunciation": pronunciation,
                    "Meaning": meaning
                }
                
                if count_val not in words_by_count:
                    words_by_count[count_val] = []
                words_by_count[count_val].append(word_item)
            except Exception as e:
                continue
                
    print("Đọc thành công file CSV ngân hàng đề!")
    for count, items in words_by_count.items():
        print(f" - Nhóm Count {count}: có {len(items)} từ vựng")

except FileNotFoundError:
    print(f"Lỗi: Không tìm thấy file '{csv_file_path}' ở thư mục hiện tại!")
    exit()

# ----------------- PHẦN TRỘN VÀ PHÂN BỔ ----------------- #
print("\nBắt đầu lọc và trộn ngẫu nhiên từ vựng cho các bài học...")

# Bước 1: Trộn ngẫu nhiên (shuffle) từng nhóm từ vựng một lần duy nhất lúc ban đầu
for count_val in words_by_count:
    random.shuffle(words_by_count[count_val])

final_lessons = []

# Bước 2: Phân bổ không lặp lại (Slice / Pop)
for rule in lessons_rule:
    lesson_num = rule["lesson"]
    lesson_questions = []
    
    for count_val_raw, limit in rule["distribution"].items():
        count_val = int(count_val_raw)
        available_words = words_by_count.get(count_val, [])
        
        # Cắt lấy số lượng từ cần dùng cho bài học này
        selected = available_words[:limit]
        
        # Xóa các từ đã lấy khỏi danh sách chờ (pool) để các bài học sau không bị trùng
        words_by_count[count_val] = available_words[limit:]
        
        # Cảnh báo nếu dữ liệu bị thiếu hụt ngoài ý muốn
        if len(selected) < limit:
            print(f"[Cảnh báo] Lesson {lesson_num} cần {limit} từ của Count {count_val}, nhưng chỉ còn {len(selected)} từ!")
            
        lesson_questions.extend(selected)
        
    # Xáo trộn ngẫu nhiên 30 câu hỏi của bài học này để đan xen sinh động các Count
    random.shuffle(lesson_questions)
    
    final_lessons.append({
        "lesson": lesson_num,
        "questions": lesson_questions
    })

# 3. Xuất kết quả ra file JSON
with open(json_output_path, 'w', encoding='utf-8') as f:
    json.dump(final_lessons, f, ensure_ascii=False, indent=2)

print(f"\n==> THÀNH CÔNG: Đã tạo xong file '{json_output_path}' hoàn chỉnh!")