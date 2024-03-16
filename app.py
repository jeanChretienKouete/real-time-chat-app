from flask import Flask
from flask_migrate import Migrate

from apps import create_app
from utils.utils import db

app: Flask = create_app()

migrate = Migrate(app, db)
