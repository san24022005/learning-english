from flask import Blueprint, render_template, jsonify, request
import json
import random

# Khởi tạo Blueprint
main_bp = Blueprint('main', __name__)

# Hàm phụ trợ: Đọc dữ liệu từ file JSON
def get_words_data():
    # Vì chạy từ file run.py ở thư mục gốc nên đường dẫn là 'words.json'
    with open('words.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Route 1: Hiển thị trang chủ giao diện
@main_bp.route("/")
def home():
    return render_template("index.html")

# Route 2: API Lấy một từ vựng ngẫu nhiên đã bị xáo trộn
@main_bp.route("/api/get-quiz", methods=["GET"])
def get_quiz():
    words = get_words_data()
    chosen_word = random.choice(words)
    
    word_chars = list(chosen_word["word"])
    random.shuffle(word_chars)
    scrambled_word = "".join(word_chars)
    
    return jsonify({
        "id": chosen_word["id"],
        "scrambled": scrambled_word,
        "meaning": chosen_word["meaning"]
    })

# Route 3: API Kiểm tra đáp án
@main_bp.route("/api/check-answer", methods=["POST"])
def check_answer():
    data = request.json
    user_answer = data.get("answer", "").strip().lower()
    word_id = data.get("id")
    
    words = get_words_data()
    correct_word = next((w for w in words if w["id"] == word_id), None)
    
    if not correct_word:
        return jsonify({"error": "Không tìm thấy từ vựng"}), 404
        
    if user_answer == correct_word["word"].lower():
        return jsonify({"is_correct": True, "message": "Chính xác! Bạn thật tuyệt vời!"})
    else:
        return jsonify({"is_correct": False, "message": f"Sai rồi. Đáp án đúng là: {correct_word['word']}"})