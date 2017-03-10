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

import logging
import os, tempfile

class LockerError(Exception):
    pass

class Locker:
    def __init__(self, id, dir=None):
        self.id = id
        if dir == None:
            tmp = tempfile.gettempdir()
        else:
            tmp = dir
        self.file_path = "%s/%s" % (tmp, id)
        logging.debug("lock path: %s" % self.file_path)
    def is_lock(self):
        return os.path.isfile(self.file_path)
    def lock(self):
        logging.debug("Lock program: %s" % self.file_path)
        if self.is_lock():
            raise LockerError
        open(self.file_path, 'a').close()
    def unlock(self):
        logging.debug("Unlock program: %s" % self.file_path)
        if self.is_lock():
            os.remove(self.file_path)