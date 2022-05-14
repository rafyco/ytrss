from typing import Optional

from ytrss.configuration.entity.configuration_data import YtrssConfiguration
from ytrss.core.managers.destination_manager import DestinationManager
from ytrss.core.managers.plugin_manager import PluginManager
from ytrss.core.managers.sources_manager import SourcesManager
from ytrss.core.managers.templates_manager import TemplatesManager
from ytrss.database.database import Database
from ytrss.database.sqlite.sqlite_database import SqliteDatabase


class ManagerService:
    """ Manager service

    A container to singletons and constructors of many objects used in script
    """

    def __init__(self) -> None:
        self._configuration: Optional[YtrssConfiguration] = None
        self._sources_manager: Optional[SourcesManager] = None
        self._destination_manager: Optional[DestinationManager] = None
        self._plugin_manager: Optional[PluginManager] = None
        self._templates_manager: Optional[TemplatesManager] = None
        self._database: Optional[Database] = None

    @property
    def configuration(self) -> YtrssConfiguration:
        """ Ytrss configuration """
        if self._configuration is None:
            raise ValueError("Configuration not exists")
        return self._configuration

    @configuration.setter
    def configuration(self, configuration: YtrssConfiguration) -> None:
        """ Ytrss configuration setter """
        self._configuration = configuration

    @property
    def sources_manager(self) -> SourcesManager:
        """ Sources manager """
        if self._sources_manager is None:
            self._sources_manager = SourcesManager(self.plugin_manager)
            for sources in self.configuration.sources:
                self._sources_manager.add_from_info(sources)
        return self._sources_manager

    @property
    def destination_manager(self) -> DestinationManager:
        """ Destination manager """
        if self._destination_manager is None:
            self._destination_manager = DestinationManager(self.plugin_manager)
            for _, info_value in self.configuration.destinations.items():
                self._destination_manager.add_from_info(info_value)
        return self._destination_manager

    @property
    def plugin_manager(self) -> PluginManager:
        """ Plugin manager """
        if self._plugin_manager is None:
            self._plugin_manager = PluginManager()
        return self._plugin_manager

    @property
    def templates_manager(self) -> TemplatesManager:
        """ Templates manager """
        if self._templates_manager is None:
            self._templates_manager = TemplatesManager()
        return self._templates_manager

    @property
    def database(self) -> Database:
        """
        Build defined object from parameter
        """
        if self._database is None:
            self._database = SqliteDatabase(self.configuration, self.plugin_manager)
        return self._database


_manager_service = ManagerService()


def default_manager_service() -> ManagerService:
    """ Return default Manager Service """
    return _manager_service
