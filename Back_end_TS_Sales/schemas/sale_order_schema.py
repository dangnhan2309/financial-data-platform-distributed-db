from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date
from schemas.export_document_set_schema import ExportDocumentSetResponse # Đảm bảo đã import từ file document

# 1. Schema cơ sở
class SaleOrderBase(BaseModel):
    order_date: Optional[date] = None
    delivery_date: Optional[date] = None
    total_amount: Optional[float] = 0.0
    currency: Optional[str] = "USD"
    status: Optional[str] = "Pending"

# 2. Schema dùng khi tạo mới Sale Order
class SaleOrderCreate(SaleOrderBase):
    contract_id: int

# 3. Schema dùng để cập nhật
class SaleOrderUpdate(SaleOrderBase):
    contract_id: Optional[int] = None

# 4. Schema trả về dữ liệu cơ bản
class SaleOrderResponse(SaleOrderBase):
    sale_order_id: int
    contract_id: int

    model_config = ConfigDict(from_attributes=True)

# 5. Schema trả về CHI TIẾT (Bao gồm danh sách chứng từ đi kèm)
class SaleOrderDetailResponse(SaleOrderResponse):
    # Lấy danh sách bộ hồ sơ xuất khẩu liên quan
    document_sets: List[ExportDocumentSetResponse] = []