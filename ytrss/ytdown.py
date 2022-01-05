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
Add one or more URL addresses to download file.

Example usage
=============

To invoke program type in your console::

    ytdown [url]

or::

    python -m ytrss.ytdown [url]

for more option call program with flag C{--help}
"""

import sys
import logging
from argparse import ArgumentParser, Namespace
from typing import Optional, Sequence

from ytrss import get_version
from ytrss.configuration.algoritms import create_configuration
from ytrss.configuration.factory import configuration_factory
from ytrss.download.algoritms import download_all_movie
from ytrss.finder.algoritms import prepare_urls
from ytrss.podcast.algoritms import rss_generate
from ytrss.configuration.configuration import ConfigurationError, Configuration, \
    ConfigurationFileNotExistsError


def __option_args(argv: Optional[Sequence[str]] = None) -> Namespace:
    """
    Parsing argument for command line program.

    @param argv: Option parameters
    @type argv: list
    @return: parsed arguments
    """
    parser = ArgumentParser(description="Save one or more urls from "
                                        "Youtube to file.",
                            prog='ytdown')
    parser.add_argument("-v", "--version", action='version',
                        version='%(prog)s {}'.format(get_version()))
    parser.add_argument("-c", "--conf", dest="config_file",
                        help="configuration file", default="", metavar="FILE")
    parser.add_argument("--create-configuration", dest="create_config",
                        help="create default configuration", default="", metavar="FILE")
    parser.add_argument("-l", "--log", dest="logLevel",
                        choices=['DEBUG', 'INFO', 'WARNING',
                                 'ERROR', 'CRITICAL'],
                        help="Set the logging level")
    parser.add_argument("-s", "--show", action="store_true",
                        dest="show_config", default=False,
                        help="Write configuration")
    parser.add_argument("-r", "--read", action="store_true",
                        dest="daemon_run", default=False,
                        help="Read urls to download from rss")
    parser.add_argument("-d", "--download", action="store_true",
                        dest="download_run", default=False,
                        help="Download all movies to output path")
    parser.add_argument("-x", "--delete-outdate", action="store_true",
                        dest="outdated", default=False,
                        help="delete old files")
    parser.add_argument("-g", "--generate-podcast", action="store_true",
                        dest="generate_podcast", default=False,
                        help="Generate Podcast files")
    # TODO: Add possibility to download from selected url
    # parser.add_argument("urls", nargs='*', default=[], type=str,
    #                    help="Url to download.")
    return parser.parse_args(argv)


def main_work(configuration: Configuration, options: Namespace) -> None:
    """
    Make all jobs for ytdown program.

    @param configuration: Settings handle
    @type configuration: L{YTSettings<ytrss.core.settings.YTSettings>}
    @param options: option handle
    @type options: unknown
    """
    force_rss = False
    if options.download_run:
        try:
            download_all_movie(configuration, lambda: rss_generate(configuration))
        except Exception as ex:  # pylint: disable=W0703
            force_rss = True
            raise ex

    if force_rss or options.generate_podcast:
        rss_generate(configuration)


def main(argv: Optional[Sequence[str]] = None) -> None:
    """
    Main function for command line program.

    @param argv: Option parameters
    @type argv: list
    """
    options = __option_args(argv)
    logging.basicConfig(format='%(asctime)s - %(name)s - '
                               '%(levelname)s - %(message)s',
                        level=options.logLevel)
    if options.create_config is not None and options.create_config != "":
        try:
            create_configuration(options.create_config)
        # pylint: disable=W0703
        except Exception as ex:
            print(f"Cannot create configuration file: {ex}")
            sys.exit(1)
        sys.exit(0)

    try:
        configuration = configuration_factory(options.config_file)
    except ConfigurationFileNotExistsError:
        print("File not exists")
        sys.exit(1)
    except ConfigurationError as ex:
        logging.debug("%s: %s", type(ex), ex)
        print("Configuration file not exist.")
        sys.exit(2)

    if options.show_config:
        print(configuration)
        sys.exit()

    if options.daemon_run or options.download_run:
        prepare_urls(configuration)

    main_work(configuration, options)

    if (not options.download_run
            and not options.daemon_run and not options.generate_podcast
            and not options.outdated):
        print("Require url to download")
        sys.exit(1)


if __name__ == "__main__":
    main()
