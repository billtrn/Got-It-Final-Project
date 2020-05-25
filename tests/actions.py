import json

from tests.helpers import create_request_headers, load_decoded_response


def register_user(client, information):
    """
    Send request to register user
    :param information
    :param client
    """

    response = client.post(
        '/users',
        headers=create_request_headers(),
        data=json.dumps(information)
    )
    json_response = load_decoded_response(response)
    return response, json_response


def authorize_user(client, authentication):
    """
    Send request to log in user
    :param authentication
    :param client
    """

    response = client.post(
        '/auth',
        headers=create_request_headers(),
        data=json.dumps(authentication)
    )
    json_response = load_decoded_response(response)
    return response, json_response


def get_access_token(client, authentication):
    json_response = authorize_user(client, authentication)[1]
    return json_response['access_token']
