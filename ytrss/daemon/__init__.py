from ytrss.core.sys.debug import Debug
from ytrss.core import YTsettingsFile
from ytrss.core import SettingException
from ytrss.core.sys.locker import Locker, LockerError
from optparse import OptionParser
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
    parser.add_option("-c", "--conf", dest="configuration", 
                      help="configuration file", default="", metavar="FILE")
    try:
        argcomplete.autocomplete(parser)
    except NameError:
        pass
    (options, args) = parser.parse_args()
    return options

def main():
    options = option_args()
    Debug.get_instance().set_debug(options.debug_mode)
    Debug.get_instance().debug_log("Debug mode: Run")
    try:
        settings = YTsettingsFile(options.configuration)
    except SettingException:
        print("Configuration file not exist.")
        exit(1)
        
    locker = Locker('lock_ytdown')
    try:
        locker.lock()
    except LockerError:
        print("Program is running.")
        exit(1)
        
        
        
        

    locker.unlock()
    Debug.get_instance().debug_log("End")