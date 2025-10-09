"""CRUD operations for Tag model."""

from app.crud.base import CRUDBase
from app.models import Tag
from app.schemas import TagCreate, TagUpdate


class CRUDTag(CRUDBase[Tag, TagCreate, TagUpdate]):
    """CRUD operations for Tag model."""
    pass


# Create instance
tag = CRUDTag(Tag)

