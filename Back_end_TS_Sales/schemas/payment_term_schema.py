from pydantic import BaseModel, ConfigDict
from typing import Optional

# 1. Schema cơ sở: Các trường thông tin cốt lõi
class PaymentTermBase(BaseModel):
    description: str # Ví dụ: "Thanh toán trong vòng 30 ngày kể từ ngày nhận hóa đơn"
    number_of_days: int = 0 # Số ngày được phép nợ
    status: Optional[str] = "Active"

# 2. Schema dùng để tạo mới
class PaymentTermCreate(PaymentTermBase):
    pass

# 3. Schema dùng để cập nhật (Các trường đều Optional)
class PaymentTermUpdate(BaseModel):
    description: Optional[str] = None
    number_of_days: Optional[int] = None
    status: Optional[str] = None

# 4. Schema trả về dữ liệu (Response)
class PaymentTermResponse(PaymentTermBase):
    payment_term_id: int

    # Cho phép Pydantic đọc dữ liệu từ SQLAlchemy ORM
    model_config = ConfigDict(from_attributes=True)