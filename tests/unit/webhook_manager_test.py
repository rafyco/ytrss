"""
Tests of webhook manager.
"""

import unittest
from unittest.mock import MagicMock, patch
from urllib.parse import parse_qs, urlsplit

from ytrss.core.entity.webhooks import FailedDownloadMovieWebhook
from ytrss.core.managers.webhook_manager import WebhookManager


class TestWebhookManager(unittest.TestCase):
    """
    Tests of WebhookManager.invoke_hook
    """

    def test_encodes_parameters(self) -> None:
        """ Characters with a special meaning in url stay inside of the parameter """
        cause = "ERROR: a&b=c #1?"
        configuration = MagicMock()
        configuration.get_webhook.return_value = ["http://localhost:8000/hook?cause={cause}&id={id}"]
        movie = MagicMock()
        movie.title = "title"
        movie.url = "https://example.com/watch?v=abc"
        movie.identity = "abc"
        movie.description = "description"

        with patch("ytrss.core.managers.webhook_manager.requests.get") as get:
            get.return_value.status_code = 200
            WebhookManager(configuration).invoke_hook(FailedDownloadMovieWebhook(movie, Exception(cause)))

        url = urlsplit(get.call_args.args[0])
        self.assertEqual(url.fragment, "")
        self.assertEqual(parse_qs(url.query), {"cause": [cause], "id": ["abc"]})


if __name__ == "__main__":
    unittest.main()
