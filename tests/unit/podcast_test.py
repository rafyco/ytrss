"""
Testing Podcast module.
"""

import unittest

from ytrss.core.helpers.templates import format_desc


class TestPodcast(unittest.TestCase):  # pylint: disable=R0904
    """
    Podcast tests.
    """

    def test_description_file(self) -> None:
        """
        Check podcast description formatter
        """
        samples = [
            {
                "text": "test",
                "predict": "test",
            },
            {
                "text": "user@email.com",
                "predict": "<a href='mailto:user@email.com'>user@email.com</a>",
            },
            {
                "text": "http://test.com",
                "predict": "<a href='http://test.com'>http://test.com</a>",
            },
            {
                "text": "https://test.com",
                "predict": "<a href='https://test.com'>https://test.com</a>",
            },
            {
                "text": "httpd://test.com",
                "predict": "httpd://test.com",
            },
            {
                "text": "/redirect?one=one&two=two",
                "predict": "<a href='https://youtube.com/redirect?one=one&two=two'"
                           ">/redirect?one=one&two=two</a>",
            },
            {
                "text": "/redirect?one=one&q=https%3A%2F%2Ftest.com%2Ftest&two=two",
                "predict": "<a href='https://test.com/test'>https://test.com/test</a>",
            },
            {
                "text": "/redirect?one=one&two=two&q=https%3A%2F%2Ftest.com%2Ftest",
                "predict": "<a href='https://test.com/test'>https://test.com/test</a>",
            },
            {
                "text": "/redirect?one=one&two=two&q=https%3A%2F%2Ftest.com%2Ftest\n",
                "predict": "<a href='https://test.com/test'>https://test.com/test</a><br />\n",
            },
            {
                "text": "/redirect?q=https%3A%2F%2Ftest.com%2Ftest&one=one",
                "predict": "<a href='https://test.com/test'>https://test.com/test</a>",
            },
            {
                "text": "/redirect?q=https%3A%2F%2Ftest.com%2Ftest",
                "predict": "<a href='https://test.com/test'>https://test.com/test</a>",
            },
            {
                "text": "sth /redirect?q=https%3A%2F%2Ftest.com%2Ftest sth",
                "predict": "sth <a href='https://test.com/test'>https://test.com/test</a> sth",
            },
        ]
        for elem in samples:
            result = format_desc(elem['text'])
            self.assertEqual(result, elem['predict'])


if __name__ == "__main__":
    unittest.main()
