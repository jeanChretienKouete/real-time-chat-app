import datetime
from typing import Any

from flask_login import current_user

from models.user import User
from utils.utils import db


class Message(db.Model):
    __tablename__: str = "messages"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    def __repr__(self) -> str:
        return super().__repr__()

    def json(self) -> dict:
        return {"content": self.content, "read": self.read, "date": self.date}

    def json_(self) -> dict:
        return {
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "content": self.content,
            "read": self.read,
        }

    @classmethod
    def get_messages(cls, user: User) -> Any:
        sent_msg = Message.query.filter_by(
            sender_id=user.id, receiver_id=current_user.id
        ).all()
        received_msg = Message.query.filter_by(
            sender_id=current_user.id, receiver_id=user.id
        ).all()

        messages = [(_.json(), "outgoing") for _ in sent_msg] + [
            (_.json(), "incomming") for _ in received_msg
        ]
        messages.sort(key=lambda x: x[0].get("date"))

        return messages
