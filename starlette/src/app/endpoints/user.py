from sqlalchemy.orm import selectinload
from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.templating import Jinja2Templates

from app.models import db_session, User


templates = Jinja2Templates(directory='templates')


class Userlist(HTTPEndpoint):
    def get_objects(self):
        return db_session.query(User).order_by(User.email)

    async def get(self, request):
        template = 'user/users.html'
        users = self.get_objects()
        context = {'request': request, 'users': users}
        return templates.TemplateResponse(template, context)


class Userdetail(HTTPEndpoint):
    def get_object(self, request):
        user = (
            db_session
            .query(User)
            .options(selectinload(User.groups))
            .get(request.path_params['id'])
        )
        if not user:
            raise HTTPException(404)
        return user

    async def get(self, request):
        template = 'user/user.html'
        user = self.get_object(request)
        context = {'request': request, 'user': user}
        return templates.TemplateResponse(template, context)
