from jinja2 import Environment, Template, FileSystemLoader

from ytrss import templates as ytrss_templates
from ytrss.core.helpers.templates import format_str, format_desc, format_date


class TemplatesManager:
    """ Templates Manager

    Manager that returns a template from ytrss package
    """

    def __init__(self) -> None:
        self._env = Environment(
            loader=FileSystemLoader(ytrss_templates.__path__[0]),
        )
        self._env.filters["format_str"] = format_str
        self._env.filters["format_desc"] = format_desc
        self._env.filters["format_date"] = format_date

    def _get_template(self, path: str) -> Template:
        return self._env.get_template(path)

    def __getitem__(self, key: str) -> Template:
        return self._get_template(key)
