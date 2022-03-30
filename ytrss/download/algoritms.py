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
"""
Module with algorithms that download files
"""

import logging
import sys
from typing import Callable, Optional

from ytrss.configuration.configuration import Configuration
from ytrss.core.factory.database_get import create_database_get
from ytrss.database.file_db.locker import Locker, LockerError


# pylint: disable=R0915
def download_all_movie(
        configuration: Configuration,
        on_success: Optional[Callable[[], None]] = None
) -> int:
    """
    Download all movie saved in download_file.

    @param configuration: Settings handle
    @param on_success: callback invoked on success
    @return: count of downloaded movies
    """

    logging.info("download movie from urls")
    downloaded = 0
    try:
        with Locker('lock_ytdown'):
            with create_database_get(configuration) as database:

                for movie in database.movies():
                    if not database.is_new(movie):
                        print(f"URL {movie} cannot again download")
                        continue
                    if not movie.is_ready:
                        print("movie is not ready to download")
                        database.down_next_time(movie)
                        continue
                    if movie.download(configuration):
                        # finish ok
                        print("finish ok")
                        database.add_to_history(movie)
                        if on_success is not None:
                            on_success()
                        downloaded = downloaded + 1
                    else:
                        # finish error
                        print("finish error")
                        database.mark_error(movie)

    except LockerError:
        print("Program is running.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Keyboard Interrupt by user.")
        sys.exit(1)
    except Exception as ex:
        print("Unexpected Error: {}".format(ex))
        raise ex
    if downloaded == 0:
        logging.debug("Cannot find url to download")
    return downloaded