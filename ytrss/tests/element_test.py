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
Testing Element module

@see: L{Locker<ytrss.core.element>}
"""

from __future__ import unicode_literals
import unittest
from ytrss.core.element import Element
from ytrss.core.element import InvalidParameterElementError


# This is tested class. Can have too many method
class TestElement(unittest.TestCase):  # pylint: disable=R0904
    """
    Locker tests.

    Testing for L{ytrss.core.element} module
    """
    def test_input_argument_parse(self):
        """
        Testing usage of module.

        @param self: object handle
        @type self: L{TestElement<ytrss.tests.element_test.TestElement>}
        """
        test_suites = [{
            "arg": "https://www.youtube.com/watch?v=I-JxpVFlaos",
            "code": "I-JxpVFlaos",
            "url": "https://www.youtube.com/watch?v=I-JxpVFlaos"
        }, {
            "arg": "http://www.youtube.com/watch?v=I-JxpVFlaos",
            "code": "I-JxpVFlaos",
            "url": "https://www.youtube.com/watch?v=I-JxpVFlaos"
        }, {
            "arg": "https://youtu.be/I-JxpVFlaos",
            "code": "I-JxpVFlaos",
            "url": "https://www.youtube.com/watch?v=I-JxpVFlaos"
        }, {
            "arg": "http://youtu.be/I-JxpVFlaos",
            "code": "I-JxpVFlaos",
            "url": "https://www.youtube.com/watch?v=I-JxpVFlaos"
        }, {
            "arg": "I-JxpVFlaos",
            "code": "I-JxpVFlaos",
            "url": "https://www.youtube.com/watch?v=I-JxpVFlaos"
        }, {
            "arg": "{ \"code\": \"I-JxpVFlaos\" }",
            "code": "I-JxpVFlaos",
            "url": "https://www.youtube.com/watch?v=I-JxpVFlaos"
        }, {
            "arg": {"code": "I-JxpVFlaos", "data": "today"},
            "code": "I-JxpVFlaos",
            "url": "https://www.youtube.com/watch?v=I-JxpVFlaos"
        }]

        for elem in test_suites:
            test_elem = Element(elem['arg'])
            self.assertEqual(test_elem.code, elem['code'])
            self.assertEqual(test_elem.url, elem['url'])

    def test_invalid_argument(self):
        """
        Testing invalid argument element.

        @param self: object handle
        @type self: L{TestElement<ytrss.tests.element_test.TestElement>}
        """
        test_suites = [
            "https://www.youtube.com/watch?w=I-JxpVFlaos",
            "https://www.youtube.com/watch?v=I-JxpVFlaosfs",
            "https://www.youdupe.com/watch?v=I-JxpVFlaos",
            "{'miss_code': 'I-JxpVFlaos'}",
            "{ fdsa: 'fdsa}",
            {"missing_code": 'I-JxpVFlaos'},
            234321412,
            ['this', 'should', 'not', 'work']
        ]
        for elem in test_suites:
            with self.assertRaises(InvalidParameterElementError):
                Element(elem)

    def test_comparation(self):
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
            elem1 = Element(elem['ob1'])
            elem2 = Element(elem['ob2'])
            self.assertEqual(elem1,
                             elem2,
                             "Not equal [{} != {}".format(elem['ob1'],
                                                          elem['ob2']))

    def test_serialization(self):
        """
        Testing serialization methods.

        @param self: object handle
        @type self: L{TestElement<ytrss.tests.element_test.TestElement>}
        """
        elem1 = Element("I-JxpVFlaos")
        element_string = elem1.to_string()
        elem2 = Element(element_string)
        self.assertEqual(elem1, elem2)
        self.assertEqual(elem1.code, "I-JxpVFlaos")
        self.assertEqual(elem2.code, "I-JxpVFlaos")

if __name__ == "__main__":
    unittest.main()
