from starlette.config import Config
from starlette.datastructures import URL, Secret, CommaSeparatedStrings


config = Config()


ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CommaSeparatedStrings)
DATABASE_URL = config('DATABASE_URL', cast=URL)
DEBUG = config('DEBUG', cast=bool, default=False)
LOGIN_REDIRECT_URL = config('LOGIN_REDIRECT_URL', cast=str, default='auth:login')
LOGOUT_REDIRECT_URL = config('LOGOUT_REDIRECT_URL', cast=str, default='auth:login')
SECRET_KEY = config('SECRET_KEY', cast=Secret)
