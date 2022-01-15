#!/usr/bin/env python3
###########################################################################
#                                                                         #
#  Copyright (C) 2017-2022 Rafal Kobel <rafalkobel@rafyco.pl>             #
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
import os
from typing import Iterable, Optional

from ytrss.configuration.configuration import Configuration
from ytrss.core.entity.movie import Movie
from ytrss.database.database_get import DatabaseGet, DatabaseGetOpen
from ytrss.database.file_db.database_file_config import DatabaseFileConfig
from ytrss.database.file_db.database_file_controller import DatabaseFileController


class FileDatabaseGetOpen(DatabaseGetOpen):
    """
    TODO: documentation
    """

    def __init__(self, configuration: Configuration):
        self.__configuration = configuration
        self.__file_config = DatabaseFileConfig(configuration)

        self.__download_file = DatabaseFileController(self.__file_config.download_file)
        self.__download_file.read_backup(self.__file_config.url_backup)
        self.__download_file.read_backup(self.__file_config.next_time)
        self.__download_file.delete_file()
        self.__download_file.save_as(self.__file_config.url_backup)
        self.__next_time_file = DatabaseFileController(self.__file_config.next_time)

        self.__error_file = DatabaseFileController(self.__file_config.err_file)
        self.__history_file = DatabaseFileController(self.__file_config.history_file)

    def mark_error(self, movie: Movie) -> None:
        self.__error_file.add_movie(movie)

    def close(self, exc_value: Optional[BaseException]) -> None:
        if exc_value is None:
            os.remove(self.__file_config.url_backup)

    def is_new(self, movie: Movie) -> bool:
        return self.__history_file.is_new(movie)

    def down_next_time(self, movie: Movie) -> None:
        return self.__next_time_file.add_movie(movie)

    def add_to_history(self, movie: Movie) -> None:
        return self.__history_file.add_movie(movie)

    def movies(self) -> Iterable[Movie]:
        """
        TODO: documentation
        """
        return self.__download_file.database


class FileDatabaseGet(DatabaseGet):
    """
    TODO: documentation
    """
    def __init__(self, configurations: Configuration):
        DatabaseGet.__init__(self)
        self.__configuration = configurations

    def open(self) -> DatabaseGetOpen:
        """
        TODO: documentation
        """
        return FileDatabaseGetOpen(self.__configuration)
