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
Command line program to checking movie's URL in subscription.

Program checking subscription and playlist from config and save it
to downloading file. It's recomended to add this file to crontab or call
it manually.

Example usage
=============

To invoke program type in your console::

    python -m ytrss.subs

for more option call program with flag C{--help}
"""

import logging

from ytrss.configuration.configuration import Configuration
from ytrss.core.factory.database_put import create_database_put
from ytrss.finder.url_finder import URLFinder


def prepare_urls(settings: Configuration) -> None:
    """
    Prepare urls for downloader.
    """
    logging.info("Prepare new urls")
    finder = URLFinder(settings.conf.sources)
    queue = create_database_put(settings)
    for movie in finder.movies:
        if queue.queue_mp3(movie):
            print(f"Nowy element: {movie.title} [{movie.identity}]")
        else:
            logging.info("Element istnieje: %s", movie.url)
