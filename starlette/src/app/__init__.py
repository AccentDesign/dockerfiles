from starlette.applications import Starlette
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app import settings
from app.auth.backends import ModelAuthBackend
from app.globals import templates
from app.middleware import DatabaseMiddleware
from app.routing import routes


# the app
app = Starlette(debug=settings.DEBUG, routes=routes)


# middleware
app.add_middleware(AuthenticationMiddleware, backend=ModelAuthBackend())
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.add_middleware(DatabaseMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)


# exception handlers
@app.exception_handler(404)
async def not_found(request, exc):
    template = '404.html'
    context = {'request': request}
    return templates.TemplateResponse(template, context, status_code=exc.status_code)


@app.exception_handler(500)
async def server_error(request, exc):
    template = '500.html'
    context = {'request': request}
    return templates.TemplateResponse(template, context, status_code=exc.status_code)