from flask import jsonify

from main.app import app
from main.models.item import ItemModel
from main.schemas.item import ItemSchema
from main.exception import ForbiddenError
from main.helpers import token_required, load_data, validate_category, validate_item
from main.db import db


@app.route('/categories/<int:category_id>/items', methods=['GET'])
@validate_category
def get_items(category):
    """
    Get all items in a category
    :param: category's id
    :return: information about all items in that category. Raise a NotFoundError if cannot find the category
    """
    return jsonify(ItemSchema(many=True, only=('id', 'name', 'description', 'created', 'user_id')).dump(category.items))


@app.route('/categories/<int:category_id>/items', methods=['POST'])
@token_required
@load_data(ItemSchema)
@validate_category
def add_item(user_id, data, category):
    """
    Post a new item to a category
    :param: category's id, user's id, item's information
    :return: created item's information. Raise a NotFoundError if cannot find the category
    """
    item = ItemModel(category_id=category.id, user_id=user_id, **data)
    db.session.add(item)
    db.session.commit()

    return jsonify(ItemSchema(only=('id', 'name', 'description', 'created', 'user_id')).dump(item)), 201


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['GET'])
@validate_item
def get_item(item):
    """
    Get an item in a category
    :param: category's id, item's id
    :return:
    Information about the item.
    Raise a NotFoundError if cannot find item or category with that id
    """
    return jsonify(ItemSchema(only=('id', 'name', 'description', 'created', 'user_id')).dump(item)), 200


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['PUT'])
@token_required
@load_data(ItemSchema)
@validate_item
def update_item(user_id, data, item):
    """
    Update an item
    :param: category's id, user_id, item's id, new information about item
    :return:
    Information about updated item in json if succeed
    Raise a NotFoundError if cannot find item or category with that id
    Raise a ForbiddenError if not allowed to update this item
    """
    if item.user_id != user_id:
        raise ForbiddenError('Not allowed to modify this item.')

    item.name = data['name']
    item.description = data['description']
    db.session.add(item)
    db.session.commit()

    return jsonify(ItemSchema(only=('id', 'name', 'description', 'updated', 'user_id')).dump(item)), 200


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['DELETE'])
@token_required
@validate_item
def delete_item(user_id, item):
    """
    Delete an item
    :param: category's id, user_id, item's id
    :return:
    Success message in json if succeed
    Raise a NotFoundError if cannot find item or category with that id
    Raise a ForbiddenError if not allowed to delete this item
    """
    if item.user_id != user_id:
        raise ForbiddenError('Not allowed to modify this item.')

    db.session.delete(item)
    db.session.commit()

    return jsonify({'message': 'Item deleted successfully'}), 200
