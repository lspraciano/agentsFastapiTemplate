from fastapi import FastAPI

from app.entrypoints.rest.api_generator import ApiFactory

app: FastAPI = ApiFactory().app

if __name__ == "__main__":
    import uvicorn

    from configuration.configs import settings

    uvicorn.run(
        app="app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.SERVER_RELOAD,
    )
