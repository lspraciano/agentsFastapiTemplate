from fastapi import FastAPI

from app.api.events.lifespan import lifespan
from app.api.router.router_register import api_routers
from app.core.shared.exceptions_handlers.register_exceptions_handlers import register_exceptions_handlers
from app.core.shared.metadata.metadata import get_project_metadata
from app.infrastructure.middleware.cors.register_cors_middleware import register_cors_middleware
from app.infrastructure.middleware.http.http_logger_middleware import register_http_logger_middleware
from app.infrastructure.middleware.http.register_real_ip_middleware import register_real_ip_middleware
from configuration.configs import settings


def api_factory() -> FastAPI:
    project_metadata: dict = get_project_metadata()

    current_api: FastAPI = FastAPI(
        lifespan=lifespan,
        title=project_metadata["name"],
        description=project_metadata["description"],
        version=project_metadata["version"],
        root_path=settings.PROXY_ROOT_PATH,
        docs_url=f"/docs",
        redoc_url=f"/redoc",
        openapi_url=f"/openapi.json",
        servers=[
            {
                "url": f"{settings.from_env('development').API_URL_BASE}",
                "description": "Development environment"
            },
            {
                "url": f"{settings.from_env('production').API_URL_BASE}",
                "description": "Production environment"
            },
        ],
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "operationsSorter": "method",
            "filter": True,
            "docExpansion": None,
        },
    )

    register_real_ip_middleware(
        app=current_api
    )

    register_http_logger_middleware(
        app=current_api
    )

    current_api.include_router(
        router=api_routers,
        prefix=f"{settings.API_PREFIX}"
    )

    register_cors_middleware(
        app=current_api,
    )

    register_exceptions_handlers(
        app=current_api
    )

    return current_api
