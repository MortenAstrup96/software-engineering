import unittest
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import reader as file_reader
import board as game_board
from game_engine import Engine
class TestEngine(unittest.TestCase):
    def test_engine_move(self):
        
        board = game_board.Board("low","black",12,12,12,12,24,[
	[{"xy":[1,1], "owner": "black"},{"xy":[1,2], "owner":"none"},{"xy":[1,3], "owner":"none"}],
	[{"xy":[1,1], "owner": "black"},{"xy":[2,1], "owner":"none"},{"xy": [3,1], "owner": "none"}] ])
        engine = Engine(board)
        engine.move_piece((1,1),(1,2),"black")
        old_owner = board.get_owner((1,1))
        new_owner = board.get_owner((1,2))

        self.assertEqual(old_owner, "none")
        self.assertEqual(new_owner, 'black')
        # errors
        
    def test_engine_illegal_move(self):
        
        board = game_board.Board("low","black",12,12,12,12,24,[
	[{"xy":[1,1], "owner": "black"},{"xy":[1,2], "owner":"white"},{"xy":[1,3], "owner":"none"}],
	[{"xy":[1,1], "owner": "black"},{"xy":[2,1], "owner":"none"},{"xy": [3,1], "owner": "none"}] ])
        engine = Engine(board)
        engine.move_piece((1,1),(1,2),"black")
        old_owner = board.get_owner((1,1))
        new_owner = board.get_owner((1,2))

        self.assertEqual(old_owner, "black")
        self.assertEqual(new_owner, 'white')
            
if __name__ == '__main__':
    unittest.main()
