import json

import pytest

from tests.helpers import create_request_headers, load_decoded_response


def add_categories(client, data):
    response = client.post(
        '/categories',
        headers=create_request_headers(),
        data=json.dumps(data)
    )
    json_response = load_decoded_response(response)
    return response, json_response


@pytest.mark.parametrize(
    'data, status_code',
    [
        # Test case: Successfully create a new category
        (
                {
                    'name': 'Sports',
                    'description': 'All Sportswear'
                },
                201
        ),
    ]
)
def test_add_categories_valid(client, data, status_code):
    response, json_response = add_categories(client, data)

    assert response.status_code == status_code
    assert all(key in json_response for key in ['id', 'name', 'description', 'created_on']) is True


@pytest.mark.parametrize(
    'data, status_code, message',
    [
        # Test case: Incorrect data type for name
        (
                {
                    'name': [],
                    'description': 'abc'
                },
                400,
                'Not a valid string.'
        ),
        # Test case: Incorrect data type for description
        (
                {
                    'name': "People",
                    'description': []
                },
                400,
                'Not a valid string.'
        ),
        # Test case: Missing name
        (
                {
                    'description': '1997'
                },
                400,
                'Missing data for required field.'
        ),
        # Test case: Name is too long
        (
                {
                    'name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                    'description': 'asdf'
                },
                400,
                'Name must have between 1-45 characters.'
        ),
        # Test case: Category name already exists
        (
                {
                    'name': 'Films',
                    'description': 'After 2000s'
                },
                400,
                'A Category with that name already exists.'
        )
    ]
)
def test_post_categories_invalid(client, data, status_code, message):
    response, json_response = add_categories(client, data)

    assert response.status_code == status_code
    assert json_response['message'] == message
