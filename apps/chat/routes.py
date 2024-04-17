import datetime
from typing import Any

from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from models.message import Message
from models.user import User
from utils.utils import db, login_manager, socketio

app = Blueprint("chat", __name__)


@login_manager.user_loader
def load_user(user_id) -> Any | None:
    return User.query.get(int(user_id))


@app.get("/users")
@login_required
def users() -> None:
    users = User.query.all()
    status = {True: "online", False: "offline"}
    users = [
        (user, status[user.is_authenticated]) for user in users if user != current_user
    ]

    return render_template(template_name_or_list="pages/users.jinja", users=users)


@app.get("/chat/<int:user>")
@login_required
def chat(user: int) -> None:
    user = User.query.filter_by(id=user).first()
    messages = Message.get_messages(user)
    print(messages)
    return render_template(
        "pages/chat.jinja", user=user, status="Online", messages=messages
    )


@app.post("/chat")
@login_required
def message() -> None:
    message = Message(
        sender_id=current_user.id,
        receiver_id=int(request.form.get("incoming_id")),
        content=request.form.get("message"),
        date=datetime.datetime.now(),
    )
    db.session.add(message)
    # db.session.commit()
    socketio.emit("message", data=message.json_())
    return {"message": "Message sent successfully"}, 200


@app.post("/search")
@login_required
def search():
    ...
