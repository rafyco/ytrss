import os.path
import pkgutil


def create_configuration(config_file_name: str) -> None:
    if os.path.isfile(os.path.expanduser(config_file_name)):
        raise FileExistsError(f"file {config_file_name} exists")

    try:
        os.makedirs(os.path.abspath(os.path.join(config_file_name, "..")))
    except OSError:
        pass

    data = pkgutil.get_data(__name__, "default_config.yml")
    if data is None:
        raise RuntimeError("data object not exists")
    with open(os.path.expanduser(config_file_name), "w+") as config_file:
        config_file.write(data.decode("utf-8"))
