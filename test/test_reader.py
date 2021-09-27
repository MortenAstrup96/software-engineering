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

        reader.read("../src/test.json")
        board = reader.board

        self.assertEqual(board.get_difficulty(), 'low')
        self.assertEqual(board.get_turn_number(), 0)
        self.assertEqual(board.get_player_turn(), "White")
        self.assertEqual(board.get_white_pieces_in_hand(), 12)
        self.assertEqual(board.get_black_pieces_in_hand(), 12)
        self.assertEqual(board.get_white_pieces_left(), 12) 
        self.assertEqual(board.get_black_pieces_left(), 12)
        self.assertEqual(board.get_board_size(), 24)
        self.assertEqual(board.get_lines(), [
            [{"xy":[1,1], "owner": "black"},{"xy":[1,2], "owner":"none"},{"xy":[1,3], "owner":"none"}],
            [{"xy":[1,1], "owner": "black"},{"xy":[2,1], "owner":"none"},{"xy": [3,1], "owner": "none"}],
            [{"xy":[3,1], "owner": "none"},{"xy":[4,1], "owner":"none"},{"xy": [5,1], "owner": "none"}]
            ])




        # errors
        with self.assertRaises(Exception):
            reader.read("fddsfsdfsdf")


            
if __name__ == '__main__':
    unittest.main()
