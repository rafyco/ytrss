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
import os

from ytrss.configuration.configuration import Configuration


class DatabaseFileConfig:
    """
    Object with database files destinations.
    """

    def __init__(self, configuration: Configuration):
        self.url_rss = os.path.join(configuration.config_path, "rss_remember.txt")
        self.download_file = os.path.join(configuration.config_path, "download_yt.txt")
        self.next_time = os.path.join(configuration.config_path, "download_yt_next.txt")
        self.url_backup = os.path.join(configuration.config_path, "download_yt_last.txt")
        self.history_file = os.path.join(configuration.config_path, "download_yt_history.txt")
        self.err_file = os.path.join(configuration.config_path, "download_yt.txt.err")
