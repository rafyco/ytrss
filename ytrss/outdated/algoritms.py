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
Command line program to generation Podcast in files.

Program to generate podcast in files. It require mp3 files and json files.
That can be generate by ytrss program.

Example usage
=============

To invoke program type in your console::

    python -m ytrss.rssgenerate

for more option call program with flag C{--help}
"""

import os
from datetime import datetime
from datetime import timedelta

from ytrss.configuration.configuration import Configuration
from ytrss.podcast.algoritms import list_elements_in_dir


def rss_delete_outdated(settings: Configuration) -> int:
    """
    delete all outdated files

    @param settings: Settings handle
    @type settings: L{YTSettings<ytrss.core.settings.YTSettings>}
    @return: count of removed movies
    @rtype: int
    """
    result = 0
    nowtimestamp = datetime.now()

    for dirname in os.listdir(settings.output):
        print(f"Checking file to delete: {dirname}")
        list_elements = list_elements_in_dir(dirname, settings)

        for movie in list_elements:
            try:
                if nowtimestamp - movie.date > timedelta(days=15):
                    movie.delete()
                    result = result + 1
                else:
                    print(f"item: {movie.date} ({movie.element.title})")
            except ValueError:
                print(f"error: {movie.mp3}")
    return result
