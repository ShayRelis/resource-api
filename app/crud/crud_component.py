"""CRUD operations for Component model."""

from typing import List, Optional
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Component
from app.models.component import (
    component_teams,
    component_tags,
    component_container_images,
    component_versions,
)
from app.schemas import ComponentCreate, ComponentUpdate


class CRUDComponent(CRUDBase[Component, ComponentCreate, ComponentUpdate]):
    """CRUD operations for Component model with association management."""

    async def create_with_associations(
        self, db: AsyncSession, *, obj_in: ComponentCreate
    ) -> Component:
        """
        Create a new component with its associations.
        
        Args:
            db: Database session
            obj_in: Component creation data including association IDs
            
        Returns:
            Created component instance
        """
        # Extract association IDs
        team_ids = obj_in.team_ids
        tag_ids = obj_in.tag_ids
        container_image_ids = obj_in.container_image_ids
        version_ids = obj_in.version_ids
        
        # Create component without associations
        obj_data = obj_in.model_dump(
            exclude={"team_ids", "tag_ids", "container_image_ids", "version_ids"}
        )
        db_obj = Component(**obj_data)
        db.add(db_obj)
        await db.flush()  # Flush to get the ID
        
        # Create associations
        if team_ids:
            await db.execute(
                component_teams.insert(),
                [{"component_id": db_obj.id, "team_id": team_id} for team_id in team_ids]
            )
        
        if tag_ids:
            await db.execute(
                component_tags.insert(),
                [{"component_id": db_obj.id, "tag_id": tag_id} for tag_id in tag_ids]
            )
        
        if container_image_ids:
            await db.execute(
                component_container_images.insert(),
                [{"component_id": db_obj.id, "container_image_id": img_id} for img_id in container_image_ids]
            )
        
        if version_ids:
            await db.execute(
                component_versions.insert(),
                [{"component_id": db_obj.id, "version_id": version_id} for version_id in version_ids]
            )
        
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_associations(
        self, db: AsyncSession, *, component_id: int
    ) -> dict:
        """
        Get all association IDs for a component.
        
        Args:
            db: Database session
            component_id: Component ID
            
        Returns:
            Dictionary with lists of associated IDs
        """
        # Get team IDs
        result = await db.execute(
            select(component_teams.c.team_id).where(component_teams.c.component_id == component_id)
        )
        team_ids = [row[0] for row in result.fetchall()]
        
        # Get tag IDs
        result = await db.execute(
            select(component_tags.c.tag_id).where(component_tags.c.component_id == component_id)
        )
        tag_ids = [row[0] for row in result.fetchall()]
        
        # Get container image IDs
        result = await db.execute(
            select(component_container_images.c.container_image_id).where(
                component_container_images.c.component_id == component_id
            )
        )
        container_image_ids = [row[0] for row in result.fetchall()]
        
        # Get version IDs
        result = await db.execute(
            select(component_versions.c.version_id).where(component_versions.c.component_id == component_id)
        )
        version_ids = [row[0] for row in result.fetchall()]
        
        return {
            "team_ids": team_ids,
            "tag_ids": tag_ids,
            "container_image_ids": container_image_ids,
            "version_ids": version_ids,
        }

    async def update_with_associations(
        self,
        db: AsyncSession,
        *,
        db_obj: Component,
        obj_in: ComponentUpdate
    ) -> Component:
        """
        Update a component and its associations.
        
        Args:
            db: Database session
            db_obj: Existing component instance
            obj_in: Component update data
            
        Returns:
            Updated component instance
        """
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # Extract association IDs if provided
        team_ids = update_data.pop("team_ids", None)
        tag_ids = update_data.pop("tag_ids", None)
        container_image_ids = update_data.pop("container_image_ids", None)
        version_ids = update_data.pop("version_ids", None)
        
        # Update basic fields
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.flush()
        
        # Update team associations if provided
        if team_ids is not None:
            await db.execute(
                delete(component_teams).where(component_teams.c.component_id == db_obj.id)
            )
            if team_ids:
                await db.execute(
                    component_teams.insert(),
                    [{"component_id": db_obj.id, "team_id": team_id} for team_id in team_ids]
                )
        
        # Update tag associations if provided
        if tag_ids is not None:
            await db.execute(
                delete(component_tags).where(component_tags.c.component_id == db_obj.id)
            )
            if tag_ids:
                await db.execute(
                    component_tags.insert(),
                    [{"component_id": db_obj.id, "tag_id": tag_id} for tag_id in tag_ids]
                )
        
        # Update container image associations if provided
        if container_image_ids is not None:
            await db.execute(
                delete(component_container_images).where(component_container_images.c.component_id == db_obj.id)
            )
            if container_image_ids:
                await db.execute(
                    component_container_images.insert(),
                    [{"component_id": db_obj.id, "container_image_id": img_id} for img_id in container_image_ids]
                )
        
        # Update version associations if provided
        if version_ids is not None:
            await db.execute(
                delete(component_versions).where(component_versions.c.component_id == db_obj.id)
            )
            if version_ids:
                await db.execute(
                    component_versions.insert(),
                    [{"component_id": db_obj.id, "version_id": version_id} for version_id in version_ids]
                )
        
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete_with_associations(
        self, db: AsyncSession, *, id: int
    ) -> Optional[Component]:
        """
        Delete a component and clean up its associations.
        
        Args:
            db: Database session
            id: Component ID
            
        Returns:
            Deleted component instance if found, None otherwise
        """
        obj = await self.get(db, id)
        if obj:
            # Delete associations first
            await db.execute(
                delete(component_teams).where(component_teams.c.component_id == id)
            )
            await db.execute(
                delete(component_tags).where(component_tags.c.component_id == id)
            )
            await db.execute(
                delete(component_container_images).where(component_container_images.c.component_id == id)
            )
            await db.execute(
                delete(component_versions).where(component_versions.c.component_id == id)
            )
            
            # Delete the component
            await db.delete(obj)
            await db.commit()
        
        return obj


# Create instance
component = CRUDComponent(Component)

