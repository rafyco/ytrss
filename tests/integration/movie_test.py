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
Testing movie module
"""

from __future__ import unicode_literals

import json
import unittest
from io import StringIO

from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.controlers.youtube_dl.movie import YouTubeMovie


# This is tested class. Can have too many method
from ytrss.core.typing import Url
from ytrss.database.entity.movie_task import MovieTask


class TestMovie(unittest.TestCase):  # pylint: disable=R0904
    """
    movie integration tests
    """
    def test_serialization(self) -> None:
        """
        Testing serialization methods.

        @param self: object handle
        @type self: L{TestElement<ytrss.tests.element_test.TestElement>}
        """
        elem1 = YouTubeMovie(Url("https://youtube.com/watch?v=I-JxpVFlaos"))
        dest = DestinationId("fake")
        movie_task = MovieTask.from_objects(elem1, dest)
        element_string = movie_task.row
        elem2 = MovieTask.from_json(json.load(StringIO(element_string)))
        self.assertEqual(elem1, elem2.movie)
        self.assertEqual(elem1.identity, "ytdl:youtube:I-JxpVFlaos")
        self.assertEqual(elem2.movie.identity, "ytdl:youtube:I-JxpVFlaos")
