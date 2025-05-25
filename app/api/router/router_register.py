from fastapi import APIRouter

from app.api.router.v1 import v1_api_routers_dict
from app.api.schemas.generic_responses_schemas import generic_response_404, generic_response_422

api_routers_dict_list: list[dict] = [
    v1_api_routers_dict
]

for api_routers_dict in api_routers_dict_list:
    api_routers: APIRouter = APIRouter(
        prefix=api_routers_dict["prefix"]
    )

    for router in api_routers_dict["routers_list"]:
        api_routers.include_router(
            router=router,
            responses={
                **generic_response_404,
                **generic_response_422,
            }
        )
