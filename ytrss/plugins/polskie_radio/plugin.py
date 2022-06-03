from typing import Optional

from ytrss.configuration.entity.source import Source
from ytrss.core.entity.plugin import Plugin
from ytrss.core.entity.source_downloader import SourceDownloader
from ytrss.plugins.polskie_radio.polskie_radio_source_downloader import PolskieRadioSourceDownloader


class PolskieRadioPlugin(Plugin):

    def create_source_downloader(self, source: Source) -> Optional[SourceDownloader]:
        return PolskieRadioSourceDownloader(source)
