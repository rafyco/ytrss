import os
import json

from ytrss.configuration.configuration import ConfigurationError, ConfigurationFileNotExistsError, \
    Configuration
from ytrss.configuration.entity.configuration_data import ConfigurationData


class JsonConfigurationParseError(ConfigurationError):
    """ Json configuration error. """


class JsonConfigurationFileNotExistsError(ConfigurationFileNotExistsError):
    """ Json configuration file not exists """


class JsonConfiguration(Configuration):
    """ Configuration json object """

    @property
    def conf(self) -> ConfigurationData:
        return self.__configuration

    def __init__(self, conf_file: str) -> None:
        if not os.path.isfile(os.path.expanduser(conf_file)):
            raise ConfigurationError("File not exists")
        try:
            with open(os.path.expanduser(conf_file)) as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            raise JsonConfigurationFileNotExistsError()

        if data == {}:
            raise JsonConfigurationParseError("Cannot find data from file")

        self.__configuration = ConfigurationData.from_json(data)
