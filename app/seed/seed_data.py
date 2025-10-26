import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import select

from app.db.database import async_session
from app.models import (
    Company, User, UserRole, CloudProvider, RegistryProvider, 
    ServiceType, Tag, Team, RegistryCredential, Registry, ContainerImage, Version,
    Environment, Component, component_teams, component_tags, component_container_images, component_versions
)


COMPANIES = [
    {"name": "Relis"},
    {"name": "AWS"},
]


USERS = [
    {
        "name": "Shay Admin",
        "email": "shayadmin@relis.io",
        "phone": "+155555501",
        "company_name": "Relis",
        "password_hash": "fakehashedpassword1",
        "role": UserRole.admin,
    },
    {
        "name": "Shay User",
        "email": "shay@relis.io",
        "phone": "+155555502",
        "company_name": "Relis",
        "password_hash": "fakehashedpassword2",
        "role": UserRole.user,
    },
    {
        "name": "AWS User",
        "email": "user@aws.com",
        "phone": "+155555502",
        "company_name": "AWS",
        "password_hash": "fakehashedpassword3",
        "role": UserRole.user,
    },
]


CLOUD_PROVIDERS = [
    {"name": "AWS"},
    {"name": "GCP"},
    {"name": "Azure"},
]


REGISTRY_PROVIDERS = [
    {"name": "Docker Hub"},
    {"name": "Amazon ECR"},
    {"name": "Google Container Registry"},
    {"name": "Azure Container Registry"},
]


SERVICE_TYPES = [
    {
        "name": "Web API",
        "description": "RESTful API service",
        "is_managed": True,
    },
    {
        "name": "Frontend",
        "description": "React/Vue/Angular frontend application",
        "is_managed": True,
    },
    {
        "name": "Background Worker",
        "description": "Async task processing service",
        "is_managed": True,
    },
    {
        "name": "Database",
        "description": "Database service",
        "is_managed": False,
    },
]


TEAMS = [
    {"name": "Engineering", "company_name": "Relis"},
    {"name": "DevOps", "company_name": "Relis"},
    {"name": "Platform", "company_name": "AWS"},
]


TAGS = [
    {"name": "production", "company_name": "Relis"},
    {"name": "staging", "company_name": "Relis"},
    {"name": "development", "company_name": "Relis"},
    {"name": "critical", "company_name": "Relis"},
]


REGISTRY_CREDENTIALS = [
    {
        "name": "Relis ECR Credentials",
        "access_key": "AKIAIOSFODNN7EXAMPLE",
        "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "region": "us-east-1",
        "registry_provider_name": "Amazon ECR",
    },
]


REGISTRIES = [
    {
        "name": "Relis Production Registry",
        "url": "123456789012.dkr.ecr.us-east-1.amazonaws.com",
        "is_private": True,
        "registry_provider_name": "Amazon ECR",
        "registry_credential_name": "Relis ECR Credentials",
    },
    {
        "name": "Docker Hub Public",
        "url": "docker.io",
        "is_private": False,
        "registry_provider_name": "Docker Hub",
        "registry_credential_name": None,
    },
]


CONTAINER_IMAGES = [
    {
        "name": "relis-api",
        "tag": "v1.0.0",
        "registry_name": "Relis Production Registry",
        "pushed_at": "2025-10-01T10:00:00",
    },
    {
        "name": "relis-api",
        "tag": "v1.0.1",
        "registry_name": "Relis Production Registry",
        "pushed_at": "2025-10-02T14:30:00",
    },
    {
        "name": "relis-frontend",
        "tag": "v2.1.0",
        "registry_name": "Relis Production Registry",
        "pushed_at": "2025-10-03T09:15:00",
    },
    {
        "name": "relis-worker",
        "tag": "v1.0.0",
        "registry_name": "Relis Production Registry",
        "pushed_at": "2025-10-01T10:30:00",
    },
]


VERSIONS = [
    {
        "name": "Release 1.0.0",
        "container_images": [
            ("relis-api", "v1.0.0"),
            ("relis-frontend", "v2.1.0"),
            ("relis-worker", "v1.0.0"),
        ],
    },
    {
        "name": "Release 1.0.1",
        "container_images": [
            ("relis-api", "v1.0.1"),
            ("relis-frontend", "v2.1.0"),
            ("relis-worker", "v1.0.0"),
        ],
    },
]


