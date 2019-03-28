from starlette.config import Config
from starlette.datastructures import URL, Secret, CommaSeparatedStrings


config = Config()


DEBUG = config('DEBUG', cast=bool, default=False)
TESTING = config('TESTING', cast=bool, default=False)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CommaSeparatedStrings)
DATABASE_URL = config('DATABASE_URL', cast=URL)
LOGIN_URL = config('LOGIN_URL', cast=str, default='auth:login')
LOGIN_REDIRECT_URL = config('LOGIN_REDIRECT_URL', cast=str, default='auth:login')
LOGOUT_REDIRECT_URL = config('LOGOUT_REDIRECT_URL', cast=str, default='auth:login')
SECRET_KEY = config('SECRET_KEY', cast=Secret)

if TESTING:
    DATABASE_URL = DATABASE_URL.replace(path=DATABASE_URL.path + '_test')
