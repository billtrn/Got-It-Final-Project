from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from werkzeug.exceptions import HTTPException

from main.configs import config
from main.exception import BaseError
from main.db import db


# Create our Flask app and update configurations
app = Flask(__name__)
app.config.from_object(config)
# Initialize our Flask app with this database setup
db.init_app(app)
ma = Marshmallow(app)


# Create all tables specified in the app
@app.before_first_request
def create_tables():
    db.create_all()


# Register error handler for our Flask app
@app.errorhandler(BaseError)
def handle_customized_error(error):
    return error.messages()


@app.errorhandler(HTTPException)
def handle_http_error(error):
    return jsonify(message=error.description), error.code
