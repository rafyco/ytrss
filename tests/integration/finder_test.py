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

import unittest

from ytrss.configuration.entity.source import Source
from ytrss.download.source_downloader import SourceDownloader


class TestFinder(unittest.TestCase):  # pylint: disable=R0904
    """ Test of finder """

    def test_user_find(self) -> None:
        """ Test user finder. """
        source = SourceDownloader(Source.from_json(dict(code="UCViVL2aOkLWKcFVi0_p6u6g")))
        movies = list(source.movies)
        self.assertGreater(len(movies), 0)
        for movie in movies:
            print(f"url: {movie}")
            self.assertTrue(movie.url.startswith("https://www.youtube.com/watch?v="))

    def test_playlist_find(self) -> None:
        """ Test playlist finder. """
        source = SourceDownloader(Source.from_json(dict(
            code="PLgVGo5sYBI-QeaAlxmJvw0Spw63nohIq6",
            type="playlist"
        )))
        movies = list(source.movies)
        self.assertGreater(len(movies), 0)
        for movie in movies:
            print(f"url: {movie}")
            self.assertTrue(movie.url.startswith("https://www.youtube.com/watch?v="))
