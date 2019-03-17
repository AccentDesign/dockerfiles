from .base import (
    INSTALLED_APPS,
    MIDDLEWARE
)


# Security

DEBUG = True


# debug toolbar

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_COLLAPSED': True,
    'SHOW_TOOLBAR_CALLBACK': 'app.settings.helpers.show_toolbar',
}

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


# auth

AUTH_PASSWORD_VALIDATORS = []
