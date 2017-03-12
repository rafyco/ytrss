#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
#                                                                         #
#  Copyright (C) 2017  Rafal Kobel <rafalkobel@rafyco.pl>                 #
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

    ytrss_subs

or::

    python -m ytrss.subs

for more option call program with flag C{--help}
"""

from __future__ import unicode_literals
from __future__ import print_function
import logging
from argparse import ArgumentParser
from ytrss import get_version
from ytrss.core import DownloadQueue
from ytrss.core.settings import YTSettings
from ytrss.core.settings import SettingException
from ytrss.core.url_finder import URLFinder
try:
    import argcomplete
except ImportError:
    pass


def __option_args(argv=None):
    """
    Parsing argument for command line program.

    @param argv: Option parameters
    @type argv: list
    @return: parsed arguments
    """
    parser = ArgumentParser(description="Save urls from Youtube's "
                                        "subscription or playlists to file.",
                            prog='ytrss_subs',
                            version='%(prog)s {}'.format(get_version()))
    parser.add_argument("-s", "--show", action="store_true",
                        dest="show_config", default=False,
                        help="Write configuration")
    parser.add_argument("-c", "--conf", dest="configuration",
                        help="configuration file", default="", metavar="FILE")
    parser.add_argument("-l", "--log", dest="logLevel",
                        choices=['DEBUG', 'INFO', 'WARNING',
                                 'ERROR', 'CRITICAL'],
                        help="Set the logging level")

    try:
        argcomplete.autocomplete(parser)
    except NameError:
        pass
    options = parser.parse_args(argv)
    return options


def main(argv=None):
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
        settings = YTSettings(options.configuration)
    except SettingException:
        print("Configuration file not exist.")
        exit(1)

    if options.show_config:
        print(settings)
        exit()

    finder = URLFinder(settings)
    urls = finder.get_urls()
    queue = DownloadQueue(settings)
    for url in urls:
        if queue.queue_mp3(url):
            print("Nowy element: {}".format(url))
        else:
            print("Element istnieje: {}".format(url))

    logging.debug("End")

if __name__ == "__main__":
    main()
