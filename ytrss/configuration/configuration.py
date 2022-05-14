from typing import Any

from ytrss.configuration.readers.base import ConfigurationReader


class ConfigurationError(Exception):
    """ Configuration error """


class ConfigurationFileNotExistsError(ConfigurationError):
    """ Configuration file not exists error

    The error that raised when the configuration file is not existed.
    """


class Configuration:
    """ Configuration object """

    def __init__(self, reader: ConfigurationReader) -> None:
        self._reader = reader

    @property
    def conf(self) -> Any:
        """ Returns object with configuration data. """
        return self._reader.read_config
