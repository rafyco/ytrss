import abc

from ytrss.configuration.entity.configuration_data import ConfigurationData


class ConfigurationError(Exception):
    pass


class ConfigurationFileNotExistsError(ConfigurationError):
    pass


class Configuration(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def conf(self) -> ConfigurationData:
        pass

    def __str__(self) -> str:
        return self.conf.__str__()
