################################
 YTRSS - automatic podcast maker
################################

Program to automatic download any types of files from Internet and
generates podcast from them.

.. image:: https://img.shields.io/badge/author-Rafa%C5%82%20Kobel-blue.svg
   :target: https://rafyco.pl

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
============

YTRSS is a program that checks defined sources and downloads a movie or sound files
from them and arrange them to podcast files. It can be highly configured with many plugins
that add any other destinations.

The program in basic version use `youtube_dl` script to download files, so it cooperates
with all services implements by this library. However user can extends this capabilities by
his own custom plugins with external Downloaders.

Requires
--------

To download files, ytrss use following programs:

* `yt-dlp <https://github.com/yt-dlp/yt-dlp>`_

Installation
------------

The installation can be carried out in two ways. You can download
packages from PyPi repository or install it from sources.

For installation from PyPi you can use ``pip`` program. It is likely
that you must use ``pip3`` instead ``pip``.

.. code::

   pip install ytrss

You can also use source from github repository to install ``ytrss``. To
make that download code and invoke command:

.. code::

   python setup.py install

To checking the installation you can use to call ``ytrss``. Unittest can be also
helpful with verification.

Other information
-----------------

For more information about installation, configuration and bash completion read the `documentation <https://ytrss.readthedocs.io>`_.

Author
======

Rafal Kobel rafalkobel@rafyco.pl

.. image:: https://img.shields.io/static/v1.svg?label=Linkedin&message=Rafal%20Kobel&color=blue&logo=linkedin
   :target: https://www.linkedin.com/in/rafa%C5%82-kobel-03850910a/

.. image:: https://img.shields.io/static/v1.svg?label=Github&message=rafyco&color=blue&logo=github
   :target: https://github.com/rafyco

.. image:: https://img.shields.io/static/v1.svg?label=Facebook&message=Rafal%20Kobel&color=blue&logo=facebook
   :target: https://facebook.com/rafyco
