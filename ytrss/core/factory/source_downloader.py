#!/usr/bin/env python3
###########################################################################
#                                                                         #
#  Copyright (C) 2017-2022 Rafal Kobel <rafalkobel@rafyco.pl>             #
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
from ytrss.configuration.entity.source import Source
from ytrss.controlers.youtube.source_downloader import YouTubeSourceDownloader
from ytrss.download.source_downloader import SourceDownloader


def create_source_downloader(source: Source) -> SourceDownloader:
    """
    Create source downloader object from args
    """
    return YouTubeSourceDownloader(source)
