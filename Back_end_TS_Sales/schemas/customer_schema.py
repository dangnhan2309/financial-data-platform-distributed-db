from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime

# 1. Schema cơ sở: Chứa các trường chung
class CustomerBase(BaseModel):
    customer_type: Optional[str] = None
    customer_code: Optional[str] = None
    company_name: str # Tên công ty thường là bắt buộc
    short_name: Optional[str] = None
    tax_id: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None # Sử dụng EmailStr để tự động validate định dạng email
    website: Optional[str] = None
    industry: Optional[str] = None
    status: Optional[str] = "Active"
    preferred_currency: Optional[str] = "USD"

# 2. Schema dùng khi tạo mới Customer
class CustomerCreate(CustomerBase):
    pass # Thường dùng luôn các trường từ Base

# 3. Schema dùng để cập nhật (Tất cả các trường đều có thể Optional)
class CustomerUpdate(CustomerBase):
    company_name: Optional[str] = None  # type: ignore

# 4. Schema trả về dữ liệu (Response)
class CustomerResponse(CustomerBase):
    customer_id: int
    created_at: Optional[datetime] = None

    # Cấu hình để Pydantic đọc được dữ liệu từ SQLAlchemy Model
    model_config = ConfigDict(from_attributes=True)