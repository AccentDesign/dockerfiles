from starlette.routing import Mount, Route, Router

from app.example.endpoints import Token, UserDetail, UserList


routes = [
    Route('/token', endpoint=Token, methods=['GET', 'POST'], name="token"),
    Mount('/users', app=Router([
        Route('/', endpoint=UserList, methods=['GET'], name="users"),
        Route('/{id:int}', endpoint=UserDetail, methods=['GET'], name="user"),
    ])),
]
