from datetime import datetime, timedelta

import jwt
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.exc import NoResultFound
from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from app import settings
from app.auth.models import User
from app.auth.schemas import LoginSchema
from app.globals import forms, templates


class ForceError(HTTPEndpoint):
    async def get(self, request):
        raise ValueError('holy shit')


class Token(HTTPEndpoint):
    JWT_SECRET = str(settings.SECRET_KEY)
    JWT_ALGORITHM = 'HS256'
    JWT_EXP_DELTA_SECONDS = 20

    errors = {
        'invalid': 'invalid email or password'
    }

    async def get(self, request):
        template = 'example/token.html'
        form = forms.Form(LoginSchema)
        context = {'request': request, 'form': form}
        return templates.TemplateResponse(template, context)

    async def post(self, request):
        data = await request.json()

        login, errors = LoginSchema.validate_or_error(data)
        if errors:
            return JSONResponse({'status': self.errors['invalid']}, status_code=400)

        try:
            user = User.query.filter(User.email == login.email.lower()).one()
            if user.check_password(login.password):
                payload = {
                    'user_id': user.id,
                    'exp': datetime.utcnow() + timedelta(seconds=self.JWT_EXP_DELTA_SECONDS)
                }
                jwt_token = jwt.encode(payload, self.JWT_SECRET, self.JWT_ALGORITHM)
                return JSONResponse({'token': jwt_token.decode('utf-8')})

        except NoResultFound:
            pass

        return JSONResponse({'status': self.errors['invalid']}, status_code=400)


class UserList(HTTPEndpoint):
    async def get(self, request):
        template = 'example/users.html'
        users = User.query.order_by(User.email)
        context = {'request': request, 'users': users}
        return templates.TemplateResponse(template, context)


class UserDetail(HTTPEndpoint):
    @staticmethod
    def get_user(pk):
        user = User.query.options(selectinload(User.groups)).get(pk)
        if not user:
            raise HTTPException(404)
        return user

    async def get(self, request):
        template = 'example/user.html'
        user = self.get_user(request.path_params['id'])
        context = {'request': request, 'user': user}
        return templates.TemplateResponse(template, context)
