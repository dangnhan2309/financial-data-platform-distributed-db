from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

# 1. Schema cơ sở: Chứa các trường thông tin chung
class ExportDocumentSetBase(BaseModel):
    issue_date: Optional[date] = None
    document_type: Optional[str] = None # Ví dụ: Bill of Lading, Certificate of Origin, etc.
    file_path: Optional[str] = None
    status: Optional[str] = "Pending"

# 2. Schema dùng khi tạo mới (Cần sale_order_id)
class ExportDocumentSetCreate(ExportDocumentSetBase):
    sale_order_id: int

# 3. Schema dùng để cập nhật
class ExportDocumentSetUpdate(ExportDocumentSetBase):
    sale_order_id: Optional[int] = None

# 4. Schema trả về dữ liệu (Response)
class ExportDocumentSetResponse(ExportDocumentSetBase):
    document_set_id: int
    sale_order_id: int

    # Cấu hình để Pydantic đọc dữ liệu từ SQLAlchemy Model
    model_config = ConfigDict(from_attributes=True)