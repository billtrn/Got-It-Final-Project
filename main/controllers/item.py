import json

from flask import jsonify

from main.app import app
from main.models.item import ItemModel
from main.schemas.item import ItemSchema
from main.models.category import CategoryModel
from main.exception import NotFoundError, ForbiddenError
from main.helpers import token_required, load_data


@app.route('/categories/<int:category_id>/items', methods=['GET'])
def get_items(category_id):
    """
    Get all items in a category
    :param: category's id
    :return: information about all items in that category. Raise a NotFoundError if cannot find the category
    """

    category = CategoryModel.query.filter_by(id=category_id).first()
    if not category:
        raise NotFoundError('No Category with that ID.')

    return jsonify(ItemSchema(many=True).dump(category.items)), 200


@app.route('/categories/<int:category_id>/items', methods=['POST'])
@token_required
@load_data(ItemSchema)
def add_item(user_id, category_id, data):
    """
    Post a new item to a category
    :param: category's id, user's id, item's information
    :return: created item's information. Raise a NotFoundError if cannot find the category
    """

    category = CategoryModel.query.filter_by(id=category_id).first()
    if not category:
        raise NotFoundError('No Category with that ID.')

    description = data['description']
    name = data['name']
    item = ItemModel(name, description, category_id, user_id)
    item.save_to_db()
    return jsonify(ItemSchema().dump(item)), 201


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['GET'])
def get_item(category_id, item_id):
    """
    Get an item in a category
    :param: category's id, item's id
    :return:
    Information about the item.
    Raise a NotFoundError if cannot find item or category with that id
    """

    category = CategoryModel.query.filter_by(id=category_id).first()
    if not category:
        raise NotFoundError('No Category with that ID.')

    item = ItemModel.query.filter_by(id=item_id, category_id=category_id).first()

    if not item:
        raise NotFoundError('No items with that ID in this category.')

    return jsonify(ItemSchema().dump(item)), 200


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['PUT'])
@token_required
@load_data(ItemSchema)
def update_item(user_id, data, category_id, item_id):
    """
    Update an item
    :param: category's id, user_id, item's id, new information about item
    :return:
    Information about updated item in json if succeed
    Raise a NotFoundError if cannot find item or category with that id
    Raise a ForbiddenError if not allowed to update this item
    """

    category = CategoryModel.query.filter_by(id=category_id).first()
    if not category:
        raise NotFoundError('No Category with that ID.')

    item = ItemModel.query.filter_by(id=item_id, category_id=category_id).first()

    if not item:
        raise NotFoundError('No items with that ID in this category.')

    if item.user_id != user_id:
        raise ForbiddenError('Not allowed to modify this item.')

    item.name = data['name']
    item.description = data['description']
    item.save_to_db()
    return jsonify(ItemSchema().dump(item)), 200


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['DELETE'])
@token_required
def delete_item(user_id, category_id, item_id):
    """
    Delete an item
    :param: category's id, user_id, item's id
    :return:
    Success message in json if succeed
    Raise a NotFoundError if cannot find item or category with that id
    Raise a ForbiddenError if not allowed to delete this item
    """

    category = CategoryModel.query.filter_by(id=category_id).first()
    if not category:
        raise NotFoundError('No Category with that ID.')

    item = ItemModel.query.filter_by(id=item_id, category_id=category_id).first()

    if not item:
        raise NotFoundError('No items with that ID in this category.')

    if item.user_id != user_id:
        raise ForbiddenError('Not allowed to modify this item.')

    item.delete_from_db()
    return jsonify({'message': 'Item deleted successfully'}), 200
