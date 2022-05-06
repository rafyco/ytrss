import abc

from typing import Any


class ConfigurationReader(metaclass=abc.ABCMeta):
    """ An abstract reader for configuration """

    @property
    @abc.abstractmethod
    def read_config(self) -> Any:
        """ Returns object with configuration data. """
