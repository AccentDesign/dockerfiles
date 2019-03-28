from starlette.routing import Route, Router

from .endpoints import Login, Logout


app = Router([
    Route('/login', endpoint=Login, methods=['GET', 'POST'], name="login"),
    Route('/logout', endpoint=Logout, methods=['GET'], name="logout"),
])
