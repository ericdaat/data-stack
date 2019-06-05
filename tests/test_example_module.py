import unittest

from python_package import example_module


class TestSomeFunction(unittest.TestCase):
    def test_basic(self):
        result = example_module.some_function()
        self.assertIsInstance(result, str)
