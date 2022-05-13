from typing import Tuple
from flask import Flask

from werkzeug.exceptions import HTTPException

from ytrss.core.managers.manager_service import ManagerService, default_manager_service


def main_web(app: Flask, manager_service: ManagerService = default_manager_service()) -> None:
    """ Main web elements """

    @app.errorhandler(Exception)
    def main_error(ex: Exception) -> str:
        template = manager_service.templates_manager["web/error/error.html"]
        if isinstance(ex, HTTPException):
            return template.render(title=f"Error Page: {ex.code}", error=ex, error_code=ex.code)
        return template.render(title="Error Page: 500", error=ex, error_code="500")

    @app.route(manager_service.configuration.web_prefix)
    def main_index() -> Tuple[str, int]:
        """ main site """
        template = manager_service.templates_manager["web/index.html"]
        return template.render(title="Main Site"), 200
