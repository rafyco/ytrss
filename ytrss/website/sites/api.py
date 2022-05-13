from typing import Tuple, Any, Optional

from flask import Flask, Blueprint
from flask_restx import Api, Resource

from ytrss import Version
from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.core.managers.manager_service import ManagerService, default_manager_service


def api_web(flask: Flask, manager_service: ManagerService = default_manager_service()) -> None:
    """ Api web elements """

    blueprint = Blueprint('ytrss api', __name__, url_prefix=f"{manager_service.configuration.web_prefix}/api/v1")
    api = Api(blueprint, doc="/swagger/", version=Version().version)
    flask.register_blueprint(blueprint)

    @api.route("/subscriptions")
    class Subscriptions(Resource):
        @classmethod
        def get(cls) -> Tuple[Any, int]:
            return [source.json for source in manager_service.configuration.sources], 200

    @api.route("/destinations")
    class Destinations(Resource):
        @classmethod
        def get(cls) -> Tuple[Any, int]:
            return [destination.info.json for destination in manager_service.destination_manager], 200

    @api.route("/movies/<string:destination>")
    @api.doc(params={"destination": "Destination's identity"})
    class MovieList(Resource):
        @classmethod
        def get(cls, destination: str) -> Tuple[Optional[Any], int]:
            destination = manager_service.destination_manager[DestinationId(destination)]
            if destination is None:
                return None, 404
            return [movie.json for movie in destination.saved_movies], 200
