"""CRUD operations for Company model."""

from app.crud.base import CRUDBase
from app.models import Company
from app.schemas import CompanyCreate, CompanyUpdate


class CRUDCompany(CRUDBase[Company, CompanyCreate, CompanyUpdate]):
    """CRUD operations for Company model."""
    pass


# Create instance
company = CRUDCompany(Company)

