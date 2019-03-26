from starlette.templating import Jinja2Templates
from typesystem import Jinja2Forms


forms = Jinja2Forms(directory='templates')
templates = Jinja2Templates(directory='templates')
