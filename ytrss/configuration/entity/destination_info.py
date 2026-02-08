import os
from typing import Optional, Dict, Any, NewType

from ytrss.configuration.exceptions import ConfigurationError

from ytrss.core.helpers.typing import Path

DestinationId = NewType("DestinationId", str)


class DestinationInfo:
    """ Destination info

    An object with destination information from json object.
    """

    def __init__(self, identity: DestinationId) -> None:
        self.identity = identity
        self.type: str = "rss"
        self.title: str = "unknown title"
        self.author: str = "Nobody"
        self.language: str = "pl-pl"
        self.link: str = "http://youtube.com"
        self.desc: str = "No description"
        self.url_prefix: str = ""
        self.img: Optional[str] = None
        self.output_path: Optional[Path] = None
        self.limit: int = 20

    # pylint: disable=R0912
    @staticmethod
    def from_json(
            json: Optional[Dict[str, Any]],
            identity: DestinationId,
            url_prefix: str,
            storage_path: str
    ) -> 'DestinationInfo':
        """ Create object from json dictionary. """
        podcast = DestinationInfo(identity)
        if json is not None:
            if 'type' in json and isinstance(json['type'], str):
                podcast.type = json['type']

            if 'title' in json and isinstance(json['title'], str):
                podcast.title = json['title']
            if 'author' in json and isinstance(json['author'], str):
                podcast.author = json['author']
            if 'language' in json and isinstance(json['language'], str):
                podcast.language = json['language']
            if 'link' in json and isinstance(json['link'], str):
                podcast.link = json['link']
            if 'desc' in json and isinstance(json['desc'], str):
                podcast.desc = json['desc']
            if 'img' in json and isinstance(json['img'], str):
                podcast.img = json['img']

            directory = json.get('directory', '')

            if 'url_prefix' in json and isinstance(json['url_prefix'], str):
                podcast.url_prefix = json['url_prefix']
            else:
                podcast.url_prefix = f"{url_prefix}/{directory}"

            if 'path' in json and isinstance(json['path'], str):
                if 'directory' in json:
                    raise ConfigurationError("Cannot set both 'directory' and 'path' values")
                podcast.output_path = Path(os.path.expanduser(json['path']))
            else:
                podcast.output_path = Path(os.path.expanduser(os.path.join(storage_path, directory)))

            if 'filters' in json and isinstance(json, Dict):
                if 'limit' in json['filters'] and isinstance(json['filters']['limit'], int):
                    podcast.limit = json['filters']['limit']
        return podcast
