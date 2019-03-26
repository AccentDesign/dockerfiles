from starlette.middleware.base import BaseHTTPMiddleware

from app.db import db_session


class DatabaseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request.state.db = db_session
        response = await call_next(request)
        request.state.db.close()
        return response
