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
import json
import logging
import os
from io import StringIO
from json import JSONDecodeError
from typing import List

from ytrss.core.factory import CoreFactoryError
from ytrss.core.factory.movie import create_movie
from ytrss.core.entity.movie import InvalidParameterMovieError, Movie


class URLRemembererError(Exception):
    """ URLRememberer Exception. """


class DatabaseFileController:
    """
    Remember URLs or read it from file.

    @ivar file_name: name of checking file
    @type file_name: str
    @ivar file_data: source of file with data
    @type file_data: str
    @ivar database: list of checking urls
    @type database: list
    """
    def __init__(self, file_name: str) -> None:
        """
        UrlRememberer constructor.

        @param self: object handle
        @type self: L{DatabaseFileController}
        @param file_name: name of checking file
        @type file_name: str
        """
        self.file_data = ""
        self.database: List[Movie] = []
        logging.debug("url_remember: %s", file_name)
        self.file_name = file_name
        try:
            with open(self.file_name) as file_handle:
                self.file_data = file_handle.read()
            for elem in self.file_data.split('\n'):
                try:
                    tmp_elem = create_movie(json.load(StringIO(elem))['url'])
                    self.database.append(tmp_elem)
                except (InvalidParameterMovieError, CoreFactoryError, JSONDecodeError) as ex:
                    logging.debug("Error: %s", ex)

        except IOError as ex:
            logging.debug("Unknown error %s", ex)

    def add_movie(self, movie: Movie) -> None:
        """
        Add address to base.

        @param self: object handle
        @type self: L{DatabaseFileController}
        @param movie: adding address
        @type movie: L{Element<ytrss.core.element.Element>}
        """
        self.database.append(movie)
        if self.file_name == "":
            return
        with open(self.file_name, 'a') as file_handle:
            file_handle.writelines(movie.to_string() + '\n')
        logging.debug("Add %s to file: %s", movie.to_string(), self.file_name)
        self.file_data = f"{self.file_data}\n{movie.to_string()}\n"

    def is_new(self, movie: Movie) -> bool:
        """
        Check is URL not exist in file.

        @param self: object handle
        @type self: L{DatabaseFileController}
        @param movie: element to check
        @type movie: L{Element<ytrss.core.element.Element>}
        @return: C{True} if address new, C{False} otherwise
        @rtype: Boolean
        """
        logging.debug("Sprawdzanie pliku: %s", self.file_name)
        for elem in self.database:
            logging.debug("Analiza: %s", elem.url)
            if elem == movie:
                logging.debug("old element %s", movie.url)
                return False
        return True

    def save_as(self, file_name: str) -> None:
        """
        Save copy to file.

        @param self: object handle
        @type self: L{DatabaseFileController}
        @param file_name: path to save
        @type file_name: str
        """
        with open(file_name, 'a') as file_handle:
            for elem in self.database:
                file_handle.writelines(elem.to_string() + '\n')

    def delete_file(self) -> None:
        """
        Delete file with data.

        @param self: object handle
        @type self: L{DatabaseFileController}
        """
        if self.file_name == "":
            return
        if os.path.isfile(self.file_name):
            os.remove(self.file_name)
        self.file_name = ""
        self.file_data = ""

    def read_backup(self, backup_file: str) -> None:
        """
        Merge with another file.

        @param self: object handle
        @type self: L{DatabaseFileController}
        @param backup_file: path to read data
        @type backup_file: str

        @warn: If file not exist method not raise any exception
        """
        logging.debug("read backup: %s", backup_file)
        if os.path.isfile(backup_file):
            try:
                with open(backup_file) as file_handle:
                    file_data = file_handle.read()
                    for elem in file_data.split('\n'):
                        try:
                            self.add_movie(create_movie(json.load(StringIO(elem))['url']))
                        except JSONDecodeError:
                            pass
                        except CoreFactoryError as ex:
                            logging.error("Exception: %s", ex)
            except IOError:
                pass
            os.remove(backup_file)
