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
