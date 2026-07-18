from pathlib import Path
from flask import Flask
from config import Config
from flask_mysqldb import MySQL

# Tạo đối tượng MySQL toàn cục ở đây để file routes có thể dùng ké
mysql = MySQL()

def create_app():
    base_dir = Path(__file__).resolve().parent
    app = Flask(__name__, template_folder=str(base_dir / "templates"), static_folder=str(base_dir / "static"))

    # Nạp các cấu hình cứng cho MySQL (Cổng 3307 theo XAMPP của bạn)
    app.secret_key = 'your_secret_key'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''  
    app.config['MYSQL_DB'] = 'learning_english'
    app.config['MYSQL_PORT'] = 3307

    # Khởi tạo mysql với ứng dụng
    mysql.init_app(app)

    # Đăng ký Blueprint (Luồng xử lý route)
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Đăng ký API blueprint từ lesson.py
    try:
        from app.api.lesson import api_bp
        app.register_blueprint(api_bp)
    except ImportError:
        pass

    return app