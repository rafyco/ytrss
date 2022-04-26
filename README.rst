#########################################
 YTRSS - subscription downloader
#########################################

Program to automatic download any types of files from Internet.

.. image:: https://img.shields.io/badge/author-Rafa%C5%82%20Kobel-blue.svg
   :target: https://rafyco.pl

.. image:: https://github.com/rafyco/ytrss/actions/workflows/pythonpackage.yml/badge.svg?branch=master
   :target: https://github.com/rafyco/ytrss/actions/workflows/pythonpackage.yml

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

*************
 Description
*************

.. todo::
    Make a description. tell about youtube, planning plugins, build podcasts

YTRSS is a simple script to automate your YouTube podcast adventure. It
is allow you to download your favorite movies, convert it to mp3 and
arrange them to podcast files.

**************
 How to start
**************

.. todo ::
    How to start, add to crontab, set a server

First of all you need to prepare config file, which helps you describe
all the channels or playlists that you want to subscribe. After that you
need to share generated podcast on your private http server.

Remember that this library have no secure podcast file from other
viewers. You public it on your own responsibility. Please make sure that
author of your favorite movies allows you to make podcast from his
files.

Installation
============

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

To checking the installation you can use to call ``ytrss``. Unittest can
be also helpful with verification.

.. todo ::
    install bash completions

***********
 Testing and code checks
***********

.. todo ::
    link to document with tox information

``ytrss`` have a few unittest that you can use to checking code
correctness. You can call it from ``setup.py`` file or using
``ytrss.tests`` module after installation. Check one of below command
and try it yourself.

********
 Author
********

Rafal Kobel rafalkobel@rafyco.pl

.. image:: https://img.shields.io/static/v1.svg?label=Linkedin&message=Rafal%20Kobel&color=blue&logo=linkedin
   :target: https://www.linkedin.com/in/rafa%C5%82-kobel-03850910a/

.. image:: https://img.shields.io/static/v1.svg?label=Github&message=rafyco&color=blue&logo=github
   :target: https://github.com/rafyco

.. image:: https://img.shields.io/static/v1.svg?label=Facebook&message=Rafal%20Kobel&color=blue&logo=facebook
   :target: https://facebook.com/rafyco
