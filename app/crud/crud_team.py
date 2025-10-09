"""CRUD operations for Team model."""

from app.crud.base import CRUDBase
from app.models import Team
from app.schemas import TeamCreate, TeamUpdate


class CRUDTeam(CRUDBase[Team, TeamCreate, TeamUpdate]):
    """CRUD operations for Team model."""
    pass


# Create instance
team = CRUDTeam(Team)

