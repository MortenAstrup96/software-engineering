"""
reader_tests.py

Software-engineering project group B

14/09/2021
v0.1

Laurent VOURIOT
"""

import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import reader as file_reader

class TestReader(unittest.TestCase):
    def test_reader(self):
        reader = file_reader.Reader()

        reader.read("src/test.json")
        board = reader.board
        self.assertEqual(board.get_difficulty(), 'low')
        # errors
        with self.assertRaises(Exception):
            reader.read("fddsfsdfsdf")


            
if __name__ == '__main__':
    unittest.main()
