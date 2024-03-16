import datetime
from typing import Any

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_migrate import Migrate

from apps import create_app
from forms.login import LoginForm
from forms.register import RegistrationForm
from models.message import Message
from models.user import User
from utils.utils import bcrypt, db, login_manager, socketio

app: Flask = create_app()

migrate = Migrate(app, db)

login_manager.init_app(app)

socketio.init_app(app)


@login_manager.user_loader
def load_user(user_id) -> Any | None:
    return User.query.get(int(user_id))


@app.get("/")
def signup() -> Any:
    return render_template("pages/signup.jinja")


@app.post("/")
def register() -> Any:
    if (form := RegistrationForm(request.form)) and form.validate():
        if User.email_exist(form.data.get("email")):
            return jsonify({"message": "Email already used"}), 400

        if user := User(
            username=form.data.get("fname") + " " + form.data.get("lname"),
            email=form.data.get("email"),
            password=bcrypt.generate_password_hash(form.data.get("password")),
        ):
            db.session.add(user)
            db.session.commit()
            login_user(user)
            socketio.emit("login", data=user.json())
            return jsonify({"message": "Account created successfully"}), 200

    else:
        return form.errors, 400
        return jsonify({"message": "Errors in inputs"}), 400


@app.get("/login")
def signin():
    return render_template("pages/login.jinja")


@app.post("/login")
def login() -> None:
    if (form := LoginForm(request.form)) and form.validate():
        user = User.query.filter_by(email=form.data.get("email")).first()
        if user and bcrypt.check_password_hash(
            user.password, form.data.get("password")
        ):
            login_user(user)
            socketio.emit("login", data=user.json())
            return jsonify({"message": "Your are logged in succesfully"}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@app.get("/logout")
@login_required
def logout() -> None:
    socketio.emit("logout", data=current_user.json())
    logout_user()
    return redirect(url_for("signin"))


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
def search(): ...
