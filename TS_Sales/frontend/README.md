# GC Food TS_SALES Frontend

Hệ thống Frontend để quản lý bán hàng xuất khẩu của Tập đoàn GC Food (VietFarm & VinaCoco).

## 🚀 Starting

### Prerequisites
- Node.js 18+ 
- npm hoặc yarn

### Installation

```bash
cd frontend
npm install
# hoặc
yarn install
```

### Development

```bash
npm run dev
# hoặc
yarn dev
```

Truy cập: http://localhost:3000

### Build for Production

```bash
npm run build
npm run start
```

## 📦 Project Structure

```
src/
├── app/                          # Next.js App Router
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Public landing page
│   ├── globals.css              # Global styles
│   └── dashboard/               # Dashboard routing
│
├── core/                        # Shared code
│   ├── components/              # Reusable components (DataTable, etc)
│   ├── layouts/                 # DashboardLayout, PublicLayout
│   ├── services/                # API client, types, mock data
│   └── utils/                   # Formatters, validation schemas
│
└── modules/                     # Feature modules (MVC)
    ├── public_site/             # Landing page
    ├── master_data/             # Staff, Customer, Product, PaymentTerm, Incoterm
    ├── quotation/               # Báo giá kỹ thuật (avec Specifications)
    ├── proforma_invoice/        # Hóa đơn tạm tính
    ├── contract/                # Hợp đồng khung
    ├── sale_order/              # Đơn hàng
    ├── export_document/         # Bộ chứng từ XK
    └── oracle_execution/        # Oracle DB execution hub
```

## 🎨 Tech Stack

- **Frontend Framework:** Next.js 14 + React 18 + TypeScript
- **Styling:** Tailwind CSS 3 + PostCSS
- **Form Management:** React Hook Form + Zod Validation
- **HTTP Client:** Axios
- **API Integration:** Configurable API client with interceptors

## 📋 Key Features

### 1. Public Website
- Hero Banner với thông tin GC Food
- Giới thiệu VietFarm (Nha đam) & VinaCoco (Thạch dừa)
- Danh sách sản phẩm
- Form liên hệ
- Footer với thông tin liên lạc

### 2. Dashboard - Master Data Management
- **Staff:** Quản lý nhân viên (Họ tên, VỊ trí, Email, Phòng ban, Status)
- **Customers:** Quản lý khách hàng B2B (Tên, Địa chỉ, Quốc gia, Email, Status)
- **Products:** Quản lý sản phẩm (Loại, Giá, Brix, pH, Mesh Size)
- **Payment Terms:** Quản lý Điều khoản thanh toán (Net 30, Net 60, etc)
- **Incoterms:** Quản lý Incoterm (FOB, CIF, EXW, etc)

### 3. Quotation Management (Báo giá Kỹ thuật)
- Tạo báo giá từ Customer + Staff + Product
- **Master-Detail Form:** Thêm nhiều sản phẩm vào báo giá
- **Specifications:** BẮT BUỘC nhập `Brix (%)`, `pH`, `Mesh Size` cho từng item
- Pipeline trạng thái: `Draft → Sent → Interested → Sampling → Closed/Won`
- Hiển thị tổng giá trị báo giá

### 4. Proforma Invoice (Hóa đơn Tạm tính)
- Tạo PI từ Quotation với 1 click "Auto-fill"
- Chọn Payment Term và Staff
- Nhập Port of Loading/Discharge
- Hiển thị chi tiết Quotation Items

### 5. Contract Management (Hợp đồng)
- Tạo Hợp đồng từ Proforma Invoice
- Chọn Incoterm, Loading Port, Destination Port
- Quản lý trạng thái Hợp đồng (Active, Pending, Closed)
- Thống kê tổng số lượng & giá trị

### 6. Sale Order (Đơn hàng)
- Tạo Sale Order từ Hợp đồng
- Lưu Ngày lệnh, Ngày giao hàng
- Theo dõi trạng thái: Confirmed → Shipped → Delivered
- Thống kê đơn hàng theo trạng thái

### 7. Export Document Management (Bộ Chứng từ XK)
- **Kanban Board:** 3 cột (Pending, Issued, Completed)
- Quản lý các chứng từ:
  - 🏛️ **Certificate of Origin (C/O)**
  - 🇻🇳 **Customs Declaration (CQ)**
  - 📦 **Packing List**
  - ⛴️ **Bill of Lading (B/L)**
- Tải file chứng từ từ dashboard

### 8. Oracle Execution Hub (Công cụ DB - Admin Only)
- **Tabs:** Procedures, Functions, Packages, Indexes, Triggers, Sequences
- Hiển thị danh sách Oracle Objects
- Dynamic Form nhập tham số đầu vào
- Terminal-style JSON result viewer
- Query Builder để soạn thảo SQL tuỳ ý

## 🔌 API Integration

Tất cả API calls thông qua `apiClient` centralized:

```typescript
import { apiClient } from '@core/services/api-client';

// GET
const { data } = await apiClient.get<Customer[]>('/api/customers');

// POST
await apiClient.post('/api/quotations', quotationData);

// PUT
await apiClient.put(`/api/quotations/${id}`, updatedData);

// DELETE
await apiClient.delete(`/api/quotations/${id}`);
```

**Base URL:** Từ `NEXT_PUBLIC_API_BASE_URL` (default: http://localhost:8000)

## 🎯 Workflow (Luồng Chứng từ)

```
Customer + Staff 
    ↓
Quotation (với Specifications)
    ↓
Proforma Invoice
    ↓
Contract (với Incoterm)
    ↓
Sale Order (nhiều từ 1 Contract)
    ↓
Export Documents (C/O, CQ, PL, B/L)
```

## 🔐 Authentication

- Token lưu trong `localStorage`
- Auto-attach vào request header: `Authorization: Bearer <token>`
- Auto-redirect đến login nếu 401

## 📱 Responsive Design

- Mobile-first approach
- Desktop-optimized Dashboard
- Tailwind CSS breakpoints

## 🚀 Deployment

### Vercel (Recommended)
```bash
npm install -g vercel
vercel
```

### Docker
```bash
docker build -t gc-food-ts-sales .
docker run -p 3000:3000 gc-food-ts-sales
```

## 📚 Environment Variables

Tạo file `.env.local`:

```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_TIMEOUT=30000
```

## 🐛 Troubleshooting

- **Module not found:** Kiểm tra `tsconfig.json` paths
- **Tailwind styles không load:** Chạy `npm run build` lại
- **API 401:** Kiểm tra token trong localStorage

## 📖 Documentation

Xem thêm:
- [Next.js Docs](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [React Hook Form](https://react-hook-form.com/)
- [Zod Validation](https://zod.dev/)

---

**Version:** 1.0.0  
**Last Updated:** Jan 2025  
**GC Food Development Team**