ENVIRONMENTS = [
    {
        "name": "development",
        "description": "Development environment for testing new features",
        "version_name": "Release 1.0.0",
        "company_name": "Relis",
    },
    {
        "name": "staging",
        "description": "Staging environment for pre-production testing",
        "version_name": "Release 1.0.0",
        "company_name": "Relis",
    },
    {
        "name": "production",
        "description": "Production environment serving live traffic",
        "version_name": "Release 1.0.1",
        "company_name": "Relis",
    },
    {
        "name": "qa",
        "description": "QA environment for quality assurance testing",
        "version_name": "Release 1.0.0",
        "company_name": "Relis",
    },
    {
        "name": "production",
        "description": "AWS production environment",
        "version_name": "Release 1.0.1",
        "company_name": "AWS",
    },
]


COMPONENTS = [
    {
        "name": "API Gateway Service",
        "description": "Main API gateway handling all REST requests",
        "repository_url": "https://github.com/relis/api-gateway",
        "is_managed": True,
        "is_third_party": False,
        "company_name": "Relis",
        "team_names": ["Engineering", "DevOps"],
        "tag_names": ["production", "critical"],
        "container_image_keys": [("relis-api", "v1.0.0"), ("relis-api", "v1.0.1")],
        "version_names": ["Release 1.0.0", "Release 1.0.1"],
    },
    {
        "name": "Frontend Application",
        "description": "React-based user interface",
        "repository_url": "https://github.com/relis/frontend",
        "is_managed": True,
        "is_third_party": False,
        "company_name": "Relis",
        "team_names": ["Engineering"],
        "tag_names": ["production"],
        "container_image_keys": [("relis-frontend", "v2.1.0")],
        "version_names": ["Release 1.0.0", "Release 1.0.1"],
    },
    {
        "name": "Background Worker",
        "description": "Async task processing service for heavy workloads",
        "repository_url": "https://github.com/relis/worker",
        "is_managed": True,
        "is_third_party": False,
        "company_name": "Relis",
        "team_names": ["DevOps"],
        "tag_names": ["production"],
        "container_image_keys": [("relis-worker", "v1.0.0")],
        "version_names": ["Release 1.0.0", "Release 1.0.1"],
    },
    {
        "name": "PostgreSQL Database",
        "description": "Primary relational database",
        "repository_url": None,
        "is_managed": False,
        "is_third_party": True,
        "company_name": "Relis",
        "team_names": ["DevOps"],
        "tag_names": ["production", "critical"],
        "container_image_keys": [],
        "version_names": [],
    },
    {
        "name": "Redis Cache",
        "description": "In-memory caching layer",
        "repository_url": None,
        "is_managed": False,
        "is_third_party": True,
        "company_name": "Relis",
        "team_names": ["DevOps"],
        "tag_names": ["production"],
        "container_image_keys": [],
        "version_names": [],
    },
]


