import datetime

import jwt
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from main.app import app
from main.models.user import UserModel
from main.schemas.user import UserSchema, UserAuthenticationSchema
from main.exception import BadRequestError, UnauthorizedError
from main.helpers import load_data
from main.db import db


@app.route('/register', methods=['POST'])
@load_data(UserSchema)
def register(data):
    """
    Allow user to register
    :param: user's username and password
    :return: username and id in json format. Raise a BadRequestError if username already exists
    """
    if UserModel.query.filter_by(username=data['username']).one_or_none():
        raise BadRequestError('An User with that name already exists.')

    hashed_password = generate_password_hash(data.pop('password'))
    data['hashed_password'] = hashed_password

    user = UserModel(**data)
    db.session.add(user)
    db.session.commit()

    return jsonify(UserSchema().dump(user)), 201


@app.route('/login', methods=['POST'])
@load_data(UserSchema)
def login(data):
    """
    Allow user to log in to an existing account
    :param: user's username and password
    :return: username, token, and id in json format.
    Raise a BadRequestError if credentials is invalid
    """
    user = UserModel.query.filter_by(username=data['username']).one_or_none()
    if not user:
        raise UnauthorizedError('Invalid credentials.')

    if not check_password_hash(user.hashed_password, data['password']):
        raise UnauthorizedError('Invalid credentials.')

    token = jwt.encode(
        {'sub': user.id,
         'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
        app.config['SECRET_KEY'])

    authentication = {'username': data['username'], 'access_token': token,
                      'id': user.id, 'created': user.created}

    return jsonify(UserAuthenticationSchema().dump(authentication)), 200
