"""
example test module.
"""

import unittest


class TestExample(unittest.TestCase):
    """
    Example test object
    """

    def test_example(self) -> None:
        """
        test example
        """
        self.assertTrue(True)  # pylint: disable=W1503


if __name__ == "__main__":
    unittest.main()
