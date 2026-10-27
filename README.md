# Chat History AI — Ứng dụng trò chuyện AI có lưu lịch sử

**Chat History AI** là dự án xây dựng ứng dụng trò chuyện với mô hình ngôn ngữ lớn (LLM), sử dụng FastAPI, PostgreSQL, React và TypeScript.

Dự án tập trung vào cách xây dựng một ứng dụng AI có khả năng lưu lịch sử hội thoại, quản lý nhiều cuộc trò chuyện, lựa chọn ngữ cảnh theo ngân sách token và hiển thị câu trả lời của AI dưới dạng Markdown.

- **Tác giả:** PakeNguyen
- **Repository:** [PakeNguyen/Chat-History-AI](https://github.com/PakeNguyen/Chat-History-AI)
- **Trạng thái:** Dự án học tập và xây dựng portfolio AI Engineer

## Mục lục

- [1. Giới thiệu](#1-giới-thiệu)
- [2. Tính năng chính](#2-tính-năng-chính)
- [3. Công nghệ sử dụng](#3-công-nghệ-sử-dụng)
- [4. Kiến trúc hệ thống](#4-kiến-trúc-hệ-thống)
- [5. Cấu trúc thư mục](#5-cấu-trúc-thư-mục)
- [6. Yêu cầu trước khi cài đặt](#6-yêu-cầu-trước-khi-cài-đặt)
- [7. Cài đặt và cấu hình](#7-cài-đặt-và-cấu-hình)
- [8. Chạy dự án bằng Docker Compose](#8-chạy-dự-án-bằng-docker-compose)
- [9. Chạy dự án thủ công trên máy tính](#9-chạy-dự-án-thủ-công-trên-máy-tính)
- [10. Hướng dẫn sử dụng](#10-hướng-dẫn-sử-dụng)
- [11. API và tài liệu Swagger](#11-api-và-tài-liệu-swagger)
- [12. Cơ chế lưu lịch sử hội thoại](#12-cơ-chế-lưu-lịch-sử-hội-thoại)
- [13. Quản lý cơ sở dữ liệu](#13-quản-lý-cơ-sở-dữ-liệu)
- [14. Xử lý lỗi thường gặp](#14-xử-lý-lỗi-thường-gặp)
- [15. Bảo mật](#15-bảo-mật)
- [16. Hướng phát triển](#16-hướng-phát-triển)
- [17. Giấy phép](#17-giấy-phép)

## 1. Giới thiệu

Các ứng dụng trò chuyện AI cần nhiều hơn một giao diện gửi câu hỏi và nhận câu trả lời. Để xây dựng một hệ thống có thể sử dụng lâu dài, ứng dụng cần lưu trữ hội thoại, quản lý dữ liệu, lựa chọn ngữ cảnh phù hợp và giao tiếp với mô hình AI thông qua API.

Chat History AI được xây dựng nhằm thực hành những thành phần cốt lõi này.

Ứng dụng cho phép người dùng tạo cuộc trò chuyện, gửi câu hỏi đến AI, xem lại nội dung đã trao đổi và tiếp tục cuộc trò chuyện dựa trên lịch sử được lưu trong PostgreSQL.

Dự án cũng tìm hiểu cách quản lý ngân sách token nhằm giới hạn lượng lịch sử gửi đến mô hình trong mỗi lần tạo câu trả lời.

## 2. Tính năng chính

- **Trò chuyện với AI:** Gửi câu hỏi và nhận câu trả lời thông qua OpenAI API.
- **Quản lý cuộc trò chuyện:** Tạo mới và xem danh sách các cuộc trò chuyện.
- **Lưu lịch sử hội thoại:** Lưu tin nhắn người dùng và AI trong PostgreSQL.
- **Tiếp tục hội thoại:** Truy xuất lịch sử của cuộc trò chuyện để cung cấp ngữ cảnh cho câu hỏi mới.
- **Quản lý ngân sách token:** Chọn lịch sử phù hợp với giới hạn token được cấu hình.
- **Tạo tiêu đề cuộc trò chuyện:** Có thể tạo tiêu đề dựa trên tin nhắn đầu tiên bằng mô hình AI, theo phần triển khai hiện tại của backend.
- **Hiển thị Markdown:** Hỗ trợ hiển thị nội dung như tiêu đề, danh sách, liên kết và khối mã.
- **REST API:** Xây dựng backend bằng FastAPI.
- **Quản lý schema cơ sở dữ liệu:** Sử dụng Alembic để quản lý các phiên bản thay đổi cấu trúc database.
- **Tổ chức frontend và backend riêng biệt:** Giúp dễ phát triển, bảo trì và mở rộng ứng dụng.

## 3. Công nghệ sử dụng

| Thành phần | Công nghệ |
|---|---|
| Frontend | React, TypeScript, Vite |
| Giao diện | CSS |
| Hiển thị Markdown | React Markdown, remark-gfm |
| Backend | Python, FastAPI |
| Tích hợp LLM | OpenAI API |
| Cơ sở dữ liệu | PostgreSQL |
| ORM | SQLAlchemy |
| Migration database | Alembic |
| Đếm token | tiktoken |
| Đóng gói môi trường | Docker, Docker Compose |
| Quản lý mã nguồn | Git, GitHub |

## 4. Kiến trúc hệ thống

Ứng dụng được tổ chức theo mô hình frontend – backend – database, kết hợp với dịch vụ AI bên ngoài.

```text
┌────────────────────────────────────┐
│         Frontend                   │
│      React + TypeScript            │
│                                    │
│  Giao diện chat                    │
│  Quản lý danh sách hội thoại       │
│  Hiển thị Markdown                 │
└─────────────────┬──────────────────┘
                  │ HTTP / JSON
                  ▼
┌────────────────────────────────────┐
│            Backend                 │
│             FastAPI                │
│                                    │
│  Conversation API                  │
│  Message Management                │
│  Chat History Selection            │
│  Token Budget Management            │
│  OpenAI API Integration            │
└──────────────┬──────────────┬──────┘
               │              │
               ▼              ▼
┌──────────────────────┐  ┌──────────────────────┐
│     PostgreSQL       │  │      OpenAI API      │
│                      │  │                      │
│  Conversations       │  │  Tạo câu trả lời     │
│  Messages            │  │  Tạo tiêu đề         │
└──────────────────────┘  └──────────────────────┘
```

### Luồng xử lý một tin nhắn

1. Người dùng nhập câu hỏi trên giao diện frontend.
2. Frontend gửi yêu cầu đến backend thông qua HTTP API.
3. Backend xác định cuộc trò chuyện và truy xuất lịch sử tin nhắn tương ứng từ PostgreSQL.
4. Hệ thống lựa chọn phần lịch sử phù hợp với ngân sách token.
5. Backend gửi lịch sử đã chọn cùng câu hỏi hiện tại đến OpenAI API.
6. Backend nhận câu trả lời từ mô hình AI.
7. Tin nhắn người dùng và câu trả lời của AI được lưu vào PostgreSQL.
8. Frontend nhận kết quả và hiển thị nội dung cho người dùng.

## 5. Cấu trúc thư mục

```text
Chat-History-AI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── router.py
│   │   │   └── routes/
│   │   │       └── conversations.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   ├── models/
│   │   │   ├── conversation.py
│   │   │   └── message.py
│   │   ├── schemas/
│   │   │   ├── conversation.py
│   │   │   └── message.py
│   │   ├── services/
│   │   │   └── llm.py
│   │   └── main.py
│   ├── migrations/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── alembic.ini
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.tsx
│   │   ├── App.css
│   │   ├── api.ts
│   │   ├── index.css
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── .env.example
├── .gitignore
├── compose.yaml
└── README.md
```

### Vai trò của các thành phần chính

- `backend/app/api/routes/conversations.py`: xử lý các API liên quan đến cuộc trò chuyện và gửi tin nhắn.
- `backend/app/services/llm.py`: tích hợp mô hình AI, đếm token và lựa chọn lịch sử theo ngân sách.
- `backend/app/models/`: định nghĩa các model tương ứng với dữ liệu trong database.
- `backend/app/schemas/`: định nghĩa cấu trúc dữ liệu đầu vào và đầu ra của API.
- `backend/app/db/`: cấu hình kết nối và quản lý phiên làm việc với database.
- `backend/migrations/`: chứa các migration dùng để cập nhật cấu trúc database.
- `frontend/src/App.tsx`: thành phần giao diện chính của ứng dụng.
- `frontend/src/api.ts`: quản lý các yêu cầu từ frontend đến backend.
- `compose.yaml`: cấu hình các dịch vụ chạy bằng Docker Compose.

## 6. Yêu cầu trước khi cài đặt

Cài đặt các công cụ sau:

- Git
- Python 3.11 hoặc phiên bản tương thích với các thư viện của dự án
- Node.js và npm
- PostgreSQL hoặc Docker Desktop kèm Docker Compose
- OpenAI API key có quyền sử dụng mô hình đã cấu hình

Kiểm tra các công cụ trên Windows bằng CMD:

```cmd
git --version
python --version
node --version
npm --version
docker --version
docker compose version
```

Docker chỉ cần thiết nếu em chọn cách chạy bằng Docker Compose. Nếu đã có PostgreSQL hoạt động trên máy, có thể chạy backend và frontend trực tiếp.

## 7. Cài đặt và cấu hình

### 7.1. Tải mã nguồn

```cmd
git clone https://github.com/PakeNguyen/Chat-History-AI.git
cd Chat-History-AI
```

### 7.2. Tạo file môi trường

Sao chép file cấu hình mẫu:

```cmd
copy .env.example .env
```

Sau đó mở file `.env` và điền các thông tin phù hợp với môi trường của em.

- `.env.example`: chứa tên biến và giá trị mẫu, được đưa lên GitHub.
- `.env`: chứa cấu hình thực tế như API key và mật khẩu database, không được commit lên GitHub.

### 7.3. Cấu hình OpenAI API

Trong `.env`, khai báo API key theo đúng tên biến mà dự án sử dụng.

Ví dụ:

```dotenv
OPENAI_API_KEY=your_openai_api_key_here
```

Đây chỉ là giá trị mẫu. Hãy thay bằng API key của em trong file `.env` cục bộ.

API key phải được sử dụng ở backend, không đưa trực tiếp vào mã frontend.

### 7.4. Cấu hình PostgreSQL

Ví dụ định dạng kết nối PostgreSQL:

```dotenv
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE_NAME
```

Trong đó:

- `USER`: tên người dùng database.
- `PASSWORD`: mật khẩu database.
- `HOST`: địa chỉ máy chủ database.
- `PORT`: cổng PostgreSQL, thường là `5432`.
- `DATABASE_NAME`: tên database.

Ví dụ minh họa khi PostgreSQL chạy trực tiếp trên máy:

```dotenv
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/chat_history
```

**Lưu ý:** Ví dụ trên không đảm bảo database đã tồn tại hoặc tài khoản có quyền truy cập. Hãy sử dụng đúng thông tin database mà em đã tạo.

Nếu backend chạy trong Docker container, `localhost` thường chỉ chính container backend. Khi kết nối đến database trong một Compose network, cần sử dụng tên dịch vụ database được khai báo trong `compose.yaml`.

Nếu mật khẩu chứa ký tự đặc biệt như `@`, cần mã hóa URL phù hợp để tránh lỗi phân tích chuỗi kết nối.

### 7.5. Kiểm tra cấu hình

Tên biến môi trường và cách ứng dụng nạp file `.env` cần khớp với:

- `backend/app/core/config.py`
- `.env.example`
- `compose.yaml`

Nếu một biến được khai báo trong `.env` nhưng code không đọc biến đó, ứng dụng sẽ không tự động sử dụng giá trị tương ứng.

## 8. Chạy dự án bằng Docker Compose

Phương pháp này phù hợp khi muốn chạy các dịch vụ đã được định nghĩa trong `compose.yaml`.

### Bước 1: Chuẩn bị môi trường

Đảm bảo Docker Desktop đang hoạt động, đồng thời đã tạo `.env` và cấu hình đúng thông tin kết nối database cùng OpenAI API key.

### Bước 2: Khởi động các dịch vụ

Mở CMD tại thư mục gốc của dự án:

```cmd
docker compose up --build
```

Lệnh này xây dựng image cần thiết và khởi động các dịch vụ được khai báo trong Compose.

Theo dõi log trong terminal để xác nhận backend và các dịch vụ liên quan đã khởi động thành công.

### Bước 3: Dừng ứng dụng

```cmd
docker compose down
```

Lệnh này dừng và xóa các container của dự án. Dữ liệu trong named volume thường được giữ lại.

**Không chạy `docker compose down -v` nếu chưa hiểu rõ tác động**, vì tùy cấu hình, lệnh này có thể xóa volume chứa dữ liệu database.

Các cổng truy cập cụ thể phụ thuộc vào cấu hình trong `compose.yaml`.

## 9. Chạy dự án thủ công trên máy tính

Phương pháp này phù hợp khi phát triển và gỡ lỗi từng thành phần.

### Bước 1: Khởi động PostgreSQL

Khởi động PostgreSQL trên máy hoặc khởi động riêng dịch vụ database bằng Docker.

Đảm bảo database tồn tại và thông tin kết nối trong `.env` là chính xác.

### Bước 2: Tạo môi trường Python

Tại thư mục gốc dự án:

```cmd
python -m venv .venv
```

Kích hoạt môi trường:

```cmd
.venv\Scripts\activate
```

Cài đặt thư viện backend:

```cmd
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
```

Nếu đã có môi trường Python riêng cho dự án, em có thể kích hoạt môi trường đó thay vì tạo môi trường mới.

### Bước 3: Áp dụng migration database

Dự án sử dụng Alembic để quản lý thay đổi cấu trúc database.

Lệnh thường dùng:

```cmd
alembic -c backend\alembic.ini upgrade head
```

Lệnh này áp dụng các migration đến phiên bản mới nhất theo cấu hình Alembic.

**Lưu ý:** Đường dẫn migration và cách nạp biến môi trường phụ thuộc vào `backend/alembic.ini` và `backend/migrations/env.py`. Nếu lệnh trên báo lỗi đường dẫn hoặc không tìm thấy cấu hình, hãy kiểm tra cấu hình thực tế trước khi chạy lại.

### Bước 4: Khởi động backend

Tại thư mục gốc:

```cmd
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 --app-dir backend
```

Hoặc chuyển vào thư mục backend trước:

```cmd
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Khi backend khởi động thành công, mở:

- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

### Bước 5: Cài đặt thư viện frontend

Mở một cửa sổ CMD khác:

```cmd
cd frontend
npm ci
```

Lệnh `npm ci` cài đặt các thư viện theo phiên bản đã được ghi trong `package-lock.json`.

### Bước 6: Khởi động frontend

Trong thư mục `frontend`, chạy:

```cmd
npm run dev
```

Vite sẽ hiển thị địa chỉ truy cập trong terminal. Với cấu hình mặc định thường gặp, địa chỉ có thể là:

http://localhost:5173/

Hãy sử dụng đúng địa chỉ mà terminal thực tế hiển thị.

### Bước 7: Kiểm tra kết nối

Nếu frontend không gọi được backend:

1. Kiểm tra backend có đang chạy hay không.
2. Kiểm tra URL API trong `frontend/src/api.ts`.
3. Kiểm tra cấu hình CORS trong backend.
4. Kiểm tra log của backend và Console/Network trong trình duyệt.

## 10. Hướng dẫn sử dụng

Sau khi backend, database và frontend đã hoạt động:

1. Mở địa chỉ frontend trên trình duyệt.
2. Tạo một cuộc trò chuyện mới.
3. Nhập câu hỏi vào ô soạn tin nhắn.
4. Gửi câu hỏi và chờ AI trả lời.
5. Đọc câu trả lời trong giao diện chat.
6. Chọn cuộc trò chuyện khác trong danh sách hoặc tạo cuộc trò chuyện mới.
7. Tải lại trang để kiểm tra dữ liệu hội thoại đã được lưu và có thể truy xuất lại hay chưa.

Nếu tính năng tạo tiêu đề tự động được bật trong backend, tiêu đề cuộc trò chuyện có thể được tạo dựa trên tin nhắn đầu tiên.

### Một số câu hỏi mẫu

```text
Giải thích cách PostgreSQL lưu trữ các tin nhắn trong một cuộc trò chuyện.
```

```text
Phân biệt system message, user message và assistant message.
```

```text
Viết một ví dụ FastAPI endpoint bằng Python và giải thích từng phần.
```

Nội dung câu trả lời phụ thuộc vào mô hình đã cấu hình, lịch sử được gửi kèm, chất lượng câu hỏi và trạng thái hoạt động của OpenAI API.

## 11. API và tài liệu Swagger

Backend sử dụng FastAPI để cung cấp REST API.

Mở Swagger UI tại:

http://127.0.0.1:8000/docs

Tại đây có thể xem các endpoint thực tế, cấu trúc request/response và thử gọi API.

Các nhóm thao tác chính của ứng dụng bao gồm:

| Nhóm thao tác | Mục đích |
|---|---|
| Quản lý cuộc trò chuyện | Tạo và lấy danh sách hội thoại |
| Quản lý tin nhắn | Truy xuất tin nhắn của một cuộc trò chuyện |
| Gửi câu hỏi cho AI | Gửi câu hỏi và nhận câu trả lời |
| Lưu lịch sử | Lưu tin nhắn người dùng và AI vào database |

Phương thức HTTP, đường dẫn và schema chính xác được xác định trong các router và schema của backend. Hãy dùng Swagger UI để xem đặc tả hiện tại thay vì suy đoán endpoint.

## 12. Cơ chế lưu lịch sử hội thoại

Mô hình ngôn ngữ không tự động ghi nhớ toàn bộ các lần gọi API độc lập. Nếu ứng dụng muốn AI sử dụng thông tin từ các lượt trò chuyện trước, backend cần cung cấp phần ngữ cảnh phù hợp trong request mới.

Trong dự án này, PostgreSQL đóng vai trò lưu trữ lâu dài cho cuộc trò chuyện và tin nhắn.

### Luồng xử lý lịch sử

1. Mỗi cuộc trò chuyện được lưu thành một bản ghi trong database.
2. Các tin nhắn được liên kết với cuộc trò chuyện tương ứng.
3. Khi người dùng gửi câu hỏi mới, backend truy xuất lịch sử của cuộc trò chuyện đó.
4. Hàm lựa chọn lịch sử chọn những tin nhắn phù hợp với ngân sách token.
5. Lịch sử đã chọn cùng câu hỏi mới được gửi đến mô hình AI.
6. Tin nhắn mới và câu trả lời được lưu vào PostgreSQL.

### Tại sao cần ngân sách token?

Cuộc trò chuyện càng dài thì lượng văn bản cần gửi đến mô hình có thể càng lớn. Giới hạn token giúp kiểm soát lượng ngữ cảnh được đưa vào mỗi request.

Token là đơn vị mà mô hình ngôn ngữ sử dụng để xử lý văn bản; một token không tương đương chính xác với một từ hoặc một ký tự.

Chiến lược chọn lịch sử là logic do ứng dụng triển khai. Việc lưu lịch sử không đảm bảo mô hình luôn nhớ mọi chi tiết của toàn bộ cuộc trò chuyện.

### Conversation ID và bảo mật

Conversation ID giúp backend xác định các tin nhắn thuộc về cuộc trò chuyện nào.

Tuy nhiên, ID không thay thế cơ chế xác thực và phân quyền. Nếu triển khai cho nhiều người dùng, backend cần xác minh quyền sở hữu cuộc trò chuyện trên từng endpoint để ngăn người dùng truy cập dữ liệu của người khác.

## 13. Quản lý cơ sở dữ liệu

Dự án sử dụng SQLAlchemy để làm việc với database và Alembic để quản lý các thay đổi schema.

Lệnh áp dụng migration đến phiên bản mới nhất:

```cmd
alembic -c backend\alembic.ini upgrade head
```

Lệnh này cần được chạy từ thư mục mà cấu hình Alembic hỗ trợ. Nếu cấu hình đường dẫn tương đối, hãy kiểm tra `backend/alembic.ini` và `backend/migrations/env.py`.

Trước khi áp dụng migration vào database chứa dữ liệu quan trọng, nên xem lại nội dung migration và sao lưu dữ liệu khi cần thiết.

## 14. Xử lý lỗi thường gặp

### 14.1. Lỗi xác thực OpenAI API

Nguyên nhân có thể là:

- API key không đúng hoặc đã bị thu hồi.
- Tài khoản chưa có quyền sử dụng mô hình.
- Hết quota hoặc có vấn đề về billing.
- Tên mô hình cấu hình không hợp lệ.

Cách xử lý:

1. Kiểm tra biến môi trường trong `.env`.
2. Xác nhận code backend đang đọc đúng biến.
3. Kiểm tra quyền sử dụng mô hình và hạn mức API.
4. Không đăng API key lên GitHub hoặc gửi trong log công khai.

### 14.2. Không kết nối được PostgreSQL

Kiểm tra:

- PostgreSQL đã khởi động chưa.
- Database đã tồn tại chưa.
- Username, password, host và port có đúng không.
- Backend đang chạy trên máy thật hay trong Docker container.
- `DATABASE_URL` có được nạp vào ứng dụng không.

### 14.3. Frontend không kết nối được backend

Kiểm tra:

- Backend có chạy tại cổng đã cấu hình không.
- URL API trong `frontend/src/api.ts` có chính xác không.
- CORS có cho phép origin của frontend không.
- Console và Network trong trình duyệt có thông báo lỗi gì không.

### 14.4. Database chưa có bảng

Kiểm tra cấu hình Alembic, migration và database URL. Đảm bảo migration được áp dụng vào đúng database mà backend đang sử dụng.

### 14.5. Cổng đã được sử dụng

Nếu cổng đang bị một ứng dụng khác chiếm dụng, hãy dừng ứng dụng đó hoặc thay đổi cổng và cập nhật các cấu hình liên quan.

## 15. Bảo mật

- Không commit file `.env` có chứa API key hoặc mật khẩu thật.
- Chỉ sử dụng giá trị giả trong `.env.example`.
- Không đưa API key OpenAI vào mã frontend.
- Không trả stack trace hoặc thông tin bí mật trong response gửi đến người dùng.
- Kiểm tra dữ liệu đầu vào và xử lý lỗi từ dịch vụ bên ngoài.
- Hạn chế quyền truy cập database theo nhu cầu thực tế.
- Bổ sung xác thực và phân quyền theo người dùng trước khi triển khai hệ thống nhiều người dùng.
- Rà soát các dependency và cập nhật khi cần thiết.

## 16. Hướng phát triển

Các hướng nâng cấp có thể thực hiện trong những phiên bản tiếp theo:

- Xác thực người dùng và phân quyền theo cuộc trò chuyện.
- Tối ưu chiến lược quản lý ngữ cảnh dài bằng tóm tắt lịch sử.
- Hỗ trợ streaming để hiển thị câu trả lời từng phần.
- Cải thiện retry và xử lý lỗi từ OpenAI API.
- Mở rộng kiểm thử API và database.
- Bổ sung chức năng tìm kiếm, xuất và xóa cuộc trò chuyện.
- Triển khai ứng dụng lên một nền tảng hosting phù hợp.
- Bổ sung ảnh chụp giao diện và video demo.

Đây là các hướng phát triển dự kiến, không phải khẳng định rằng những tính năng này đã được triển khai.

## 17. Giấy phép

Hiện dự án chưa khai báo giấy phép sử dụng mã nguồn.

Nếu muốn cho phép người khác sử dụng, sửa đổi hoặc phân phối mã nguồn theo các điều kiện cụ thể, hãy chọn một giấy phép phù hợp và thêm file `LICENSE` vào repository.

Việc repository ở chế độ Public không tự động có nghĩa là mã nguồn được cấp phép sử dụng tự do.

---

**Tác giả:** PakeNguyen

**GitHub:** [PakeNguyen](https://github.com/PakeNguyen)

**Dự án:** [Chat-History-AI](https://github.com/PakeNguyen/Chat-History-AI)
