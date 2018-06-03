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
import os
import sys
import logging
from argparse import ArgumentParser
from ytrss import get_version
from ytrss.subs import prepare_urls
from ytrss.rssgenerate import rss_generate
from ytrss.outdated import rss_delete_outdated
from ytrss.core import UrlRememberer
from ytrss.core import DownloadQueue
from ytrss.core.settings import YTSettings
from ytrss.core.settings import SettingException
from ytrss.core.settings import SettingsParseJSONError
from ytrss.core.locker import Locker
from ytrss.core.locker import LockerError
try:
    import argcomplete
except ImportError:
    pass


class URLError(Exception):
    """ Problem with URL """
    pass


def download_all_movie(settings):
    """
    Download all movie saved in download_file.

    @param settings: Settings handle
    @type settings: L{YTSettings<ytrss.core.settings.YTSettings>}
    @return: count of downloaded movies
    @rtype: int
    """
    logging.info("download movie from urls")
    locker = Locker('lock_ytdown')
    downloaded = 0
    try:
        locker.lock()
    except LockerError:
        print("Program is running.")
        sys.exit(1)
    try:
        if not os.path.isfile(
                settings.download_file) and not os.path.isfile(
                    settings.url_backup):
            raise URLError
        urls = UrlRememberer(settings.download_file)
        urls.read_backup(settings.url_backup)
        urls.delete_file()
        urls.save_as(settings.url_backup)

        error_file = UrlRememberer(settings.err_file)
        history_file = UrlRememberer(settings.history_file)

        for elem in urls.database:
            if not history_file.is_new(elem):
                print("URL {} cannot again download".format(elem))
                continue

            if elem.download(settings):
                # finish ok
                print("finish ok")
                history_file.add_element(elem)
                downloaded = downloaded + 1
            else:
                # finish error
                print("finish error")
                error_file.add_element(elem)

        locker.unlock()

        os.remove(settings.url_backup)
    except KeyboardInterrupt as ex:
        locker.unlock()
        print("Keyboard Interrupt by user.")
        sys.exit(1)
    except URLError:
        locker.unlock()
        logging.debug("Cannot find url to download")
        sys.exit()
    except Exception as ex:
        locker.unlock()
        print("Unexpected Error: {}".format(ex))
        raise ex
    return downloaded


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
    parser.add_argument("-x", "--delete-outdate", action="store_true",
                        dest="outdated", default=False,
                        help="delete old files")
    parser.add_argument("-g", "--generate-podcast", action="store_true",
                        dest="generate_podcast", default=False,
                        help="Generate Podcast files")
    parser.add_argument("urls", nargs='*', default=[], type=str,
                        help="Url to download.")
    try:
        argcomplete.autocomplete(parser)
    except NameError:
        pass
    return parser.parse_args(argv)


def main_work(settings, options):
    """
    Make all jobs for ytdown program.

    @param settings: Settings handle
    @type settings: L{YTSettings<ytrss.core.settings.YTSettings>}
    @param option: option handle
    @type option: unknown
    """
    downloaded = 0
    force_rss = False
    if options.download_run:
        try:
            downloaded = download_all_movie(settings)
        except Exception:  # pylint: disable=W0703
            force_rss = True

    if force_rss or downloaded > 0 or options.outdated:
        if rss_delete_outdated(settings) > 0:
            force_rss = True

    if force_rss or downloaded > 0 or options.generate_podcast:
        rss_generate(settings)


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
    logging.basicConfig(format='%(asctime)s - %(name)s - '
                               '%(levelname)s - %(message)s',
                        level=options.logLevel)
    try:
        settings = YTSettings(options.configuration)
    except SettingException:
        print("Configuration file not exist.")
        exit(1)
    except SettingsParseJSONError:
        print("Problem with JSON file.")
        exit(2)

    if options.show_config:
        print(settings)
        exit()

    if options.daemon_run or options.download_run:
        prepare_urls(settings)

    main_work(settings, options)

    if (len(options.urls) < 1 and not options.download_run and
            not options.daemon_run and not options.generate_podcast and
            not options.outdated):
        print("Require url to download")
        exit(1)

    queue = DownloadQueue(settings)
    for url in options.urls:
        if queue.queue_mp3(url):
            print("Filmik zostanie pobrany: {}".format(url))
        else:
            print("Filmik nie zostanie pobrany: {}".format(url))


if __name__ == "__main__":
    main()
