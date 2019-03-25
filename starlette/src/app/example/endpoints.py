from datetime import datetime, timedelta

import jwt
from sqlalchemy.orm import selectinload
from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates
from typesystem import Jinja2Forms

from app import settings
from app.auth.models import User
from app.auth.schemas import LoginSchema


forms = Jinja2Forms(directory='templates')
templates = Jinja2Templates(directory='templates')


class Token(HTTPEndpoint):
    JWT_SECRET = str(settings.SECRET_KEY)
    JWT_ALGORITHM = 'HS256'
    JWT_EXP_DELTA_SECONDS = 20

    async def get(self, request):
        template = 'example/token.html'
        form = forms.Form(LoginSchema)
        context = {'request': request, 'form': form}
        return templates.TemplateResponse(template, context)

    async def post(self, request):
        data = await request.json()

        login, errors = LoginSchema.validate_or_error(data)
        if errors:
            return JSONResponse(dict(errors), status_code=400)

        user = request.state.db.query(User).filter(User.email == login.email).first()
        if user and user.check_password(login.password):
            payload = {
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(seconds=self.JWT_EXP_DELTA_SECONDS)
            }
            jwt_token = jwt.encode(payload, self.JWT_SECRET, self.JWT_ALGORITHM)
            return JSONResponse({'token': jwt_token.decode('utf-8')})

        return JSONResponse({'error': 'invalid email or password'}, status_code=400)


class UserList(HTTPEndpoint):
    @staticmethod
    def get_users(request):
        return request.state.db.query(User).order_by(User.email)

    async def get(self, request):
        template = 'example/users.html'
        users = self.get_users(request)
        context = {'request': request, 'users': users}
        return templates.TemplateResponse(template, context)


class UserDetail(HTTPEndpoint):
    @staticmethod
    def get_user(request):
        user = (
            request.state.db
            .query(User)
            .options(selectinload(User.groups))
            .get(request.path_params['id'])
        )
        if not user:
            raise HTTPException(404)
        return user

    async def get(self, request):
        template = 'example/user.html'
        user = self.get_user(request)
        context = {'request': request, 'user': user}
        return templates.TemplateResponse(template, context)
