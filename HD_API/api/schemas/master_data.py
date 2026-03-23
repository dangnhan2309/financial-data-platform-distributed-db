from pydantic import BaseModel
from datetime import date


class IngredientBase(BaseModel):
    name: str
    unit_of_measure: str
    is_active: int


class IngredientCreate(IngredientBase):
    ingredient_id: str


class IngredientResponse(IngredientBase):
    ingredient_id: str

    class Config:
        from_attributes = True


class PackagingSpecificationBase(BaseModel):
    name: str
    unit_of_measure: str
    volume: int
    material: str


class PackagingSpecificationCreate(PackagingSpecificationBase):
    packaging_id: str


class PackagingSpecificationResponse(PackagingSpecificationBase):
    packaging_id: str

    class Config:
        from_attributes = True


class CertificationBase(BaseModel):
    name: str
    issue_date: date
    expiry_date: date
    issued_by: str


class CertificationCreate(CertificationBase):
    certification_id: str


class CertificationResponse(CertificationBase):
    certification_id: str

    class Config:
        from_attributes = True


class IncotermBase(BaseModel):
    name: str
    description: str


class IncotermCreate(IncotermBase):
    incoterm_id: str


class IncotermResponse(IncotermBase):
    incoterm_id: str

    class Config:
        from_attributes = True