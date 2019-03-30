from starlette.endpoints import HTTPEndpoint
from starlette.responses import RedirectResponse

from app import settings


class Logout(HTTPEndpoint):
    async def get(self, request):
        request.session.clear()
        return RedirectResponse(request.url_for(settings.LOGOUT_REDIRECT_URL))
