# Learning English

Phiên bản: 1.2.1

---

Dự án học tiếng Anh nhỏ dùng Flask cho backend và JavaScript cho frontend. Backend hiện cung cấp:
- API phục vụ bài học từ file `lessons.json`
- Trang index hiển thị 5 lesson mỗi trang với phân trang
- Xác thực đơn giản qua login/logout

---

## Yêu cầu

- Python 3.8+
- Pip
- MySQL (XAMPP) nếu bạn dùng tính năng đăng nhập/đăng ký

## Cài đặt nhanh

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Mở trình duyệt: `http://localhost:5000/`

---

## Cấu trúc dự án

- `run.py` — entrypoint Flask
- `lessons.json` — dữ liệu bài học
- `app/`
  - `__init__.py` — tạo app và đăng ký blueprint
  - `routes.py` — route frontend và login/logout/register
  - `api/` — REST API endpoints
    - `__init__.py` — shared `api_bp`
    - `lesson.py` — lesson endpoints
    - `info.py` — session info endpoint
  - `static/` — CSS, JS, images
  - `templates/` — HTML templates
- `tests/` — kiểm thử đơn giản

---

## API hiện tại

Tất cả endpoint bắt đầu bằng `/api`.

- `GET /api/lessons`
  - Trả về toàn bộ danh sách lesson từ `lessons.json`.
  - Response mẫu:
    ```json
    {
      "success": true,
      "total_lessons": 126,
      "data": [ ... ]
    }
    ```

- `GET /api/lesson/<lesson_id>`
  - Trả về bài học cụ thể theo `lesson_id`.
  - Ví dụ: `GET /api/lesson/1`

- `GET /api/info`
  - Trả về thông tin người dùng hiện tại nếu đã login.
  - Response mẫu:
    ```json
    {
      "success": true,
      "username": "...",
      "level": 1
    }
    ```

---

## Frontend

- Trang chính là `app/templates/index.html`.
- Script `app/static/js/load-lesson.js` gọi `GET /api/lessons` và hiển thị 5 lesson mỗi trang.
- Nút `« Trước` và `Tiếp »` điều hướng trang.
- Level hiện tại của người dùng được lấy từ session và đưa vào trang để xác định page ban đầu.

---

## Login / Session

- `app/routes.py` xử lý login, logout, register.
- `session['loggedin']` và `session['level']` được dùng để xác thực và xác định level.
- Endpoint `GET /api/info` trả về `username` và `level` khi session hợp lệ.

---

## Chỉnh sửa dữ liệu bài học

- Dữ liệu bài học chính là `lessons.json`.
- Mỗi lesson chứa trường `lesson` và `questions`.
- Thay đổi file này cần khởi động lại server để cập nhật dữ liệu nếu dùng cache nhớ.

---

## Cần sửa nếu muốn mở rộng

- Nếu muốn xài thêm API mới, tạo file mới trong `app/api` và dùng `api_bp` chung.
- Nếu muốn dùng DB thay vì JSON, chuyển `lessons.json` sang database và viết query tương ứng.
- Nếu muốn hiển thị thêm thông tin lesson, cập nhật `app/static/js/load-lesson.js` và template `index.html`.

---

## Gợi ý kiểm thử nhanh

- Kiểm tra API lesson:
  ```bash
  curl http://localhost:5000/api/lessons
  curl http://localhost:5000/api/lesson/1
  ```
- Kiểm tra info nếu đã login:
  ```bash
  curl http://localhost:5000/api/info
  ```

---

## Liên hệ

- Tác giả: Siu San
- Email: siusan2005@gmail.com



