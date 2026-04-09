# 🔗 API Integration Guide - TS_SALES Frontend

## 📋 Tình trạng hiện tại
- ✅ Frontend structure: Complete
- ✅ Mock data: Tất cả modules đều có mock data
- ⏳ Backend API: Chờ hoàn thành Oracle procedures/functions
- 🔄 Integration: Sẵn sàng để swap mock data → real API

---

## 🗂 Mock Data Location

| Module | Mock File | Exports |
|--------|-----------|---------|
| **Master Data** | `src/modules/master_data/models/mock-data.ts` | `mockCustomers`, `mockStaff`, `mockProducts`, `mockPaymentTerms`, `mockIncoterms` |
| **Quotation** | `src/modules/quotation/models/mock-data.ts` | `mockQuotations`, `mockQuotationItems` |
| **Proforma Invoice** | Module file | `mockProformaInvoices` |
| **Contract** | Module file | `mockContracts` |
| **Sale Order** | Module file | `mockSaleOrders` |
| **Export Document** | Module file | `mockExportDocs` |

---

## 🔌 API Client Setup

Location: `src/core/services/api-client.ts`

```typescript
// Centralized Axios instance với auth interceptor
// Base URL: process.env.NEXT_PUBLIC_API_BASE_URL (default: http://localhost:8000)
// Timeout: 30000ms
// Headers: Content-Type: application/json
```

---

## 📡 Expected Backend Endpoints

### **Quản lý Khách hàng**
```
GET    /api/customers              → Danh sách khách hàng
GET    /api/customers/:id          → Chi tiết khách hàng
POST   /api/customers              → Thêm khách hàng
PUT    /api/customers/:id          → Cập nhật khách hàng
DELETE /api/customers/:id          → Xóa khách hàng
```

### **Báo giá Kỹ thuật**
```
GET    /api/quotations             → Danh sách báo giá
GET    /api/quotations/:id         → Chi tiết báo giá
POST   /api/quotations             → Tạo báo giá mới
PUT    /api/quotations/:id         → Cập nhật báo giá
GET    /api/quotations/:id/items   → Items của báo giá
POST   /api/quotations/:id/items   → Thêm item vào báo giá
```

### **Hóa đơn Proforma**
```
GET    /api/proforma-invoices      → Danh sách hóa đơn
POST   /api/proforma-invoices      → Tạo hóa đơn từ quotation
PUT    /api/proforma-invoices/:id  → Cập nhật hóa đơn
```

### **Hợp đồng**
```
GET    /api/contracts              → Danh sách hợp đồng
POST   /api/contracts              → Tạo hợp đồng mới
PUT    /api/contracts/:id          → Cập nhật hợp đồng
```

### **Đơn hàng**
```
GET    /api/sale-orders            → Danh sách đơn hàng
POST   /api/sale-orders            → Tạo đơn hàng
PUT    /api/sale-orders/:id        → Cập nhật đơn hàng
```

### **Chứng từ Xuất khẩu**
```
GET    /api/export-documents       → Danh sách chứng từ
PUT    /api/export-documents/:id   → Cập nhật trạng thái chứng từ
```

---

## 🔄 Cách thay đổi từ Mock → Real Data

### Step 1: Tạo API Service Hook
```typescript
// src/modules/quotation/controllers/useQuotation.ts
export function useQuotations() {
    const { data, isLoading, error } = useSWR('/api/quotations', apiClient.get);
    return { quotations: data, isLoading, error };
}
```

### Step 2: Update View Component
```typescript
// src/modules/quotation/views/QuotationDashboard.tsx
import { useQuotations } from '../controllers/useQuotation';

export default function QuotationDashboard() {
    const { quotations, isLoading } = useQuotations();
    
    // Replace mockQuotations → quotations
    return <DataTable data={quotations} isLoading={isLoading} />;
}
```

### Step 3: Environment Configuration
```env
# .env.local
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_TIMEOUT=30000
```

---

## 📦 Dependency cần thiết

```json
// Đã có sẵn trong package.json
{
  "axios": "^1.6.0",
  "react-hook-form": "^7.0.0",
  "zod": "^3.0.0"
}
```

---

## ✅ Pre-integration Checklist

Trước khi kết nối Oracle API:

- [ ] Oracle procedures/functions đã được tạo
- [ ] Test API endpoints bằng Postman/Curl
- [ ] Response format match với TypeScript interfaces
- [ ] Error handling được define
- [ ] CORS configured trên backend

---

## 📝 TypeScript Interfaces

Location: `src/core/services/types.ts`

Tất cả các interfaces đã được define sẵn:
- `Customer`, `Staff`, `Product`, `PaymentTerm`, `Incoterm`
- `Quotation`, `QuotationItem`
- `ProformaInvoice`, `Contract`, `SaleOrder`
- `ExportDocument`, `Shipment`

---

## 🚀 Integration Timeline

| Phase | Status | Target |
|-------|--------|--------|
| **Phase 1** | ✅ Frontend + Mock Data | April 2026 |
| **Phase 2** | ⏳ Oracle Procedures/Functions | April 2026 |
| **Phase 3** | ⏳ Backend FastAPI Integration | May 2026 |
| **Phase 4** | ⏳ Real Data Integration | May 2026 |

---

## 📞 Support

Khi hoàn thành Oracle backend, hãy contact frontend team để:
1. Update environment variables
2. Replace mock data imports
3. Test API integration
4. Deploy to production

---

**Last Updated:** April 9, 2026
