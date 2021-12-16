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
Module with download queue object.
"""

import logging
from typing import Optional

from ytrss.configuration.configuration import Configuration
from ytrss.core.movie import Movie
from ytrss.database.database_file_config import DatabaseFileConfig
from ytrss.database.url_remember import UrlRememberer


class DownloadQueue:
    """
    Class saving urls to download.

    @ivar url_rss: path to file with readed urls
    @type url_rss: str
    @ivar download_file: file ready to download
    @type download_file: str
    @ivar rememberer: object remembering urls
    @type rememberer: L{UrlRememberer}
    """

    def __init__(self, configuration: Configuration, base_file: Optional[str] = None):
        """
        DownloadQueue constructor.

        @param self: object handle
        @type self: L{DownloadQueue}
        @param configuration: settings for DownloadQueue
        @type configuration: L{YTSettings<ytrss.core.settings.YTSettings>}
        @param base_file: path to file with remember subscription
        @type base_file: str

        @note:: if C{base_file} not set, it is get from settings object.
        """
        config_file = DatabaseFileConfig(configuration)
        self.url_rss = config_file.url_rss
        self.download_file = config_file.download_file
        self.download_yt = UrlRememberer(self.download_file)
        base_file = base_file if base_file is not None else config_file.url_rss
        logging.debug(base_file)
        self.rememberer = UrlRememberer(base_file)

    def queue_mp3(self, address: Movie) -> bool:
        """
        Add address to download.

        @param self: object handle
        @type self: L{DownloadQueue}
        @param address: adress to download
        @type address: str

        @return: C{True} if C{address} can be downloaded, C{False} otherwise
        @rtype: Boolean
        """
        logging.debug("DOWNLOAD: %s", address.url)
        if self.rememberer.is_new(address):
            logging.debug("Download address: %s", address.url)
            self.download_yt.add_movie(address)
            self.rememberer.add_movie(address)
            return True
        return False
