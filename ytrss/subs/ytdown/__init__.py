from ytrss.core.sys.debug import Debug
from urllib import urlopen
from xml.dom import minidom
import abc

class YTdown_abstract:
    """ Klasa do pobierania listy adresow url filmow z podanego zrodla. """
    __metaclass__ = abc.ABCMeta
    def __init__(self, code):
        self.code = code
    @abc.abstractmethod
    def build_url(self):
        pass
    def getUrls(self):
        url = self.build_url()
        Debug.get_instance().debug_log("URL: %s" % url)
        return self.youtube_list_from_address(url)
    def youtube_list_from_address(self, address):
        """ Zwraca liste filmow dla uzytkownika o podanym adresie. """
        xml_str = urlopen(address).read()
        xmldoc = minidom.parseString(xml_str)
        tags = xmldoc.getElementsByTagName('link')
        result = []
        iterator = 0
        for elem in tags:
            if iterator != 0 and iterator != 1:
                url = elem.getAttribute("href")
                result.append(url)
            iterator = iterator + 1
        return result