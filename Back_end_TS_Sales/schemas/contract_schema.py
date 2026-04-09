from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date
from schemas.contract_item_schema import ContractItemDetailResponse # Import từ file đã tạo trước đó
from schemas.customer_schema import CustomerResponse
from schemas.incoterm_schema import IncotermResponse
# 1. Schema chứa các trường cơ bản (Dùng chung)
class ContractBase(BaseModel):
    contract_type: Optional[str] = None
    contract_date: Optional[date] = None
    effective_date: Optional[date] = None
    expiry_date: Optional[date] = None
    total_contract_value: Optional[float] = 0.0
    total_quantity: Optional[float] = 0.0
    currency: Optional[str] = "USD"
    loading_port: Optional[str] = None
    destination_port: Optional[str] = None
    status: Optional[str] = "Draft"
    signed_date: Optional[date] = None

# 2. Schema dùng khi tạo mới Contract (Cần các ID quan hệ)
class ContractCreate(ContractBase):
    customer_id: int
    incoterm_id: int
    proforma_invoice_id: int

# 3. Schema dùng để cập nhật Contract
class ContractUpdate(ContractBase):
    customer_id: Optional[int] = None
    incoterm_id: Optional[int] = None
    proforma_invoice_id: Optional[int] = None

# 4. Schema trả về cơ bản (Response)
class ContractResponse(ContractBase):
    contract_id: int
    customer_id: int
    incoterm_id: int
    proforma_invoice_id: int

    model_config = ConfigDict(from_attributes=True)

# 5. Schema trả về CHI TIẾT (Bao gồm danh sách sản phẩm)
class ContractDetailResponse(ContractResponse):
    # Lồng danh sách items vào đây
    items: List[ContractItemDetailResponse] = []
    
    # Bạn có thể lồng thêm thông tin Customer hoặc Incoterm nếu muốn
    customer: CustomerResponse 
    incoterm: IncotermResponse