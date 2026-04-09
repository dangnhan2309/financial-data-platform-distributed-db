from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from schemas.product_schema import ProductResponse # Import từ file product schema đã tạo

# 1. Schema cơ sở
class QuotationItemBase(BaseModel):
    quotatition_id : Optional[int] = None
    quantity: float = Field(..., gt=0)
    unit_price: float = Field(..., ge=0)
    discount: Optional[float] = 0.0
    tax_rate: Optional[float] = 0.0
    total_price: Optional[float] = None

# 2. Schema dùng để tạo mới (Cần 2 khóa ngoại)
class QuotationItemCreate(QuotationItemBase):
    quotation_id: int
    product_id: int

# 3. Schema dùng để cập nhật
class QuotationItemUpdate(BaseModel):
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    discount: Optional[float] = None
    tax_rate: Optional[float] = None
    total_price: Optional[float] = None

# 4. Schema trả về dữ liệu (Response)
class QuotationItemResponse(QuotationItemBase):
    quotation_id: int
    product_id: int
    total_price: float # type: ignore

    model_config = ConfigDict(from_attributes=True)

# 5. Schema trả về chi tiết kèm thông tin Sản phẩm
class QuotationItemDetailResponse(QuotationItemResponse):
    product: ProductResponse