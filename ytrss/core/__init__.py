#!/usr/bin/env python
from ytrss.core.sys.debug import Debug
import abc, os, json

class UrlRememberer:
    def __init__(self, file_name):
        self.file_name = file_name
        try:
            plik = open(self.file_name)
            try:
                self.database = plik.read()
            finally:
                plik.close()
        except:
            self.database = ""
    def add_element(self, address):
        """ Dodaj dane do bazydanych. """
        plik = open(self.file_name, 'a')
        plik.writelines(address+'\n')
        plik.close()
        self.database = "%s\n%s\n" % (self.database, address)
    def is_new(self, address):
        """ Czy dane znajduja sie w pliku. """
        for line in self.database.split('\n'):
            if line.find(address) != -1:
                print("isnieje %s" % address)
                return False
        print("nieisnieje %s" % address)
        return True

class Downloader:
    def __init__(self, settings):
        self.url_rss, self.download_file = settings.get_paths()
        self.rememberer = UrlRememberer(self.url_rss)
    def _download_mp3(self, address):
        """ Dodaj do pliku z danymi do pobrania. """
        if Debug.get_instance().is_debug():
            return
        plik = open(self.download_file, 'a')
        plik.writelines(address+'\n')
        plik.close()
    def download_mp3(self, address):
        Debug.get_instance().debug_log("DOWNLOAD: %s" % address)
        if self.rememberer.is_new(address):
            self._download_mp3(address)
            if not(Debug.get_instance().is_debug()):
                self.rememberer.add_element(address)

class SettingException(Exception):
    pass

class YTsettings:
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

class YTsettingsFile(YTsettings):
    def check_confiugration_file(self, conf=""):
        if conf != "":
            if os.path.expanduser(conf):
                return conf
            else:
                raise SettingException("file: '%s' not exist.")
        if os.path.isfile(os.path.expanduser("~/.subs_config")):
            return os.path.expanduser("~/.subs_config")
        elif os.path.isfile("/etc/subs_config"):
            return "/etc/subs_config"
        else:
            raise Exception("Cannot find configuration file.")       
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
