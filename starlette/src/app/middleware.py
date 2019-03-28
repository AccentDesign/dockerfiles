from starlette.middleware.base import BaseHTTPMiddleware

from app.db import Session


class DatabaseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request.state.db = Session()
        response = await call_next(request)
        request.state.db.close()
        return response
