from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)

    # Nạp cấu hình từ file config.py vào app
    app.config.from_object(Config)

    # Đăng ký Blueprint (Luồng xử lý route)
    # Lưu ý: Import ở ĐÂY để tránh lỗi vòng lặp (Circular Import)
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Đăng ký API blueprint
    from app.api.words import api_bp
    app.register_blueprint(api_bp)

    return app