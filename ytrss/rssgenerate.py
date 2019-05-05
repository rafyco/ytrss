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
import logging
import sys
import io
import os
from argparse import ArgumentParser
from ytrss import get_version
from ytrss.core.settings import YTSettings
from ytrss.core.settings import SettingException
from ytrss.core.podcast import Podcast
from ytrss.core.movie import Movie
from ytrss.core.movie import MovieFileError
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


def list_elements_in_dir(dirname, settings):
    """
    Return list of movie in directory.

    @param dirname: name of directory
    @type dirname: str
    @param settings: Settings handle
    @type settings: L{YTSettings<ytrss.core.settings.YTSettings>}
    @return: list of movie in directory
    @rtype: list
    """
    result = []
    for filename in os.listdir(os.path.join(settings.output, dirname)):
        if filename.endswith(".json"):
            try:
                movie = Movie(settings, dirname, filename[0:len(filename) - 5])
                result.append(movie)
            except MovieFileError:
                pass
    return result


def rss_generate(settings):
    """
    Generate podcast file.

    @param settings: Settings handle
    @type settings: L{YTSettings<ytrss.core.settings.YTSettings>}
    """
    for dirname in os.listdir(settings.output):
        if os.path.isdir(os.path.join(settings.output, dirname)):
            print("Generate Podcast: {}".format(dirname))
            podcast = Podcast(dirname,
                              settings.get_podcast_information(dirname))
            for movie in list_elements_in_dir(dirname, settings):
                logging.debug("item: %s", movie.name)
                try:
                    podcast.add_item(movie=movie,
                                     dirname=dirname)
                    print("add item: %s" % movie.name)
                except ValueError:
                    print("Cannot add item")
            podcast_file = os.path.join(settings.output, dirname, "podcast.xml")
            logging.debug("try to save: %s", podcast_file)
            file_handler = io.open(podcast_file, "w", encoding="utf-8")
            file_handler.write(podcast.generate())
            file_handler.close()


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
    rss_generate(settings)


if __name__ == "__main__":
    main()
