import unittest
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import reader as file_reader
import board as game_board
#import heuristic as game_heuristics
from game_engine import Engine
from heuristic import Heuristic



class testHeuristic(unittest.TestCase):
    def test_game_heuristics(self):

         board = game_board.Board("low",0,"black",12,12,12,12,24,[
    [{"xy":[1,1], "owner": "black"},{"xy":[1,2], "owner":"none"},{"xy":[1,3], "owner":"none"}],
    [{"xy":[1,1], "owner": "black"},{"xy":[2,1], "owner":"none"},{"xy": [3,1], "owner": "none"}] ])
         engine = Engine(board)
         heuristic = Heuristic()
         check = heuristic.firstPhaseState(board)
#         check = heuristic.secondPhaseState(board)


