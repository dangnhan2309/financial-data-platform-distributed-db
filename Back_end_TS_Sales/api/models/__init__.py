from api.models.export_document_set import ExportDocumentSet
from api.models.sale_order import SaleOrder
from api.models.contract_item import ContractItem
from api.models.contract import Contract
from api.models.proforma_invoice import ProformaInvoice
from api.models.quotation_item import QuotationItem
from api.models.quotation import Quotation
from api.models.incoterm import Incoterm
from api.models.payment_term import PaymentTerm
from api.models.product import Product
from api.models.customer import Customer
from api.models.staff import Staff
from api.utils.database import Base


class BaseModel(Base):
    """
    Base model class for all database models.
    Does NOT automatically add columns - keep models simple and match SQL schema.
    """
    __abstract__ = True


# Import all models to register them with SQLAlchemy
