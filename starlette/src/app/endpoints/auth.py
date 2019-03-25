from datetime import datetime, timedelta

import jwt
from app.forms import forms, LoginSchema
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app import settings
from app.models import db_session, User


templates = Jinja2Templates(directory='templates')


class Token(HTTPEndpoint):
    JWT_SECRET = str(settings.SECRET_KEY)
    JWT_ALGORITHM = 'HS256'
    JWT_EXP_DELTA_SECONDS = 20

    async def get(self, request):
        template = 'auth/token.html'
        form = forms.Form(LoginSchema)
        context = {'request': request, 'form': form}
        return templates.TemplateResponse(template, context)

    async def post(self, request):
        data = await request.json()

        login, errors = LoginSchema.validate_or_error(data)
        if errors:
            return JSONResponse(dict(errors), status_code=400)

        user = db_session.query(User).filter(User.email == login.email).first()
        if user and user.check_password(login.password):
            payload = {
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(seconds=self.JWT_EXP_DELTA_SECONDS)
            }
            jwt_token = jwt.encode(payload, self.JWT_SECRET, self.JWT_ALGORITHM)
            return JSONResponse({'token': jwt_token.decode('utf-8')})

        return JSONResponse({'error': 'invalid email or password'}, status_code=400)


class Login(HTTPEndpoint):
    LOGIN_REDIRECT_URL = '/auth/login'

    async def get(self, request):
        template = 'auth/login.html'
        form = forms.Form(LoginSchema)
        context = {'request': request, 'form': form}
        return templates.TemplateResponse(template, context)

    async def post(self, request):
        template = 'auth/login.html'

        data = await request.form()
        login, errors = LoginSchema.validate_or_error(data)
        if errors:
            form = forms.Form(LoginSchema, values=data, errors=errors)
            context = {'request': request, 'form': form}

            return templates.TemplateResponse(template, context)

        user = db_session.query(User).filter(User.email == login.email).first()
        if user and user.check_password(login.password):
            request.session['user'] = user.id

            return RedirectResponse(self.LOGIN_REDIRECT_URL)

        form = forms.Form(LoginSchema)
        context = {'request': request, 'form': form}

        return templates.TemplateResponse(template, context)


class Logout(HTTPEndpoint):
    LOGOUT_REDIRECT_URL = '/auth/login'

    async def get(self, request):
        if 'user' in request.session:
            del request.session['user']
        return RedirectResponse(self.LOGOUT_REDIRECT_URL)
