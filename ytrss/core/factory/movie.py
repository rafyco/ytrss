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
from typing import Union, Dict, Any

from ytrss.configuration.consts import DEFAULT_PODCAST_DIR
from ytrss.controlers.youtube.movie import YouTubeMovie
from ytrss.core.movie import Movie


def create_movie(arg: Union[str, Dict[str, Any]],
                 destination_dir: str = DEFAULT_PODCAST_DIR) -> Movie:
    """
    Create Movie object from args
    """
    return YouTubeMovie(arg, destination_dir)
