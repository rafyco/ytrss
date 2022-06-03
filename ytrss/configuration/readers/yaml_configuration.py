import os
from typing import Any
import yaml
from ytrss.configuration.configuration import ConfigurationError, ConfigurationFileNotExistsError
from ytrss.configuration.readers.base import ConfigurationReader


class YamlConfigurationParseError(ConfigurationError):
    """ Yaml configuration error """


class YamlConfigurationFileNotExistsError(ConfigurationFileNotExistsError):
    """ Yaml configuration file not exists error. """


class YamlConfiguration(ConfigurationReader):
    """ Configuration yaml object """

    @property
    def read_config(self) -> Any:
        return self.__configuration

    def __init__(self, conf_file: str) -> None:
        if not os.path.isfile(os.path.expanduser(conf_file)):
            raise ConfigurationError("File not exists")
        try:
            with open(os.path.expanduser(conf_file), encoding="utf-8") as data_file:
                # pylint: disable=E1120
                data = yaml.safe_load(data_file)
        except FileNotFoundError as exc:
            raise YamlConfigurationFileNotExistsError(exc) from exc

        if data == {}:
            raise YamlConfigurationParseError("Cannot find data from file")

        self.__configuration = data
