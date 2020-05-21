from tests.helpers import create_request_headers, load_decoded_response, get_category_ids


def get_items(client, category_id=None):
    response = client.get(
        '/categories/{}/items'.format(category_id),
        headers=create_request_headers(),
    )
    json_response = load_decoded_response(response)
    return response, json_response


def test_get_items_valid(client):
    response, json_response = get_items(client, category_id=1)
    assert response.status_code == 200
    for category in json_response:
        assert all(key in category for key in ['id', 'name', 'description']) is True


def test_get_items_invalid(client):
    category_id = max(get_category_ids()) + 1
    response, json_response = get_items(client, category_id)

    assert response.status_code == 404
    assert json_response['message'] == 'No Category with that ID.'


