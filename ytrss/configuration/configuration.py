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
                "code"    : "<subscritpion_id>"
            },
            {
                "code"    : "<subscription_id>",
                "enabled" : false
            }
        ]
    }

"""
import abc

from ytrss.configuration.entity.configuration_data import ConfigurationData


class ConfigurationError(Exception):
    """ Configuration error. """


class ConfigurationFileNotExistsError(ConfigurationError):
    """ File not found error. """


class Configuration(metaclass=abc.ABCMeta):
    """
    Default settings for ytrss.

    Abstract configuration object. It has a configuration information.
    """

    @property
    @abc.abstractmethod
    def conf(self) -> ConfigurationData:
        """ Configuration object. """

    def __str__(self) -> str:
        return self.conf.__str__()
