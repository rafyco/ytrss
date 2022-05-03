from typing import Optional, Sequence, Callable

from ytrss.configuration.configuration import Configuration
from ytrss.core.factory import BaseFactory
from ytrss.database.database import Database
from ytrss.database.sqlite.sqlite_database import SqliteDatabase


class DatabaseFactory(BaseFactory[Configuration, Database]):
    """
    Factory for Database
    """

    def __init__(self) -> None:
        self._database: Optional[Database] = None

    @property
    def plugins(self) -> Sequence[Callable[[Configuration], Optional[Database]]]:
        return []

    def build(self, param: Configuration) -> Database:
        """
        Build defined object from parameter
        """
        if self._database is None:
            self._database = SqliteDatabase(param)
        return self._database


create_database = DatabaseFactory()
