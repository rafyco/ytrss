"""
Settings parser module.

File are read from the first of the following location.

For MS Windows

    - I{~/YTRSS/config}

For Linux (and other systems)

    - I{/etc/ytrss/config}
    - I{~/.config/ytrss/config}

In some case you can set file path in constructor or read data in json format.

Config file structure
=====================

Configuration file is in a json format with following option:

    - I{output} - Path to folder where program should download files.
    - I{subscription} - List of subscription.
        For more see: L{parsing function
        <ytrss.core.settings.YTSettings.__parse_subsctiptions>}
    - I{arguments} - (optional) List of argument for C{youtube_dl} script
    - I{podcasts} - (optional) Dictionary of directory settings
        where key is dir name.
        For more see: L{rss generator
        <ytrss.core.settings.YTSettings.get_podcast_information>}

Example file
============

code of example file::

    {
        "output"   : "<output_file>",
        "subscriptions" : [
            {
                "code"    : "<playlist_id>",
                "type"    : "playlist"
            },
            {
                "code"    : "<subscription_id>"
            },
            {
                "code"    : "<subscription_id>",
                "enabled" : false
            }
        ]
    }

"""
import os
import json

from ytrss.configuration.configuration import ConfigurationError, ConfigurationFileNotExistsError, \
    Configuration
from ytrss.configuration.entity.configuration_data import ConfigurationData


class JsonConfigurationParseError(ConfigurationError):
    """ Settings parse JSON error. """


class JsonConfigurationFileNotExistsError(ConfigurationFileNotExistsError):
    """ Json configuration file not exists. """


class JsonConfiguration(Configuration):
    """
    Parser configuration for ytrss from json file.
    """

    @property
    def conf(self) -> ConfigurationData:
        return self.__configuration

    def __init__(self, conf_file: str) -> None:
        """
        YTSettings constructor.

        @param self: object handle
        @param conf_file: path to configuration file

        @raise JsonConfigurationFileNotExistsError: In case when conf_file not exists
        @raise JsonConfigurationParseError: In case of error in parsing
        """
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
