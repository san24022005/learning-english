import os
from dotenv import load_dotenv

# Tải các biến môi trường từ file .env
load_dotenv()

class Config:
    # Nếu trong .env không có SECRET_KEY thì lấy chuỗi mặc định phía sau
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bi-mat-mac-dinh'

    # Bạn có thể thêm cấu hình Database ở đây sau này:
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
