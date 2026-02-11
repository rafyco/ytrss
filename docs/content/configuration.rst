Configuration
=============

Configuration file
------------------

The behaviour of the program you can define in configuration file.
It tells what sources should be checked for new files and where will be
saved or how to distribute them. The configuration file is a simple yaml
(or json) file that named: ``config.yml`` (or ``config.json`` for json).

Localization
~~~~~~~~~~~~

The ytrss looking for following directory to find this file and get first
available to work with.

#. From location defined in ``PYTHON_YTRSS_CONFIG`` environment.
#. For windows from ``$HOME\\YTRSS`` file
#. For linux in ``~/.config/ytrss`` or ``/etc/ytrss/`` file.

User also can set specific configuration file by define it with
``-c`` or ``--conf`` parameter in terminal client

Example configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~

The configuration file has yaml format. The example of the file looks like this:

.. code-block:: yaml

    ---
    url_prefix: https://my.domain/ytdown
    storage: /home/user/podcasts/ytdown
    subscriptions:
      - name: Private playlist
        url: https://youtube.com/playlist?list=<playlist_id>
        destination: default
      - name: YouTube
        destination: youtube
        url: https://www.youtube.com/@YouTube
    destinations:
      default:
        title: Youtube - podcast
        author: youtube
        link: https://youtube.com
        desc: My favourite movies from YouTube
        img: https://www.youtube.com/yts/img/yt_1200-vfl4C3T0K.png
        directory: default

      youtube:
        title: Youtube channel
        author: youtube
        link: https://youtube.com
        desc: YouTube channel
        img: https://www.youtube.com/yts/img/yt_1200-vfl4C3T0K.png
        directory: youtube

Main structure
~~~~~~~~~~~~~~

.. list-table:: Configuration keys
    :widths: 20 20 20 40
    :header-rows: 1

    * - key
      -
      - default value
      - description

    * - subscriptions
      - required
      - \-
      - List of sources that will be look for new files. See :ref:`Subscriptions structure`.

    * - destinations
      - required
      - \-
      - A list of elements where the files should be placed. See :ref:`Destinations structure`.

    * - config_dir
      - optional
      - ``~/.config/ytrss`` for unix or ``~\\YTRSS`` for windows
      - Directory where the configuration should be places

    * - cache_path
      - optional
      - ``<config_dir>/cache``
      - A place where all file should be downloaded before copy to destination

    * - arguments
      - optional
      - []
      - A list of parameters that are added to ``youtube_dl`` command

    * - url_prefix
      - optional
      - http://localhost
      - A default url that is add to podcast address

    * - storage
      - optional
      - ~/podcasts
      - A place with all subscriptions

Subscriptions structure
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Subscriptions structure
    :widths: 20 20 20 40
    :header-rows: 1

    * - key
      -
      - default value
      - description

    * - name
      - optional
      - "<unknown>"
      - Readable name of source

    * - url
      - required
      - \-
      - A localization of source (e.x. url to youtube channel)

    * - destination
      - optional
      - "default"
      - The destination where the file will be transfer. See :ref:`Destinations structure`.

    * - enable
      - optional
      - ``True``
      - If set to ``False`` the source won't be used

Destinations structure
~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Destination structure
    :widths: 20 20 20 40
    :header-rows: 1

    * - key
      -
      - default value
      - description

    * - type
      - optional
      - rss
      - Type of destination (e.x. rss for podcast)

    * - title
      - optional
      - "unknown title"
      - Title of podcast

    * - url_prefix
      - optional
      - (empty)
      - a string that have been added to podcast url

    * - author
      - optional
      - "Nobody"
      - Author of podcast

    * - link
      - optional
      - "http://youtube.com"
      - List to podcast (e.x. to youtube channel)

    * - desc
      - optional
      - "No description"
      - Description of podcast

    * - img
      - optional
      - None
      - Optional url to podcast image

    * - path
      - optional
      - \-
      - Full path that the file should be saved (cannot be used with 'directory' option)

    * - directory
      - optional
      - \-
      - A directory to store files in storage destinaltion (cannot be used with 'path' option)

    * - filters
      - optional
      - limit: 20
      - An object with rules what files should be delete :ref:`Filters`

Filters
~~~~~~~

Filter is a mechanism that tells software when movies can be deleted

We support following values:

.. list-table:: Filters
    :widths: 20 20 40
    :header-rows: 1

    * - key
      - default value
      - description

    * - limit
      - 20
      - A count of movies that can be stored for one destination

:warn: The movie are deleted after downloaded.
