# Chat History AI — Giai đoạn 1

FastAPI + SQLAlchemy + Alembic + PostgreSQL. Chưa tích hợp LangChain/OpenAI hoặc frontend ở giai đoạn này.

## Chạy trên Windows
1. Cài và mở Docker Desktop.
2. Copy `.env.example` thành `.env`.
3. Mở terminal tại thư mục dự án và chạy:

```powershell
docker compose up --build -d
docker compose exec backend alembic upgrade head
```

4. Mở:
- Health: http://localhost:8000/health
- Swagger: http://localhost:8000/docs

## Thử API trong Swagger
1. `POST /api/v1/conversations`, body `{"title":"Chat thử đầu tiên"}`. Copy `id` trong response.
2. `GET /api/v1/conversations` để xem danh sách.
3. `POST /api/v1/conversations/{id}/messages`, body `{"content":"Xin chào, đây là tin nhắn thử."}`.
4. `GET /api/v1/conversations/{id}/messages` để xem lịch sử.

## Database
Mặc định dùng PostgreSQL local trong Docker Compose. `DATABASE_URL` dùng dạng SQLAlchemy:
`postgresql+psycopg://USER:PASSWORD@HOST:PORT/DATABASE`

Trong Compose, hostname local là `db`. Nếu chạy backend trực tiếp trên Windows, thường dùng `localhost`. Muốn dùng Supabase, thay `DATABASE_URL` bằng connection URL Supabase đã đổi prefix sang `postgresql+psycopg://`. URL-encode ký tự đặc biệt trong mật khẩu.

`docker compose down` giữ dữ liệu. Không dùng `docker compose down -v` nếu muốn giữ volume database.

## Chưa phải production public
Giai đoạn này chưa có đăng nhập, phân quyền theo người dùng, gọi LLM hoặc giới hạn truy cập. Không public API lên Internet trước khi bổ sung các lớp này. Không commit `.env` hoặc secrets lên GitHub.
