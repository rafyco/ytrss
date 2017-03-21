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
Add one or more URL address to downlad file.

Example usage
=============

To invoke program type in your console::

    ytdown [url]

or::

    python -m ytrss.ytdown [url]

for more option call program with flag C{--help}
"""

from __future__ import unicode_literals
from __future__ import print_function
import sys
import time
import logging
from argparse import ArgumentParser
from ytrss import get_version
from ytrss.daemon import download_all_movie
from ytrss.subs import prepare_urls
from ytrss.core import DownloadQueue
from ytrss.core.settings import YTSettings
from ytrss.core.settings import SettingException
from daemonocle import Daemon
from daemonocle.exceptions import DaemonError
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
    parser = ArgumentParser(description="Save one or more urls from "
                                        "Youtube to file.",
                            prog='ytdown')
    parser.add_argument("-v", "--version", action='version',
                        version='%(prog)s {}'.format(get_version()))
    parser.add_argument("-c", "--conf", dest="configuration",
                        help="configuration file", default="", metavar="FILE")
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
    parser.add_argument("urls", nargs='*', default=[], type=str,
                        help="Url to download.")
    try:
        argcomplete.autocomplete(parser)
    except NameError:
        pass
    return parser.parse_args(argv)


def main(argv=None):
    """
    Main function for command line program.

    @param argv: Option parameters
    @type argv: list
    """
    options = __option_args(argv)
    logging.basicConfig(format='%(asctime)s - %(name)s - '
                               '%(levelname)s - %(message)s',
                        level=options.logLevel)
    try:
        settings = YTSettings(options.configuration)
    except SettingException:
        print("Configuration file not exist.")
        exit(1)

    if options.show_config:
        print(settings)
        exit()

    if options.daemon_run or options.download_run:
        prepare_urls(settings)

    if options.download_run:
        download_all_movie(settings)

    if (len(options.urls) < 1 and not options.download_run and
            not options.daemon_run):
        print("Require url to download")
        exit(1)

    queue = DownloadQueue(settings)
    for url in options.urls:
        if queue.queue_mp3(url):
            print("Filmik zostanie pobrany: {}".format(url))
        else:
            print("Filmik nie zostanie pobrany: {}".format(url))


def daemon_main():
    """
    Daemon main function.
    """
    while True:
        try:
            settings = YTSettings()
            try:
                prepare_urls(settings)
            except SystemExit:
                pass
            try:
                download_all_movie(settings)
            except SystemExit:
                pass
        except SettingException:
            logging.error("Configuration file not exist.")
        except Exception as ex:
            logging.error("Unknown error: {}".format(ex))
        # Wait 10 min.
        time.sleep(60 * 10)


def daemon_error_print():
    """
    Print error message in case of invalid argument.
    """
    print("[info] Usage: /etc/init.d/ytrss {start|stop|restart|status}")


def daemon(argv=None):
    """
    Daemon script function.

    This script turn on daemon.

    @param argv: Option parameters
    @type argv: list
    """
    daemon = Daemon(worker=daemon_main,
                    pidfile='/var/run/daemonocle_example.pid'
                    )
    if argv is None:
        argv = sys.argv
    logging.basicConfig(
        filename='/var/log/ytrss_daemon.log',
        level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s',
    )
    if len(argv) != 2:
        daemon_error_print()
        exit(1)
    try:
        if argv[1] == "start":
            try:
                YTSettings()
            except SettingException:
                print("Configuration file not exist.")
                exit(1)
        daemon.do_action(argv[1])
        sys.exit(0)
    except (DaemonError, IndexError):
        daemon_error_print()
        sys.exit(1)


if __name__ == "__main__":
    main()
