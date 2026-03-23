# Sử dụng image Python chính thức (bản nhẹ)
FROM python:3.11-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Ngăn Python tạo file .pyc và hỗ trợ log hiển thị ngay lập tức
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Cài đặt các thư viện hệ thống cần thiết (nếu bạn dùng Postgres hoặc các thư viện C)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements và cài đặt thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào container
COPY . .

# Mở port (thông thường là 8000 cho API)
EXPOSE 8000

# Lệnh chạy ứng dụng (Ví dụ cho FastAPI dùng Uvicorn)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]