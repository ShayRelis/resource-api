"""API v1 router aggregation."""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    companies,
    components,
    teams,
    cloud_providers,
    registry_providers,
    registries,
    registry_credentials,
    container_images,
    environments,
    service_types,
    tags,
    versions,
)

api_router = APIRouter()

# Authentication routes (no prefix, no tags)
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Resource routes
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(components.router, prefix="/components", tags=["components"])
api_router.include_router(teams.router, prefix="/teams", tags=["teams"])
api_router.include_router(cloud_providers.router, prefix="/cloud-providers", tags=["cloud-providers"])
api_router.include_router(registry_providers.router, prefix="/registry-providers", tags=["registry-providers"])
api_router.include_router(registries.router, prefix="/registries", tags=["registries"])
api_router.include_router(registry_credentials.router, prefix="/registry-credentials", tags=["registry-credentials"])
api_router.include_router(container_images.router, prefix="/container-images", tags=["container-images"])
api_router.include_router(environments.router, prefix="/environments", tags=["environments"])
api_router.include_router(service_types.router, prefix="/service-types", tags=["service-types"])
api_router.include_router(tags.router, prefix="/tags", tags=["tags"])
api_router.include_router(versions.router, prefix="/versions", tags=["versions"])

