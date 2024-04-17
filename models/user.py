import datetime

from flask_login import UserMixin

from utils.utils import db


class User(db.Model, UserMixin):
    __tablename__: str = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    image = db.Column(db.String(300), default="profile.jpg")
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    def __repr__(self) -> str:
        return super().__repr__()

    def __eq__(self, other) -> bool:
        return self.id is other.id

    def json(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "image": self.image,
        }

    @staticmethod
    def email_exist(email: str) -> bool:
        return User.query.filter_by(email=email).first() is not None
