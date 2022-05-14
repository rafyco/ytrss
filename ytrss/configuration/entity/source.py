"""
Module with source data object
"""
from typing import Dict, Any

from ytrss.configuration.entity.destination_info import DestinationId


class Source:
    """
    Source data object

    This object contains an information about source, where the podcast can be downloaded
    """

    def __init__(self) -> None:
        self.url: str = "none"
        self.destination: DestinationId = DestinationId("")
        self.name: str = "<unknown>"
        self.enable: bool = True

    @property
    def json(self) -> Dict[str, Any]:
        """
        Dictionary representation of file
        """
        return {
            "name": self.name,
            "url": self.url,
            "destination": self.destination,
            "enable": self.enable
        }

    @staticmethod
    def from_json(json: Dict[str, Any]) -> 'Source':
        """ Create Source object from dictionary. """
        source = Source()
        if 'name' in json and isinstance(json['name'], str):
            source.name = json['name']
        if 'url' in json and isinstance(json['url'], str):
            source.url = json['url']
        if 'destination' in json and isinstance(json['destination'], str):
            source.destination = DestinationId(json['destination'])
        else:
            raise ValueError
        if 'enable' in json and isinstance(json['enable'], bool):
            source.enable = json['enable']
        return source
