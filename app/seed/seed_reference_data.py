"""Seed reference data for tenant schemas."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cloud_provider import CloudProvider
from app.models.registry_provider import RegistryProvider
from app.models.service_type import ServiceType


async def seed_tenant_reference_data(session: AsyncSession, company_id: int) -> None:
    """
    Seed reference data into a tenant schema.
    
    This function populates cloud providers, registry providers, and service types
    for a new company's tenant schema.
    
    Args:
        session: Database session with search_path set to tenant schema
        company_id: Company ID (for logging/reference)
    """
    # Seed Cloud Providers
    cloud_providers = [
        CloudProvider(name="AWS"),
        CloudProvider(name="Azure"),
        CloudProvider(name="GCP"),
        CloudProvider(name="On-Premise"),
        CloudProvider(name="DigitalOcean"),
        CloudProvider(name="Oracle Cloud"),
    ]
    session.add_all(cloud_providers)

    # Seed Registry Providers
    registry_providers = [
        RegistryProvider(name="DockerHub"),
        RegistryProvider(name="AWS ECR"),
        RegistryProvider(name="GCP GCR"),
        RegistryProvider(name="Azure ACR"),
        RegistryProvider(name="GitHub Container Registry"),
        RegistryProvider(name="GitLab Container Registry"),
        RegistryProvider(name="Harbor"),
        RegistryProvider(name="JFrog Artifactory"),
    ]
    session.add_all(registry_providers)

    # Seed Service Types
    service_types = [
        ServiceType(
            name="API",
            description="RESTful API service",
            is_managed=True
        ),
        ServiceType(
            name="Worker",
            description="Background worker service",
            is_managed=True
        ),
        ServiceType(
            name="Frontend",
            description="Frontend web application",
            is_managed=True
        ),
        ServiceType(
            name="Database",
            description="Database service",
            is_managed=False
        ),
        ServiceType(
            name="Cache",
            description="Caching service (Redis, Memcached)",
            is_managed=False
        ),
        ServiceType(
            name="Message Queue",
            description="Message queue service (RabbitMQ, Kafka)",
            is_managed=False
        ),
        ServiceType(
            name="Microservice",
            description="General microservice",
            is_managed=True
        ),
    ]
    session.add_all(service_types)

    # Commit all changes
    await session.commit()
    
    print(f"✓ Seeded reference data for company_{company_id}")

