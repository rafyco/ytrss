from argparse import Namespace

from ytrss.commands import BaseCommand
from ytrss.website.app import WebApp


class WebsiteCommand(BaseCommand):
    """ Start website service
    """

    def __init__(self) -> None:
        BaseCommand.__init__(self, "website")

    def run(self, options: Namespace) -> int:
        app = WebApp()

        app.run(
            host=self.manager_service.configuration.web_host,
            port=self.manager_service.configuration.web_port
        )
        return 0
