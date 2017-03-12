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
Locking program module

This modul allow you to blocking program for make more of one instance.

Example of usage::

    locker = Locker('program_name')
    try:
        locker.lock()
    catch LockerError:
        print("Blocked file")
        exit(1)
    # code of our application
    locker.unlock()

@warn: Before out of program method -L{unlock() <Locker.unlock>} should
    be invoke.

"""

import os
import logging
import tempfile


class LockerError(Exception):
    """ Locker exception """
    pass


class Locker(object):
    """
    Class for blocking running program

    @warn: Before out of program method L{unlock() <Locker.unlock>} should
        be invoke.

    @ivar file_path: program's blocking file
    """
    def __init__(self, identify, direcotry=None):
        """
        Locker constructor

        @param self: object handle
        @type self: L{Locker}
        @param identify: identification of blocking application
        @type identify: str
        @param direcotry: path to direcotory with blocking file
            (if direcotry is C{None} file will be in temporary path)
        """
        if direcotry is None:
            tmp = tempfile.gettempdir()
        else:
            tmp = direcotry
        self.file_path = os.path.join(tmp, identify)
        logging.debug("lock path: %s", self.file_path)

    def is_lock(self):
        """
        Is program lock.

        @param self: object handle
        @type self: L{Locker}
        @return: C{True} is blocking on, C{False} otherwise.
        @rtype: Boolean
        """
        return os.path.isfile(self.file_path)

    def lock(self):
        """
        Lock program.

        @param self: object handle
        @type self: L{Locker}
        @raise LockerError: in case of locked
        """
        logging.debug("Lock program: %s", self.file_path)
        if self.is_lock():
            raise LockerError
        open(self.file_path, 'a').close()

    def unlock(self):
        """
        Unlock program.

        @param self: object handle
        @type self: L{Locker}
        @warn: This method not raise any exception.
        """
        logging.debug("Unlock program: %s", self.file_path)
        if self.is_lock():
            os.remove(self.file_path)
