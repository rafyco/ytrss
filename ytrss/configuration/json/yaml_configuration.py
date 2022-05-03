import os
import yaml

from ytrss.configuration.configuration import ConfigurationError, ConfigurationFileNotExistsError, \
    Configuration
from ytrss.configuration.entity.configuration_data import ConfigurationData


class YamlConfigurationParseError(ConfigurationError):
    pass


class YamlConfigurationFileNotExistsError(ConfigurationFileNotExistsError):
    pass


class YamlConfiguration(Configuration):

    @property
    def conf(self) -> ConfigurationData:
        return self.__configuration

    def __init__(self, conf_file: str) -> None:
        if not os.path.isfile(os.path.expanduser(conf_file)):
            raise ConfigurationError("File not exists")
        try:
            with open(os.path.expanduser(conf_file)) as data_file:
                # pylint: disable=E1120
                data = yaml.safe_load(data_file)
        except FileNotFoundError:
            raise YamlConfigurationFileNotExistsError()

        if data == {}:
            raise YamlConfigurationParseError("Cannot find data from file")

        self.__configuration = ConfigurationData.from_json(data)
