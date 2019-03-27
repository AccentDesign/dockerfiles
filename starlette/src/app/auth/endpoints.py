from starlette.endpoints import HTTPEndpoint
from starlette.responses import RedirectResponse

from app import settings
from app.auth.models import User
from app.auth.schemas import LoginSchema
from app.globals import forms, templates


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

        user = request.state.db.query(User).filter(User.email == login.email).first()
        if user and user.check_password(login.password):
            request.session['user'] = user.id

            return RedirectResponse(request.url_for(settings.LOGIN_REDIRECT_URL))

        form = forms.Form(LoginSchema)
        context = {'request': request, 'form': form}

        return templates.TemplateResponse(template, context)


class Logout(HTTPEndpoint):
    async def get(self, request):
        request.session.clear()
        return RedirectResponse(request.url_for(settings.LOGOUT_REDIRECT_URL))
