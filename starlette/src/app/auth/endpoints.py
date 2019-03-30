from sqlalchemy.orm.exc import NoResultFound
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.responses import RedirectResponse
from typesystem import ValidationError, Message

from app import settings
from app.globals import forms, templates
from .models import User
from .schemas import LoginSchema, ChangePasswordSchema


class ChangePassword(HTTPEndpoint):
    @requires(['authenticated'])
    async def get(self, request):
        template = 'auth/change_password.html'
        form = forms.Form(ChangePasswordSchema)
        context = {'request': request, 'form': form}
        return templates.TemplateResponse(template, context)

    @requires(['authenticated'])
    async def post(self, request):
        template = 'auth/change_password.html'

        data = await request.form()
        passwords, errors = ChangePasswordSchema.validate_or_error(data)

        if errors:
            form = forms.Form(ChangePasswordSchema, errors=errors)
            context = {'request': request, 'form': form}
            return templates.TemplateResponse(template, context)

        if not request.user.check_password(passwords.old_password):
            message = Message(text='Enter your current Password.', index=['old_password'])
            errors = ValidationError(messages=[message])

            form = forms.Form(ChangePasswordSchema, errors=errors)
            context = {'request': request, 'form': form}
            return templates.TemplateResponse(template, context)

        else:
            request.user.set_password(passwords.new_password)

        return RedirectResponse(request.url_for(settings.CHANGE_PASSWORD_REDIRECT_URL))


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

        form = forms.Form(LoginSchema)
        context = {'request': request, 'form': form}

        return templates.TemplateResponse(template, context)


class Logout(HTTPEndpoint):
    async def get(self, request):
        request.session.clear()
        return RedirectResponse(request.url_for(settings.LOGOUT_REDIRECT_URL))
