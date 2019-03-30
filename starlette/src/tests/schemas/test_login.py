from app.auth.schemas import LoginSchema


def test_fields():
    keys = LoginSchema.fields.keys()
    assert list(keys) == ['email', 'password']


def test_valid():
    data = {'email': 'stu@example.com', 'password': 'password'}
    result, errors = LoginSchema.validate_or_error(data)
    assert dict(result) == data
    assert errors is None


def test_invalid():
    data = {}
    _, errors = LoginSchema.validate_or_error(data)
    assert dict(errors) == {'email': 'This field is required.', 'password': 'This field is required.'}

    data = {'email': '', 'password': ''}
    _, errors = LoginSchema.validate_or_error(data)
    assert dict(errors) == {'email': 'Must not be blank.', 'password': 'Must not be blank.'}

    data = {'email': 'invalid.com'}
    _, errors = LoginSchema.validate_or_error(data)
    assert dict(errors)['email'] == 'Must be a valid email.'

    data = {'password': 'pass'}
    _, errors = LoginSchema.validate_or_error(data)
    assert dict(errors)['password'] == 'Must have at least 8 characters.'
