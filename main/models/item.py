from datetime import datetime

from main.db import db


class ItemModel(db.Model):
    """
    Item Model
    """

    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45))
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated = db.Column(db.DateTime, default=datetime.now,
                        onupdate=datetime.now)
    category = db.relationship('CategoryModel')
    user = db.relationship('UserModel')

    def __init__(self, name, description, category_id, user_id):
        self.name = name
        self.description = description
        self.category_id = category_id
        self.user_id = user_id
        self.updated = datetime.now()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
