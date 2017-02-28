from ytrss.core.sys.debug import Debug
from ytrss.core import SettingException
from ytrss.core import Downloader
from ytrss.core import YTsettingsFile
from optparse import OptionParser
import os
try:
    import argcomplete
except ImportError:
    pass

def option_args():
    parser = OptionParser(description="Save one url from youtube to file.")
    parser.add_option("-d", "--debug", action="store_true",
                      dest="debug_mode", default=False,
                      help="show debug information")
    parser.add_option("-c", "--conf", dest="configuration", 
                      help="configuration file", default="", metavar="FILE")
                      
    parser
    try:
        argcomplete.autocomplete(parser)
    except NameError:
        pass
    (options, args) = parser.parse_args()

    return (options, args)

def main():
    (options, args) = option_args()
    Debug.get_instance().set_debug(options.debug_mode)
    try:
        settings = YTsettingsFile(options.configuration)
    except SettingException:
        print("Configuration file not exist.")
        exit(1)
        
    if len(args) < 1:
        print("Require url to download")
        exit(1)
        
    downloader = Downloader(settings)
    for url in args:
        downloader.download_mp3(url)
    