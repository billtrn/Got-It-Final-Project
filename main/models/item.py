from main.models.base import BaseModel
from main.db import db


class ItemModel(BaseModel):
    __tablename__ = 'item'
    name = db.Column(db.String(45))
    description = db.Column(db.Text)
    updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    category = db.relationship('CategoryModel')
    user = db.relationship('UserModel')
