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

from __future__ import unicode_literals
from ytrss.core.sys.debug import Debug
import abc, os, json

class SettingException(Exception):
    pass

class YTSettings:
    urls = []
    playlists = [] 

    def __init__(self, conf):
        try:
            os.makedirs(YTSettings.get_os_conf_path())
        except OSError:
            pass
        
        conf_find = self.check_configuration_file(conf)
        Debug().debug_log("Configuration file: %s" % conf_find)
        with open(conf_find) as data_file:
            data = json.load(data_file)
                
        self.output = os.path.expanduser(data['output'])
        if self.output == "":
            self.output = os.path.expanduser("~/ytrss_output")
        
        self.parse_subsctiptions(data['subscriptions'])

    """ Bobieranie danych dla skryptu. """
    def get_user_urls(self):
        return self.urls
    @staticmethod
    def get_os_conf_path():
        conf_path = "ytrss"
        if os.uname()[0] == 'Linux':
            conf_path = os.path.join("~/.config", conf_path)
        return os.path.expanduser(conf_path)

    @staticmethod
    def get_conf_file_path(file_name):
        return os.path.join(YTSettings.get_os_conf_path(), file_name)

    def get_playlist_urls(self):
        return self.playlists

    def get_url_rss(self):
        return YTSettings.get_conf_file_path("rss_remember.txt")

    def get_download_file(self):
        return YTSettings.get_conf_file_path("download_yt.txt")
        
    def get_url_backup(self):
        return YTSettings.get_conf_file_path("download_yt_last.txt")
        
    def get_history_file(self):
        return YTSettings.get_conf_file_path("download_yt_history.txt")
    
    def get_err_file(self):
        return YTSettings.get_conf_file_path("download_yt.txt.err")
       
    def get_cache_path(self):
        return YTSettings.get_conf_file_path("cache")
        
    def get_output_path(self):
        try:
            os.makedirs(self.output)
        except OSError:
            pass
        return self.output

    def __str__(self):
        result = "Youtube configuration:\n\n"
        result += "output-file: %s\n" % self.output
        for elem in self.urls:
            result += "\turlfile: %s\n" % elem
        for elem in self.playlists:
            result += "\tplaylist: %s\n" % elem
        return result

    def check_configuration_file(self, conf=""):
        if conf != "":
            if os.path.expanduser(conf):
                return conf
            else:
                raise SettingException("file: '%s' not exist.")
        conf_file_path = YTSettings.get_conf_file_path("config")
        if os.path.isfile(conf_file_path):
            return conf_file_path
        elif os.uname()[0] == 'Linux' and os.path.isfile("/etc/subs_config"):
            return "/etc/subs_config"
        else:
            raise SettingException("Cannot find configuration file.")

    def parse_subsctiptions(self, subs):
        for elem in subs:
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
