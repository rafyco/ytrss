import os.path
from typing import List
from jinja2 import Environment, FileSystemLoader

import ytrss
from ytrss.configuration.entity.destination_info import DestinationInfo
from ytrss.core.entity.downloaded_movie import DownloadedMovie
from ytrss.controlers.rss.podcast.helpers import format_str, format_desc, format_date


class Podcast:

    def __init__(self, podcast_info: DestinationInfo) -> None:
        self.__podcast_info = podcast_info
        self.__items: List[DownloadedMovie] = []

    def add_item(self, movie: DownloadedMovie) -> None:
        self.__items.append(movie)

    def generate(self) -> str:
        env = Environment(
            loader=FileSystemLoader(os.path.join(ytrss.__path__[0], "templates")),  # type: ignore
        )
        env.filters["format_str"] = format_str
        env.filters["format_desc"] = format_desc
        env.filters["format_date"] = format_date

        template = env.get_template("podcast.xml")
        return template.render(podcast_info=self.__podcast_info, movies=self.__items)

    def __str__(self) -> str:
        return self.generate()
