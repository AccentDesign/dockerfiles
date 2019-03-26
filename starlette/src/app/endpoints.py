from starlette.endpoints import HTTPEndpoint

from app.globals import templates


class Homepage(HTTPEndpoint):
    async def get(self, request):
        template = 'index.html'
        context = {'request': request}
        return templates.TemplateResponse(template, context)
