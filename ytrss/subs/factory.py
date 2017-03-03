from ytrss.core.sys.debug import Debug
from ytrss.subs.ytdown.ytdown_playlist import YTdown_playlist
from ytrss.subs.ytdown.ytdown_user import YTdown_user

class Factory:
    def __init__(self, settings = None):
        self.tab = []
        if settings != None:
            self.add_user_url(settings.get_user_urls())
            self.add_playlist_url(settings.get_playlist_urls())
    def add_user_url(self, url):
        if isinstance(url, list):
            for elem in url:
                self.add_user_url(elem)
        else:
            Debug.get_instance().debug_log("add user url: %s" % url)
            self.tab.append(YTdown_user(url))
    def add_playlist_url(self, url):
        if isinstance(url, list):
            for elem in url:
                self.add_playlist_url(elem)
        else:
            Debug.get_instance().debug_log("add playlist url: %s" % url)
            self.tab.append(YTdown_playlist(url))
    def getUrls(self):
        urls = []
        for elem in self.tab:
            Debug.get_instance().debug_log("Contener: %s" % elem)
            addresses = elem.getUrls()
            for address in addresses:
                Debug.get_instance().debug_log("El: %s" % address)
                urls.append(address)
        return urls