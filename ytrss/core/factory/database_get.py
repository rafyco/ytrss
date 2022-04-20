from ytrss.configuration.configuration import Configuration
from ytrss.database.database_get import DatabaseGet
from ytrss.database.file_db.file_database_get import FileDatabaseGet


def create_database_get(settings: Configuration) -> DatabaseGet:
    """
    Create DatabasePut object from settings
    """
    return FileDatabaseGet(settings)
