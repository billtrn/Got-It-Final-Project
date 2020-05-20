import json

from flask import jsonify

from main.app import app, token_required, load_data, get_user_id
from main.models.item import ItemModel
from main.schemas.item import ItemSchema
from main.models.category import CategoryModel
from main.exception import NotFoundError, BadRequestError, ForbiddenError


@app.route('/categories/<int:id>/items', methods=['GET'])
def get_items(id):
    """
    Get all items in a category
    :param: category's id
    :return: information about all items in that category. Raise a NotFoundError if cannot find the category
    """

    category = CategoryModel.query.filter_by(id=id).first()
    if category:
        return jsonify(ItemSchema(many=True, only=('id', 'name', 'description')).dump(category.items)), 200
    raise NotFoundError('No Category with that ID')


@app.route('/categories/<int:id>/items', methods=['POST'])
@token_required
@load_data(ItemSchema)
@get_user_id
def add_item(user_id, id, data):
    """
    Post a new item to a category
    :param: category's id, user's id, item's information
    :return: created item's information. Raise a NotFoundError if cannot find the category
    """

    try:
        name = data['name']
    except KeyError:
        raise BadRequestError('Missing Input')
    category = CategoryModel.query.filter_by(id=id).first()
    if category:
        description = data['description']
        item = ItemModel(name, description, id, user_id)
        item.save_to_db()
        return jsonify(ItemSchema().dump(item)), 201
    raise NotFoundError('No Category with that ID')


@app.route('/categories/<int:id>/items/<int:item_id>', methods=['GET'])
def get_item(id, item_id):
    """
    Get an item in a category
    :param: category's id, item's id
    :return:
    Information about the item.
    Raise a NotFoundError if cannot find item or category with that id
    Raise a BadRequestError if item does not belong to category
    """

    item = ItemModel.query.filter_by(id=item_id).first()
    category = CategoryModel.query.filter_by(id=id).first()
    if not category:
        raise NotFoundError('No Category with that ID')
    if not item:
        raise NotFoundError('No Item with that ID')
    if item_id in [item.id for item in category.items.all()]:
        return jsonify(ItemSchema().dump(item)), 200
    raise BadRequestError('This item does not belong to this category')


@app.route('/categories/<int:id>/items/<int:item_id>', methods=['PUT'])
@token_required
@load_data(ItemSchema)
@get_user_id
def update_item(user_id, data, id, item_id):
    """
    Update an item
    :param: category's id, user_id, item's id, new information about item
    :return:
    Information about updated item in json if succeed
    Raise a NotFoundError if cannot find item or category with that id
    Raise a ForbiddenError if not allowed to update this item
    Raise a BadRequestError if item does not belong to category
    """

    try:
        name = data['name']
    except KeyError:
        raise BadRequestError('Missing Input')
    item = ItemModel.query.filter_by(id=item_id).first()
    category = CategoryModel.query.filter_by(id=id).first()
    if not category:
        raise NotFoundError('No Category with that ID')
    if not item:
        raise NotFoundError('No Item with that ID')
    if item_id in [item.id for item in category.items.all()]:
        if item.user_id == user_id:
            item.name = data['name']
            item.description = data['description']
            item.save_to_db()
            return jsonify(ItemSchema().dump(item)), 200
        else:
            raise ForbiddenError('Not allowed to modify this item')
    raise BadRequestError('This item does not belong to this category')


@app.route('/categories/<int:id>/items/<int:item_id>', methods=['DELETE'])
@token_required
@get_user_id
def delete_item(user_id, id, item_id):
    """
    Delete an item
    :param: category's id, user_id, item's id
    :return:
    Success message in json if succeed
    Raise a NotFoundError if cannot find item or category with that id
    Raise a ForbiddenError if not allowed to delete this item
    Raise a BadRequestError if item does not belong to category
    """

    item = ItemModel.query.filter_by(id=item_id).first()
    category = CategoryModel.query.filter_by(id=id).first()
    if not category:
        raise NotFoundError('No Category with that ID')
    if not item:
        raise NotFoundError('No Item with that ID')
    if item_id in [item.id for item in category.items.all()]:
        if item.user_id == user_id:
            item.delete_from_db()
            return json.dumps({'message': 'Item deleted successfully'}), 200
        else:
            raise ForbiddenError('Not allowed to modify this item')
    raise BadRequestError('This item does not belong to this category')
