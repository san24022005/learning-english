from app import create_app

# Gọi hàm tạo ứng dụng từ thư mục app
app = create_app()

if __name__ == '__main__':
    # Chạy ứng dụng
    app.run(debug=True)
