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
import sys
from argparse import ArgumentParser, Namespace
from typing import Sequence, Optional

from ytrss import get_version
from ytrss.configuration.factory import configuration_factory
from ytrss.database.download_queue import DownloadQueue
from ytrss.configuration.configuration import ConfigurationException, Configuration
from ytrss.core.url_finder import URLFinder


def __option_args(argv: Optional[Sequence[str]] = None) -> Namespace:
    """
    Parsing argument for command line program.

    @param argv: Option parameters
    @type argv: list
    @return: parsed arguments
    """
    parser = ArgumentParser(description="Save urls from Youtube's "
                                        "subscription or playlists to file.",
                            prog='ytrss_subs')
    parser.add_argument("-v", "--version", action='version',
                        version='%(prog)s {}'.format(get_version()))
    parser.add_argument("-c", "--conf", dest="configuration",
                        help="configuration file", default="", metavar="FILE")
    parser.add_argument("-l", "--log", dest="logLevel",
                        choices=['DEBUG', 'INFO', 'WARNING',
                                 'ERROR', 'CRITICAL'],
                        help="Set the logging level")

    return parser.parse_args(argv)


def prepare_urls(settings: Configuration) -> None:
    """
    Prepare urls for downloader.
    """
    logging.info("Prepare new urls")
    finder = URLFinder(settings.sources)
    elements = finder.elements
    queue = DownloadQueue(settings)
    for element in elements:
        if queue.queue_mp3(element):
            print("Nowy element: {} [{}]".format(element.title, element.code))
        else:
            logging.info("Element istnieje: %s", element.url)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    Main function for command line program.

    @param argv: Option parameters
    @type argv: list
    """
    options = __option_args(argv)
    logging.basicConfig(format='%(asctime)s - %(name)s '
                               '- %(levelname)s - %(message)s',
                        level=options.logLevel)
    logging.debug("Debug mode: Run")
    try:
        settings = configuration_factory(options.configuration)
    except ConfigurationException:
        print("Configuration file not exist.")
        sys.exit(1)
    prepare_urls(settings)


if __name__ == "__main__":
    main()
