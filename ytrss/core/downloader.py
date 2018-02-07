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
Download mp3 file from YouTube using I{youtube_dl} library.

@see: U{https://rg3.github.io/youtube-dl/}
"""

from __future__ import unicode_literals
from __future__ import print_function
import os
import shutil
import logging
import youtube_dl
import ytrss


class Downloader(object):
    """
    Download mp3 file from YouTube.

    Class download file to cache folder. In case of success files are
    moved to output file. Output and cache folder are describe in
    L{YTSettings<ytrss.core.settings.YTSettings>} object.

    @ivar settings: Setting object
    @type settings: L{YTSettings<ytrss.core.settings.YTSettings>}
    @ivar url: URL to download
    @type url: str
    @ivar output_path: Path to output folder
    @type output_path: str
    """
    def __init__(self, settings, url):
        """
        Downloader constructor.

        @param self: object handler
        @type self: L{Downloader}
        @param settings: settings handler
        @type settings: L{YTSettings<ytrss.core.settings.YTSettings>}
        @param url: URL to YouTube movie
        @type url: L{Element<ytrss.core.element.Element>}
        """
        assert isinstance(url, ytrss.core.element.Element)
        self.settings = settings
        self.url = url
        self.output_path = settings.output

    def download(self):
        """
        Download YouTube movie.

        Function download movie, convert to mp3 and move to output file.

        @param self: object handler
        @type self: L{Downloader}
        @return: C{True} if success, C{False} otherwise
        @rtype: Boolean
        """
        status = 0
        cache_path = self.settings.cache_path
        try:
            os.makedirs(cache_path)
        except OSError:
            pass
        current_path = os.getcwd()
        os.chdir(cache_path)

        logging.info("url: %s", self.url.url)
        command = self.settings.args + ['-o',
                                        "{}.mp3".format(self.url.code),
                                        self.url.url]
        try:
            youtube_dl.main(command)
        except SystemExit as ex:
            if ex.code is None:
                status = 0
            else:
                status = ex.code  # pylint: disable=E0012,R0204

        finded = False
        full_file_name = "{}.mp3".format(self.url.code)
        metadate_name = "{}.json".format(self.url.code)
        if os.path.isfile(full_file_name):
            source_path = os.path.join(cache_path, full_file_name)
            destination_path = os.path.join(self.output_path,
                                            self.url.destination_dir,
                                            full_file_name)
            metadate_path = os.path.join(self.output_path,
                                         self.url.destination_dir,
                                         metadate_name)
            try:
                os.mkdir(self.output_path)
            except OSError:
                pass
            try:
                os.mkdir(os.path.join(self.output_path,
                                      self.url.destination_dir))
            except OSError:
                pass
            logging.debug("source_path: %s", source_path)
            logging.debug("destination_path: %s", destination_path)
            shutil.move(source_path, destination_path)
            file_handler = open(metadate_path, 'w')
            file_handler.write(self.url.get_json_description())
            file_handler.close()
            finded = True

        for find_file in os.listdir(cache_path):
            if find_file.endswith(".mp3"):
                print("Unknown file: {}".format(find_file))

        os.chdir(current_path)
        return status == 0 and finded
