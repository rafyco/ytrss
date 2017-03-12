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
Module with additional class for ytrss tools.
"""

from __future__ import unicode_literals
from __future__ import print_function
import os
import abc
import json
import logging


class URLRemembererError(Exception):
    """ URLRememberer Exception. """
    pass


class UrlRememberer(object):
    """
    Remember URLs or read it from file.

    @ivar file_name: name of checking file
    @type file_name: str
    @ivar file_data: source of file with data
    @type file_data: str
    @ivar database: list of checking urls
    @type database: list
    """
    def __init__(self, file_name):
        """
        UrlRememberer constructor.

        @param self: object handle
        @type self: L{UrlRememberer}
        @param file_name: name of checking file
        @type file_name: str
        """
        self.file_data = ""
        self.database = []
        self.file_name = ""
        logging.debug("url_remember: %s", file_name)
        self.file_name = file_name
        try:
            plik = open(self.file_name)
            try:
                self.file_data = plik.read()
            finally:
                plik.close()
            for elem in self.file_data.split('\n'):
                if elem != "":
                    self.database.append(elem)

        except IOError as ex:
            logging.debug("Unknown error %s", ex)

    def add_element(self, address):
        """
        Add address to base.

        @param self: object handle
        @type self: L{UrlRememberer}
        @param address: adding address
        @type address: str
        """
        if address == "":
            return
        self.database.append(address)
        if self.file_name == "":
            return
        plik = open(self.file_name, 'a')
        plik.writelines(address + '\n')
        plik.close()
        self.file_data = "{}\n{}\n".format(self.file_data, address)

    def is_new(self, address):
        """
        Check is URL not exist in file.

        @param self: object handle
        @type self: L{UrlRememberer}
        @param address: address to check
        @type address: str
        @return: C{True} if address new, C{False} otherwise
        @rtype: Boolean
        """
        logging.debug("Sprawdzanie pliku: %s", self.file_name)
        for elem in self.database:
            logging.debug("Analiza: %s", elem)
            if elem == address:
                logging.debug("old element %s", address)
                return False
        return True

    def save_as(self, file_name):
        """
        Save copy to file.

        @param self: object handle
        @type self: L{UrlRememberer}
        @param file_name: path to save
        @type file_name: str
        """
        plik = open(file_name, 'a')
        for elem in self.database:
            plik.writelines(elem + '\n')
        plik.close()

    def delete_file(self):
        """
        Delete file with data.

        @param self: object handle
        @type self: L{UrlRememberer}
        """
        if self.file_name == "":
            return
        os.remove(self.file_name)
        self.file_name = ""
        self.file_data = ""

    def read_backup(self, backup_file):
        """
        Merge with another file.

        @param self: object handle
        @type self: L{UrlRememberer}
        @param backup_file: path to read data
        @type backup_file: str
        @warn: If file not exist method not raise any exception
        """
        logging.debug("read backup: %s", backup_file)
        if os.path.isfile(backup_file):
            try:
                plik = open(backup_file)
                try:
                    file_data = plik.read()
                finally:
                    plik.close()
                for elem in file_data.split('\n'):
                    if elem != "":
                        self.add_element(elem)
            except IOError:
                pass
            os.remove(backup_file)


class DownloadQueue(object):
    """
    Class saving urls to download.

    @ivar url_rss: path to file with readed urls
    @type url_rss: str
    @ivar download_file: file ready to download
    @type download_file: str
    @ivar rememberer: object remebering urls
    @type rememberer: L{UrlRememberer}
    """

    def __init__(self, settings, base_file=None):
        """
        DownloadQueue constructor.

        @param self: object handle
        @type self: L{DownloadQueue}
        @param settings: settings for DownloadQueue
        @type settings: L{YTSettings<ytrss.core.settings.YTSettings>}
        @param base_file: path to file with remember subscription
        @type base_file: str

        @note:: if C{base_file} not set, it is get from settings object.
        """
        self.url_rss = settings.url_rss
        self.download_file = settings.download_file
        self.download_yt = UrlRememberer(self.download_file)
        if base_file is None:
            base_file = settings.url_rss
        logging.debug(base_file)
        self.rememberer = UrlRememberer(base_file)

    def queue_mp3(self, address):
        """
        Add address to download.

        @param self: object handle
        @type self: L{DownloadQueue}
        @param address: adress to download
        @type address: str

        @return: C{True} if C{address} can be downloaded, C{False} otherwise
        @rtype: Boolean
        """
        logging.debug("DOWNLOAD: %s", address)
        if self.rememberer.is_new(address):
            logging.debug("Download adress: %s", address)
            self.download_yt.add_element(address)
            self.rememberer.add_element(address)
            return True
        return False
