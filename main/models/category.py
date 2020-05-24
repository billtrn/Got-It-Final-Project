from main.models.base import BaseModel
from main.db import db


class CategoryModel(BaseModel):
    __tablename__ = 'category'
    name = db.Column(db.String(45))
    description = db.Column(db.Text)
    items = db.relationship('ItemModel', lazy='dynamic')
