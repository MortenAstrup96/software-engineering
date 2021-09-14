"""
reader_tests.py

Software-engineering project group B

14/09/2021
v0.1

Laurent VOURIOT
"""

import unittest

from src.reader import Reader


class TestReader(unittest.TestCase):
    def test_reader(self):
        reader = Reader()

        reader.read("test.json")
        # TODO : test read function lol

        # errors
        with self.assertRaises(Exception):
            reader.read("fddsfsdfsdf")
