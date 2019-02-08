=======================================
YTRSS - Youtube subscription downloader
=======================================

Program to automatic download YouTube files by ``youtube_dl`` scripts.

.. image:: https://img.shields.io/badge/author-Rafa%C5%82%20Kobel-blue.svg
    :target: https://rafyco.pl

.. image:: https://img.shields.io/travis/rafyco/ytrss.svg
   :target: https://travis-ci.org/rafyco/ytrss

.. image:: https://img.shields.io/github/last-commit/rafyco/ytrss.svg
   :target: https://github.com/rafyco/ytrss

.. image:: https://img.shields.io/github/issues/rafyco/ytrss.svg
   :target: https://github.com/rafyco/ytrss/issues

.. image:: https://img.shields.io/pypi/v/ytrss.svg
   :target: https://pypi.python.org/pypi/ytrss/

.. image:: https://img.shields.io/github/license/rafyco/ytrss.svg
   :target: https://www.gnu.org/licenses/gpl.html


Instalation
-----------

PyPi
~~~~

::

    sudo pip install ytrss

setup.py
~~~~~~~~

::

    sudo python setup.py install

Usage
-----

Start service

::

    sudo service ytrss start

Manual once run.

::

    ytdown -d

Add new file to queue

::

    ytdown <file_url>

Example configuration
---------------------

::

    vi ~/.config/ytrss/config

For linux daemon config file should be created in ``root`` path.

::

    {
        "output"   : "<output_file>",
        "subscriptions" : [
            {
                "code"    : "<playlist_id>",
                "type"    : "playlist"
            },
            {
                "code"    : "<subscritpion_id>"
            },
            {
                "code"    : "<subscription_id>", 
                "enabled" : false
            }
        ]
    }

Unit test
---------

For testing module write:

::

    python setup.py test

Author
------

Rafal Kobel rafalkobel@rafyco.pl

License
-------

    Copyright (C) 2017 Rafal Kobel

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see http://www.gnu.org/licenses/.
