import functools

from flask import Flask, request, jsonify
from marshmallow import ValidationError
import jwt
from jwt import InvalidTokenError
from werkzeug.exceptions import HTTPException

from main.configs import config
from main.exception import BadRequestError, BaseError
from main.db import db


# Create our Flask app and update configurations
app = Flask(__name__)
app.config.from_object(config)
# Initialize our Flask app with this database setup
db.init_app(app)


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
            except ValidationError:
                raise BadRequestError('Invalid Input')
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
            user_id = data['id']
        except InvalidTokenError:
            raise BadRequestError('Invalid Token')

        return func(user_id=user_id, *args, **kwargs)

    return decorated


# Register error handler for our Flask app
@app.errorhandler(BaseError)
def handle_customized_error(e):
    return e.messages()


@app.errorhandler(HTTPException)
def handle_http_error(e):
    return jsonify(description=e.description), e.code
