from flask import Flask
from typing import Sequence, Callable

from ytrss.website.sites.api import api_web
from ytrss.website.sites.main import main_web
from ytrss.website.sites.resources import resources_web


class WebApp(Flask):
    """ Web app in flask """

    __WEBSITES__: Sequence[Callable[[Flask], None]] = [
        api_web,
        main_web,
        resources_web
    ]

    def __init__(self) -> None:
        Flask.__init__(self, "ytrss")

        for web in self.__WEBSITES__:
            web(self)
