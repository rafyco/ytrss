Terminal client
===============

`ytrss` is a command-line program that allows managing the process of downloading movies and generating podcasts
based on a configuration file. It also handles the removal of files that are older than the specified item limit.

The `ytrss` utility is a powerful tool designed to manage the `ytrss` package, allowing users to track, generate,
and download content based on specified sources.

Usage
-----

The basic syntax for the command is:

.. code-block:: shell

    ytrss [OPTIONS] COMMAND [ARGS]...

More information about available commands you can search using `--help` argument.

.. runblock:: console

    $ ytrss --help

Global Options
--------------

.. list-table::
    :widths: 25 75
    :header-rows: 1

    * - Option
      - Description

    * - -h, --help
      - Show the help message and exit.

    * - -c FILE, --conf FILE
      - Path to the configuration file to be used.

    * - -d, --debug-log
      - Enable verbose debug logging for troubleshooting.

Commands
--------

You must use one of the following commands to interact with the package:

help
~~~~

Print the help message and exit.

version
~~~~~~~

Show the current version of the ytrss program.

run
~~~

Scans defined sources for new movies based on the configuration file. It attempts to download new content as well as any items that failed in previous attempts.

Upon a successful download, it:
 * Generates updated podcast files (feeds) for the corresponding source.
 * Rotates files by deleting the oldest movies if the predefined limit of elements is exceeded.

daemon
~~~~~~

Executes the run command periodically at one-hour intervals.

This command blocks the output until interrupted (e.g., via Ctrl+C).

Designed for automation and is the primary entry point when running within a Docker container.

clean
~~~~~

Manually triggers the cleanup process to remove movies that are older than the specified limit.

generate
~~~~~~~~

Refreshes podcast files in the destination directories if changes have occurred, or generates them from scratch if they do not yet exist.

configuration
~~~~~~~~~~~~~

Prints the current active configuration to the console for verification.

download
~~~~~~~~

Immediately attempts to download a specific movie provided as a parameter using built-in mechanisms. The file is saved directly into the directory from which the program was invoked.

url
~~~

Adds a specific movie URL to the download queue.

The movie will be automatically processed and downloaded during the next run or daemon cycle.

By default, it is assigned to the "default" destination, which can be overridden via command arguments.

Examples
--------

Display Configuration:

.. code-block:: bash

    ytrss configuration


Run in Debug Mode:

.. code-block:: bash

    ytrss -d run

Using a Specific Config File:

.. code-block:: bash

    ytrss --conf ./my_config.yaml generate

Add new url to download queue

.. code-block:: bash

    ytrss url "https://yoututbe.com?watch=fdasdfas"


.. warning::
    Before using the client, ensure that the configuration is set appropriately to customize the client's behavior
    according to your preferences.
