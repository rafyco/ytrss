import os

from ytrss.configuration.configuration import Configuration


class DatabaseFileConfig:
    """
    Object with database files destinations.
    """

    def __init__(self, configuration: Configuration):
        self.url_rss = os.path.join(configuration.conf.config_path, "rss_remember.txt")
        self.download_file = os.path.join(configuration.conf.config_path, "download_yt.txt")
        self.next_time = os.path.join(configuration.conf.config_path, "download_yt_next.txt")
        self.url_backup = os.path.join(configuration.conf.config_path, "download_yt_last.txt")
        self.history_file = os.path.join(configuration.conf.config_path, "download_yt_history.txt")
        self.err_file = os.path.join(configuration.conf.config_path, "download_yt.txt.err")
