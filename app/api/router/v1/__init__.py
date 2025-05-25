from app.api.router.v1 import chat, root

v1_api_routers_dict: dict = {
    "prefix": "/v1",
    "routers_list": [
        root.router,
        chat.router
    ]
}
