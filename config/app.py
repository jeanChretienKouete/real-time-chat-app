import os

from dotenv import load_dotenv

load_dotenv(override=True)


class AppConfig:
    FLASK_APP: str = os.getenv("FLASK_APP", "app")
    FLASK_ENV: str = os.getenv("FLASK_ENV", "developpement")
    SECRET_KEY: str = os.environ.get("SECRET_KEY") or os.getenv("SECRET_KEY", "")
    DEBUG = bool(os.getenv("DEBUG", True))
    TESTING = bool(os.getenv("TESTING"))
