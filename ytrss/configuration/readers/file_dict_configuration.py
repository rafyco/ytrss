import abc
import os

from typing import Any

from ytrss.configuration.exceptions import ConfigurationError
from ytrss.configuration.readers.base import ConfigurationReader


class FileDictConfiguration(ConfigurationReader, metaclass=abc.ABCMeta):
    """ Configuration json object """

    @property
    def read_config(self) -> Any:
        return self.__configuration

    @abc.abstractmethod
    def read_data_from_file(self, conf_file: str) -> Any:
        """ Read data from file """

    def __init__(self, conf_file: str) -> None:
        if not os.path.isfile(os.path.expanduser(conf_file)):
            raise ConfigurationError("File not exists")

        self.__configuration = self.read_data_from_file(conf_file)
