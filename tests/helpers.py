import json

from main.app import app
from main.db import db
from main.models.category import CategoryModel
from main.models.item import ItemModel


def get_item_ids():
    """
    Get all items' ids
    :return: a list of all item ids
    """
    with app.app_context():
        item_ids = [item_id[0] for item_id in db.session.query(ItemModel.id).all()]
    return item_ids


def get_category_ids():
    """
    Get all categories' ids
    :return: a list of all category ids
    """
    with app.app_context():
        category_ids = [category_id[0] for category_id in db.session.query(CategoryModel.id).all()]
    return category_ids


def create_request_headers(access_token=None):
    """
    Create header for request
    :param access_token
    :return: a dictionary of headers
    """
    header = {'Content-Type': 'application/json'}
    if access_token:
        header['Authorization'] = '{}'.format(access_token)
    return header


def load_decoded_response(response):
    """
    Load json response into dictionary
    :param response
    :return: response in dictionary format
    """
    return json.loads(response.data.decode('utf-8'))
