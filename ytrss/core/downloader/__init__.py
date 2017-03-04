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

import subprocess
import re

class Downloader:
    def __init__(self):
        self.name = ""
        self.output = ""
    def download(self, url):
        status = 0
        print("url: %s" % url)
        command = [ "/usr/bin/youtube-dl", '--extract-audio',  '--audio-format',  'mp3', '-o',  "%(uploader)s - %(title)s.%(ext)s", url ]
        #process = subprocess.Popen(command, stdout=subprocess.PIPE)
        #self.output = process.communicate()
        self.output = "('[youtube] Setting language\n[youtube] YZuFsI-bttM: Downloading video webpage\n[youtube] YZuFsI-bttM: Downloading video info webpage\n[youtube] YZuFsI-bttM: Extracting video information\n[download] Destination: G.F. Darwin - \"Orki z Majorki\"  (Official Video Clip).mp4\n\r[download]   0.0% of 47.53M at  324.89k/s ETA 02:35\r[download]   0.0% of 47.53M at  757.78k/s ETA 01:05\r[download]   0.0% of 47.53M at  810.85k/s ETA 01:00\r[download]   0.0% of 47.53M at    1.14M/s ETA 00:42\r[download]   0.1% of 47.53M at    1.60M/s ETA 00:30\r[download]   0.1% of 47.53M at    2.20M/s ETA 00:21\r[download]   0.3% of 47.53M at    1.35M/s ETA 00:35\r[download]   0.5% of 47.53M at    1.87M/s ETA 00:25\r[download]   1.0% of 47.53M at    2.19M/s ETA 00:21\r[download]   2.1% of 47.53M at    2.41M/s ETA 00:19\r[download]   4.2% of 47.53M at    2.67M/s ETA 00:17\r[download]   8.4% of 47.53M at    2.69M/s ETA 00:16\r[download]  14.7% of 47.53M at    2.61M/s ETA 00:15\r[download]  20.6% of 47.53M at    2.60M/s ETA 00:14\r[download]  26.5% of 47.53M at    2.49M/s ETA 00:14\r[download]  31.7% of 47.53M at    2.44M/s ETA 00:13\r[download]  36.7% of 47.53M at    2.39M/s ETA 00:12\r[download]  41.5% of 47.53M at    2.36M/s ETA 00:11\r[download]  46.5% of 47.53M at    2.34M/s ETA 00:10\r[download]  51.5% of 47.53M at    2.34M/s ETA 00:09\r[download]  56.9% of 47.53M at    2.32M/s ETA 00:08\r[download]  61.7% of 47.53M at    2.32M/s ETA 00:07\r[download]  67.2% of 47.53M at    2.30M/s ETA 00:06\r[download]  72.0% of 47.53M at    2.31M/s ETA 00:05\r[download]  77.6% of 47.53M at    2.29M/s ETA 00:04\r[download]  82.4% of 47.53M at    2.33M/s ETA 00:03\r[download]  89.9% of 47.53M at    2.32M/s ETA 00:02\r[download]  95.1% of 47.53M at    2.32M/s ETA 00:00\r[download] 100.0% of 47.53M at    2.32M/s ETA 00:00\n[ffmpeg] Destination: G.F. Darwin - \"Orki z Majorki\"  (Official Video Clip).mp3\n', None)"
        #print(self.output)
        
        urls = re.split("^\[ffmpeg\] (\W+)$", self.output)
        print(urls)
        
        #print(dir(process))
        
        
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
