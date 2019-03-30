from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.responses import RedirectResponse
from typesystem import ValidationError, Message

from app import settings
from app.globals import forms, templates
from ..schemas import ChangePasswordSchema


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
