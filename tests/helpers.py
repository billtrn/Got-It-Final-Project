def create_request_headers(access_token=None):
    """
    Create header for request
    :param access_token
    :return: a dictionary of headers
    """
    header = {'Content-Type': 'application/json'}
    if access_token:
        header['Authorization'] = 'Bearer {}'.format(access_token)
    return header


def load_decoded_response(response):
    """
    Load json response into dictionary
    :param response
    :return: response in dictionary format
    """
    return response.json
