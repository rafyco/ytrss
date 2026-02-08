from typing import Any

from ytrss.configuration.readers.base import ConfigurationReader


class Configuration:
    """ Configuration object """

    def __init__(self, reader: ConfigurationReader) -> None:
        self._reader = reader

    @property
    def conf(self) -> Any:
        """ Returns object with configuration data. """
        return self._reader.read_config
