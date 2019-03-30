from sqlalchemy.orm.exc import NoResultFound
from starlette.endpoints import HTTPEndpoint
from starlette.responses import RedirectResponse
from typesystem import Message, ValidationError

from app import settings
from app.globals import forms, templates
from ..models import User
from ..schemas import LoginSchema


class Login(HTTPEndpoint):
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

        try:
            user = User.query.filter(User.email == login.email.lower()).one()
            if user.check_password(login.password):
                request.session['user'] = user.id
                return RedirectResponse(request.url_for(settings.LOGIN_REDIRECT_URL))

        except NoResultFound:
            pass

        request.session.clear()

        message = Message(text='Invalid email or password.', index=['password'])
        errors = ValidationError(messages=[message])

        form = forms.Form(LoginSchema, errors=errors)
        context = {'request': request, 'form': form}

        return templates.TemplateResponse(template, context)
