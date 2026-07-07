from flask import Blueprint, render_template

# Khởi tạo Blueprint
main_bp = Blueprint('main', __name__)


# Route 1: Hiển thị trang chủ giao diện
@main_bp.route("/")
def home():
    return render_template("index.html")