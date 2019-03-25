from starlette.middleware.base import BaseHTTPMiddleware

from app.db import SessionLocal


class DatabaseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request.state.db = SessionLocal()
        response = await call_next(request)
        request.state.db.close()
        return response
