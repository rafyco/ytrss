#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###########################################################################
#                                                                         #
#  Copyright (C) 2019  Rafal Kobel <rafalkobel@rafyco.pl>               #
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
Testing Podcast module.

@see: L{Podcast<ytrss.core.podcast>}
"""

import unittest
from ytrss.core.podcast import desc_format


class TestPodcast(unittest.TestCase):  # pylint: disable=R0904
    """
    Podcast tests.

    Testing for L{ytrss.core.podcast} module
    """

    def test_description_file(self):
        """
        Check podcast description formater

        @param self: object handle
        @type self: L{TestPodcast<ytrss.tests.podcast_test.TestPodcast>}
        """
        samples = [
            {
                "text": "test",
                "predict": "test",
            },
            {
                "text": "user@email.com",
                "predict": "<a href='mailto:user@email.com'>user@email.com</a>",
            },
            {
                "text": "http://test.com",
                "predict": "<a href='http://test.com'>http://test.com</a>",
            },
            {
                "text": "https://test.com",
                "predict": "<a href='https://test.com'>https://test.com</a>",
            },
            {
                "text": "httpd://test.com",
                "predict": "httpd://test.com",
            },
            {
                "text": "/redirect?one=one&two=two",
                "predict": "<a href='https://youtube.com/redirect?one=one&two=two'"
                           ">/redirect?one=one&two=two</a>",
            },
            {
                "text": "/redirect?one=one&q=https%3A%2F%2Ftest.com%2Ftest&two=two",
                "predict": "<a href='https://test.com/test'>https://test.com/test</a>",
            },
            {
                "text": "/redirect?one=one&two=two&q=https%3A%2F%2Ftest.com%2Ftest",
                "predict": "<a href='https://test.com/test'>https://test.com/test</a>",
            },
            {
                "text": "/redirect?one=one&two=two&q=https%3A%2F%2Ftest.com%2Ftest\n",
                "predict": "<a href='https://test.com/test'>https://test.com/test</a><br />\n",
            },
            {
                "text": "/redirect?q=https%3A%2F%2Ftest.com%2Ftest&one=one",
                "predict": "<a href='https://test.com/test'>https://test.com/test</a>",
            },
            {
                "text": "/redirect?q=https%3A%2F%2Ftest.com%2Ftest",
                "predict": "<a href='https://test.com/test'>https://test.com/test</a>",
            },
            {
                "text": "sth /redirect?q=https%3A%2F%2Ftest.com%2Ftest sth",
                "predict": "sth <a href='https://test.com/test'>https://test.com/test</a> sth",
            },
        ]
        for elem in samples:
            result = desc_format(elem['text'])
            self.assertEqual(result, elem['predict'])


if __name__ == "__main__":
    unittest.main()
