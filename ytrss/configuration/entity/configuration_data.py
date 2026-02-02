import os
import sys

from typing import Dict, Sequence, Iterable, Union

from ytrss.configuration.configuration import Configuration
from ytrss.configuration.entity.destination_info import DestinationId, DestinationInfo
from ytrss.configuration.entity.source import Source
from ytrss.core.entity.webhooks import WebhookType
from ytrss.core.helpers.logging import logger
from ytrss.core.helpers.typing import Path


class YtrssConfiguration:
    """ Configuration data. """

    # pylint: disable=R0912,R0915
    def __init__(self, configuration: Configuration) -> None:
        """
        Configuration data constructor.
        """
        self._configuration_data = configuration.conf

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
    def database_path(self) -> Path:
        """ Path to database directory """
        database_dir = self.config_path
        try:
            database_dir = Path(os.path.join(self.config_path, "database"))
            os.makedirs(database_dir)
        except OSError:
            pass
        return database_dir

    @property
    def args(self) -> Sequence[str]:
        """ youtube_dl argument """
        if 'arguments' in self._configuration_data:
            if isinstance(self._configuration_data['arguments'], list):
                return self._configuration_data['arguments']
            return [self._configuration_data['arguments']]
        return []

    def get_webhook(self, webhook: Union[WebhookType, str]) -> Iterable[str]:
        """ Get list of urls to defined webhook"""
        webhook_key = webhook if isinstance(webhook, str) else webhook.name
        try:
            webhooks = self._configuration_data['webhooks'][webhook_key]
            return webhooks if isinstance(webhooks, list) else [webhooks]
        except KeyError:
            return []

    @property
    def webhooks(self) -> Sequence[str]:
        """ List of all webhooks that has at least one defined url """
        try:
            webhooks = self._configuration_data['webhooks']
            if isinstance(webhooks, dict):
                return list(webhooks.keys())
        except KeyError:
            logger.debug("No webhooks defined in configuration")
        return []
