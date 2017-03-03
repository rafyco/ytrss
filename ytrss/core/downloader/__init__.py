import subprocess
import re

class Downloader:
    def __init__(self):
        self.name = ""
        self.output = ""
    def download(self, url):
        status = 0
        print("url: %s" % url)
        command = [ "/usr/bin/youtube-dl", '--extract-audio',  '--audio-format',  'mp3', '-o',  '"%(uploader)s - %(title)s.%(ext)s"', url ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        self.output = process.communicate()
        print(dir(process))
        
        
        return status == 0
    def get_downloaded_file(self):
        return self.name

def debug_test():
    down = Downloader()

    result = down.download("https://www.youtube.com/watch?v=YZuFsI-bttM")
    if result:
        print("result: true")
    else:
        print("result: false")
        
if __name__ == '__main__':
    debug_test()
