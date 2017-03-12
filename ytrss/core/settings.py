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
Settings parser module.

File are read from the first of the following location.

For MS Windows

    - I{~/YTRSS/config}

For Linux (and other systems)

    - I{/etc/subs_config}
    - I{~/.config/ytrss/config}

In some case you can set file path in constructor or read data in json format.

Config file structure
=====================

Configuration file is in a json format with following option:

    - I{output} - Path to folder where program should download files.
    - I{subscription} - List of subscription.
        For more see: L{parsing function
        <ytrss.core.settings.YTSettings.__parse_subsctiptions>}

Example file
============

code of example file::

    {
        "output"   : "<output_file>",
        "subscriptions" : [
            {
                "code"    : "<playlist_id>",
                "type"    : "playlist"
            },
            {
                "code"    : "<subscritpion_id>"
            },
            {
                "code"    : "<subscription_id>",
                "enabled" : false
            }
        ]
    }

"""

from __future__ import unicode_literals
import os
import sys
import json
import logging


class SettingException(Exception):
    """ Settings exception. """
    pass


class YTSettings(object):
    """
    Parser settings for ytrss.

    Class read settings from parameters or from default conf file.

    @ivar url_rss: file with list of read urls
    @type url_rss: str
    @ivar download_file: file ready to download
    @type download_file: str
    @ivar url_backup: file with actuall downloading files
    @type url_backup: str
    @ivar history_file: file with successfull download urls
    @type history_file: str
    @ivar err_file: file with urls with not downloaded
    @type err_file: str
    @ivar cache_path: path to cache folder
    @type cache_path: str
    """

    urls = []
    """ @cvar: list of subscription codes """
    playlists = []
    """ @cvar: list of playlist codes """

    def __init__(self, conf_file="", conf_str=""):
        """
        YTSettings constructor.

        @param self: object handle
        @type self: L{YTSettings}
        @param conf_file: Path to configuration file
        @type conf_file: str
        @param conf_str: Json format string configuration
        @type conf_str: str
        @raise SettingException: In case of C{conf_file} and C{conf_str}
            are not set.
        """
        conf_path = ""
        if sys.platform.lower().startswith('win'):
            conf_path = os.path.join("~\\YTRSS", conf_path)
        else:
            conf_path = os.path.join("~/.config/ytrss", conf_path)
        self.conf_path = os.path.expanduser(conf_path)

        try:
            os.makedirs(self.conf_path)
        except OSError:
            pass

        data = {}
        if conf_str is not "":
            data = json.load(conf_str)
        else:
            conf_find = self.__check_configuration_file(conf_file)
            logging.debug("Configuration file: %s", conf_find)
            with open(conf_find) as data_file:
                data = json.load(data_file)

        if data is {}:
            raise SettingException

        self.__parse_data(data)

    def __parse_data(self, data):
        """
        Save parsing data from json to object.

        @param self: object handle
        @type self: L{YTSettings}
        @param data: data from json
        @type data: dict
        @see: L{ytrss.core.settings}
        """
        if 'output' in data:
            self.output = os.path.expanduser(data['output'])
        else:
            self.output = os.path.expanduser("~/ytrss_output")
            try:
                os.makedirs(self.output)
            except OSError:
                pass

        self.__parse_subsctiptions(data['subscriptions'])

        self.url_rss = self.__conf_file_path("rss_remember.txt")
        self.download_file = self.__conf_file_path("download_yt.txt")
        self.url_backup = self.__conf_file_path("download_yt_last.txt")
        self.history_file = self.__conf_file_path("download_yt_history.txt")
        self.err_file = self.__conf_file_path("download_yt.txt.err")
        self.cache_path = self.__conf_file_path("cache")

    def __str__(self):
        """
        Display settings information.

        @param self: object handle
        @type self: L{YTSettings}
        @return: formated configuration
        @rtype: str
        """
        result = "Youtube configuration:\n\n"
        result += "output-file: %s\n" % self.output
        for elem in self.urls:
            result += "\turlfile: %s\n" % elem
        for elem in self.playlists:
            result += "\tplaylist: %s\n" % elem
        return result

    def __conf_file_path(self, file_name):
        """
        Create path to file in working folder.

        @param self: object handle
        @type self: L{YTSettings}
        @param file_name: name of searching file
        @type file_name: str
        @return: path to searching file
        @rtype: str
        """
        return os.path.join(self.conf_path, file_name)

    def __check_configuration_file(self, conf=""):
        """
        Get path to configuration file.

        @param self: object handle
        @type self: L{YTSettings}
        @param conf: path to prefer configuration file
        @type conf: str
        @return: path to existing configuration file
        @rtype: str
        @raise SettingException: configuration file not exist
        """
        if conf != "":
            if os.path.expanduser(conf):
                return conf
            else:
                raise SettingException("file: '%s' not exist.")
        conf_file_path = self.__conf_file_path("config")
        if os.path.isfile(conf_file_path):
            return conf_file_path
        elif not(sys.platform.lower().startswith('win')) and os.path.isfile("/etc/subs_config"):
            return "/etc/subs_config"
        else:
            raise SettingException("Cannot find configuration file.")

    def __parse_subsctiptions(self, subs):
        """
        Save parsing information about subscriptions and playlists.

        Information is a list of dict with following fileds.

            - I{type [ url | playlist ]} - type of subscription code. C{url}
                for usual subscription, C{playlist} for playlists.
                (C{url} is default)
            - I{code} - identificator to source of movies. It can be extracted
                from url.
            - I{enabled} - Is element should be downloaded.
                (C{True} is default)


        @param self: object handle
        @type self: L{YTSettings}
        @param subs: list of dicts
        @type subs: list
        """
        for elem in subs:
            if 'type' in elem:
                link_type = elem['type']
            else:
                link_type = 'url'
            if 'enabled' in elem and not elem['enabled']:
                continue
            if link_type == 'playlist':
                self.playlists.append(elem['code'])
            else:
                self.urls.append(elem['code'])
