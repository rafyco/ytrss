class DownloadMovieError(Exception):
    """ Error with download of movie. """


class CookieError(DownloadMovieError):
    """ The downloader cannot connect to the service because its cookies are invalid. """
