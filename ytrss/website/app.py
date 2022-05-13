from typing import Sequence, Callable
from flask import Flask

from ytrss.website.sites.main import main_web


class WebApp(Flask):
    """ Web app in flask """

    __WEBSITES__: Sequence[Callable[[Flask], None]] = [
        main_web
    ]

    def __init__(self) -> None:
        Flask.__init__(self, "ytrss")

        for web in self.__WEBSITES__:
            web(self)
