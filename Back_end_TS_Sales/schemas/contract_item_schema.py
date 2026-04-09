from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from .product_schema import ProductResponse

# Schema cơ bản chứa các trường chung
class ContractItemBase(BaseModel):
    quantity: float = Field(..., gt=0, description="Số lượng phải lớn hơn 0")
    unit_price: float = Field(..., ge=0)
    discount: Optional[float] = 0.0
    tax_rate: Optional[float] = 0.0

# Schema dùng để nhận dữ liệu từ Client khi tạo mới
class ContractItemCreate(ContractItemBase):
    contract_id: int
    product_id: int
    # Lưu ý: total_price thường được tính toán ở Server nên không nhất thiết phải bắt Client gửi lên
    total_price: Optional[float] = None

# Schema dùng để cập nhật dữ liệu
class ContractItemUpdate(BaseModel):
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    discount: Optional[float] = None
    tax_rate: Optional[float] = None
    total_price: Optional[float] = None

# Schema dùng để trả về dữ liệu (Response)
class ContractItemResponse(ContractItemBase):
    contract_id: int
    product_id: int
    total_price: float

    # Cho phép Pydantic đọc dữ liệu từ SQLAlchemy Model (ORM)
    model_config = ConfigDict(from_attributes=True)
class ContractItemDetailResponse(ContractItemResponse):
    product: ProductResponse