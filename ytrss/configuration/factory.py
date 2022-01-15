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
Configuration factory
"""
import os
import sys
from typing import Optional

from ytrss.configuration.algoritms import create_configuration
from ytrss.configuration.configuration import Configuration, ConfigurationError
from ytrss.configuration.json.json_configuration import JsonConfiguration
from ytrss.configuration.json.yaml_configuration import YamlConfiguration


# pylint: disable=R0911
def configuration_factory(configuration_file: Optional[str] = None, should_create: bool = False) -> Configuration:
    """
    Method that creates global configuration object

    File are read from the first of the following location.

    For MS Windows

        - I{~/YTRSS/config.json}

    For Linux (and other systems)

        - I{/etc/ytrss/config.json}
        - I{~/.config/ytrss/config.json}

    """
    if configuration_file is not None and os.path.isfile(configuration_file):
        if configuration_file.endswith(".json"):
            return JsonConfiguration(configuration_file)
        if configuration_file.endswith(".yml"):
            return YamlConfiguration(configuration_file)
        raise ConfigurationError("Not implements this type of file")

    if sys.platform.lower().startswith('win'):
        if os.path.isfile(os.path.expanduser("~\\YTRSS\\config.yml")):
            return YamlConfiguration("~\\YTRSS\\config.yml")
        if os.path.isfile(os.path.expanduser("~\\YTRSS\\config.json")):
            return JsonConfiguration("~\\YTRSS\\config.json")

    if os.path.isfile("/etc/ytrss/config.yml"):
        return YamlConfiguration("/etc/ytrss/config.yml")

    if os.path.isfile("/etc/ytrss/config.json"):
        return JsonConfiguration("/etc/ytrss/config.json")

    if os.path.isfile(os.path.expanduser("~/.config/ytrss/config.yml")):
        return YamlConfiguration("~/.config/ytrss/config.yml")

    if os.path.isfile(os.path.expanduser("~/.config/ytrss/config.json")):
        return JsonConfiguration("~/.config/ytrss/config.json")

    if should_create:
        if sys.platform.lower().startswith('win'):
            create_configuration("~\\YTRSS\\config.yml")
            return JsonConfiguration("~\\YTRSS\\config.yml")
        create_configuration("~/.config/ytrss/config.yml")
        return YamlConfiguration("~/.config/ytrss/config.yml")

    raise ConfigurationError("Cannot find configuration file")
