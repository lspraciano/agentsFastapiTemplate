from app.api.endpoints.v1 import root, chat

v1_api_routers_dict: dict = {
    "prefix": "/v1",
    "routers_list": [
        root.router,
        chat.router
    ]
}
