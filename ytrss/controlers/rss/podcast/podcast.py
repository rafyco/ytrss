"""
Podcast's source builder modules.

This class prepare source for rss file. It can be configured by dictionary
set as argument in constructor.
"""
import os.path
from typing import List
from jinja2 import Environment, FileSystemLoader

import ytrss
from ytrss.configuration.entity.destination_info import DestinationInfo
from ytrss.core.entity.downloaded_movie import DownloadedMovie
from ytrss.controlers.rss.podcast.helpers import format_str, format_desc, format_date


class Podcast:
    """
    Podcast builder.

    Class makes source for rss file. It can be customizable by specyfic args
    defined in constructor.

    Argument dictionary should have following fields:

        - I{title} - Name of podcastv
            (C{"unknown title"} is default)
        - I{author} - Name of podcast author
            (C{"Nobody"} is default)
        - I{language} - Language of podcast
            (C{"pl-pl"} is default)
        - I{link} - Link to website
            (C{"http://youtube.com"} is default)
        - I{desc} - Description of source
            (C{"No description"} is default)
        - I{url_prefix} - Prefix for movie's url
            (C{""} is default)
        - I{img} - Image of movie
            (C{None} is default)
    """

    def __init__(self, podcast_info: DestinationInfo) -> None:
        """
        Object constructor.

        @param self: object handle
        @type self: L{Podcast}
        @param podcast_info: Dictionary of args described
            L{here<ytrss.core.podcast.Podcast>}
        @type podcast_info: dict
        """
        self.__podcast_info = podcast_info
        self.__items: List[DownloadedMovie] = []

    def add_item(self, movie: DownloadedMovie) -> None:
        """
        Add item to podcast source.

        @param self: object handle
        @type self: L{Podcast}
        @param movie: movie's file
        @type movie: L{Movie<ytrss.core.movie.Movie>}
        """
        self.__items.append(movie)

    def generate(self) -> str:
        """
        Generate podcast source.

        @param self: object handle
        @type self: L{Podcast}
        @return: source of podcast
        @rtype: str
        """
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
