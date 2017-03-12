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

from __future__ import unicode_literals
from __future__ import print_function
import os
import sys
import logging
from argparse import ArgumentParser
from ytrss import get_version
from ytrss.core import UrlRememberer
from ytrss.core.locker import Locker, LockerError
from ytrss.core.downloader import Downloader
from ytrss.core.settings import YTSettings
from ytrss.core.settings import SettingException
try:
    import argcomplete
except ImportError:
    pass


def __option_args(argv=None):
    parser = ArgumentParser(description="Download all Youtube's movie "
                                        "to youtube path.",
                            prog='ytrss_daemon',
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


class DaemonError(Exception):
    pass


# pylint: disable=R0915
def main(argv=None):
    options = __option_args(argv)
    logging.basicConfig(format='%(asctime)s - %(name)s - '
                               '%(levelname)s - %(message)s',
                        level=options.logLevel)
    logging.debug("Debug mode: Run")
    try:
        settings = YTSettings(options.configuration)
    except SettingException:
        print("Configuration file not exist.")
        sys.exit(1)

    locker = Locker('lock_ytdown')
    try:
        locker.lock()
    except LockerError:
        print("Program is running.")
        sys.exit(1)
    try:
        if not os.path.isfile(settings.download_file) and not os.path.isfile(settings.url_backup):
            raise DaemonError
        urls = UrlRememberer(settings.download_file)
        urls.read_backup(settings.url_backup)
        urls.delete_file()
        urls.save_as(settings.url_backup)

        error_file = UrlRememberer(settings.err_file)
        history_file = UrlRememberer(settings.history_file)

        for elem in urls.get_elements():
            if not history_file.is_new(elem):
                print("URL {} cannot again download".format(elem))
                continue
            task = Downloader(settings, elem)
            if task.download():
                # finish ok
                print("finish ok")
                history_file.add_element(elem)
            else:
                # finish error
                print("finish error")
                error_file.add_element(elem)

        locker.unlock()

        os.remove(settings.url_backup)
        logging.debug("End")
    except KeyboardInterrupt as ex:
        locker.unlock()
        print("Keyboard Interrupt by user.")
        sys.exit(1)
    except DaemonError:
        locker.unlock()
        logging.debug("Cannot find url to download")
        sys.exit()
    except Exception as ex:
        locker.unlock()
        print("Unexpected Error: {}".format(ex))
        raise ex


def daemon():
    print("Not implemented yet.")
    sys.exit(1)

if __name__ == "__main__":
    main()
