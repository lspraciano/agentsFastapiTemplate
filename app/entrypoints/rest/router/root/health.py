from fastapi import APIRouter, status

from app.entrypoints.rest.schemas.root_schemas import HealthResponseSchema

router: APIRouter = APIRouter(
    tags=["Root"],
    prefix="",
)


@router.get(
    path="/health",
    status_code=status.HTTP_200_OK,
    response_model=HealthResponseSchema,
)
async def health() -> HealthResponseSchema:
    return HealthResponseSchema(status="ok")
