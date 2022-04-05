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
Testing Element module

@see: L{Locker<ytrss.core.element>}
"""

from __future__ import unicode_literals

import json
import unittest
from io import StringIO

from typing import List, Dict, Any

from ytrss.controlers.youtube.movie import YouTubeMovie
from ytrss.core.entity.movie import InvalidParameterMovieError


# This is tested class. Can have too many method
class TestMovie(unittest.TestCase):  # pylint: disable=R0904
    """
    Movie tests.

    Testing for L{ytrss.core.element} module
    """
    def test_input_argument_parse(self) -> None:
        """
        Testing usage of module.

        @param self: object handle
        @type self: L{TestElement<ytrss.tests.element_test.TestElement>}
        """
        test_suites: List[Dict[str, Any]] = [{
            "arg": "https://www.youtube.com/watch?v=I-JxpVFlaos",
            "identity": "ytdl:youtube:I-JxpVFlaos",
            "url": "https://www.youtube.com/watch?v=I-JxpVFlaos"
        }, {
            "arg": "http://www.youtube.com/watch?v=I-JxpVFlaos",
            "identity": "ytdl:youtube:I-JxpVFlaos",
            "url": "http://www.youtube.com/watch?v=I-JxpVFlaos"
        }, {
            "arg": "https://youtu.be/I-JxpVFlaos",
            "identity": "ytdl:youtube:I-JxpVFlaos",
            "url": "https://youtu.be/I-JxpVFlaos"
        }]

        for elem in test_suites:
            test_elem = YouTubeMovie(elem['arg'])
            self.assertEqual(test_elem.identity, elem['identity'])
            self.assertEqual(test_elem.url, elem['url'])

    def test_invalid_argument(self) -> None:
        """
        Testing invalid argument element.

        @param self: object handle
        @type self: L{TestElement<ytrss.tests.element_test.TestElement>}
        """
        test_suites: List[str] = [
            "https://www.youtube.com/watch?v=fakeI-JxpVFlaosfs",
            "https://www.youdupe.com/watch?v=I-JxpVFlaos",
        ]
        for elem in test_suites:
            with self.assertRaises(InvalidParameterMovieError):
                YouTubeMovie(elem)

    def test_comparation(self) -> None:
        """
        Testing comparation elements.

        @param self: object handle
        @type self: L{TestElement<ytrss.tests.element_test.TestElement>}
        """
        test_suites = [{
            "ob1": "https://www.youtube.com/watch?v=I-JxpVFlaos",
            "ob2": "https://www.youtube.com/watch?v=I-JxpVFlaos"
        }, {
            "ob1": "https://www.youtube.com/watch?v=I-JxpVFlaos",
            "ob2": "I-JxpVFlaos"
        }, {
            "ob1": "I-JxpVFlaos",
            "ob2": "I-JxpVFlaos"
        }, {
            "ob1": "I-JxpVFlaos",
            "ob2": "http://youtu.be/I-JxpVFlaos",
        }]
        for elem in test_suites:
            elem1 = YouTubeMovie(elem['ob1'])
            elem2 = YouTubeMovie(elem['ob2'])
            self.assertEqual(elem1,
                             elem2,
                             "Not equal [{} != {}".format(elem['ob1'],
                                                          elem['ob2']))

    def test_serialization(self) -> None:
        """
        Testing serialization methods.

        @param self: object handle
        @type self: L{TestElement<ytrss.tests.element_test.TestElement>}
        """
        elem1 = YouTubeMovie("https://youtube.com/watch?v=I-JxpVFlaos")
        element_string = elem1.to_string()
        elem2 = YouTubeMovie(json.load(StringIO(element_string))['url'])
        self.assertEqual(elem1, elem2)
        self.assertEqual(elem1.identity, "ytdl:youtube:I-JxpVFlaos")
        self.assertEqual(elem2.identity, "ytdl:youtube:I-JxpVFlaos")
