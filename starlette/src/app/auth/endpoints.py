from starlette.endpoints import HTTPEndpoint
from starlette.responses import RedirectResponse

from app.auth.models import User
from app.auth.schemas import LoginSchema
from app.globals import forms, templates


class Login(HTTPEndpoint):
    LOGIN_REDIRECT_URL = 'auth:login'

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

            return RedirectResponse(request.url_for(self.LOGIN_REDIRECT_URL))

        form = forms.Form(LoginSchema)
        context = {'request': request, 'form': form}

        return templates.TemplateResponse(template, context)


class Logout(HTTPEndpoint):
    LOGOUT_REDIRECT_URL = 'auth:login'

    async def get(self, request):
        if 'user' in request.session:
            del request.session['user']
        return RedirectResponse(request.url_for(self.LOGOUT_REDIRECT_URL))
