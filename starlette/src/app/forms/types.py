import typing

import typesystem


class Email(typesystem.String):
    errors = typesystem.String.errors
    errors.update({"pattern": "Must be a valid email."})

    def __init__(self, **kwargs: typing.Any) -> None:
        kwargs['pattern'] = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
        kwargs['format'] = 'email'
        self.errors["pattern"] = "Must be a valid email."
        super().__init__(**kwargs)
