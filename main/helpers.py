import functools

import jwt
from marshmallow import ValidationError
from flask import request
from jwt import InvalidTokenError
from main.exception import BadRequestError
from main.app import app


def token_required(func):
    """
    Check if the  access token is valid.
    :return: Raise a BadRequestError if the token is missing or invalid
    """

    @functools.wraps(func)
    def decorated(*args, **kwargs):
        try:
            token = request.headers['Authorization']
        except KeyError:
            raise BadRequestError('Missing Token')

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except InvalidTokenError:
            raise BadRequestError('Invalid Token')

        return func(*args, **kwargs)

    return decorated


def load_data(schema):
    """
    Deserialize a request using a specified Schema
    :param schema: The Schema used to deserialize
    :return: the deserialized data
    """

    def wrapper(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            try:
                data = schema().load(request.get_json())
            except ValidationError as error:
                message = list(error.messages.values())[0][0]
                raise BadRequestError(message)

            return func(data=data, *args, **kwargs)

        return decorated

    return wrapper


def get_user_id(func):
    """
    Get user_id based on the provided jwt token.
    :return: user_id if the access_token passed is valid. Raise a BadRequestError otherwise.
    """

    @functools.wraps(func)
    def decorated(*args, **kwargs):
        try:
            token = request.headers['Authorization']
        except KeyError:
            raise BadRequestError('Missing Token')

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            user_id = data['sub']
        except InvalidTokenError:
            raise BadRequestError('Invalid Token')

        return func(user_id=user_id, *args, **kwargs)

    return decorated
