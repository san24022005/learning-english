# Learning English 

Phiên bản: 1.2.1

---

Mục tiêu: dự án nhỏ dùng để học và thực hành xây dựng REST API bằng Flask cho phần backend, và sử dụng JavaScript (Fetch API) phía frontend để lấy dữ liệu và hiển thị.

Nội dung README này mô tả cách cài đặt, cấu trúc dự án, API endpoints và cách phát triển mở rộng.

## **Những điểm đã sửa/chuẩn hóa**
- Tách phần API vào thư mục `app/api` (Blueprint Flask).
- Thêm helper đọc `words.json` từ `app/data.py`.
- Frontend bây giờ gọi `GET /api/words` (và các endpoint khác) thay vì gọi trực tiếp JSON Server.
- Đã loại bỏ các thông tin nhạy cảm (SĐT, mã sinh viên) khỏi file công khai. (Email giữ lại nếu bạn muốn liên hệ.)

---

## **Yêu cầu**
- Python 3.10+ (hoặc 3.8+)
- `pip` để cài package

## **Cài đặt nhanh (local)**

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

Mở trình duyệt: http://localhost:5000/

---

## **Cấu trúc chính của dự án**

- `run.py` — entrypoint để chạy Flask app
- `words.json` — dữ liệu từ vựng mẫu (tĩnh)
- `app/` — package Flask
    - `__init__.py` — tạo app và đăng ký Blueprints
    - `routes.py` — route phục vụ frontend (template)
    - `data.py` — helper đọc `words.json`
    - `api/words.py` — Blueprint REST API (các endpoint)
    - `static/` — CSS, JS, images
    - `templates/` — HTML templates

---

## **API (REST) — Endpoints**

Tất cả các endpoint bắt đầu bằng tiền tố `/api` (Blueprint `api_bp`).

- `GET /api/words`
    - Mô tả: trả về danh sách tất cả từ vựng (JSON array).
    - Ví dụ:
        ```bash
        curl http://localhost:5000/api/words
        ```

- `GET /api/words/<id>`
    - Mô tả: lấy chi tiết một từ theo `id`.
    - Ví dụ:
        ```bash
        curl http://localhost:5000/api/words/1
        ```

- `GET /api/quiz`
    - Mô tả: trả về một từ ngẫu nhiên đã bị xáo trộn (scrambled) cùng `meaning` và `id`.
    - Ví dụ:
        ```bash
        curl http://localhost:5000/api/quiz
        ```

- `POST /api/check`
    - Mô tả: kiểm tra đáp án. Gửi body JSON: `{ "id": <number>, "answer": "..." }`.
    - Trả về JSON `{ "is_correct": true|false, "message": "..." }`.
    - Ví dụ:
        ```bash
        curl -X POST http://localhost:5000/api/check -H "Content-Type: application/json" -d '{"id":1, "answer":"apple"}'
        ```

---

## **Frontend**

Frontend dùng file template `app/templates/index.html` và script `app/static/js/load-words.js`.
- Khi trang được load, `load-words.js` sẽ gọi `/api/words` (fetch) và hiển thị từ ngẫu nhiên cho người dùng.

Nếu bạn muốn chuyển sang gọi `GET /api/quiz` thay vì lấy toàn bộ `words`, sửa `load-words.js` để gọi endpoint đó.

---

## **Thêm/Chỉnh sửa dữ liệu từ vựng**

File dữ liệu chính là `words.json`. Mỗi mục là object với cấu trúc:

```json
{
    "id": 1,
    "word": "apple",
    "meaning": "Quả táo"
}
```

Bạn có thể thêm/bớt chỉnh trực tiếp file này; khi thay đổi, server Flask cần khởi động lại để load dữ liệu mới (do hiện tại helper đọc file trên mỗi request — nếu muốn tối ưu, có thể cache hoặc kết nối DB).

---

## **CORS / Truy cập từ domain khác**

Hiện tại API và frontend được phục vụ từ cùng một Flask app (cùng origin), nên không cần cấu hình CORS. Nếu bạn tách frontend ra host ở origin khác, cài thêm `flask-cors`:

```bash
pip install flask-cors
```

Và đăng ký trong `app/__init__.py`:

```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
```

---

## **Phát triển & Mở rộng**

- Để thêm API mới, tạo file mới trong `app/api` và khai báo Blueprint, sau đó `app.register_blueprint()` trong `create_app()` (`app/__init__.py`).
- Khi dự án lớn hơn, cân nhắc dùng database (SQLite/Postgres) thay vì file JSON.
- Dự án đã có thêm 3 thư mục mới cho hướng phát triển AI/ML:
  - `tests/` — chứa các bài kiểm thử đơn giản cho mô hình.
  - `data/` — nơi lưu dữ liệu huấn luyện và dữ liệu chuẩn bị.
  - `preprocessing/` — chứa mô hình và tiền xử lý dữ liệu đơn giản.
- Endpoint mới: `GET /api/recommend` dùng mô hình AI nhẹ để gợi ý từ phù hợp với mức độ học viên.

---

## **Chạy tests / kiểm thử nhanh**

Bạn có thể kiểm thử các endpoint bằng `curl` hoặc Postman.

Ví dụ kiểm tra quiz và check:

```bash
curl http://localhost:5000/api/quiz
curl -X POST http://localhost:5000/api/check -H "Content-Type: application/json" -d '{"id":1,"answer":"apple"}'
```

---

## **Góp ý & Liên hệ**

- Tác giả: Siu San
- Email: siusan2005@gmail.com

---

## **License**



