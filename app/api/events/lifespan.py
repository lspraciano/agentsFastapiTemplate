from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(
        app: FastAPI
):
    print("StartUp Application")
    yield
    print("Stopping Application")
