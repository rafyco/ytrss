#!/usr/bin/env python3
###########################################################################
#                                                                         #
#  Copyright (C) 2017-2021 Rafal Kobel <rafalkobel@rafyco.pl>             #
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
"""
Download mp3 file from YouTube using I{youtube_dl} library.

@see: U{https://rg3.github.io/youtube-dl/}
"""

import os
import json
import shutil
import logging
from typing import Dict, Any, Sequence

import youtube_dl

from ytrss.configuration.configuration import Configuration
from ytrss.configuration.entity.destination import Destination
from ytrss.core.typing import Url


class YouTubeDownloader:
    """
    Download mp3 file from YouTube.

    Class download file to cache folder. In case of success files are
    moved to output file. Output and cache folder are describe in
    L{YTSettings<ytrss.core.settings.YTSettings>} object.

    @ivar configuration: Setting object
    @type configuration: L{YTSettings<ytrss.core.settings.YTSettings>}
    @ivar output_path: Path to output folder
    @type output_path: str
    """
    def __init__(self, configuration: Configuration) -> None:
        """
        Downloader constructor.
        """
        self.configuration = configuration
        self.output_path = os.path.expanduser(configuration.conf.output)

    @classmethod
    def __invoke_ytdl(cls, args: Sequence[str]) -> int:
        try:
            youtube_dl.main(args)
            status = 0
        except SystemExit as ex:
            if ex.code is None:
                status = 0
            else:
                status = ex.code  # pylint: disable=E0012,R0204
        return status

    def download(
            self,
            code: str,
            url: Url,
            destination: Destination,
            json_info: Dict[str, Any]
    ) -> bool:
        """
        Download YouTube movie.

        Function download movie, convert to mp3 and move to output file.
        """
        try:
            os.makedirs(self.configuration.conf.cache_path)
        except OSError:
            pass
        current_path = os.getcwd()
        os.chdir(self.configuration.conf.cache_path)

        logging.info("url: %s", url)
        status = self.__invoke_ytdl(self.configuration.conf.args + ['-o', f"{code}.mp3", url])

        finded = False
        full_file_name = f"{code}.mp3"
        metadate_name = f"{code}.json"
        if os.path.isfile(full_file_name):
            source_path = os.path.join(self.configuration.conf.cache_path, full_file_name)
            destination_path = os.path.join(self.output_path,
                                            destination.destination_dir,
                                            full_file_name)
            metadate_path = os.path.join(self.output_path,
                                         destination.destination_dir,
                                         metadate_name)
            try:
                os.mkdir(self.output_path)
            except OSError:
                pass
            try:
                os.mkdir(os.path.join(self.output_path,
                                      destination.destination_dir))
            except OSError:
                pass
            logging.debug("source_path: %s", source_path)
            logging.debug("destination_path: %s", destination_path)
            shutil.move(source_path, destination_path)
            with open(metadate_path, 'w') as file_handler:
                file_handler.write(json.dumps(json_info))
            finded = True

        for find_file in os.listdir(self.configuration.conf.cache_path):
            if find_file.endswith(".mp3"):
                print(f"Unknown file: {find_file}")

        os.chdir(current_path)
        return status == 0 and finded
