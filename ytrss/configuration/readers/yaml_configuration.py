import os
from typing import Any
import yaml
from ytrss.configuration.configuration import ConfigurationError, ConfigurationFileNotExistsError
from ytrss.configuration.readers.file_dict_configuration import FileDictConfiguration


class YamlConfigurationParseError(ConfigurationError):
    """ Yaml configuration error """


class YamlConfigurationFileNotExistsError(ConfigurationFileNotExistsError):
    """ Yaml configuration file not exists error. """


class YamlConfiguration(FileDictConfiguration):
    """ Configuration yaml object """

    def read_data_from_file(self, conf_file: str) -> Any:
        try:
            with open(os.path.expanduser(conf_file), encoding="utf-8") as data_file:
                # pylint: disable=E1120
                data = yaml.safe_load(data_file)
        except FileNotFoundError as exc:
            raise YamlConfigurationFileNotExistsError(exc) from exc

        if data == {}:
            raise YamlConfigurationParseError("Cannot find data from file")
        return data
