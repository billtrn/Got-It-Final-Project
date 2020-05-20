import pytest
import random
from tests.actions import get_access_token
from tests.helpers import create_request_headers, load_decoded_response, get_category_ids, get_item_ids


def delete_item(client, authentication=None, category_id=None, item_id=None):
    access_token = get_access_token(client, authentication)
    response = client.delete(
        '/categories/{}/items/{}'.format(category_id, item_id),
        headers=create_request_headers(access_token=access_token)
    )
    return response


def test_delete_item_valid(client):
    authentication = {'username': 'bill', 'password': 'asdf'}
    response = delete_item(client, authentication=authentication, category_id=1, item_id=1)

    assert response.status_code == 200


@pytest.mark.parametrize(
    'authentication, category_id, item_id, status_code, description',
    [
        # Test case: Category not found
        (
                {'username': 'bill', 'password': 'asdf'},
                max(get_category_ids()) + 1,
                random.choice(get_item_ids()),
                404,
                'No Category with that ID'
        ),
        # Test case: Item not found
        (
                {'username': 'bill', 'password': 'asdf'},
                random.choice(get_category_ids()),
                max(get_item_ids()) + 1,
                404,
                'No Item with that ID'
        ),
        # Test case: Trying to delete an item you do not own
        (
                {'username': 'duc', 'password': 'ghjk'},
                1,
                random.choice(get_item_ids()),
                403,
                'Not allowed to modify this item'
        ),
    ]
)
def test_delete_item_with_invalid_data(client, authentication, category_id, item_id, status_code, description):
    response = delete_item(client, authentication=authentication, category_id=category_id, item_id=item_id)
    json_response = load_decoded_response(response)

    assert response.status_code == status_code
    assert json_response['description'] == description


def test_delete_item_with_invalid_token(client):
    category_id = 1
    item_id = random.choice(get_item_ids())
    response = client.delete(
        '/categories/{}/items/{}'.format(category_id, item_id),
        headers=create_request_headers(access_token='a' * 130)
    )
    json_response = load_decoded_response(response)

    assert response.status_code == 400
    assert json_response['description'] == 'Invalid Token'
