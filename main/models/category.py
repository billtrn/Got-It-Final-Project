from main.models.base import BaseModel
from main.db import db


class CategoryModel(BaseModel):
    """
    Category Model
    """

    __tablename__ = 'category'
    name = db.Column(db.String(45))
    description = db.Column(db.Text)
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
