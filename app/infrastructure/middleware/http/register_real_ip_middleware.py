from typing import Callable

from fastapi import FastAPI, Request, Response


def register_real_ip_middleware(
        app: FastAPI
) -> None:
    @app.middleware(middleware_type="http")
    async def real_ip_middleware(
            request: Request,
            call_next: Callable
    ) -> Response:
        x_forwarded_for: str | None = request.headers.get("x-forwarded-for")
        x_real_ip: str | None = request.headers.get("x-real-ip")

        if x_forwarded_for:
            real_ip: str = x_forwarded_for.split(",")[0].strip()
        elif x_real_ip:
            real_ip: str = x_real_ip.strip()
        else:
            real_ip: str = request.client.host

        request.state.real_ip = real_ip

        return await call_next(request)
