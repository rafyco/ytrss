import os
from typing import Tuple, Optional

from flask import Flask, Response

from ytrss.core.managers.manager_service import ManagerService, default_manager_service
from ytrss.res import static as ytrss_res


def resources_web(flask: Flask, manager_service: ManagerService = default_manager_service()) -> None:
    """ Api web elements """
    mime_types = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
        ".png": "image/png",
        ".ico": "image/x-icon"
    }

    def get_file(filename: str) -> bytes:  # pragma: no cover
        return open(filename, "rb").read()

    @flask.route(f"{manager_service.configuration.web_prefix}/res/<path:path>")
    def res_main(path: str) -> Tuple[Optional[Response], int]:
        """ resource site """

        complete_path = os.path.join(ytrss_res.__path__[0], path)  # type: ignore
        ext = os.path.splitext(path)[-1]
        if not os.path.isfile(complete_path) or ext == ".py":
            return None, 404
        mimetype = mime_types.get(ext, "text/html")
        try:
            content = get_file(complete_path)
        except Exception as exc:
            return Response(str(exc), mimetype="text/html"), 500
        return Response(content, mimetype=mimetype), 200

    @flask.route(f"{manager_service.configuration.web_prefix}/favicon.ico")
    def res_favicon() -> Tuple[Optional[Response], int]:
        """ Favicon resource """
        return res_main("favicon.ico")
