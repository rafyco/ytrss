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
import os.path
import pkgutil


def create_configuration(config_file_name: str) -> None:
    """
    Create configuration file in selected path
    """
    if os.path.isfile(os.path.expanduser(config_file_name)):
        raise FileExistsError(f"file {config_file_name} exists")

    try:
        os.makedirs(config_file_name)
    except OSError:
        pass

    data = pkgutil.get_data(__name__, "default_config.json")
    with open(os.path.expanduser(config_file_name), "w+") as config_file:
        config_file.write(data.decode("utf-8"))
