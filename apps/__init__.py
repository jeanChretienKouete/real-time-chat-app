from flask import Flask

from config import ConfigClass
from utils.utils import db


def create_app() -> Flask:
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(ConfigClass)

    db.init_app(app)

    return app
