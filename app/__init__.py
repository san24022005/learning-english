import importlib
from pathlib import Path
from flask import Flask
from flask_mysqldb import MySQL

base_dir = Path(__file__).resolve().parent
mysql = MySQL()

def create_app():
    app = Flask(__name__, template_folder=str(base_dir / "templates"), static_folder=str(base_dir / "static"))
    app.secret_key = 'your_secret_key'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''  
    app.config['MYSQL_DB'] = 'learning_english'
    app.config['MYSQL_PORT'] = 3307

    # Khởi tạo mysql với ứng dụng
    mysql.init_app(app)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    from app.api import api_bp

    # Import các module route trước khi đăng ký blueprint để Flask
    # có thể áp dụng các decorator route đúng thời điểm.
    importlib.import_module('app.api.lesson')
    importlib.import_module('app.api.info')

    app.register_blueprint(api_bp)

    return app