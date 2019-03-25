import typesystem

from app.forms.types import Email


class LoginSchema(typesystem.Schema):
    email = Email(
        min_length=1,
        max_length=255
    )
    password = typesystem.String(
        min_length=8,
        max_length=20,
        format='password'
    )
