import os
import json
from flask import Blueprint, jsonify, request, abort

api_bp = Blueprint('api', __name__, url_prefix='/api')

# 1. Xác định đường dẫn tuyệt đối đến file lessons.json
# Cách này giúp Flask luôn tìm thấy file kể cả khi bạn chạy server từ thư mục khác
lessons_path = '../../lessons.json'

# 2. Đọc và lưu trữ (cache) dữ liệu bài học vào bộ nhớ ngay khi chạy server
lessons_data = []
try:
    with open(lessons_path, 'r', encoding='utf-8') as f:
        lessons_data = json.load(f)
except FileNotFoundError:
    # Dự phòng trường hợp file lessons.json được đặt ở thư mục gốc của dự án
    lessons_path_fallback = os.path.join(os.getcwd(), 'lessons.json')
    try:
        with open(lessons_path_fallback, 'r', encoding='utf-8') as f:
            lessons_data = json.load(f)
    except FileNotFoundError:
        print(f"CẢNH BÁO: Không tìm thấy file lessons.json tại {lessons_path} hoặc {lessons_path_fallback}")


# 3. Định nghĩa API Endpoint tải bài học theo ID
@api_bp.route('/lesson/<int:lesson_id>', methods=['GET', 'POST'])
def load_lesson(lesson_id):
    # Tìm kiếm bài học tương ứng trong dữ liệu đã nạp sẵn
    lesson = next((item for item in lessons_data if item.get('lesson') == lesson_id), None)
    
    # Trả về lỗi 404 nếu không tìm thấy ID bài học (ví dụ truyền vào lesson_id > 126)
    if not lesson:
        return jsonify({
            "success": False,
            "error": f"Không tìm thấy bài học (Lesson) với ID: {lesson_id}"
        }), 404
        
    # Trả về danh sách câu hỏi của bài học đó dưới dạng JSON
    return jsonify({
        "success": True,
        "lesson": lesson_id,
        "questions": lesson.get("questions", []),
        "total_questions": len(lesson.get("questions", []))
    }), 200