import pytest

from main.app import app
from main.db import db
from tests.db_setup import drop_tables, init_categories, init_users, init_items
from main.controllers.category import *
from main.controllers.item import *
from main.controllers.user import *


@pytest.fixture
def app_setup():
    try:
        drop_tables()
    except:
        pass
    db.create_all(app=app)
    with app.app_context():
        init_categories()
        init_users()
        init_items()
    return app


@pytest.fixture
def client(app_setup):
    return app_setup.test_client()
