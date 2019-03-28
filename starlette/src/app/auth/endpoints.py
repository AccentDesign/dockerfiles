from sqlalchemy.orm.exc import NoResultFound
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.responses import RedirectResponse

from app import settings
from app.globals import forms, templates
from .models import User
from .schemas import LoginSchema


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
    @requires(['authenticated'], redirect=settings.LOGOUT_REDIRECT_URL)
    async def get(self, request):
        request.session.clear()
        return RedirectResponse(request.url_for(settings.LOGOUT_REDIRECT_URL))
