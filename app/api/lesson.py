import os
import json
from flask import jsonify
from app.api import api_bp

# 1. Xác định đường dẫn tuyệt đối đến file lessons.json dựa trên vị trí của file code này
# __file__ là đường dẫn của file python hiện tại.
# Thay đổi số lượng os.path.dirname tùy thuộc vào cấu trúc thư mục thực tế của bạn.
current_dir = os.path.dirname(os.path.abspath(__file__))

# Giả sử file code này ở thư mục /app/routes/, và lessons.json ở /app/
# Bạn chỉnh sửa '..' cho đúng với cấu trúc dự án của mình.
lessons_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'lessons.json')) 

def load_lessons_data():
    """Hàm hỗ trợ đọc file JSON an toàn"""
    if not os.path.exists(lessons_path):
        # Dự phòng: Thử tìm ở thư mục gốc chạy script (Current Working Directory)
        fallback_path = os.path.join(os.getcwd(), 'lessons.json')
        if not os.path.exists(fallback_path):
            print(f"CẢNH BÁO: Không tìm thấy file lessons.json tại {lessons_path} hoặc {fallback_path}")
            return []
        target_path = fallback_path
    else:
        target_path = lessons_path

    try:
        with open(target_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"CẢNH BÁO: File {target_path} không đúng định dạng JSON hợp lệ.")
        return []
    except Exception as e:
        print(f"CẢNH BÁO: Lỗi khi đọc file {target_path}: {e}")
        return []

# 2. Đọc và lưu trữ (cache) dữ liệu bài học vào bộ nhớ ngay khi chạy server
lessons_data = load_lessons_data()

# 3. Định nghĩa API Endpoint tải bài học theo ID (Chỉ cần GET)
@api_bp.route('/lesson/<int:lesson_id>', methods=['GET'])
def load_lesson(lesson_id):
    # Tìm kiếm bài học tương ứng trong dữ liệu đã nạp sẵn
    lesson = next((item for item in lessons_data if item.get('lesson') == lesson_id), None)
    
    # Trả về lỗi 404 nếu không tìm thấy ID bài học
    if not lesson:
        return jsonify({
            "success": False,
            "error": f"Không tìm thấy bài học (Lesson) với ID: {lesson_id}"
        }), 404
        
    # Trả về danh sách câu hỏi của bài học đó dưới dạng JSON
    questions = lesson.get("questions", [])
    return jsonify({
        "success": True,
        "lesson": lesson_id,
        "questions": questions,
        "total_questions": len(questions)
    }), 200

# 4. Định nghĩa API Endpoint lấy toàn bộ bài học (Chỉ cần GET)
@api_bp.route('/lessons', methods=['GET'])
def get_all_lessons():
    # Kiểm tra xem dữ liệu có trống không để báo lỗi phù hợp
    if not lessons_data:
        return jsonify({
            "success": False,
            "error": "Dữ liệu bài học trống hoặc chưa được tải."
        }), 404
        
    return jsonify({
        "success": True,
        "total_lessons": len(lessons_data),
        "data": lessons_data
    }), 200