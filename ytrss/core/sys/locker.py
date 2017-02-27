from ytrss.core.sys.debug import Debug
import os, tempfile

class LockerError(Exception):
    pass

class Locker:
    def __init__(self, id, dir=None):
        self.id = id
        if dir == None:
            tmp = tempfile.gettempdir()
        else:
            tmp = dir
        self.file_path = "%s/%s" % (tmp, id)
        Debug.get_instance().debug_log("lock path: %s" % self.file_path)
    def is_lock(self):
        return os.path.isfile(self.file_path)
    def lock(self):
        Debug.get_instance().debug_log("Lock program: %s" % self.file_path)
        if self.is_lock():
            raise LockerError
        open(self.file_path, 'a').close()
    def unlock(self):
        Debug.get_instance().debug_log("Unlock program: %s" % self.file_path)
        if self.is_lock():
            os.remove(self.file_path)