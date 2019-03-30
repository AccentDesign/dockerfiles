from starlette.config import Config
from starlette.datastructures import URL, Secret, CommaSeparatedStrings


config = Config()

# base
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CommaSeparatedStrings)
DATABASE_URL = config('DATABASE_URL', cast=URL)
DEBUG = config('DEBUG', cast=bool, default=False)
SECRET_KEY = config('SECRET_KEY', cast=Secret)
TESTING = config('TESTING', cast=bool, default=False)

# auth
LOGIN_URL = config('LOGIN_URL', cast=str, default='auth:login')
LOGIN_REDIRECT_URL = config('LOGIN_REDIRECT_URL', cast=str, default='auth:login')
LOGOUT_REDIRECT_URL = config('LOGOUT_REDIRECT_URL', cast=str, default='auth:login')
CHANGE_PASSWORD_REDIRECT_URL = config('CHANGE_PASSWORD_REDIRECT_URL', cast=str, default='auth:login')

# test
if TESTING:
    DATABASE_URL = DATABASE_URL.replace(path=DATABASE_URL.path + '_test')
