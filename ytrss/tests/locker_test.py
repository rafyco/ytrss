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
Testing Locker module

@see: L{Locker<ytrss.core.locker>}
"""

from __future__ import unicode_literals
import os
import unittest
import tempfile
from ytrss.core.locker import Locker
from ytrss.core.locker import LockerError


class TestLocker(unittest.TestCase):
    """
    Locker tests.

    Testing for L{ytrss.core.locker} module
    """
    def setUp(self):
        """ Prepare container for tests. """
        self.lockers = []

    def tearDown(self):
        """ Remove all locks after testing. """
        for lock in self.lockers:
            cleaned_locker = Locker(lock)
            cleaned_locker.unlock()

    def prepare_locker(self, text):
        """ Prepare locker object for testing. """
        self.lockers.append(text)
        return Locker(text)

    def test_usage(self):
        """ Testing usage of module. """
        tested_locker = self.prepare_locker("ytrss_module_test")

        self.assertFalse(tested_locker.is_lock())
        tested_locker.lock()
        self.assertTrue(tested_locker.is_lock())
        tested_locker.unlock()
        self.assertFalse(tested_locker.is_lock())

    def test_double_lock(self):
        """ Testing is double lock raise an error. """
        tested_locker = self.prepare_locker("ytrss_double_test")

        tested_locker.lock()
        with self.assertRaises(LockerError):
            tested_locker.lock()
        tested_locker.unlock()

    def test_double_unlock(self):
        """ Locker should not raise an exception in case of double unlock. """
        tested_locker = self.prepare_locker("ytrss_double_unlock_test")
        self.assertFalse(tested_locker.is_lock())
        tested_locker.lock()
        self.assertTrue(tested_locker.is_lock())
        tested_locker.unlock()
        self.assertFalse(tested_locker.is_lock())
        tested_locker.unlock()
        self.assertFalse(tested_locker.is_lock())

    def test_separation(self):
        """ Testing if locker with different identify are not block each other. """
        tested_locker_1 = self.prepare_locker("ytrss_separation_1_test")
        tested_locker_2 = self.prepare_locker("ytrss_separation_2_test")

        self.assertFalse(tested_locker_1.is_lock())
        self.assertFalse(tested_locker_2.is_lock())

        tested_locker_1.lock()
        self.assertTrue(tested_locker_1.is_lock())
        self.assertFalse(tested_locker_2.is_lock())

    def test_duplicate_instance(self):
        """ Testing if locker with identical identify can block each other. """
        tested_locker_1 = self.prepare_locker("ytrss_duplicate_test")
        tested_locker_2 = self.prepare_locker("ytrss_duplicate_test")
        self.assertNotEquals(tested_locker_1, tested_locker_2)

        self.assertFalse(tested_locker_1.is_lock())
        self.assertFalse(tested_locker_2.is_lock())

        tested_locker_1.lock()

        self.assertTrue(tested_locker_1.is_lock())
        self.assertTrue(tested_locker_2.is_lock())

        tested_locker_2.unlock()

        self.assertFalse(tested_locker_1.is_lock())
        self.assertFalse(tested_locker_2.is_lock())

    def test_path_locker(self):
        """ Testing if locker can be hosted in specific direcotry. """
        directory = os.path.join(tempfile.gettempdir(), "ytrss_test_path")
        try:
            os.makedirs(directory)
        except OSError:
            pass
        test_name = "ytrss_path_test"
        tested_locker = Locker(test_name, directory)
        self.assertEquals(os.path.join(directory, test_name), tested_locker.file_path)
        tested_locker.lock()
        self.assertTrue(os.path.isfile(os.path.join(directory, test_name)))
        tested_locker.unlock()
        self.assertFalse(os.path.isfile(os.path.join(directory, test_name)))
        os.rmdir(directory)

    def test_separation_direcotry(self):
        """
        Testing if locker with directory not blocking another
        locker with the same idefify.
        """
        directory = os.path.join(tempfile.gettempdir(), "ytrss_test_path")
        try:
            os.makedirs(directory)
        except OSError:
            pass
        test_name = "ytrss_path_test"
        tested_locker_d = Locker(test_name, directory)
        tested_locker = self.prepare_locker(test_name)
        tested_locker_d.lock()
        self.assertTrue(tested_locker_d.is_lock())
        self.assertFalse(tested_locker.is_lock())

        tested_locker_d.unlock()
        os.rmdir(directory)


if __name__ == "__main__":
    unittest.main()
