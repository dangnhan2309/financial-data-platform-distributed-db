from pydantic import BaseModel, ConfigDict
from typing import Optional

# 1. Schema cơ sở: Định nghĩa các trường dữ liệu cốt lõi
class IncotermBase(BaseModel):
    name: str # Ví dụ: FOB, CIF, EXW
    description: Optional[str] = None
    version: Optional[str] = "2020" # Ví dụ: Incoterms 2010, 2020
    status: Optional[str] = "Active"

# 2. Schema dùng khi tạo mới Incoterm
class IncotermCreate(IncotermBase):
    pass

# 3. Schema dùng để cập nhật
class IncotermUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    status: Optional[str] = None

# 4. Schema trả về dữ liệu (Response)
class IncotermResponse(IncotermBase):
    incoterm_id: int

    # Cấu hình để Pydantic đọc dữ liệu từ SQLAlchemy Model
    model_config = ConfigDict(from_attributes=True)