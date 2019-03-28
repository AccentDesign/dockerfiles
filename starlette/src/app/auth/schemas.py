import typesystem

from app.typings import Email


class LoginSchema(typesystem.Schema):
    email = Email()
    password = typesystem.String(
        min_length=8,
        max_length=20,
        format='password'
    )
