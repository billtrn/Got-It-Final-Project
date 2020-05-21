from main.models.base import BaseModel
from main.db import db


class ItemModel(BaseModel):
    """
    Item Model
    """

    __tablename__ = 'item'
    name = db.Column(db.String(45))
    description = db.Column(db.Text)
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    category = db.relationship('CategoryModel')
    user = db.relationship('UserModel')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
