from starlette.config import Config
from starlette.datastructures import URL, Secret, CommaSeparatedStrings


config = Config()


DEBUG = config('DEBUG', cast=bool, default=False)
DATABASE_URL = config('DATABASE_URL', cast=URL)
SECRET_KEY = config('SECRET_KEY', cast=Secret)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CommaSeparatedStrings)
