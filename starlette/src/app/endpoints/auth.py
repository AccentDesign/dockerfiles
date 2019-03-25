from datetime import datetime, timedelta

import jwt
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
        context = {'request': request}
        return templates.TemplateResponse(template, context)

    async def post(self, request):
        json = await request.json()
        email = json.get('email')
        password = json.get('password')

        user = db_session.query(User).filter(User.email == email).first()
        if user and user.check_password(password):
            payload = {
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(seconds=self.JWT_EXP_DELTA_SECONDS)
            }
            jwt_token = jwt.encode(payload, self.JWT_SECRET, self.JWT_ALGORITHM)
            return JSONResponse({'token': jwt_token.decode('utf-8')})

        return JSONResponse({'error': 'invalid email or password'}, status_code=400)


class Login(HTTPEndpoint):
    async def get(self, request):
        template = 'auth/login.html'
        context = {'request': request}
        return templates.TemplateResponse(template, context)

    async def post(self, request):
        form = await request.form()
        email = form.get('email')
        password = form.get('password')

        user = db_session.query(User).filter(User.email == email).first()
        if user and user.check_password(password):
            request.session['user'] = user.id
            return RedirectResponse(request.url)

        template = 'auth/login.html'
        context = {'request': request}

        return templates.TemplateResponse(template, context)


class Logout(HTTPEndpoint):
    async def get(self, request):
        if 'user' in request.session:
            del request.session['user']
        return RedirectResponse('/auth/login')
