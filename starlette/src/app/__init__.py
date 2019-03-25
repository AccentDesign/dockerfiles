from starlette.applications import Starlette
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.templating import Jinja2Templates

from app import settings
from app.auth import ModelAuthBackend
from app.routes import routes


# the app
app = Starlette(
    debug=settings.DEBUG,
    routes=routes
)

# middleware
app.add_middleware(
    AuthenticationMiddleware,
    backend=ModelAuthBackend()
)

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY
)

# get our templates directory
templates = Jinja2Templates(directory='templates')


@app.exception_handler(404)
async def not_found(request, exc):
    template = '404.html'
    context = {'request': request}
    return templates.TemplateResponse(template, context, status_code=404)


@app.exception_handler(500)
async def server_error(request, exc):
    template = '500.html'
    context = {'request': request}
    return templates.TemplateResponse(template, context, status_code=500)
