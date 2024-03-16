import os

from dotenv import load_dotenv

load_dotenv(override=True)


test_mode = bool(int(os.getenv("TESTING")))


class DatabaseConfig:
    if not test_mode:
        SQLALCHEMY_DATABASE_URI: str | None = os.getenv("SQLALCHEMY_DATABASE_URI_DEV")
    else:
        SQLALCHEMY_DATABASE_URI: str | None = os.getenv("SQLALCHEMY_DATABASE_URI_TEST")

    SQLALCHEMY_TRACK_MODIFICATIONS = bool(
        os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", True)
    )
