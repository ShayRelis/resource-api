"""CRUD operations for Environment model."""

from app.crud.base import CRUDBase
from app.models.environment import Environment
from app.schemas.environment import EnvironmentCreate, EnvironmentUpdate


class CRUDEnvironment(CRUDBase[Environment, EnvironmentCreate, EnvironmentUpdate]):
    """CRUD operations for Environment model."""
    pass


# Create instance
environment = CRUDEnvironment(Environment)

