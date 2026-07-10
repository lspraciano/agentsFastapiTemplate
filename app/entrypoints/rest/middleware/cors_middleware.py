from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware as FastAPICorsMiddleware

from configuration.configs import settings


class CorsMiddleware:
    def __init__(
        self,
        app: FastAPI,
        origins: list[str] | None = None,
    ):
        self._app: FastAPI = app
        self._origins: list[str] = (
            origins if origins is not None else settings.CORS_ORIGINS
        )

    def register(self) -> None:
        if not settings.ENABLE_CORS:
            return

        self._app.add_middleware(
            middleware_class=FastAPICorsMiddleware,
            allow_origins=self._origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
