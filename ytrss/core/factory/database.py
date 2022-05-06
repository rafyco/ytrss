from typing import Optional, Sequence, Callable

from ytrss.configuration.entity.configuration_data import YtrssConfiguration
from ytrss.core.factory import BaseFactory
from ytrss.database.database import Database
from ytrss.database.sqlite.sqlite_database import SqliteDatabase


class DatabaseFactory(BaseFactory[YtrssConfiguration, Database]):
    """
    Factory for Database
    """

    def __init__(self) -> None:
        self._database: Optional[Database] = None

    @property
    def plugins(self) -> Sequence[Callable[[YtrssConfiguration], Optional[Database]]]:
        """ A list of functions that try to produce an object """
        return []

    def build(self, param: YtrssConfiguration) -> Database:
        """
        Build defined object from parameter
        """
        if self._database is None:
            self._database = SqliteDatabase(param)
        return self._database


create_database = DatabaseFactory()
