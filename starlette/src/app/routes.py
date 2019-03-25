from starlette.routing import Mount, Route, Router
from starlette.staticfiles import StaticFiles

from . import endpoints


routes = [
    Route('/', endpoint=endpoints.Homepage, methods=['GET']),
    Mount('/auth', app=Router([
        Route('/token', endpoint=endpoints.Token, methods=['GET', 'POST'], name="token"),
        Route('/login', endpoint=endpoints.Login, methods=['GET', 'POST'], name="login"),
        Route('/logout', endpoint=endpoints.Logout, methods=['GET'], name="logout"),
    ])),
    Mount('/users', app=Router([
        Route('/', endpoint=endpoints.Userlist, methods=['GET'], name="users"),
        Route('/{id:int}', endpoint=endpoints.Userdetail, methods=['GET'], name="user"),
    ])),
    Mount('/static', app=StaticFiles(directory='static'), name="static")
]
