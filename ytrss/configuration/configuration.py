import abc

from ytrss.configuration.entity.configuration_data import ConfigurationData


class ConfigurationError(Exception):
    """ Configuration error """


class ConfigurationFileNotExistsError(ConfigurationError):
    """ Configuration file not exists error

    The error that raised when the configuration file is not existed.
    """


class Configuration(metaclass=abc.ABCMeta):
    """ Configuration object """

    @property
    @abc.abstractmethod
    def conf(self) -> ConfigurationData:
        """ Returns object with configuration data. """
