import os
import sys
from typing import Optional

from ytrss.configuration.configuration import Configuration, ConfigurationError, \
    ConfigurationFileNotExistsError
from ytrss.configuration.readers.base import ConfigurationReader
from ytrss.configuration.readers.default_configuration import DefaultConfiguration
from ytrss.configuration.readers.json_configuration import JsonConfiguration
from ytrss.configuration.readers.yaml_configuration import YamlConfiguration


class _ConfigurationFactory:
    """ Configuration builder """

    @classmethod
    def _create_from_file(
            cls,
            configuration_file: str
    ) -> ConfigurationReader:
        if not os.path.isfile(configuration_file):
            raise ConfigurationFileNotExistsError(configuration_file)
        if configuration_file.endswith(".json"):
            return JsonConfiguration(configuration_file)
        if configuration_file.endswith(".yml"):
            return YamlConfiguration(configuration_file)
        raise ConfigurationError("Not implements this type of file")

    @classmethod
    def _create_from_envs(cls, env_name: str) -> ConfigurationReader:
        conf_env_path = os.path.expanduser(os.environ[env_name])
        if os.path.isfile(os.path.join(conf_env_path, "config.yml")):
            return YamlConfiguration(os.path.join(conf_env_path, "config.yml"))
        if os.path.isfile(os.path.join(conf_env_path, "config.yml")):
            return YamlConfiguration(os.path.join(conf_env_path, "config.yml"))
        return DefaultConfiguration()

    @classmethod
    def _create_for_windows(cls, program_name: str) -> ConfigurationReader:
        if os.path.isfile(os.path.expanduser(f"~\\{program_name.upper()}\\config.yml")):
            return YamlConfiguration(f"~\\{program_name.upper()}\\config.yml")
        if os.path.isfile(os.path.expanduser(f"~\\{program_name.upper()}\\config.json")):
            return JsonConfiguration(f"~\\{program_name.upper()}\\config.json")
        return DefaultConfiguration()

    @classmethod
    def _create_for_unix(cls, program_name: str) -> ConfigurationReader:
        if os.path.isfile(os.path.expanduser(f"~/.config/{program_name}/config.yml")):
            return YamlConfiguration(f"~/.config/{program_name}/config.yml")
        if os.path.isfile(os.path.expanduser(f"~/.config/{program_name}/config.json")):
            return JsonConfiguration(f"~/.config/{program_name}/config.json")
        if os.path.isfile(f"/etc/{program_name}/config.yml"):
            return YamlConfiguration(f"/etc/{program_name}/config.yml")
        if os.path.isfile(f"/etc/{program_name}/config.json"):
            return JsonConfiguration(f"/etc/{program_name}/config.json")
        return DefaultConfiguration()

    @classmethod
    def _create_reader(
            cls,
            program_name: str,
            configuration_file: Optional[str]
    ) -> ConfigurationReader:
        """ Create Configuration Reader

        This method returns a configuration object.
        TODO: Write about localization of configuration files.
        """

        if configuration_file is not None and configuration_file != "":
            return cls._create_from_file(configuration_file)
        if "TOX_ENV_DIR" in os.environ:
            return cls._create_from_envs("TOX_ENV_DIR")
        if f"PYTHON_{program_name.upper()}_CONFIG" in os.environ:
            return cls._create_from_file(f"PYTHON_{program_name.upper()}_CONFIG")
        if sys.platform.lower().startswith('win'):
            return cls._create_for_windows(program_name)
        return cls._create_for_unix(program_name)

    def __call__(
            self,
            program_name: str = "python",
            configuration_file: Optional[str] = None
    ) -> Configuration:
        return Configuration(self._create_reader(program_name, configuration_file))


create_configuration = _ConfigurationFactory()
