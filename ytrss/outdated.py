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
Command line program to generation Podcast in files.

Program to generate podcast in files. It require mp3 files and json files.
That can be generate by ytrss program.

Example usage
=============

To invoke program type in your console::

    python -m ytrss.rssgenerate

for more option call program with flag C{--help}
"""

from __future__ import unicode_literals
from __future__ import print_function
import sys
import logging
import os
from datetime import datetime
from datetime import timedelta
from argparse import ArgumentParser
from ytrss import get_version
from ytrss.core.settings import YTSettings
from ytrss.core.settings import SettingException
from ytrss.rssgenerate import list_elements_in_dir
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
    parser = ArgumentParser(description="Delete outdated elements",
                            prog='ytrss_subs')
    parser.add_argument("-v", "--version", action='version',
                        version='%(prog)s {}'.format(get_version()))
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


def rss_delete_outdated(settings):
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
        print("Checking file to delete: {}".format(dirname))
        list_elements = list_elements_in_dir(dirname, settings)

        for movie in list_elements:
            try:
                if nowtimestamp - movie.date > timedelta(days=15):
                    movie.delete()
                    result = result + 1
                else:
                    print("item: {} ({})".format(movie.date,
                                                 movie.element.title))
            except ValueError:
                print("error: {}".format(movie.mp3))
    return result


def main(argv=None):
    """
    Main function for command line program.

    @param argv: Option parameters
    @type argv: list
    """
    try:
        reload(sys)
        sys.setdefaultencoding("utf8")  # pylint: disable=E1101
    except NameError:  # Only python 2.7 need this
        pass
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
    rss_delete_outdated(settings)


if __name__ == "__main__":
    main()
