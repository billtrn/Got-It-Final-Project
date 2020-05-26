import random

import pytest

from tests.actions import get_access_token
from tests.helpers import create_request_headers, load_decoded_response


def delete_item(client, authentication=None, category_id=None, item_id=None):
    access_token = get_access_token(client, authentication)
    response = client.delete(
        '/categories/{}/items/{}'.format(category_id, item_id),
        headers=create_request_headers(access_token=access_token)
    )
    return response


def test_delete_item_successfully(client):
    authentication = {'username': 'bill', 'password': 'asdf'}
    response = delete_item(client, authentication=authentication, category_id=1, item_id=1)

    assert response.status_code == 200


@pytest.mark.parametrize(
    'authentication, category_id, item_id, status_code, message',
    [
        # Test case: Category not found
        (
                {'username': 'bill', 'password': 'asdf'},
                5,
                1,
                404,
                'No Category with that ID.'
        ),
        # Test case: Item not found
        (
                {'username': 'bill', 'password': 'asdf'},
                1,
                5,
                404,
                'No items with that ID in this category.'
        ),
        # Test case: Trying to delete an item you do not own
        (
                {'username': 'duc', 'password': 'ghjk'},
                1,
                1,
                403,
                'Not allowed to modify this item.'
        ),
    ]
)
def test_fail_to_delete_item_invalid_data(client, authentication, category_id, item_id, status_code, message):
    response = delete_item(client, authentication=authentication, category_id=category_id, item_id=item_id)
    json_response = load_decoded_response(response)

    assert response.status_code == status_code
    assert json_response['message'] == message


def test_fail_to_delete_item_invalid_token(client):
    response = client.delete(
        '/categories/{}/items/{}'.format(1, 1),
        headers=create_request_headers(access_token='a' * 130)
    )
    json_response = load_decoded_response(response)

    assert response.status_code == 400
    assert json_response['message'] == 'Invalid Token'


def test_fail_to_delete_item_missing_token(client):
    response = client.delete(
        '/categories/{}/items/{}'.format(1, 1),
        headers=create_request_headers(access_token=None)
    )
    json_response = load_decoded_response(response)

    assert response.status_code == 400
    assert json_response['message'] == 'Missing Token'
