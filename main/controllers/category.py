from flask import jsonify

from main.app import app
from main.models.category import CategoryModel
from main.schemas.category import CategorySchema
from main.exception import BadRequestError
from main.helpers import load_data, validate_category
from main.db import db


@app.route('/categories', methods=['GET'])
def get_categories():
    """
    Get all categories
    :return: all categories in json format
    """
    categories = CategoryModel.query.all()
    return jsonify(CategorySchema(many=True).dump(categories))


@app.route('/categories/<int:category_id>', methods=['GET'])
@validate_category
def get_category(category):
    """
    Get information about a category
    :param: category's id
    :return: category's name and description in json.
    Raise a NotFoundError if cannot find category with that id
    """
    return jsonify(CategorySchema().dump(category))


@app.route('/categories', methods=['POST'])
@load_data(CategorySchema)
def add_category(data):
    """
    Post a new category
    :param: category's name and description
    :return: created category's name and description in json
    Raise a BadRequestError if that name already exists
    """
    if CategoryModel.query.filter_by(name=data['name']).one_or_none():
        raise BadRequestError('A Category with that name already exists.')

    category = CategoryModel(**data)
    db.session.add(category)
    db.session.commit()

    return jsonify(CategorySchema().dump(category)), 201
