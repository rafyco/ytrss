#!/usr/bin/env python3
###########################################################################
#                                                                         #
#  Copyright (C) 2017-2021 Rafal Kobel <rafalkobel@rafyco.pl>             #
#                                                                         #
#  This program is free software: you can redistribute it and/or modify   #
#  it under the terms of the GNU General Public License as published by   #
#  the Free Software Foundation, either version 3 of the License, or      #
#  (at your option) any later version.                                    #
#                                                                         #
#  This program is distributed in the hope that it will be useful,        #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the           #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public License      #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                         #
###########################################################################
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

from ytrss.configuration.configuration import ConfigurationError, ConfigurationFileNotExistsError
from ytrss.configuration.json.data_configuration import DataConfiguration


class JsonConfigurationParseError(ConfigurationError):
    """ Settings parse JSON error. """


class JsonConfigurationFileNotExistsError(ConfigurationFileNotExistsError):
    """ Json configuration file not exists. """


class JsonConfiguration(DataConfiguration):
    """
    Parser configuration for ytrss from json file.
    """

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

        DataConfiguration.__init__(self, data)
