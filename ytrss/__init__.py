"""
Tools for downloading mp3 from YouTube subscription and playlists.

Installation
===========

There are a two method of installation C{ytrss} module.

From PyPI repository::

    pip install ytrss

From sources::

    git clone git@github.com:rafyco/ytrss.git
    cd ytrss
    uv install

Usage
=====

To more information try to call:

    ytrss --help

"""
from importlib.metadata import metadata, PackageNotFoundError

try:
    __title__ = 'ytrss'
    meta = metadata("ytrss")
    __version__ = meta["Version"]
    __description__ = meta["Summary"]
    __author__ = meta["Author-email"]
    __license__ = meta["License"]
except PackageNotFoundError:
    __version__ = "0"
    __description__ = "Short description"
    __author__ = "Rafał Kobel"
    __license__ = "GPL-3.0-only"
