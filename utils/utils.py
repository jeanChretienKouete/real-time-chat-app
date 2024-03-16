from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()

db = SQLAlchemy()

bcrypt = Bcrypt()

socketio = SocketIO()
