from ytrss.core.sys.singleton import Singleton

@Singleton
class Debug:
    def __init__(self):
        self.debug = False
    def set_debug(self, debug=True):
        self.debug = debug
    def is_debug(self):
        return self.debug
    def __bool__(self):
        return self.is_debug()
    def debug_log(self, text):
        if self.is_debug():
            print("log: %s" % text)