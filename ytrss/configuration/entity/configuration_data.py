import os
import sys

from typing import Optional, Dict, Sequence, Iterable

from ytrss.configuration.configuration import Configuration
from ytrss.configuration.entity.destination_info import DestinationId, DestinationInfo
from ytrss.configuration.entity.source import Source
from ytrss.core.helpers.typing import Path
from ytrss.core.managers.destination_manager import DestinationManager
from ytrss.core.managers.sources_manager import SourcesManager


class YtrssConfiguration:
    """ Configuration data. """

    # pylint: disable=R0912,R0915
    def __init__(self, configuration: Configuration) -> None:
        """
        Configuration data constructor.
        """
        self._configuration_data = configuration.conf
        self._destination_manager: Optional[DestinationManager] = None
        self._sources_manager: Optional[SourcesManager] = None

    @property
    def destinations(self) -> Dict[str, DestinationInfo]:
        """ Destinations of destinations """
        result: Dict[str, DestinationInfo] = {}
        if 'destinations' in self._configuration_data and isinstance(self._configuration_data['destinations'], dict):
            for key, value in self._configuration_data['destinations'].items():
                result[key] = DestinationInfo.from_json(value, DestinationId(key))
        return result

    @property
    def sources(self) -> Iterable[Source]:
        """ List of sources """
        if 'subscriptions' in self._configuration_data and isinstance(self._configuration_data['subscriptions'], list):
            for subscription in self._configuration_data['subscriptions']:
                source = Source.from_json(subscription)
                if source.enable:
                    yield source

    @property
    def config_path(self) -> Path:
        """ Configuration path """
        if 'config_dir' in self._configuration_data:
            return Path(os.path.expanduser(self._configuration_data['config_dir']))
        if sys.platform.lower().startswith('win'):
            return Path(os.path.expanduser(os.path.join("~\\YTRSS")))
        return Path(os.path.expanduser(os.path.join("~/.config/ytrss")))

    @property
    def cache_path(self) -> Path:
        """ Path to cache directory """
        try:
            os.makedirs(self.config_path)
        except OSError:
            pass
        return Path(os.path.join(self.config_path, "cache"))

    @property
    def args(self) -> Sequence[str]:
        """ youtube_dl argument """
        if 'arguments' in self._configuration_data:
            if isinstance(self._configuration_data['arguments'], list):
                return self._configuration_data['arguments']
            return [self._configuration_data['arguments']]
        return []

    @property
    def sources_manager(self) -> SourcesManager:
        """ Sources manager """
        if self._sources_manager is None:
            self._sources_manager = SourcesManager()
            for sources in self.sources:
                self._sources_manager.add_from_info(sources)
        return self._sources_manager

    @property
    def destination_manager(self) -> DestinationManager:
        """ Destination manager """
        if self._destination_manager is None:
            self._destination_manager = DestinationManager()
            for _, info_value in self.destinations.items():
                self._destination_manager.add_from_info(info_value)
        return self._destination_manager
