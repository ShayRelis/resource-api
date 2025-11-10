"""CRUD operations for Version model."""

from typing import List, Optional
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Version
from app.models.version import version_container_images
from app.schemas import VersionCreate, VersionUpdate


class CRUDVersion(CRUDBase[Version, VersionCreate, VersionUpdate]):
    """CRUD operations for Version model with association management."""

    async def create_with_associations(
        self, db: AsyncSession, *, obj_in: VersionCreate
    ) -> tuple[Version, dict]:
        """
        Create a new version with its associations.
        
        Args:
            db: Database session
            obj_in: Version creation data including association IDs
            
        Returns:
            Tuple of (created version instance, associations dict)
        """
        # Extract association IDs
        container_image_ids = obj_in.container_image_ids
        
        # Create version without associations
        obj_data = obj_in.model_dump(exclude={"container_image_ids"})
        db_obj = Version(**obj_data)
        db.add(db_obj)
        await db.flush()  # Flush to get the ID
        
        # Create associations
        if container_image_ids:
            await db.execute(
                version_container_images.insert(),
                [{"version_id": db_obj.id, "container_image_id": img_id} for img_id in container_image_ids]
            )
        
        # Get associations before commit (while still in tenant schema context)
        associations = await self.get_associations(db, version_id=db_obj.id)
        
        await db.commit()
        return db_obj, associations

    async def get_associations(
        self, db: AsyncSession, *, version_id: int
    ) -> dict:
        """
        Get all association IDs for a version.
        
        Args:
            db: Database session
            version_id: Version ID
            
        Returns:
            Dictionary with lists of associated IDs
        """
        # Get container image IDs
        result = await db.execute(
            select(version_container_images.c.container_image_id).where(
                version_container_images.c.version_id == version_id
            )
        )
        container_image_ids = [row[0] for row in result.fetchall()]
        
        return {
            "container_image_ids": container_image_ids,
        }

    async def update_with_associations(
        self,
        db: AsyncSession,
        *,
        db_obj: Version,
        obj_in: VersionUpdate
    ) -> tuple[Version, dict]:
        """
        Update a version and its associations.
        
        Args:
            db: Database session
            db_obj: Existing version instance
            obj_in: Version update data
            
        Returns:
            Tuple of (updated version instance, associations dict)
        """
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # Extract association IDs if provided
        container_image_ids = update_data.pop("container_image_ids", None)
        
        # Update basic fields
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.flush()
        
        # Update container image associations if provided
        if container_image_ids is not None:
            await db.execute(
                delete(version_container_images).where(version_container_images.c.version_id == db_obj.id)
            )
            if container_image_ids:
                await db.execute(
                    version_container_images.insert(),
                    [{"version_id": db_obj.id, "container_image_id": img_id} for img_id in container_image_ids]
                )
        
        # Get associations before commit (while still in tenant schema context)
        associations = await self.get_associations(db, version_id=db_obj.id)
        
        await db.commit()
        return db_obj, associations

    async def delete_with_associations(
        self, db: AsyncSession, *, id: int
    ) -> Optional[Version]:
        """
        Delete a version and clean up its associations.
        
        Args:
            db: Database session
            id: Version ID
            
        Returns:
            Deleted version instance if found, None otherwise
        """
        obj = await self.get(db, id)
        if obj:
            # Delete associations first
            await db.execute(
                delete(version_container_images).where(version_container_images.c.version_id == id)
            )
            
            # Delete the version
            await db.delete(obj)
            await db.commit()
        
        return obj


# Create instance
version = CRUDVersion(Version)

