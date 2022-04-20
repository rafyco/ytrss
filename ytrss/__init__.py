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
    python setup.py install

Usage
=====

Before you using this tools you should create configuration file. More
information you can find L{here<ytrss.core.settings>}.

YTRSS allow you to run a few command-line tool.

    - L{ytrss.daemon}
    - L{ytrss.ytdown}
    - L{ytrss.subs}
    - L{ytrss.rssgenerate}

"""


def get_version() -> str:
    """ Get version of ytrss package. """
    return "0.2.8"


def get_name() -> str:
    """ Get name of module. """
    return 'ytrss'


__version__ = get_version()
