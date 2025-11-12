# Hệ thống quản lý SPKH - Flask (no DB)

Phiên bản: không dùng cơ sở dữ liệu, dữ liệu lưu trong file JSON (`data.json`).

## Đặc điểm
- Authentication: đăng nhập (mặc định username=admin, password=ChangeMe123).
- Lưu đề tài vào `data.json` trong root project.
- Không cần cài DB, phù hợp deploy nhanh lên Render (Web service).

## Cách deploy (Render)
1. Tạo Web Service (Python) trên Render.
2. Push mã nguồn vào repo hoặc upload ZIP.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app` (Procfile có sẵn).
5. Mở site, truy cập `/login` và đăng nhập với tài khoản mặc định.

## Bảo mật
- Hãy đổi mật khẩu admin ngay sau khi deploy.