import datetime

from flask import jsonify
import jwt

from main.app import app, load_data
from main.models.user import UserModel
from main.schemas.user import UserSchema, UserAuthenticationSchema
from main.exception import BadRequestError, UnauthorizedError
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/register', methods=['POST'])
@load_data(UserSchema)
def register(data):
    try:
        username = data['username']
        password = data['password']
    except KeyError:
        raise BadRequestError('Missing Input')
    if UserModel.query.filter_by(username=data['username']).first():
        raise BadRequestError('An User with that name already exists')

    hashed_password = generate_password_hash(data['password'])
    data['hashed_password'] = hashed_password
    del data['password']

    user = UserModel(**data)
    user.save_to_db()
    return jsonify(UserSchema().dump(user)), 201


@app.route('/login', methods=['POST'])
@load_data(UserSchema)
def login(data):
    try:
        username = data['username']
        password = data['password']
    except KeyError:
        raise BadRequestError('Missing Input')
    user = UserModel.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.hashed_password, data['password']):
        token = jwt.encode(
            {'username': data['username'], 'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY'])
        authentication = {'username': data['username'], 'access_token': token, 'id': user.id}
        return jsonify(UserAuthenticationSchema().dump(authentication)), 200
    raise UnauthorizedError('Invalid Credentials')
