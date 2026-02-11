Fast start
==========

tl;dr
-----

* Install program
* Prepare configuration file
* Start ytrss client or configure docker
* **[Optional]** Share your files into external server

How to start?
-------------

First of all you need to prepare configuration file, which helps you describe
all the sources that you want to subscribe and destinations where movies should
be downloaded. See `configuration <content/configuration.html>`_ to more information.

Next you should run a `ytrss` client to store information about new episodes and
share it into described destinations. You can use:

.. code-block:: bash

    ytrss run

or if you want that the program not stop after one execution and run forever, use:

.. code-block:: bash

    ytrss daemon

After that you need to share generated podcast on your private http server.

Remember that this library have no secure podcast file from other
viewers. You public it on your own responsibility. Please make sure that
author of your favorite movies allows you to make podcast from his
files.

A good idea is to use docker instead of system installation. It is cleaner
and allows to better configuration. See: `docker documentation <content/docker.html>`_


