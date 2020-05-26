import pytest

from tests.actions import register_user


@pytest.mark.parametrize(
    'authentication, status_code',
    [
        # Test case: Valid user
        (
                {
                    'username': 'alex',
                    'password': 'asdf'
                },
                201
        ),
    ]
)
def test_register_successfully(client, authentication, status_code):
    response, json_response = register_user(client, authentication)

    assert response.status_code == status_code
    assert all(key in json_response for key in ['id', 'username', 'created']) is True
    assert all(key not in json_response for key in ['password', 'hashed_password']) is True


@pytest.mark.parametrize(
    'authentication, status_code, message',
    [
        # Test case: Incorrect data type for username
        (
                {
                    'username': [],
                    'password': 'asdf'
                },
                400,
                'Not a valid string.'
        ),
        # Test case: Incorrect data type for password
        (
                {
                    'username': 'wilson',
                    'password': 1
                },
                400,
                'Not a valid string.'
        ),
        # Test case: Username already exists
        (
                {
                    'username': 'bill',
                    'password': 'qwerty'
                },
                400,
                'An User with that name already exists.'
        ),
        # Test case: Missing username
        (
                {
                    'password': 'asdf'
                },
                400,
                'Missing data for required field.'
        ),
        # Test case: Missing password
        (
                {
                    'username': 'willy'
                },
                400,
                'Missing data for required field.'
        ),

        # Test case: Username is too long
        (
                {
                    'username': 'a' * 60,
                    'password': 'asdf'
                },
                400,
                'Username must have between 1-45 characters.'
        ),
        # Test case: Password is too long
        (
                {
                    'username': 'warren',
                    'password': 'a' * 60
                },
                400,
                'Password must have between 1-45 characters.'
        ),
        # Test case: Username contains special characters
        (
                {
                    'username': 'bill@',
                    'password': 'asdf'
                },
                400,
                'Username must contain only letters and numbers.'
        )
    ]
)
def test_fail_to_register(client, authentication, status_code, message):
    response, json_response = register_user(client, authentication)

    assert response.status_code == status_code
    assert json_response['message'] == message
