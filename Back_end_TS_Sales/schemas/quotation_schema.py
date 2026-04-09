from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date, datetime
from schemas.quotation_item_schema import QuotationItemDetailResponse # Đã tạo ở bước trước
from schemas.staff_schema import StaffResponse # Đảm bảo đã có file staff schema
# 1. Schema cơ sở: Chứa các trường thông tin chung
class QuotationBase(BaseModel):
    quotation_date: Optional[date] = None
    expiry_date: Optional[date] = None
    total_amount: Optional[float] = 0.0
    currency: Optional[str] = "USD"
    status: Optional[str] = "Draft"

# 2. Schema dùng khi tạo mới Báo giá
class QuotationCreate(QuotationBase):
    customer_id: int
    staff_id: int

# 3. Schema dùng để cập nhật
class QuotationUpdate(QuotationBase):
    customer_id: Optional[int] = None
    staff_id: Optional[int] = None

# 4. Schema trả về dữ liệu cơ bản
class QuotationResponse(QuotationBase):
    quotation_id: int
    customer_id: int
    staff_id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# 5. Schema trả về CHI TIẾT (Bao gồm danh sách Items)
class QuotationDetailResponse(QuotationResponse):
    # Lồng danh sách sản phẩm trong báo giá
    items: List[QuotationItemDetailResponse] = []
    staff : Optional[StaffResponse] = None
    # Bạn có thể lồng thêm thông tin khách hàng nếu cần hiển thị tên khách
    # customer: Optional[CustomerResponse] = None