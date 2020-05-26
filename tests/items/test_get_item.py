import random

import pytest

from tests.helpers import create_request_headers, load_decoded_response


def get_item(client, category_id=None, item_id=None):
    response = client.get(
        '/categories/{}/items/{}'.format(category_id, item_id),
        headers=create_request_headers(),
    )
    json_response = load_decoded_response(response)
    return response, json_response


def test_get_item_successfully(client):
    response, json_response = get_item(client, category_id=1, item_id=1)
    assert response.status_code == 200
    assert all(key in json_response for key in ['id', 'name', 'description', 'created', 'updated', 'user_id']) is True


@pytest.mark.parametrize(
    'category_id, item_id, status_code, message',
    [
        # Test case: Category not found
        (
                5,
                1,
                404,
                'No Category with that ID.'
        ),
        # Test case: Item not found
        (
                1,
                5,
                404,
                'No items with that ID in this category.'
        ),
    ]
)
def test_fail_to_get_item(client, category_id, item_id, status_code, message):
    response, json_response = get_item(client, category_id=category_id, item_id=item_id)

    assert response.status_code == status_code
    assert json_response['message'] == message
