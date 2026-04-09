from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from schemas.payment_term_schema import PaymentTermResponse # Đảm bảo bạn đã có file này

# 1. Schema cơ sở: Chứa các thông tin cốt lõi của Proforma
class ProformaInvoiceBase(BaseModel):
    total_contract_value: Optional[float] = 0.0
    currency: Optional[str] = "USD"
    port_of_loading: Optional[str] = None
    port_of_discharge: Optional[str] = None
    delivery_time: Optional[str] = None
    status: Optional[str] = "Draft"
    file_path: Optional[str] = None

# 2. Schema dùng để tạo mới (Cần các ID quan hệ)
class ProformaInvoiceCreate(ProformaInvoiceBase):
    quotation_id: int
    payment_term_id: int
    staff_id: int

# 3. Schema dùng để cập nhật
class ProformaInvoiceUpdate(ProformaInvoiceBase):
    quotation_id: Optional[int] = None
    payment_term_id: Optional[int] = None
    staff_id: Optional[int] = None

# 4. Schema trả về dữ liệu cơ bản
class ProformaInvoiceResponse(ProformaInvoiceBase):
    proforma_invoice_id: int
    quotation_id: int
    payment_term_id: int
    staff_id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# 5. Schema trả về CHI TIẾT (Lồng thông tin Payment Term, Staff, etc.)
class ProformaInvoiceDetailResponse(ProformaInvoiceResponse):
    # Lồng thông tin chi tiết thay vì chỉ hiện ID
    payment_term: Optional[PaymentTermResponse] = None
    # staff: Optional[StaffResponse] = None # Nếu bạn đã viết Staff Schema