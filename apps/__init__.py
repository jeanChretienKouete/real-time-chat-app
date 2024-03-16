from flask import Flask

from apps.chat.routes import app as chat
from apps.user.routes import app as user
from config import ConfigClass
from utils.utils import bcrypt, db, login_manager, socketio


def create_app() -> Flask:
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(ConfigClass)

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(user)
    app.register_blueprint(chat)

    return app
