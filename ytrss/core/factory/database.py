from ytrss.configuration.configuration import Configuration
from ytrss.database.database import Database
from ytrss.database.sqlite.sqlite_database import SqliteDatabase


def create_database(configuration: Configuration) -> Database:
    """
    Create Database object from settings
    """
    return SqliteDatabase(configuration)
