import abc
import os
import sys

from typing import Any, List, Optional, Dict, Sequence


from ytrss.configuration.entity.destination_info import DestinationId, DestinationInfo
from ytrss.configuration.entity.source import Source
from ytrss.core.managers.destination_manager import DestinationManager
from ytrss.core.managers.sources_manager import SourcesManager


class ConfigurationData(metaclass=abc.ABCMeta):
    """ Configuration data. """

    # pylint: disable=R0912,R0915
    def __init__(self) -> None:
        """
        Configuration data constructor.
        """
        self.destinations: Dict[str, DestinationInfo] = {}
        self.sources: Sequence[Source] = []
        self.config_path: str = ""
        self.cache_path: str = ""
        self.args: List[str] = []

        self._destination_manager: Optional[DestinationManager] = None
        self._sources_manager: Optional[SourcesManager] = None

    @staticmethod
    def from_json(json: Dict[str, Any]) -> 'ConfigurationData':
        """
        Create configuration data object from dictionary
        """

        config_data = ConfigurationData()

        if 'config_dir' in json:
            config_data.config_path = os.path.expanduser(json['config_dir'])
        else:
            if sys.platform.lower().startswith('win'):
                conf_path = os.path.join("~\\YTRSS")
            else:
                conf_path = os.path.join("~/.config/ytrss")
            config_data.config_path = os.path.expanduser(conf_path)

        try:
            os.makedirs(config_data.config_path)
        except OSError:
            pass

        config_data.cache_path = os.path.join(config_data.config_path, "cache")

        if 'arguments' in json:
            if isinstance(json['arguments'], list):
                config_data.args = json['arguments']
            else:
                config_data.args = [json['arguments']]

        config_data.sources = []
        if 'subscriptions' in json and isinstance(json['subscriptions'], list):
            for subscription in json['subscriptions']:
                source = Source.from_json(subscription)
                if source.enable:
                    config_data.sources.append(source)

        if 'destinations' in json and isinstance(json['destinations'], dict):
            config_data.destinations = {}
            for key in json['destinations']:
                config_data.destinations[key] = DestinationInfo.from_json(json['destinations'][key], DestinationId(key))

        return config_data

    def get_podcast_information(self, key: DestinationId) -> Optional[DestinationInfo]:
        """ Return information about podcast. """
        return self.destinations[key] if key in self.destinations else None

    def __str__(self) -> str:
        """
        Display settings information.
        """
        result = "Youtube configuration:\n\n"
        for elem in self.sources:
            result += f"  {elem.name}: [{elem.url}]\n"
        return result

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
