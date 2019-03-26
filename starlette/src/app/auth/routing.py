from starlette.routing import Route

from app.auth.endpoints import Login, Logout


routes = [
    Route('/login', endpoint=Login, methods=['GET', 'POST'], name="login"),
    Route('/logout', endpoint=Logout, methods=['GET'], name="logout"),
]
