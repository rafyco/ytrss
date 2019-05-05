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
from ytrss.core.settings import YTSettings
from ytrss.core.settings import SettingException
from ytrss.subs import prepare_urls
from ytrss.ytdown import download_all_movie
from ytrss.rssgenerate import rss_generate
try:
    from daemonocle import Daemon
    from daemonocle.exceptions import DaemonError
except ImportError:
    print("""
Import Error: cannot load daemonocle.

Deamon can't run without daemonocle package. Please try invoke:

    pip3 install daemonocle
    """)
    sys.exit(2)


if sys.platform.lower().startswith('win'):
    print("""
Daemon doesn't work on Windows. Please run it on linux, or invoke:

    ytdown -d
    """)
    sys.exit(1)


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
            downloaded = 0
            try:
                downloaded = download_all_movie(settings)
            except SystemExit:
                pass
            try:
                if downloaded > 0:
                    rss_generate(settings)
            except SystemExit:
                pass
        except SettingException:
            logging.error("Configuration file not exist.")
        # This deamon, should ignore all exception and not stop script here
        except Exception as ex:  # pylint: disable=W0703
            logging.error("Unknown error: %s", ex)
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

    daemon_tmp = Daemon(worker=daemon_main,
                        pidfile='/var/run/daemonocle_example.pid')
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
        daemon_tmp.do_action(argv[1])
        sys.exit(0)
    except (DaemonError, IndexError):
        daemon_error_print()
        sys.exit(1)

if __name__ == "__main__":
    daemon()
