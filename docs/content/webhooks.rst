Webhooks
========

Overview
--------

Webhooks allow external services to be notified automatically when specific events occur within the application. When
a triggered action takes place, the application performs an HTTP GET request to a pre-configured URL.

Information about the event is passed directly in the URL via **GET query parameters**. This enables real-time
integration with third-party scripts, automation tools, or monitoring services without the need for constant polling.

Configuration
-------------

All webhook URLs must be defined in the application **configuration file**. Users can specify which URL should be
called for each specific event type. If a URL is not provided for a particular hook in the config, that webhook will
remain inactive.

Available Webhooks
------------------

The following table lists all supported webhooks, their triggers, and the parameters available for use in the query string:

.. list-table::
    :header-rows: 1

    * - Webhook Name
      - Trigger Event
      - Available Parameters

    * - start-daemon
      - Occurs when the application daemon starts up.
      - None

    * - found-new-movie
      - Triggered when a new movie is discovered and identified.
      - title, url, id, desc, destination

    * - start-downloading-movie
      - Triggered when the download process for a specific movie begins.
      - title, url, id, desc

    * - success-download-movie
      - Occurs when a movie has been successfully downloaded.
      - title, url, id, desc

    * - failed-download-movie
      - Triggered if an error occurs during the download process.
      - title, url, id, desc, cause

    * - movie-error
      - Triggered once per destination and error type, when a movie cannot be created or downloaded. It is triggered
        again for a new error type, and after a successful download to that destination, which clears its errors.
        Movies that are not ready yet (premieres and upcoming live events) are skipped.
      - title, url, id, desc, destination, error_type, cause

Parameter Definitions
~~~~~~~~~~~~~~~~~~~~~

 * **title**: The title of the movie.
 * **url**: The source URL or link to the movie.
 * **id**: The unique internal identifier of the movie entity.
 * **desc**: The description or metadata associated with the movie.
 * **destination**: The intended storage path or category for the movie.
 * **cause**: A text message describing the error/exception that led to a download failure.
 * **error_type**: The short form of the error, the same for one kind of error on different movies.

For **movie-error**, title and desc are empty when the movie could not be created.
