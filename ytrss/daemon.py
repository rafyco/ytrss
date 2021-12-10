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
Command line program to automatic downloading files.

Program checking file and download all file descripe in it. It's recomended to
add this file to crontab or call it manualy.

Example usage
=============

To invoke program type in your console::

    ytrss_deamon

or::

    python -m ytrss.daemon

for more option call program with flag C{--help}
"""

from __future__ import unicode_literals
from __future__ import print_function
import logging
import time
import sys

from ytrss.configuration.configuration import ConfigurationException
from ytrss.configuration.factory import configuration_factory
from ytrss.podcast.algoritms import rss_generate
from ytrss.finder.algoritms import prepare_urls
from ytrss.ytdown import download_all_movie


if sys.platform.lower().startswith('win'):
    print("""
Daemon doesn't work on Windows. Please run it on linux, or invoke:

    ytdown -d
    """)
    sys.exit(1)


def daemon_main() -> None:
    """
    Daemon main function.
    """
    logging.info("Start daemon")
    while True:
        try:
            logging.info("Analysis started")
            configuration = configuration_factory()
            try:
                prepare_urls(configuration)
            except SystemExit:
                pass
            try:
                download_all_movie(configuration, lambda: rss_generate(configuration))
            except SystemExit:
                pass
            logging.info("Analysis finnish")
        except ConfigurationException:
            logging.error("Configuration file not exist.")
        # This daemon, should ignore all exception and not stop script here
        except Exception as ex:  # pylint: disable=W0703
            logging.error("Unknown error: %s", ex)
        # Wait 10 min.
        time.sleep(60 * 10)


def daemon() -> None:
    """
    Daemon script function.

    This script turn on daemon.

    """

    handlers = []

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s"))
    handlers.append(console)

    try:
        file_handler = logging.FileHandler("/var/log/ytrss.daemon.log", mode="w")
        handlers.append(file_handler)
    except PermissionError:
        logging.error("Permission problem with file")

    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=handlers
    )

    logging.info("testowy log: info")
    logging.error("testowy log: error")

    daemon_main()


if __name__ == "__main__":
    daemon()
