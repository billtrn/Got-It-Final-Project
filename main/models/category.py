from main.db import db


class CategoryModel(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45))
    description = db.Column(db.Text)
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
