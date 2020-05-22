import functools

import jwt
from marshmallow import ValidationError
from flask import request
from jwt import InvalidTokenError

from main.exception import BadRequestError, NotFoundError
from main.app import app
from main.models.category import CategoryModel
from main.models.item import ItemModel


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


def token_required(func):
    """
    Get user_id based on the provided jwt token.
    :return: user_id if the access_token passed is valid. Raise a BadRequestError otherwise.
    """

    @functools.wraps(func)
    def decorated(*args, **kwargs):
        try:
            header = request.headers['Authorization']
            token = header.split()[1]
        except (IndexError, KeyError):
            raise BadRequestError('Missing Token')

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            user_id = data['sub']
        except InvalidTokenError:
            raise BadRequestError('Invalid Token')

        return func(user_id=user_id, *args, **kwargs)

    return decorated


def validate_item(func):
    """
    Check if this item exists in the provided category or not.
    :param: category_id, item_id
    :return: The item if it exists in the provided category. Raise a NotFoundError otherwise.
    """

    @functools.wraps(func)
    def validate(*args, **kwargs):
        category = CategoryModel.query.get(kwargs['category_id'])
        if not category:
            raise NotFoundError('No Category with that ID.')

        item = ItemModel.query.filter_by(id=kwargs['item_id'], category_id=kwargs['category_id']).one_or_none()

        if not item:
            raise NotFoundError('No items with that ID in this category.')

        return func(item=item, *args, **kwargs)

    return validate


def validate_category(func):
    """
    Check if this category exists or not.
    :param: category_id
    :return: The category if it exists. Raise a NotFoundError otherwise.
    """

    @functools.wraps(func)
    def validate(*args, **kwargs):
        category = CategoryModel.query.get(kwargs['category_id'])
        if not category:
            raise NotFoundError('No Category with that ID.')
        return func(category=category, *args, **kwargs)

    return validate