async def seed():
    from datetime import datetime
    
    async with async_session() as session:
        company_by_name = {}
        cloud_provider_by_name = {}
        registry_provider_by_name = {}
        registry_credential_by_name = {}
        registry_by_name = {}
        container_image_by_key = {}
        team_by_name = {}
        tag_by_name = {}
        version_by_name = {}

        # Seed companies
        print("Seeding companies...")
        for payload in COMPANIES:
            result = await session.execute(
                select(Company).where(Company.name == payload["name"])
            )
            company = result.scalar_one_or_none()

            if company is None:
                company = Company(**payload)
                session.add(company)
                await session.flush()
                print(f"  ✓ Created company: {company.name}")
            else:
                print(f"  - Company already exists: {company.name}")

            company_by_name[company.name] = company

        # Seed cloud providers
        print("\nSeeding cloud providers...")
        for payload in CLOUD_PROVIDERS:
            result = await session.execute(
                select(CloudProvider).where(CloudProvider.name == payload["name"])
            )
            provider = result.scalar_one_or_none()

            if provider is None:
                provider = CloudProvider(**payload)
                session.add(provider)
                await session.flush()
                print(f"  ✓ Created cloud provider: {provider.name}")
            else:
                print(f"  - Cloud provider already exists: {provider.name}")

            cloud_provider_by_name[provider.name] = provider

        # Seed registry providers
        print("\nSeeding registry providers...")
        for payload in REGISTRY_PROVIDERS:
            result = await session.execute(
                select(RegistryProvider).where(RegistryProvider.name == payload["name"])
            )
            provider = result.scalar_one_or_none()

            if provider is None:
                provider = RegistryProvider(**payload)
                session.add(provider)
                await session.flush()
                print(f"  ✓ Created registry provider: {provider.name}")
            else:
                print(f"  - Registry provider already exists: {provider.name}")

            registry_provider_by_name[provider.name] = provider

        # Seed service types
        print("\nSeeding service types...")
        for payload in SERVICE_TYPES:
            result = await session.execute(
                select(ServiceType).where(ServiceType.name == payload["name"])
            )
            service_type = result.scalar_one_or_none()

            if service_type is None:
                service_type = ServiceType(**payload)
                session.add(service_type)
                print(f"  ✓ Created service type: {service_type.name}")
            else:
                print(f"  - Service type already exists: {service_type.name}")

        await session.flush()

        # Seed teams
        print("\nSeeding teams...")
        for payload in TEAMS:
            result = await session.execute(
                select(Team).where(Team.name == payload["name"])
            )
            team = result.scalar_one_or_none()

            if team is None:
                company = company_by_name[payload["company_name"]]
                team = Team(
                    name=payload["name"],
                    company_id=company.id,
                )
                session.add(team)
                await session.flush()
                print(f"  ✓ Created team: {team.name} (Company: {payload['company_name']})")
            else:
                print(f"  - Team already exists: {team.name}")

            team_by_name[team.name] = team

        await session.flush()

        # Seed tags
        print("\nSeeding tags...")
        for payload in TAGS:
            result = await session.execute(
                select(Tag).where(Tag.name == payload["name"])
            )
            tag = result.scalar_one_or_none()

            if tag is None:
                company = company_by_name[payload["company_name"]]
                tag = Tag(
                    name=payload["name"],
                    company_id=company.id,
                )
                session.add(tag)
                await session.flush()
                print(f"  ✓ Created tag: {tag.name} (Company: {payload['company_name']})")
            else:
                print(f"  - Tag already exists: {tag.name}")

            tag_by_name[tag.name] = tag

        await session.flush()

        # Seed users
        print("\nSeeding users...")
        for payload in USERS:
            result = await session.execute(
                select(User).where(User.email == payload["email"])
            )
            user = result.scalar_one_or_none()

            if user is None:
                company = company_by_name[payload["company_name"]]
                user = User(
                    name=payload["name"],
                    email=payload["email"],
                    phone=payload["phone"],
                    company_id=company.id,
                    password_hash=payload["password_hash"],
                    role=payload["role"],
                )
                session.add(user)
                print(f"  ✓ Created user: {user.email} ({user.role})")
            else:
                print(f"  - User already exists: {user.email}")

        await session.flush()

        # Seed registry credentials
        print("\nSeeding registry credentials...")
        for payload in REGISTRY_CREDENTIALS:
            result = await session.execute(
                select(RegistryCredential).where(RegistryCredential.name == payload["name"])
            )
            credential = result.scalar_one_or_none()

            if credential is None:
                registry_provider = registry_provider_by_name[payload["registry_provider_name"]]
                credential = RegistryCredential(
                    name=payload["name"],
                    access_key=payload["access_key"],
                    secret_key=payload["secret_key"],
                    region=payload["region"],
                    registry_provider_id=registry_provider.id,
                )
                session.add(credential)
                await session.flush()
                print(f"  ✓ Created registry credential: {credential.name}")
            else:
                print(f"  - Registry credential already exists: {credential.name}")

            registry_credential_by_name[credential.name] = credential

        # Seed registries
        print("\nSeeding registries...")
        for payload in REGISTRIES:
            result = await session.execute(
                select(Registry).where(Registry.name == payload["name"])
            )
            registry = result.scalar_one_or_none()

            if registry is None:
                registry_provider = registry_provider_by_name[payload["registry_provider_name"]]
                credential_id = None
                if payload["registry_credential_name"]:
                    credential = registry_credential_by_name[payload["registry_credential_name"]]
                    credential_id = credential.id

                registry = Registry(
                    name=payload["name"],
                    url=payload["url"],
                    is_private=payload["is_private"],
                    registry_provider_id=registry_provider.id,
                    registry_credentials_id=credential_id,
                )
                session.add(registry)
                await session.flush()
                print(f"  ✓ Created registry: {registry.name}")
            else:
                print(f"  - Registry already exists: {registry.name}")

            registry_by_name[registry.name] = registry

        # Seed container images
        print("\nSeeding container images...")
        for payload in CONTAINER_IMAGES:
            result = await session.execute(
                select(ContainerImage).where(
                    (ContainerImage.name == payload["name"]) & 
                    (ContainerImage.tag == payload["tag"])
                )
            )
            image = result.scalar_one_or_none()

            if image is None:
                registry = registry_by_name[payload["registry_name"]]
                image = ContainerImage(
                    name=payload["name"],
                    tag=payload["tag"],
                    registry_id=registry.id,
                    pushed_at=datetime.fromisoformat(payload["pushed_at"]),
                )
                session.add(image)
                await session.flush()
                print(f"  ✓ Created container image: {image.name}:{image.tag}")
            else:
                print(f"  - Container image already exists: {image.name}:{image.tag}")

            container_image_by_key[(image.name, image.tag)] = image

        # Seed versions
        print("\nSeeding versions...")
        for payload in VERSIONS:
            result = await session.execute(
                select(Version).where(Version.name == payload["name"])
            )
            version = result.scalar_one_or_none()

            if version is None:
                version = Version(name=payload["name"])
                session.add(version)
                await session.flush()
                print(f"  ✓ Created version: {version.name}")
                
                # Associate container images with this version
                for image_key in payload["container_images"]:
                    image = container_image_by_key.get(image_key)
                    if image:
                        # Insert into association table
                        from app.models import version_container_images
                        stmt = version_container_images.insert().values(
                            version_id=version.id,
                            container_image_id=image.id
                        )
                        await session.execute(stmt)
                        print(f"    → Associated {image.name}:{image.tag}")
            else:
                print(f"  - Version already exists: {version.name}")

            version_by_name[version.name] = version

        # Seed environments
        print("\nSeeding environments...")
        for payload in ENVIRONMENTS:
            # Get version and company
            version = version_by_name.get(payload["version_name"])
            company = company_by_name.get(payload["company_name"])
            
            if version and company:
                # Check based on unique constraint (name + version_id)
                result = await session.execute(
                    select(Environment).where(
                        Environment.name == payload["name"],
                        Environment.version_id == version.id
                    )
                )
                environment = result.scalar_one_or_none()
                
                if environment is None:
                    environment = Environment(
                        name=payload["name"],
                        description=payload["description"],
                        version_id=version.id,
                        company_id=company.id,
                    )
                    session.add(environment)
                    await session.flush()
                    print(f"  ✓ Created environment: {environment.name} (Version: {payload['version_name']}, Company: {payload['company_name']})")
                else:
                    print(f"  - Environment already exists: {environment.name} (Version: {payload['version_name']})")
            else:
                if not version:
                    print(f"  ✗ Version not found: {payload['version_name']}")
                if not company:
                    print(f"  ✗ Company not found: {payload['company_name']}")

        # Seed components
        print("\nSeeding components...")
        for payload in COMPONENTS:
            result = await session.execute(
                select(Component).where(Component.name == payload["name"])
            )
            component = result.scalar_one_or_none()

            if component is None:
                company = company_by_name[payload["company_name"]]
                component = Component(
                    name=payload["name"],
                    description=payload["description"],
                    repository_url=payload["repository_url"],
                    is_managed=payload["is_managed"],
                    is_third_party=payload["is_third_party"],
                    company_id=company.id,
                )
                session.add(component)
                await session.flush()
                print(f"  ✓ Created component: {component.name}")

                # Associate teams
                for team_name in payload["team_names"]:
                    team = team_by_name.get(team_name)
                    if team:
                        stmt = component_teams.insert().values(
                            component_id=component.id,
                            team_id=team.id
                        )
                        await session.execute(stmt)
                        print(f"    → Associated with team: {team_name}")

                # Associate tags
                for tag_name in payload["tag_names"]:
                    tag = tag_by_name.get(tag_name)
                    if tag:
                        stmt = component_tags.insert().values(
                            component_id=component.id,
                            tag_id=tag.id
                        )
                        await session.execute(stmt)
                        print(f"    → Associated with tag: {tag_name}")

                # Associate container images
                for image_key in payload["container_image_keys"]:
                    image = container_image_by_key.get(image_key)
                    if image:
                        stmt = component_container_images.insert().values(
                            component_id=component.id,
                            container_image_id=image.id
                        )
                        await session.execute(stmt)
                        print(f"    → Associated with image: {image.name}:{image.tag}")

                # Associate versions
                for version_name in payload["version_names"]:
                    version = version_by_name.get(version_name)
                    if version:
                        stmt = component_versions.insert().values(
                            component_id=component.id,
                            version_id=version.id
                        )
                        await session.execute(stmt)
                        print(f"    → Associated with version: {version_name}")
            else:
                print(f"  - Component already exists: {component.name}")

        await session.commit()

    print("\n✅ Database seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed())

