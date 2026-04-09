from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

# 1. Schema cơ sở: Chứa tất cả các trường thông tin của sản phẩm
class ProductBase(BaseModel):
    product_type: Optional[str] = None
    name: str
    description: Optional[str] = None
    price: float = Field(..., ge=0, description="Giá sản phẩm không được âm")
    application: Optional[str] = None
    brix: Optional[float] = None
    product_size: Optional[str] = None
    solid: Optional[float] = None
    ph: Optional[float] = None
    is_active: int = 1 # 1: Active, 0: Inactive

# 2. Schema dùng để tạo mới sản phẩm
class ProductCreate(ProductBase):
    pass

# 3. Schema dùng để cập nhật sản phẩm (Tất cả các trường đều Optional)
class ProductUpdate(BaseModel):
    product_type: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    application: Optional[str] = None
    brix: Optional[float] = None
    product_size: Optional[str] = None
    solid: Optional[float] = None
    ph: Optional[float] = None
    is_active: Optional[int] = None

# 4. Schema trả về dữ liệu (Response)
class ProductResponse(ProductBase):
    product_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Quan trọng: Cho phép Pydantic đọc dữ liệu từ SQLAlchemy Model
    model_config = ConfigDict(from_attributes=True)