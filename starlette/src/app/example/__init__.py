from starlette.routing import Mount, Route, Router

from . import endpoints


app = Router([
    Route('/error', endpoint=endpoints.ForceError, methods=['GET'], name='error'),
    Route('/token', endpoint=endpoints.Token, methods=['GET', 'POST'], name="token"),
    Mount('/users', app=Router([
        Route('/', endpoint=endpoints.UserList, methods=['GET'], name="users"),
        Route('/{id:int}', endpoint=endpoints.UserDetail, methods=['GET'], name="user"),
    ])),
    Route('/using-db', endpoint=endpoints.UsingDBTest, methods=['GET'], name="using_db")
])
