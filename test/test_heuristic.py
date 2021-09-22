import unittest
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import reader as file_reader
import board as game_board
import heuristic as game_heuristics
from game_engine import Engine


class testHeuristic(unittest.TestCase):
