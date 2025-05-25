from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from configuration.configs import settings


def register_cors_middleware(
        app: FastAPI,
        origins: list[str] = settings.CORS_ORIGINS,
):
    if settings.ENABLE_CORS:
        app.add_middleware(
            middleware_class=CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )
