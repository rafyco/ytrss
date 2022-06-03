import os
import json

from typing import Any

from ytrss.configuration.configuration import ConfigurationError, ConfigurationFileNotExistsError
from ytrss.configuration.readers.base import ConfigurationReader


class JsonConfigurationParseError(ConfigurationError):
    """ Json configuration error. """


class JsonConfigurationFileNotExistsError(ConfigurationFileNotExistsError):
    """ Json configuration file not exists """


class JsonConfiguration(ConfigurationReader):
    """ Configuration json object """

    @property
    def read_config(self) -> Any:
        return self.__configuration

    def __init__(self, conf_file: str) -> None:
        if not os.path.isfile(os.path.expanduser(conf_file)):
            raise ConfigurationError("File not exists")
        try:
            with open(os.path.expanduser(conf_file), encoding="utf-8") as data_file:
                data = json.load(data_file)
        except FileNotFoundError as exc:
            raise JsonConfigurationFileNotExistsError() from exc

        if data == {}:
            raise JsonConfigurationParseError("Cannot find data from file")

        self.__configuration = data
