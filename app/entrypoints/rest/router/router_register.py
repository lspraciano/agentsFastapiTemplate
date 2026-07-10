from fastapi import APIRouter

from app.entrypoints.rest.router.root import health
from app.entrypoints.rest.router.v1 import chat


class RouterRegister:
    def __init__(self):
        self.router: APIRouter = APIRouter()
        self._register_root()
        self._register_v1()

    def _register_root(self) -> None:
        self.router.include_router(router=health.router)

    def _register_v1(self) -> None:
        self.router.include_router(
            router=chat.router,
            prefix="/v1",
        )
