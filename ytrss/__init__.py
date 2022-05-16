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

To more information try to call:

    ytrss --help

"""

import sys

from ytrss.core.version import Version

__title__ = 'ytrss'
__version__ = Version().version
__url__ = 'https://github.com/rafyco/ytrss.git'
__author__ = 'Rafal Kobel'
__author_email__ = 'rafalkobel@rafyco.pl'
__license__ = 'GNU'

__required_python__ = (3, 6)

import ytrss.core.version


def check_python_version() -> None:
    """
    Check if python is in appropriate version
    """
    current_python = sys.version_info[:2]
    if current_python < __required_python__:
        current_python_str = '.'.join([str(el) for el in current_python])
        required_python_str = '.'.join([str(el) for el in __required_python__])
        sys.stderr.write(f"""
==========================
Unsupported Python version
==========================

This version of {__title__} requires Python {required_python_str}, but you're trying to
install it on Python {current_python_str}.
This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have Python {required_python_str} or newer, then try again:

    $ python3 -m pip install --upgrade pip setuptools
    $ pip3 install {__title__}

""")
        sys.exit(1)


if __name__ != "__main__":
    check_python_version()
