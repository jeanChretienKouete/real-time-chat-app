from config.app import AppConfig
from config.database import DatabaseConfig


class ConfigClass(AppConfig, DatabaseConfig):
    pass
