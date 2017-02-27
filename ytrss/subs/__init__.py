from ytrss.core.sys.debug import Debug
from ytrss.core import YTsettingsFile
from ytrss.core import Downloader
from optparse import OptionParser
from ytrss.subs.factory import Factory as YTdown_factory
import os
try:
    import argcomplete
except ImportError:
    pass

def option_args():
    parser = OptionParser(description="Save url file from youtube to file.")
    parser.add_option("-d", "--debug", action="store_true",
                      dest="debug_mode", default=False,
                      help="show debug information")
    parser.add_option("-s", "--show", action="store_true",
                      dest="show_config", default=False,
                      help="Write configuration")
    parser.add_option("-c", "--conf", dest="configuration", 
                      help="configuration file", default="", metavar="FILE")
    try:
        argcomplete.autocomplete(parser)
    except NameError:
        pass
    (options, args) = parser.parse_args()
    return options

def main():
    Debug.get_instance().debug_log("Debug mode: Run")
    options = option_args()
    Debug.get_instance().set_debug(options.debug_mode)
    #try:
    settings = YTsettingsFile(options.configuration)
    #except Exception:
    #    print("Configuration file not exist.")
    #    exit(1)
        
    if options.show_config:
        print(settings)
        exit()
    
    factory = YTdown_factory(settings)
    urls = factory.getUrls()
    downloader = Downloader(settings)
    for url in urls:
        downloader.download_mp3(url)
    
    Debug.get_instance().debug_log("End")