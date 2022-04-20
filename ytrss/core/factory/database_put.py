from ytrss.configuration.configuration import Configuration
from ytrss.database.database_put import DatabasePut
from ytrss.database.file_db.file_database_put import FileDatabasePut


def create_database_put(settings: Configuration) -> DatabasePut:
    """
    Create DatabasePut object from settings
    """
    return FileDatabasePut(settings)
