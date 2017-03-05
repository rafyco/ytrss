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

from ytrss.core.sys.debug import Debug
from sets import Set
import abc, os, json

class URLRemembererError(Exception):
    pass

class UrlRememberer:

    def __init__(self, file_name):
        self.file_data = ""
        self.database = []
        self.file_name = ""
        Debug().debug_log("url_remember: {}".format(file_name))
        self.file_name = file_name
        try:
            plik = open(self.file_name)
            try:
                self.file_data = plik.read()
            finally:
                plik.close()
            for elem in self.file_data.split('\n'):
                if elem != "":
                    self.database.append(elem)
                
        except Exception as ex:
            Debug().log_debug(ex)
        except:
            Debug().log_debug("Unknown error")

    def add_element(self, address):
        """ Dodaj dane do bazydanych. """
        if address == "":
            return
        self.database.append(address)
        if (self.file_name == ""):
            return
        plik = open(self.file_name, 'a')
        plik.writelines(address+'\n')
        plik.close()
        self.file_data = "%s\n%s\n" % (self.file_data, address)
        
    def is_new(self, address):
        """ Czy dane znajduja sie w pliku. """
        Debug().debug_log("Sprawdzanie pliku: {}".format(self.file_name))
        for elem in self.database:
            Debug().debug_log("Analiza: {}".format(elem))
            if elem == address:
                Debug().debug_log("old element {}".format(address))
                return False
        return True

    def get_elements(self):
        return self.database
    
    def get_file_source(self):
        return self.file_data
    
    def save_as(self, file_name):
        plik = open(file_name, 'a')
        for elem in self.database:
            plik.writelines(elem+'\n')
        plik.close()
    
    def delete_file(self):
        if (self.file_name == ""):
            return
        os.remove(self.file_name)
        self.file_name = ""
        self.file_data = ""
    
    def read_backup(self, backup_file):
        print("read backup: " + backup_file)
        if os.path.isfile(backup_file):
            try:
                plik = open(backup_file)
                try:
                    file_data = plik.read()
                finally:
                    plik.close()
                for elem in file_data.split('\n'):
                    if elem != "":
                        self.add_element(elem)
            except:
                pass
            os.remove(backup_file)

            
class Download_Queue:
    """ Klasa zapisująca do pliku adresy do pobrania. """
    
    def __init__(self, settings, base_file=None):
        self.url_rss = settings.get_url_rss() 
        self.download_file = settings.get_download_file()
        self.download_yt = UrlRememberer(self.download_file)
        if base_file == None:
            base_file = settings.get_url_rss()
        Debug().log_debug(base_file)
        self.rememberer = UrlRememberer(base_file)

    def _queue_mp3(self, address):
        """ Dodaj do pliku z danymi do pobrania. """
        if Debug().is_debug():
            return
        plik = open(self.download_file, 'a')
        plik.writelines(address+'\n')
        plik.close()

    def queue_mp3(self, address):
        Debug().debug_log("DOWNLOAD: %s" % address)
        if self.rememberer.is_new(address):
            #self._queue_mp3(address)
            Debug().debug_log("Download adress: {}".format(address))
            if not(Debug().is_debug()):
                self.download_yt.add_element(address)
                self.rememberer.add_element(address)
            return True
        return False
