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
Testing module ytrss.

TestCase checking module files. It should be conform to PEP8.

@see: L{ytrss}
"""

from __future__ import unicode_literals
import unittest
import pep8
import ytrss


class TestYTRSSModule(unittest.TestCase):
    """ Module testsCase. """
    def test_pap8(self):
        """ Test that we conform to PEP8. """
        pep8_style = pep8.StyleGuide(paths=['--ignore=E501'])
        # Disable E501 code (line too long). It should be enabled after fixed.
        result = pep8_style.check_files(ytrss.__path__)
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

if __name__ == "__main__":
    unittest.main()
