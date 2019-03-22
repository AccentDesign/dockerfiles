from datetime import datetime, timedelta

import jwt
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from app import settings
from app.models import db_session, User


templates = Jinja2Templates(directory='templates')


JWT_SECRET = str(settings.SECRET_KEY)
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 20


class Token(HTTPEndpoint):
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
                'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
            }
            jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
            return JSONResponse({'token': jwt_token.decode('utf-8')})

        return JSONResponse({'error': 'invalid email or password'}, status_code=400)
