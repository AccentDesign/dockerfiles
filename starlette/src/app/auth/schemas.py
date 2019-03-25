import typing
import typesystem


class Email(typesystem.String):
    def __init__(self, **kwargs: typing.Any) -> None:
        # set defaults for the email field
        kwargs['pattern'] = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
        kwargs['format'] = 'email'
        # change the default pattern error message
        self.errors["pattern"] = "Must be a valid email."
        super().__init__(**kwargs)


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
