from typing import Dict, Any

from ytrss.configuration.readers.base import ConfigurationReader


class DefaultConfiguration(ConfigurationReader):
    """ Default configuration """

    @property
    def read_config(self) -> Dict[str, Any]:
        return {}
