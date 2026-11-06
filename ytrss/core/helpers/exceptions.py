class DownloadMovieError(Exception):
    """ Error with download of movie. """


class CacheError(DownloadMovieError):
    """ A movie cannot be downloaded to cache. The message holds the real cause. """
