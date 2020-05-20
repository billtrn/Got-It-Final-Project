from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash

from main.configs import config
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel


def init_categories():
    """
    Initiate category table
    """

    categories = [
        {
            'name': 'Films',
            'description': 'Before 2000s'
        },
        {
            'name': 'Songs',
            'description': 'Rock, Pop, Soul'
        },
        {
            'name': 'Food',
            'description': 'European food'
        }
    ]
    for category in categories:
        category_object = CategoryModel(**category)
        category_object.save_to_db()


def init_users():
    """
    Initiate user table
    """

    users = [
        {
            'username': 'bill',
            'password': 'asdf',
        },
        {
            'username': 'duc',
            'password': 'ghjk',
        }
    ]
    for user in users:
        hashed_password = generate_password_hash(user['password'])
        user['hashed_password'] = hashed_password
        del user['password']
        user_object = UserModel(**user)
        user_object.save_to_db()


def init_items():
    """
    Initiate item table
    """

    items = [
        {
            'name': 'Shawshank Redemption',
            'description': 'Starring Morgan Freeman.'
        },
        {
            'name': 'The Green Mile',
            'description': 'Starring Tom Hank'
        },
    ]
    user_id = 1
    category_id = 1

    for item in items:
        item_object = ItemModel(category_id=category_id, user_id=user_id, **item)
        item_object.save_to_db()


def drop_tables():
    """
    Drop all tables to refresh
    """

    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    ItemModel.__table__.drop(engine)
    CategoryModel.__table__.drop(engine)
    UserModel.__table__.drop(engine)
