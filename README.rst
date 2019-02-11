=======================================
YTRSS - Youtube subscription downloader
=======================================

Program to automatic download YouTube files by ``youtube_dl`` scripts.

.. image:: https://img.shields.io/badge/author-Rafa%C5%82%20Kobel-blue.svg
    :target: https://rafyco.pl

.. image:: https://img.shields.io/travis/rafyco/ytrss.svg
   :target: https://travis-ci.org/rafyco/ytrss

.. image:: https://img.shields.io/readthedocs/ytrss.svg
   :target: https://ytrss.readthedocs.io

.. image:: https://img.shields.io/github/last-commit/rafyco/ytrss.svg
   :target: https://github.com/rafyco/ytrss

.. image:: https://img.shields.io/github/issues/rafyco/ytrss.svg
   :target: https://github.com/rafyco/ytrss/issues

.. image:: https://img.shields.io/pypi/v/ytrss.svg
   :target: https://pypi.python.org/pypi/ytrss/

.. image:: https://img.shields.io/github/license/rafyco/ytrss.svg
   :target: https://www.gnu.org/licenses/gpl.html


Description
-----------

YTRSS is a simple script to automate your YouTube podcast adventure.
It is allow you to download your favourite movies, convert it to mp3
and arrange them to podcast files.

How to start
------------

First of all you need to prepare config file, which helps you descirbe
all the channels or playlists that you want to subscribe. After that you
need to share generated podcast on your private http server.

Remember that this library have no secure podcast file from other viewers.
You public it on your own responsibility. Please make sure that autor of your
favourite movies allows you to make podcast from his files.

Installation
~~~~~~~~~~~~

The installation can be carried out in two ways. You can download packages from
PyPi repository or install it from sources.

For installation from PyPi you can use ``pip`` program. It is likely that you must
use ``pip3`` instead ``pip``.

::

    pip install ytrss

You can also use source from github repository to install ``ytrss``. To make that
download code and invoke command:

::

    python setup.py install

To checking the installation you can use to call ``ytss``. Unittest can be also
helpfull with verification.

Unit test
---------

``ytrss`` have a few unittest that you can use to checking code corectness. You can
call it from ``setup.py`` file or using ``ytrss.tests`` module after installation. Check
one of below command and try it yourselfe.

::

    python setup.py test
    python -m ytrss.tests

Author
------

Rafal Kobel rafalkobel@rafyco.pl
