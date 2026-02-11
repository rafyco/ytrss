Docker
======

This document provides instructions on how to containerize, run, and manage the ``ytrss``
application using Docker and Docker Compose.

Docker Hub Image
----------------

The official Docker image is available and can be pulled directly from Docker Hub:

`https://hub.docker.com/repository/docker/rafyco/ytrss/general <https://hub.docker.com/repository/docker/rafyco/ytrss/general>`_

To pull the latest image, run:

.. code-block:: bash

    docker pull rafyco/ytrss:latest

Running with Docker CLI
-----------------------

To run the application as a standalone container, you can use the standard Docker build and run commands.

Build the image (Optional):
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you prefer to build the image locally, navigate to the project root directory and run:

.. code-block:: bash

    docker build -t ytrss-app:latest .

Run the container:
~~~~~~~~~~~~~~~~~~

Example command to start the application manually:

.. code-block:: bash

    docker run -d \
    --name ytrss \
    -v $(pwd)/volumes/ytrss/config.yml:/home/ytrss/.config/ytrss/config/config.yml:ro \
    -v $(pwd)/volumes/ytrss/podcasts:/home/ytrss/podcasts \
    rafyco/ytrss:latest

Using Docker Compose
--------------------

For a production-like setup involving automatic video downloading, podcast generation, and a local web server to host
the files, use the provided docker-compose.yml configuration.

Deployment Scenario
~~~~~~~~~~~~~~~~~~~

The following configuration sets up two services:

* **ytrss**: The core application that fetches videos and converts them into podcasts.
* **webserver**: A lightweight static website server (based on lipanski/docker-static-website) that exposes the generated podcasts to your local network.

.. literalinclude:: /../docker-compose.yml
    :language: yaml

How to run
~~~~~~~~~~

To start the entire stack in detached mode, run:

.. code-block:: bash

    docker-compose up -d

The podcast feed will be available in your local network at http://<your-ip>:8080/ytdown/.

Volume Mapping Details
~~~~~~~~~~~~~~~~~~~~~~

The application relies on persistent volumes to maintain state and efficiency. Below are the descriptions of the mapped paths:

**Cache Directory**

* **Host Path**: ``./volumes/ytrss/cache``
* **Container Path**: ``/home/ytrss/.config/ytrss/cache``
* **Description** : Stores temporary segments of videos during the download process. Using a persistent volume here prevents data loss for partially downloaded files if the container restarts.

**Configuration File**

* **Host Path**: ``./volumes/ytrss/config.yml``
* **Container Path**: ``/home/ytrss/.config/ytrss/config/config.yml``
* **Description**: The main config.yml file for the program. It is mounted as Read-Only (``:ro``) to ensure the container does not modify your source configuration accidentally.

**Database**

* **Host Path**: ``./volumes/ytrss/database``
* **Container Path**: ``/home/ytrss/.config/ytrss/database``
* **Description**: Stores metadata and the history of downloaded files. This prevents the application from re-downloading videos that have already been processed.

**Podcast Storage**

* **Host Path**: ``./volumes/ytrss/podcasts``
* **Container Path**: ``/home/ytrss/podcasts``
* **Description**: The final destination for downloaded media and generated XML podcast feeds. This folder is shared with the webserver service so it can be accessed via a browser or podcast player.

User Permissions
~~~~~~~~~~~~~~~~

Note that the ``ytrss`` service runs with ``user: 1000:1000``. Ensure that the directories created on the host machine within the ``./volumes/`` path have the appropriate ownership or write permissions for this UID/GID to avoid "Permission Denied" errors.