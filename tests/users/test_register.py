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
def test_register_valid(client, authentication, status_code):
    response, json_response = register_user(client, authentication)

    assert response.status_code == status_code
    assert all(key in json_response for key in ['id', 'username']) is True
    assert any(key in json_response for key in ['password', 'hashed_password']) is False


@pytest.mark.parametrize(
    'authentication, status_code, description',
    [
        # Test case: Incorrect data type for username
        (
                {
                    'username': [],
                    'password': 'asdf'
                },
                400,
                'Invalid Input'
        ),
        # Test case: Incorrect data type for password
        (
                {
                    'username': 'wilson',
                    'password': 1
                },
                400,
                'Invalid Input'
        ),
        # Test case: Username already exists
        (
                {
                    'username': 'bill',
                    'password': 'qwerty'
                },
                400,
                'An User with that name already exists'
        ),
        # Test case: Missing username
        (
                {
                    'password': 'asdf'
                },
                400,
                'Missing Input'
        ),
        # Test case: Missing password
        (
                {
                    'username': 'brian123'
                },
                400,
                'Missing Input'
        ),

        # Test case: Username is too long
        (
                {
                    'username': 'billbillbillbillbillbillbillbillbillbillbillbillbillbillbill',
                    'password': 'asdf'
                },
                400,
                'Invalid Input'
        ),
        # Test case: Password is too long
        (
                {
                    'username': 'warren',
                    'password': 'billbillbillbillbillbillbillbillbillbillbillbillbillbillbill'
                },
                400,
                'Invalid Input'
        ),
    ]
)
def test_register_invalid(client, authentication, status_code, description):
    response, json_response = register_user(client, authentication)

    assert response.status_code == status_code
    assert json_response['description'] == description
