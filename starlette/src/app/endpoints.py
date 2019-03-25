from starlette.endpoints import HTTPEndpoint
from starlette.templating import Jinja2Templates


templates = Jinja2Templates(directory='templates')


class Homepage(HTTPEndpoint):
    async def get(self, request):
        template = 'index.html'
        context = {'request': request}
        return templates.TemplateResponse(template, context)
