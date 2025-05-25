from fastapi import APIRouter, status

from app.api.schemas.root_schemas import RootResponse
from app.core.shared.metadata.metadata import get_project_metadata
from configuration.configs import settings

router: APIRouter = APIRouter(
    tags=["Root"],
    prefix=""
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=RootResponse
)
async def check_metadata_():
    project_metadata: dict = get_project_metadata()
    return {
        "status": "online",
        "running_mode": settings.APP_RUNNING_MODE,
        **project_metadata
    }
