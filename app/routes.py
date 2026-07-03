#%%
from flask import Blueprint, render_template

# Khởi tạo Blueprint có tên là 'main'
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    # Giả lập dữ liệu lấy từ Database (Model) để truyền sang giao diện
    user_info = {
        "username": "Zero_To_Hero",
        "role": "Lập trình viên Flask",
        "skills": ["Python", "Flask", "HTML/CSS"]
    }
    # Trả về giao diện index.html kèm theo dữ liệu user
    return render_template('index.html', data=user_info)

@main_bp.route('/about')
def about():
    return "<h1>Đây là trang giới thiệu của ứng dụng!</h1>"