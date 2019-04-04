from starlette.applications import Starlette
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Route
from starlette.staticfiles import StaticFiles

from app import db, endpoints, handlers, settings
from app.auth import app as auth_app
from app.auth.backends import ModelAuthBackend
from app.example import app as example_app


# base app
app = Starlette(
    debug=settings.DEBUG,
    routes=[
        Route('/', endpoint=endpoints.Homepage, methods=['GET'])
    ]
)

# sub apps
app.mount(path='/auth', app=auth_app, name='auth')
app.mount(path='/example', app=example_app, name='example')

# static app
app.mount(path='/static', app=StaticFiles(directory='static'), name='static')

# middleware
app.add_middleware(AuthenticationMiddleware, backend=ModelAuthBackend())
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.add_middleware(GZipMiddleware)

# exception handlers
app.add_exception_handler(404, handlers.not_found)
app.add_exception_handler(500, handlers.server_error)

# sentry
if settings.SENTRY_DSN:
    try:
        from sentry_asgi import SentryMiddleware
        import sentry_sdk
        sentry_sdk.init(str(settings.SENTRY_DSN))
        app = SentryMiddleware(app)
    except ImportError:
        pass
