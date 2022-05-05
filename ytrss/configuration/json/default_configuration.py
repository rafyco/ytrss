from ytrss.configuration.configuration import Configuration
from ytrss.configuration.entity.configuration_data import ConfigurationData


class DefaultConfiguration(Configuration):
    """ Default configuration """

    @property
    def conf(self) -> ConfigurationData:
        return ConfigurationData.from_json({})
