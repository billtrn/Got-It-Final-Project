from main.models.base import BaseModel
from main.db import db


class UserModel(BaseModel):
    """
    User Model
    """

    __tablename__ = 'user'
    username = db.Column(db.String(45))
    hashed_password = db.Column(db.String(128))
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
