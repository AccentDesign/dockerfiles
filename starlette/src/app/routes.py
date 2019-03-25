from starlette.routing import Mount, Route, Router
from starlette.staticfiles import StaticFiles

from app.endpoints import Homepage
from app.auth.routes import routes as auth_routes
from app.example.routes import routes as example_routes

routes = [
    Route('/', endpoint=Homepage, methods=['GET']),
    Mount('/auth', app=Router(auth_routes), name='auth'),
    Mount('/example', app=Router(example_routes), name='example'),
    Mount('/static', app=StaticFiles(directory='static'), name="static")
]
