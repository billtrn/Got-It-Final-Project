from main.db import db


class UserModel(db.Model):
    """
    User Model
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(45))
    hashed_password = db.Column(db.String(128))
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
