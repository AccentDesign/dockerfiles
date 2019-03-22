from starlette.routing import Mount, Route, Router
from starlette.staticfiles import StaticFiles

from . import endpoints


routes = [
    Route('/', endpoint=endpoints.Homepage, methods=['GET']),
    Route('/auth/token', endpoint=endpoints.Token, methods=['GET', 'POST'], name="token"),
    Mount('/users', app=Router([
        Route('/', endpoint=endpoints.Userlist, methods=['GET'], name="users"),
        Route('/{id:int}', endpoint=endpoints.Userdetail, methods=['GET'], name="user"),
    ])),
    Mount('/static', app=StaticFiles(directory='static'), name="static")
]
