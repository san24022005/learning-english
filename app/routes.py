from flask import Blueprint, render_template, request, redirect, url_for, session
# Import trực tiếp đối tượng mysql từ file khởi tạo chính của bạn (nếu có) hoặc xử lý qua ứng dụng
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

# Tạo Blueprint để liên kết với __init__.py thay vì tạo app mới
main_bp = Blueprint('main', __name__)

# Kết nối mysql tạm thời thông qua proxy hoặc current_app
from flask import current_app

def get_db():
    # Khởi tạo mysql từ app đang chạy
    from app import mysql
    return mysql

@main_bp.route('/index')
def home():
    return render_template('index.html')

@main_bp.route('/')
def index():
    # KIỂM TRA SESSION: Nếu chưa đăng nhập thì bắt quay lại trang login
    if 'loggedin' not in session:
        return redirect(url_for('main.login'))
        
    return render_template('index.html', username=session.get('username'))

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    mysql = get_db()
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Thống nhất dùng bảng 'users' giống như file app.py cũ của bạn
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        cursor.close()
        
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            
            # ĐĂNG NHẬP XONG -> CHUYỂN HƯỚNG RA TRANG CHỦ (Tên blueprint.tên hàm)
            return redirect(url_for('main.index'))
        else:
            msg = 'Incorrect username/password!'
            
    return render_template('login.html', msg=msg) # Bỏ chữ auth/ đi vì file của bạn nằm ở thư mục gốc templates

@main_bp.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('main.login'))

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    mysql = get_db()
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s OR email = %s', (username, email))
        account = cursor.fetchone()
        
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only letters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Sửa lỗi đếm cột bằng cách liệt kê rõ tên cột muốn chèn dữ liệu
            cursor.execute('INSERT INTO users (username, password, email) VALUES (%s, %s, %s)', (username, password, email))
            mysql.connection.commit()
            cursor.close()
            
            # ĐĂNG KÝ XONG -> CHUYỂN HƯỚNG SANG TRANG ĐĂNG NHẬP
            return redirect(url_for('main.login'))
            
        cursor.close()
    return render_template('register.html', msg=msg)

@main_bp.route('/navbar.html')
def navbar():
    # Flask sẽ tìm file navbar.html trong thư mục 'templates' và trả về cho JavaScript
    return render_template('navbar.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

@main_bp.route('/history')
def history():
    return render_template('history.html')