from flask import jsonify

from main.app import app
from main.models.category import CategoryModel
from main.schemas.category import CategorySchema
from main.exception import NotFoundError, BadRequestError
from main.helpers import load_data


@app.route('/categories', methods=['GET'])
def get_categories():
    """
    Get all categories
    :return: all categories in json format
    """

    categories = CategoryModel.query.all()
    return jsonify(CategorySchema(many=True).dump(categories)), 200


@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """
    Get information about a category
    :param: category's id
    :return: category's name and description in json.
    Raise a NotFoundError if cannot find item or category with that id
    """

    category = CategoryModel.query.filter_by(id=category_id).first()
    if not category:
        raise NotFoundError('No Category with that ID')

    return jsonify(CategorySchema().dump(category)), 200


@app.route('/categories', methods=['POST'])
@load_data(CategorySchema)
def add_category(data):
    """
    Post a new category
    :param: category's name and description
    :return: created category's name and description in json
    Raise a BadRequestError if that name already exists or input is missing
    """

    if CategoryModel.query.filter_by(name=data['name']).first():
        raise BadRequestError('A Category with that name already exists')

    category = CategoryModel(**data)
    category.save_to_db()
    return jsonify(CategorySchema().dump(category)), 201
