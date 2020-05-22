import json

import pytest

from tests.actions import get_access_token
from tests.helpers import create_request_headers, load_decoded_response, get_category_ids


def add_items(client, authentication=None, category_id=None, data=None):
    access_token = get_access_token(client, authentication)
    response = client.post(
        '/categories/{}/items'.format(category_id),
        headers=create_request_headers(access_token=access_token),
        data=json.dumps(data)
    )
    json_response = load_decoded_response(response)
    return response, json_response


@pytest.mark.parametrize(
    'authentication, category_id, data',
    [
        # Test case: Name does not exist
        (
                {'username': 'bill', 'password': 'asdf'},
                1,
                {
                    'name': 'Avengers',
                    'description': '2012'
                }
        ),
    ]
)
def test_post_items_valid(client, authentication, category_id, data):
    response, json_response = add_items(client, authentication=authentication, category_id=category_id, data=data)

    assert response.status_code == 201
    assert all(key in json_response for key in ['id', 'name', 'description', 'created', 'user_id']) is True


@pytest.mark.parametrize(
    'authentication, category_id, data, status_code, message',
    [
        # Test case: Incorrect data type for name
        (
                {'username': 'bill', 'password': 'asdf'},
                1,
                {
                    'name': [],
                    'description': '2020'
                },
                400,
                'Not a valid string.'
        ),
        # Test case: Incorrect data type for description
        (
                {'username': 'bill', 'password': 'asdf'},
                1,
                {
                    'name': 'Endgame',
                    'description': []
                },
                400,
                'Not a valid string.'
        ),
        # Test case: Missing name
        (
                {'username': 'bill', 'password': 'asdf'},
                1,
                {
                    'description': 'Loki'
                },
                400,
                'Missing data for required field.'
        ),
        # Test case: Name is too long
        (
                {'username': 'bill', 'password': 'asdf'},
                1,
                {
                    'name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                    'description': '1975'
                },
                400,
                'Name must have between 1-45 characters.'
        ),
        # Test case: Category not found
        (
                {'username': 'bill', 'password': 'asdf'},
                max(get_category_ids()) + 1,
                {
                    'name': 'Titanic',
                    'description': '1999'
                },
                404,
                'No Category with that ID.'
        ),
    ]
)
def test_post_items_with_invalid_data(client, authentication, category_id, data, status_code, message):
    response, json_response = add_items(client, authentication=authentication, category_id=category_id, data=data)

    assert response.status_code == status_code
    assert json_response['message'] == message


def test_add_items_invalid_token(client):
    response = client.post(
        '/categories/{}/items'.format(1),
        headers=create_request_headers(access_token='a' * 140),
        data=json.dumps({
            'name': 'Matrix',
            'description': '1995'
        })
    )
    json_response = load_decoded_response(response)

    assert response.status_code == 400
    assert json_response['message'] == 'Invalid Token'


def test_add_items_missing_token(client):
    response = client.post(
        '/categories/{}/items'.format(1),
        headers=create_request_headers(access_token=None),
        data=json.dumps({
            'name': 'Matrix 2',
            'description': '1998'
        })
    )
    json_response = load_decoded_response(response)

    assert response.status_code == 400
    assert json_response['message'] == 'Missing Token'
