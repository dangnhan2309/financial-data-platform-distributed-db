# GC Food TS_SALES Frontend Development Guide

## 🚀 Hướng dẫn Chạy Project

### Yêu cầu Hệ thống
- **Node.js:** v18 hoặc cao hơn
- **npm:** v9+ hoặc yarn v3+
- **OS:** Windows, macOS, hoặc Linux

### Bước 1: Chuẩn bị Environment

#### Windows (PowerShell)
```powershell
# Kiểm tra Node.js
node --version
npm --version

# Di chuyển đến thư mục frontend
cd d:\PROJECT_GCFOOD\financial-data-platform-distributed-db\TS_Sales\frontend
```

#### macOS/Linux (Bash)
```bash
node --version
npm --version

cd /path/to/TS_Sales/frontend
```

### Bước 2: Cài đặt Dependencies

```bash
# Dùng npm
npm install

# Hoặc dùng yarn (nếu có)
yarn install

# Hoặc dùng pnpm (nếu có)
pnpm install
```

Quá trình này sẽ cài đặt tất cả package cần thiết từ file `package.json`.
Thời gian: ~2-5 phút (tùy tốc độ internet)

### Bước 3: Cấu hình Environment Variables

Tạo hoặc chỉnh sửa file `.env.local`:

```bash
# Windows
copy .env.example .env.local
# Hoặc mở file .env.local trong editor và thêm:

# macOS/Linux
cp .env.example .env.local
```

Nội dung `.env.local`:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_TIMEOUT=30000
```

### Bước 4: Chạy Development Server

```bash
npm run dev
```

Output sẽ hiển thị:

```
  ▲ Next.js 14.0.0
  - Local:        http://localhost:3000
  - Environments: .env.local

✓ Ready in 3.2s
```

### Bước 5: Truy cập Ứng dụng

- **Public Website (Landing Page):** http://localhost:3000
- **Dashboard Home:** http://localhost:3000/dashboard
- **Master Data:** http://localhost:3000/dashboard/master-data
- **Quotation:** http://localhost:3000/dashboard/quotation
- **Proforma Invoice:** http://localhost:3000/dashboard/proforma-invoice
- **Contract:** http://localhost:3000/dashboard/contract
- **Sale Order:** http://localhost:3000/dashboard/sale-order
- **Export Document:** http://localhost:3000/dashboard/export-document
- **Oracle Execution:** http://localhost:3000/dashboard/oracle-execution

## 🛑 Dừng Development Server

Nhấn `Ctrl + C` trong terminal (hoặc `Cmd + C` trên macOS)

## 🏗️ Build cho Production

```bash
npm run build
npm start
```

Production server sẽ chạy ở port 3000 (tối ưu hơn development)

## 🌐 Kết nối Backend API

Backend FastAPI có thể chạy tại:
- **Development:** http://localhost:8000
- **Production:** Cập nhật `NEXT_PUBLIC_API_BASE_URL` trong `.env.local`

### Kiểm tra Kết nối API

Tất cả HTTP requests tự động sẽ gửi đến backend qua `apiClient`:

```typescript
// Ví dụ trong component
const { data } = await apiClient.get('/api/customers');
```

## 🐛 Debug & Troubleshooting

### 1. "Module not found" Error
```bash
# Xóa node_modules và cài lại
rm -r node_modules
npm install
```

### 2. Tailwind CSS không load
```bash
# Rebuild project
npm run build
npm run dev
```

### 3. Port 3000 đã được dùng
```bash
# Chạy ở port khác
npm run dev -- -p 3001
```

### 4. API Connection Error
- Kiểm tra `NEXT_PUBLIC_API_BASE_URL` trong `.env.local`
- Chắc chắn Backend FastAPI đang chạy
- Kiểm tra CORS configuration trên Backend

## 📁 Cấu trúc Thư mục Quan trọng

```
frontend/
├── src/
│   ├── app/              # Next.js pages & routing
│   ├── core/             # Shared components, layouts, services
│   └── modules/          # Feature modules
├── public/               # Static assets
├── package.json          # Dependencies
├── tsconfig.json         # TypeScript config
├── tailwind.config.ts    # Tailwind configuration
├── next.config.js        # Next.js configuration
└── .env.local           # Environment variables (local)
```

## 🔑 Các Lệnh Chính

```bash
# Development
npm run dev              # Chạy dev server (auto-reload)

# Production
npm run build           # Build project cho production
npm start              # Start production server

# Lint & Code Quality
npm run lint           # Chạy ESLint để check code quality

# Clean
rm -r .next           # Xóa build cache
rm -r node_modules    # Xóa dependencies (Windows: rmdir /s node_modules)
```

## 📱 Testing Pages Locally

Sau khi chạy `npm run dev`, có thể test các pages:

### Public Site (Landing Page)
- http://localhost:3000
- Page mô tả GC Food, VietFarm, VinaCoco
- Form liên hệ

### Dashboard
- http://localhost:3000/dashboard
- Thống kê tổng quan
- 4 cards: Báo giá, Hóa đơn, Hợp đồng, Đơn hàng
- Charts thống kê

### Modules với Mock Data
- Tất cả pages đều có **mock data** sẵn
- Có thể tạo, xem, xóa (chỉ trong memory, không lưu vào DB thực)
- UI/UX đã hoàn thiện, chỉ cần kết nối API Backend

## 🔌 API Endpoints Expected

Backend cần cung cấp các endpoints:

```
GET    /api/customers
GET    /api/customers/{id}
POST   /api/customers
PUT    /api/customers/{id}
DELETE /api/customers/{id}

GET    /api/quotations
POST   /api/quotations
GET    /api/quotations/{id}
PUT    /api/quotations/{id}

GET    /api/proforma-invoices
POST   /api/proforma-invoices
# ... và các endpoints khác
```

## 📦 Production Deployment

### Option 1: Vercel (Recommended for Next.js)
```bash
npm install -g vercel
vercel login
vercel
```

### Option 2: Docker
```bash
docker build -t gc-food-frontend .
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_BASE_URL=https://api.example.com \
  gc-food-frontend
```

### Option 3: Traditional Server
```bash
npm run build
npm start
# Chạy với PM2 hoặc systemd service
```

## 📞 Support & Contact

- **Developer:** GC Food Development Team
- **GitHub:** [Repository URL]
- **Issues:** Report bugs tại Issues section

---

**Last Updated:** January 2025  
**Version:** 1.0.0
