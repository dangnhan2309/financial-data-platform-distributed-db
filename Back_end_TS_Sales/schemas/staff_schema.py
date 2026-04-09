from pydantic import BaseModel, ConfigDict
from typing import Optional

# 1. Schema cơ sở
class StaffBase(BaseModel):
    name: str

# 2. Schema dùng khi tạo mới hoặc cập nhật
class StaffCreate(StaffBase):
    pass

class StaffUpdate(BaseModel):
    name: Optional[str] = None

# 3. Schema trả về dữ liệu (Response)
class StaffResponse(StaffBase):
    staff_id: int
    # Cấu hình để Pydantic đọc dữ liệu từ SQLAlchemy Model
    model_config = ConfigDict(from_attributes=True) 