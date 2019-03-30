from app.auth.schemas import ChangePasswordSchema


def test_fields():
    keys = ChangePasswordSchema.fields.keys()
    assert list(keys) == ['old_password', 'new_password', 'confirm_new_password']


def test_valid():
    data = {
        'old_password': 'password',
        'new_password': 'password',
        'confirm_new_password': 'password'
    }
    result, errors = ChangePasswordSchema.validate_or_error(data)
    assert dict(result) == data
    assert errors is None


def test_invalid():
    data = {}
    _, errors = ChangePasswordSchema.validate_or_error(data)
    assert dict(errors) == {
        'old_password': 'This field is required.',
        'new_password': 'This field is required.',
        'confirm_new_password': 'This field is required.'
    }

    data = {'old_password': '', 'new_password': '', 'confirm_new_password': ''}
    _, errors = ChangePasswordSchema.validate_or_error(data)
    assert dict(errors) == {
        'old_password': 'Must not be blank.',
        'new_password': 'Must not be blank.',
        'confirm_new_password': 'Must not be blank.'
    }

    data = {'old_password': 'pass', 'new_password': 'pass', 'confirm_new_password': 'pass'}
    _, errors = ChangePasswordSchema.validate_or_error(data)
    assert dict(errors) == {
        'old_password': 'Must have at least 8 characters.',
        'new_password': 'Must have at least 8 characters.',
        'confirm_new_password': 'Must have at least 8 characters.'
    }

    data = {
        'old_password': 'password',
        'new_password': 'password1',
        'confirm_new_password': 'password2'
    }
    result, errors = ChangePasswordSchema.validate_or_error(data)
    assert dict(errors) == {
        'confirm_new_password': 'The passwords do not match.'
    }
