import os
import sys
from typing import Optional

from ytrss.configuration.algoritms import create_configuration
from ytrss.configuration.configuration import Configuration, ConfigurationError
from ytrss.configuration.json.json_configuration import JsonConfiguration
from ytrss.configuration.json.yaml_configuration import YamlConfiguration


# pylint: disable=R0911
def configuration_factory(configuration_file: Optional[str] = None, should_create: bool = False) -> Configuration:
    """ Create Configuration

    This method returns a configuration object.
    TODO: Write about localization of configuration files.
    """
    if configuration_file is not None and os.path.isfile(configuration_file):
        if configuration_file.endswith(".json"):
            return JsonConfiguration(configuration_file)
        if configuration_file.endswith(".yml"):
            return YamlConfiguration(configuration_file)
        raise ConfigurationError("Not implements this type of file")

    if sys.platform.lower().startswith('win'):
        if os.path.isfile(os.path.expanduser("~\\YTRSS\\config.yml")):
            return YamlConfiguration("~\\YTRSS\\config.yml")
        if os.path.isfile(os.path.expanduser("~\\YTRSS\\config.json")):
            return JsonConfiguration("~\\YTRSS\\config.json")

    if os.path.isfile(os.path.expanduser("~/.config/ytrss/config.yml")):
        return YamlConfiguration("~/.config/ytrss/config.yml")

    if os.path.isfile(os.path.expanduser("~/.config/ytrss/config.json")):
        return JsonConfiguration("~/.config/ytrss/config.json")

    if os.path.isfile("/etc/ytrss/config.yml"):
        return YamlConfiguration("/etc/ytrss/config.yml")

    if os.path.isfile("/etc/ytrss/config.json"):
        return JsonConfiguration("/etc/ytrss/config.json")

    if should_create:
        if sys.platform.lower().startswith('win'):
            create_configuration("~\\YTRSS\\config.yml")
            return JsonConfiguration("~\\YTRSS\\config.yml")
        create_configuration("~/.config/ytrss/config.yml")
        return YamlConfiguration("~/.config/ytrss/config.yml")

    raise ConfigurationError("Cannot find configuration file")
