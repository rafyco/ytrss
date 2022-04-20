"""
Testing Element module

@see: L{Locker<ytrss.core.element>}
"""

from __future__ import unicode_literals

import unittest

from typing import List, Dict, Any

from ytrss.controlers.youtube_dl.movie import YouTubeMovie
from ytrss.core.entity.movie import InvalidParameterMovieError


# This is tested class. Can have too many method
from ytrss.core.typing import Url


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
        test_suites: List[Url] = [
            Url("https://www.youtube.com/watch?v=fakeI-JxpVFlaosfs"),
            Url("https://www.youdupe.com/watch?v=I-JxpVFlaos"),
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
            elem1 = YouTubeMovie(Url(elem['ob1']))
            elem2 = YouTubeMovie(Url(elem['ob2']))
            self.assertEqual(elem1,
                             elem2,
                             "Not equal [{} != {}".format(elem['ob1'],
                                                          elem['ob2']))
