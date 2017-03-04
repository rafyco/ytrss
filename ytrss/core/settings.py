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
import abc, os, json

class SettingException(Exception):
    pass

class YTSettings:
    urls = []
    playlists = []
    rss = ""
    download_file = ""    
    """ Bobieranie danych dla skryptu. """
    def __init__(self):
        self.rss = os.path.expanduser("/opt/yt_rss")
        self.download_file = os.path.expanduser("~/download_yt.txt")
    def get_user_urls(self):
        return self.urls
    def get_playlist_urls(self):
        return self.playlists
    def get_paths(self):
        return os.path.expanduser(self.rss), os.path.expanduser(self.download_file)
    def __str__(self):
        result = "Youtube configuration:\n\n"
        result += "database-file: %s\n" % self.rss
        result += "output-file: %s\n" % self.download_file
        for elem in self.urls:
            result += "\turlfile: %s\n" % elem
        for elem in self.playlists:
            result += "\tplaylist: %s\n" % elem
        return result

class YTSettingsFile(YTSettings):
    def check_confiugration_file(self, conf=""):
        if conf != "":
            if os.path.expanduser(conf):
                return conf
            else:
                raise SettingException("file: '%s' not exist.")
        if os.path.isfile(os.path.expanduser("~/.subs_config")):
            return os.path.expanduser("~/.subs_config")
        elif os.uname()[0] == 'Linux' and os.path.isfile("/etc/subs_config"):
            return "/etc/subs_config"
        else:
            raise SettingException("Cannot find configuration file.")       
    def __init__(self, conf):
        conf_find = self.check_confiugration_file(conf)
        Debug.get_instance().debug_log("Configuration file: %s" % conf_find)
        with open(conf_find) as data_file:
            data = json.load(data_file)
        self.rss = data['database']
        self.download_file = data['output']
        for elem in data['subscriptions']:
            if elem.has_key('type'):
                type = elem['type']
            else:
                type = 'url'
            if elem.has_key('enabled') and not(elem['enabled']):
                continue
            if type == 'playlist':
                self.playlists.append(elem['code'])
            else:
                self.urls.append(elem['code'])
