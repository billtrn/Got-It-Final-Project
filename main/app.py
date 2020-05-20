import functools

from flask import Flask, request, jsonify
from marshmallow import ValidationError
import jwt
from jwt import InvalidTokenError
from werkzeug.exceptions import HTTPException

from main.configs import config
from main.exception import BadRequestError, BaseError
from main.db import db


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


def token_required(func):
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
    def wrapper(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            try:
                data = schema().load(request.get_json())
            except ValidationError:
                raise BadRequestError('Invalid Input')
            except KeyError:
                raise BadRequestError('Missing Input')
            return func(data=data, *args, **kwargs)

        return decorated

    return wrapper


def get_user_id(func):
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


@app.errorhandler(BaseError)
def handle_customized_error(e):
    return e.messages()


@app.errorhandler(HTTPException)
def handle_http_error(e):
    return jsonify(description=e.description), e.code
