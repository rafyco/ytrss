class ConfigurationError(Exception):
    """ Configuration error """


class ConfigurationFileNotExistsError(ConfigurationError):
    """ Configuration file not exists error

    The error that raised when the configuration file is not existed.
    """
