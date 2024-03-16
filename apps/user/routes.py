from typing import Any

from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from forms.login import LoginForm
from forms.register import RegistrationForm
from models.user import User
from utils.utils import bcrypt, db, login_manager, socketio

app = Blueprint("user", __name__)


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
            print("Hello world Route")
            return jsonify({"message": "Account created successfully"}), 200

    else:
        # return form.errors, 400
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
