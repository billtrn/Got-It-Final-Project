import random

from tests.helpers import create_request_headers, load_decoded_response


def get_category(client, category_id):
    response = client.get(
        '/categories/{}'.format(category_id),
        headers=create_request_headers(),
    )
    json_response = load_decoded_response(response)
    return response, json_response


def test_get_category_successfully(client):
    response, json_response = get_category(client, 1)

    assert response.status_code == 200
    assert all(key in json_response for key in ['id', 'name', 'description', 'created']) is True


def test_fail_to_get_category(client):
    response, json_response = get_category(client, 5)

    assert response.status_code == 404
    assert json_response['message'] == 'No Category with that ID.'
