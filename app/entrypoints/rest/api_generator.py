from fastapi import FastAPI

from app.entrypoints.rest.events.lifespan import lifespan
from app.entrypoints.rest.middleware.cors_middleware import CorsMiddleware
from app.entrypoints.rest.router.router_register import RouterRegister
from configuration.configs import settings


class ApiFactory:
    def __init__(self):
        self.app: FastAPI = self._create_app()
        self._register_middlewares()
        self._register_routers()

    @staticmethod
    def _create_app() -> FastAPI:
        return FastAPI(
            lifespan=lifespan,
            title="Agents FastAPI Template",
            docs_url="/docs",
            redoc_url="/redoc",
            openapi_url="/openapi.json",
            root_path=settings.PROXY_ROOT_PATH,
            swagger_ui_parameters={
                "defaultModelsExpandDepth": -1,
                "operationsSorter": "method",
                "filter": True,
                "docExpansion": None,
            },
        )

    def _register_middlewares(self) -> None:
        CorsMiddleware(app=self.app).register()

    def _register_routers(self) -> None:
        self.app.include_router(
            router=RouterRegister().router,
            prefix=settings.API_PREFIX,
        )
