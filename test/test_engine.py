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
        
    def test_engine_illegal_move_occupied(self):
        
        board = game_board.Board("low","black",12,12,12,12,24,[
	[{"xy":[1,1], "owner": "black"},{"xy":[1,2], "owner":"white"},{"xy":[1,3], "owner":"none"}],
	[{"xy":[1,1], "owner": "black"},{"xy":[2,1], "owner":"none"},{"xy": [3,1], "owner": "none"}] ])
        engine = Engine(board)
        engine.move_piece((1,1),(1,2),"black")
        old_owner = board.get_owner((1,1))
        new_owner = board.get_owner((1,2))

        self.assertEqual(old_owner, "black")
        self.assertEqual(new_owner, 'white')

    def test_engine_illegal_move_no_exist(self):
        
        board = game_board.Board("low","black",12,12,12,12,24,[
	[{"xy":[1,1], "owner": "black"},{"xy":[1,2], "owner":"white"},{"xy":[1,3], "owner":"none"}],
	[{"xy":[1,1], "owner": "black"},{"xy":[2,1], "owner":"none"},{"xy": [3,1], "owner": "none"}] ])
        engine = Engine(board)
        error_code = engine.move_piece((1,1),(1,4),"black")
        old_owner = board.get_owner((1,1))
        self.assertEqual(error_code, -1)
        self.assertEqual(old_owner, "black")
        
        
    def test_engine_all_possible_states_for_place(self):
        board = game_board.Board("low","white",12,12,12,12,24,[
        [{"xy":[1,1], "owner": "black"},{"xy":[1,2], "owner":"white"},{"xy":[1,3], "owner":"none"}],
        [{"xy":[1,1], "owner": "black"},{"xy":[2,1], "owner":"none"},{"xy": [3,1], "owner": "none"}],
        [{"xy":[3,1], "owner": "none"},{"xy":[4,1], "owner":"none"},{"xy": [5,1], "owner": "none"}]]) 
        engine = Engine(board)
        states = engine.all_possible_states_for_place()
        self.assertEqual(len(states),5)
        self.assertEqual(states[0][0][2]['owner'], "white")
                        
    def test_engine_all_possible_states_for_place_empty_board(self):
        board = game_board.Board("low","white",12,12,12,12,24,[
        [{"xy":[1,1], "owner": "none"},{"xy":[1,2], "owner":"none"},{"xy":[1,3], "owner":"none"}],
        [{"xy":[1,1], "owner": "none"},{"xy":[2,1], "owner":"none"},{"xy": [3,1], "owner": "none"}],
        [{"xy":[3,1], "owner": "none"},{"xy":[4,1], "owner":"none"},{"xy": [5,1], "owner": "none"}]]) 
        engine = Engine(board)
        states = engine.all_possible_states_for_place()
        self.assertEqual(len(states),7)
                
    def test_engine_all_possible_states_for_place_full_board(self):
        board = game_board.Board("low","white",12,12,12,12,24,[
        [{"xy":[1,1], "owner": "black"},{"xy":[1,2], "owner":"white"},{"xy":[1,3], "owner":"white"}],
        [{"xy":[1,1], "owner": "black"},{"xy":[2,1], "owner":"white"},{"xy": [3,1], "owner": "white"}],
        [{"xy":[3,1], "owner": "black"},{"xy":[4,1], "owner":"black"},{"xy": [5,1], "owner": "white"}]]) 
        engine = Engine(board)
        states = engine.all_possible_states_for_place()
        self.assertEqual(len(states),0)

if __name__ == '__main__':
    unittest.main()
