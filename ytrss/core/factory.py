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
The module with factory of plugin objects
"""
from typing import Union, Dict, Any

from ytrss.configuration.configuration import Configuration
from ytrss.configuration.consts import DEFAULT_PODCAST_DIR
from ytrss.configuration.entity.source import Source
from ytrss.controlers.youtube.downloaded_movie import YouTubeDownloadedMovie
from ytrss.controlers.youtube.movie import YouTubeMovie
from ytrss.controlers.youtube.source_downloader import YouTubeSourceDownloader
from ytrss.core.downloaded_movie import DownloadedMovie
from ytrss.core.movie import Movie
from ytrss.download.source_downloader import SourceDownloader


class CoreFactoryError(Exception):
    """
    Core Factory Error
    """


class CoreFactory:
    """
    Set of factory method to create plugin objects
    """

    @staticmethod
    def create_source_downloader(source: Source) -> SourceDownloader:
        """
        Create source downloader object from args
        """
        return YouTubeSourceDownloader(source)

    @staticmethod
    def create_movie(arg: Union[str, Dict[str, Any]], destination_dir: str = DEFAULT_PODCAST_DIR) -> Movie:
        """
        Create Movie object from args
        """
        return YouTubeMovie(arg, destination_dir)

    @staticmethod
    def create_downloaded_movie(settings: Configuration, dirname: str, name: str) -> DownloadedMovie:
        """
        Create DownloadedMovie object from args
        """
        return YouTubeDownloadedMovie(settings, dirname, name)
