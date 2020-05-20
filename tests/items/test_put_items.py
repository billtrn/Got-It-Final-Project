import json
import random

import pytest

from tests.actions import get_access_token
from tests.helpers import create_request_headers, load_decoded_response, get_category_ids, get_item_ids


def put_item(client, authentication=None, category_id=None, item_id=None, data=None):
    access_token = get_access_token(client, authentication)
    response = client.put(
        '/categories/{}/items/{}'.format(category_id, item_id),
        headers=create_request_headers(access_token=access_token),
        data=json.dumps(data)
    )
    json_response = load_decoded_response(response)
    return response, json_response


@pytest.mark.parametrize(
    'authentication, category_id, item_id, data',
    [
        # Test case: Update successfully
        (
                {'username': 'bill', 'password': 'asdf'},
                1,
                1,
                {
                    'name': 'Shawshank Redemption',
                    'description': '1975'
                }
        )
    ]
)
def test_put_item_valid(client, authentication, category_id, item_id, data):
    response, json_response = put_item(
        client, authentication=authentication, category_id=category_id, item_id=item_id, data=data)

    assert response.status_code == 200
    assert all(key in json_response for key in ['id', 'name', 'description']) is True


@pytest.mark.parametrize(
    'authentication, category_id, item_id, data, status_code, description',
    [
        # Test case: Incorrect data type for name
        (
                {'username': 'bill', 'password': 'asdf'},
                1,
                1,
                {
                    'name': [],
                    'description': '1968'
                },
                400,
                'Invalid Input'
        ),
        # Test case: Incorrect data type for description
        (
                {'username': 'bill', 'password': 'asdf'},
                1,
                1,
                {
                    'name': 'Shawshank',
                    'description': []
                },
                400,
                'Invalid Input'
        ),
        # Test case: Missing name
        (
                {'username': 'bill', 'password': 'asdf'},
                1,
                1,
                {
                    'description': '1976'
                },
                400,
                'Missing Input'
        ),
        # Test case: Name is too long
        (
                {'username': 'bill', 'password': 'asdf'},
                1,
                1,
                {
                    'name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                    'description': '2000'
                },
                400,
                'Invalid Input'
        ),
        # Test case: Category not found
        (
                {'username': 'bill', 'password': 'asdf'},
                max(get_category_ids()) + 1,
                random.choice(get_item_ids()),
                {
                    'name': 'Kong',
                    'description': '2005'
                },
                404,
                'No Category with that ID'
        ),
        # Test case: Item not found
        (
                {'username': 'bill', 'password': 'asdf'},
                random.choice(get_category_ids()),
                max(get_item_ids()) + 1,
                {
                    'name': 'Kong',
                    'description': '2005'
                },
                404,
                'No Item with that ID'
        ),
        # Test case: Trying to update an item you did not post
        (
                {'username': 'duc', 'password': 'ghjk'},
                1,
                1,
                {
                    'name': 'Race',
                    'description': '1996'
                },
                403,
                'Not allowed to modify this item'
        ),
    ]
)
def test_put_item_with_invalid_data(client, authentication, category_id, item_id, data, status_code, description):
    response, json_response = put_item(
        client, authentication=authentication,
        category_id=category_id, item_id=item_id, data=data)

    assert response.status_code == status_code
    assert json_response['description'] == description


def test_put_item_with_invalid_token(client):
    response = client.delete(
        '/categories/{}/items/{}'.format(1, 1),
        headers=create_request_headers(access_token='a' * 140),
        data=json.dumps({
            'name': 'Kong',
            'description': '2005'
        })
    )
    json_response = load_decoded_response(response)

    assert response.status_code == 400
    assert json_response['description'] == 'Invalid Token'
