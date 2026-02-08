import os
import json

from typing import Any

from ytrss.configuration.exceptions import ConfigurationError, ConfigurationFileNotExistsError
from ytrss.configuration.readers.file_dict_configuration import FileDictConfiguration


class JsonConfigurationParseError(ConfigurationError):
    """ Json configuration error. """


class JsonConfigurationFileNotExistsError(ConfigurationFileNotExistsError):
    """ Json configuration file not exists """


class JsonConfiguration(FileDictConfiguration):
    """ Configuration json object """

    def read_data_from_file(self, conf_file: str) -> Any:
        try:
            with open(os.path.expanduser(conf_file), encoding="utf-8") as data_file:
                data = json.load(data_file)
        except FileNotFoundError as exc:
            raise JsonConfigurationFileNotExistsError() from exc

        if data == {}:
            raise JsonConfigurationParseError("Cannot find data from file")
        return data
