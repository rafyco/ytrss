import os
from typing import Optional, Dict, Any, NewType
from ytrss.core.typing import Path

DestinationId = NewType("DestinationId", str)


class DestinationInfo:

    def __init__(self, identity: DestinationId) -> None:
        self.identity = identity
        self.title: str = "unknown title"
        self.author: str = "Nobody"
        self.language: str = "pl-pl"
        self.link: str = "http://youtube.com"
        self.desc: str = "No description"
        self.url_prefix: str = ""
        self.img: Optional[str] = None
        self.output_path: Optional[Path] = None

    @staticmethod
    def from_json(json: Optional[Dict[str, Any]], identity: DestinationId) -> 'DestinationInfo':
        podcast = DestinationInfo(identity)
        if json is not None:
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
            if 'url_prefix' in json and isinstance(json['url_prefix'], str):
                podcast.url_prefix = json['url_prefix']
            if 'img' in json and isinstance(json['img'], str):
                podcast.img = json['img']
            if 'path' in json and isinstance(json['path'], str):
                podcast.output_path = Path(os.path.expanduser(json['path']))
        return podcast
