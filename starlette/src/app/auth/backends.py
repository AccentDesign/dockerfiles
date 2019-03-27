from starlette.authentication import BaseUser, AuthenticationBackend, AuthCredentials

from app.auth.models import User


class AnonymousUser(BaseUser):
    @property
    def is_authenticated(self) -> bool:
        return False

    @property
    def display_name(self) -> str:
        return ''


class ModelAuthBackend(AuthenticationBackend):
    user_id = None

    def get_user(self):
        if self.user_id:
            return User.query.get(self.user_id)
        else:
            return AnonymousUser()

    async def authenticate(self, request):
        self.user_id = request.session.get('user')
        user = self.get_user()
        status = 'authenticated' if user.is_authenticated else 'anonymous'
        return AuthCredentials([status]), self.get_user()
