import pytest

from tests.actions import authorize_user


@pytest.mark.parametrize(
    'authentication, status_code',
    [
        # Test case: Valid user
        (
                {
                    'username': 'bill',
                    'password': 'asdf'
                },
                200
        ),
    ]
)
def test_login_valid(client, authentication, status_code):
    response, json_response = authorize_user(client, authentication)

    assert response.status_code == status_code
    assert all(key in json_response for key in ['access_token', 'username']) is True
    assert any(key in json_response for key in ['password', 'hashed_password']) is False


@pytest.mark.parametrize(
    'authentication, status_code, description',
    [
        # Test case: Incorrect data type for username
        (
                {
                    'username': 1,
                    'password': 'asdf'
                },
                400,
                'Not a valid string.'
        ),
        # Test case: Incorrect data type for password
        (
                {
                    'username': 'bill',
                    'password': []
                },
                400,
                'Not a valid string.'
        ),
        # Test case: Username does not exist
        (
                {
                    'username': 'superman',
                    'password': 'asdf'
                },
                401,
                'Invalid credentials.'
        ),
        # Test case: Wrong password
        (
                {
                    'username': 'bill',
                    'password': '1111'
                },
                401,
                'Invalid credentials.'
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
                    'username': 'bill'
                },
                400,
                'Missing data for required field.'
        )
    ]
)
def test_login_invalid(client, authentication, status_code, description):
    response, json_response = authorize_user(client, authentication)

    assert response.status_code == status_code
    assert json_response['description'] == description
