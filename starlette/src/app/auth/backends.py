from starlette.authentication import BaseUser, AuthenticationBackend, AuthCredentials
from starlette.requests import Request

from app.auth.models import User


class ModelUser(BaseUser):

    def __init__(self, request: Request) -> None:
        self.request = request

    def _get_user(self):
        user_id = self.request.session.get('user')
        user = None
        if user_id:
            user = self.request.state.db.query(User).get(user_id)
        return user

    @property
    def instance(self):
        if hasattr(self, '_instance'):
            return getattr(self, '_instance')

        user = self._get_user()
        setattr(self, '_instance', user)

        return getattr(self, '_instance', None)

    @property
    def is_authenticated(self) -> bool:
        return self.instance is not None

    @property
    def display_name(self) -> str:
        return getattr(self.instance, 'display_name', '')


class ModelAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        return AuthCredentials(["authenticated"]), ModelUser(request)
